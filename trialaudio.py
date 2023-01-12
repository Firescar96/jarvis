import speech_recognition
import pyaudio


# FRAMES_PER_BUFFER = 4000
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000
# p = pyaudio.PyAudio()


# stream:pyaudio.Stream = p.open(
#   format=FORMAT,
#   channels=CHANNELS,
#   rate=RATE,
#   input=True,
#   frames_per_buffer=FRAMES_PER_BUFFER
# )
with speech_recognition.Microphone() as source:
  while True:
    r = speech_recognition.Recognizer()
    audio = r.listen(source)
    try:
        said = r.recognize_google(audio)
        print(said)
    except Exception as e:
        print("Exception: " + str(e))