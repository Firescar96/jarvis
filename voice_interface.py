import pyaudio
import re
import multiprocessing
import speech_recognition
import nlp_interface

def runner(event_queue:multiprocessing.Queue):
  # pyaudio instances must be used in the same thread they are created
  # devices = speech_recognition.Microphone.list_microphone_names()
  r = speech_recognition.Recognizer()

  print("Awaiting your input, sir.")
  with speech_recognition.Microphone() as source:
    while True:
      audio = r.listen(source)
      try:
        text = r.recognize_google(audio)
        print('raw text', text)

        output:str = re.sub('(travis|chadwick|alfred)', 'jarvis', text, flags=re.IGNORECASE)
        output = re.sub('^(.*) (?=jarvis)', '', output, flags=re.IGNORECASE)

        print('output', output)
        if output.lower().startswith('jarvis'):
          next_event = nlp_interface.process_text(output)
          event_queue.put(next_event)
      except:
        pass

  
def input_voice(event_queue:multiprocessing.Queue, exit_handlers:list):
  input_voice_thread = multiprocessing.Process(target=runner, args=(event_queue,))
  input_voice_thread.start()
  
  exit_handlers.append(lambda: input_voice_thread.terminate())