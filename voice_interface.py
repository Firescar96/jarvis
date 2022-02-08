import pyaudio
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
 

stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

data = stream.read(FRAMES_PER_BUFFER)
r.recognize_google(data)