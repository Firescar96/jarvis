import re
import time
import pyaudio
import multiprocessing
import asyncio
from gpt_interface import default_interface as gpt_interface
import hue_interface
import speech_recognition
#### inputs


def input_voice(event_queue:multiprocessing.Queue):
  # pyaudio instances must be used in the same thread they are created
  devices = speech_recognition.Microphone.list_microphone_names()
  r = speech_recognition.Recognizer()
  my_mic = speech_recognition.Microphone(device_index=devices.index('jack'))
  FRAMES_PER_BUFFER = 3200
  FORMAT = pyaudio.paInt16
  CHANNELS = 1
  RATE = 16000
  p = pyaudio.PyAudio()
  

  stream:pyaudio.Stream = p.open(
    # input_device_index=devices.index('jack'),
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
  )

  data:bytes = b''
  pending_text:str = ''
  no_change_count:int = 0
  print("Awaiting your input, sir.")
  while True:
    data += stream.read(stream.get_read_available())

    print('got data')
    audio = speech_recognition.AudioData(data, RATE, 2)
    try:
        text = r.recognize_google(audio)
        print('got text')
        if text == pending_text:
          no_change_count += 1

        pending_text = text
        print('text', pending_text)
        print('pending_text', pending_text)
        if no_change_count >= 2:
          output:str = re.sub('travis', 'jarvis', pending_text, flags=re.IGNORECASE)

          pending_text = ''
          # technically this might drop the start of another text phrase, will adjust if it turns out to be an issue
          data = b''
          no_change_count = 0
          if output.lower().startswith('jarvis'):
            output = re.sub('^jarvis', '', output, flags=re.IGNORECASE)
            event_queue.put(output)
    except speech_recognition.UnknownValueError:
      # prune the empty data, but don't clear the data buffer so we don't lose the beginning of a word
      data = data[-FRAMES_PER_BUFFER*20:]

#### middle processing
def process_color_hex(input_signal:str):
  prompt = f'Hex code for {input_signal} #'
  result = gpt_interface.proxy({
    'prompt': prompt,
    'max_tokens': 40,
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
  # input_voice(main_event_queue)

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