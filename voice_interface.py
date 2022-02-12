import pyaudio
import wave
import time
import speech_recognition
#### inputs

devices = speech_recognition.Microphone.list_microphone_names()
r = speech_recognition.Recognizer()
my_mic = speech_recognition.Microphone(device_index=devices.index('jack'))
 
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
 

stream:pyaudio.Stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

data:bytes = b''
pending_text = ''
no_change_count = 0
text_chunks = []
while True:
   data += stream.read(stream.get_read_available())

   audio = speech_recognition.AudioData(data, RATE, 2)
   try:
      text = r.recognize_google(audio)
      if text == pending_text:
         no_change_count += 1

      pending_text = text
      print('text', pending_text)
      print('pending_text', pending_text)
      if no_change_count >= 2:
         text_chunks.append(pending_text)
         pending_text = ''
         # technically this might drop the start of another text phrase, will adjust if it turns out to be an issue
         data = b''
         no_change_count = 0
         print(text_chunks)
   except speech_recognition.UnknownValueError:
      # prune the empty data, but don't clear the data buffer so we don't lose the beginning of a word
      data = data[-FRAMES_PER_BUFFER*20:]