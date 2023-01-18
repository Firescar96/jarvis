import re
import multiprocessing
import pyaudio
import struct
import speech_recognition
import nlp_interface
import pvporcupine
from jarvis_secrets import pvporcupine_key

def runner(event_queue:multiprocessing.Queue):
  # pyaudio instances must be used in the same thread they are created
  # devices = speech_recognition.Microphone.list_microphone_names()
  r = speech_recognition.Recognizer()

  porcupine = pvporcupine.create(access_key=pvporcupine_key, keywords=['jarvis'])

  with speech_recognition.Microphone(sample_rate=porcupine.sample_rate, chunk_size=porcupine.frame_length) as source:
    while True:
      pcm = source.stream.read(porcupine.frame_length)
      audio_frame = struct.unpack_from("h" * porcupine.frame_length, pcm)

      keyword_index = porcupine.process(audio_frame)
      if keyword_index == -1:
        continue
      print("Awaiting your input, sir.")
      try:
        audio = r.listen(source)
        text = r.recognize_google(audio)
      
        next_event = nlp_interface.process_text(text)
        event_queue.put(next_event)
      except:
        pass

def input_voice(event_queue:multiprocessing.Queue, exit_handlers:list):
  input_voice_thread = multiprocessing.Process(target=runner, args=(event_queue,))
  input_voice_thread.start()
  
  exit_handlers.append(lambda: input_voice_thread.terminate())
