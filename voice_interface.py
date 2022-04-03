import pyaudio
import re
import multiprocessing
import speech_recognition
import nlp_interface

def runner(event_queue:multiprocessing.Queue):
  # pyaudio instances must be used in the same thread they are created
  # devices = speech_recognition.Microphone.list_microphone_names()
  r = speech_recognition.Recognizer()
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

    audio = speech_recognition.AudioData(data, RATE, 2)
    try:
      text = r.recognize_google(audio)
      print('raw text', text)
      if text == pending_text:
        no_change_count += 1

      pending_text = text
      if no_change_count>1:
        output:str = re.sub('(travis|chadwick)', 'jarvis', pending_text, flags=re.IGNORECASE)
        output = re.sub('^(.*) (?=jarvis)', '', output, flags=re.IGNORECASE)

        pending_text = ''
        # technically this might drop the start of another text phrase, will adjust if it turns out to be an issue
        data = data[-FRAMES_PER_BUFFER*4:]
        no_change_count = 0
        if output.lower().startswith('jarvis'):
          next_event = nlp_interface.process_text(output)
          event_queue.put(next_event)
    except speech_recognition.UnknownValueError:
      # prune the empty data, but don't clear the data buffer so we don't lose the beginning of a word
      data = data[-FRAMES_PER_BUFFER*4:]
    except:
      pass

  
def input_voice(event_queue:multiprocessing.Queue, exit_handlers:list):
  input_voice_thread = multiprocessing.Process(target=runner, args=(event_queue,))
  input_voice_thread.start()
  
  exit_handlers.append(lambda: input_voice_thread.terminate())