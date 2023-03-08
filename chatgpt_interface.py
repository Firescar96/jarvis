from io import BytesIO
from gtts import gTTS
import pyaudio
from pydub import AudioSegment
from pydub.effects import speedup
from jarvis_secrets import gpt3_key
import openai
import multiprocessing

openai.api_key = gpt3_key

class ChatGPTInterface():
  def message(self, data):
    response_events = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "Your name is Jarvis and you are an assistant and conversationalist to Nchinda."},
            {"role": "user", "content": data},
      ]
    )
    return response_events['choices'][0]['message']['content']

default_interface = ChatGPTInterface()

audio_queue = multiprocessing.Queue()
def playsound():
  p = pyaudio.PyAudio()
  stream = p.open(format=p.get_format_from_width(2),
    channels=1, rate=20000, output=True)
  while True:
    raw_audio = audio_queue.get(block=True)
    if not raw_audio:
      break
    stream.write(raw_audio)

async def default(text:str):

  sound_output_process = multiprocessing.Process(target=playsound)
  sound_output_process.start()

  for partial_response in default_interface.message(text).split('. '):
    print('partial_response', partial_response)
    if not partial_response:
      continue
    mp3_fp = BytesIO()
    tts = gTTS(partial_response, lang='en', tld='com.au')
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    audio = AudioSegment.from_file(mp3_fp, format="mp3")
    audio = speedup(audio,1.5,100)
    audio_queue.put(audio.raw_data)
  
  audio_queue.put(None)
  
  sound_output_process.join()


# tts.tts_to_file(text=partial_response, speaker=tts.speakers[0], language=tts.languages[0], file_path=mp3_fp)