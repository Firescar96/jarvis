from gtts import gTTS
from io import BytesIO
import pyaudio
from aiostream import stream
from pydub import AudioSegment
from pydub.effects import speedup
import multiprocessing

# import my fork of the chatgpt_wrapper library
import sys
sys.path.insert(0, '../chatgpt_wrapper_async')
from chatgpt_wrapper import ChatGPT

bot = ChatGPT()
async def setup():
  await bot.async_init()

async def chunk(iterator, size):
  async with stream.chunks(iterator, size).stream() as streamer:
    async for res in streamer:
      yield ''.join(res)

audio_queue = multiprocessing.Queue()
def playsound():
  p = pyaudio.PyAudio()
  stream = p.open(format=p.get_format_from_width(2),
    channels=1, rate=24000, frames_per_buffer=3200, output=True)
  while True:
    raw_audio = audio_queue.get(block=True)
    if not raw_audio:
      break
    stream.write(raw_audio)

async def default(text:str):

  sound_output_process = multiprocessing.Process(target=playsound)
  sound_output_process.start()

  async for partial_response in chunk(bot.ask_stream(text), 10):
    print('partial_response', partial_response)
    if not partial_response:
      continue
    mp3_fp = BytesIO()
    tts = gTTS(partial_response, lang='en', tld='co.uk')
    if not tts._tokenize(partial_response):
      continue
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    audio = AudioSegment.from_file(mp3_fp, format="mp3")
    audio = speedup(audio,1.3,150)
    audio_queue.put(audio.raw_data[6000:-12000])

  audio_queue.put(None)
  
  sound_output_process.join()