import json
import requests;
import json
import re
from secrets import gpt3_key

class GPT3Interface():
  def __init__(self):
    self.headers = {
      'Authorization': f'Bearer {gpt3_key}',
      'Content-Type': 'application/json'
    }

  def proxy(self, data):
    print(data)
    return requests.post(
      'https://api.openai.com/v1/engines/text-davinci-001/completions',
      data=json.dumps(data),
      headers=self.headers)
  

default_interface = GPT3Interface()

def process_color_hex(input_signal:str):
  prompt = f'what is the rgb code for {input_signal}\n#'
  result = default_interface.proxy({
    'prompt': prompt,
    'max_tokens': 40,
    'temperature': .3
  })
  print(result.text)
  output = result.json()['choices'][0]['text'].replace('\n', '')
  output = re.findall(r'#?(\w+).?$', output)[0]


  return output

