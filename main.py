import re
import time
import multiprocessing
import asyncio
from gpt_interface import default_interface as gpt_interface
import hue_interface
import speech_recognition
#### inputs

devices = speech_recognition.Microphone.list_microphone_names()
r = speech_recognition.Recognizer()
my_mic = speech_recognition.Microphone(device_index=devices.index('jack'))
def input_voice(event_queue:multiprocessing.Queue):
  with my_mic as source:
      # r.adjust_for_ambient_noise(source) #reduce noise
      while True:
        time.sleep(.5)
        print("Awaiting your input, sir.")
        audio = r.listen(source) #take voice input from the microphone
        try:
          output:str = r.recognize_google(audio)
          print('raw voice input:', output)
          output = re.sub('travis', 'jarvis', output, flags=re.IGNORECASE)
          if not output.lower().startswith('jarvis'):
            continue
          output = re.sub('^jarvis', '', output, flags=re.IGNORECASE)
          event_queue.put(output)
        except:
          pass

#### middle processing
def process_color_hex(input_signal:str):
  prompt = f'Hex code for {input_signal} #'
  result = gpt_interface.proxy({
    'prompt': prompt,
    'max_tokens': 20,
    'temperature': .3
  })
  print(result.text)
  output = result.json()['choices'][0]['text'].replace('\n', '')
  output = re.findall(r'#?(\w+).?$', output)[0]


  return output


### outputs

def output_console(input_signal:str):
  print(input_signal)



### main process
main_event_queue = multiprocessing.Queue()

async def main():

  input_voice_thread = multiprocessing.Process(target=input_voice, args=(main_event_queue,))
  input_voice_thread.start()

  jarvis_active = True
  while jarvis_active:
    time.sleep(.5)

    next_event = main_event_queue.get(block=True)
    print('next_event', next_event) 
    try:
      output = process_color_hex(next_event)
    except:
      continue
    output_console(output)
    try:
      await hue_interface.output_lights(output)
    except:
      continue

  input_voice_thread.join()
asyncio.get_event_loop().run_until_complete(main())