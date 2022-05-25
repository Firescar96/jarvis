import json
import requests;
import json
import re
import random
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
  with open('gpt_interface.json') as f:
    interface_memory = json.load(f)

  if input_signal in interface_memory:
    for possible_output in interface_memory[input_signal]:
      if random.random() > possible_output.probability:
        interface_memory[input_signal].probability = min(interface_memory[input_signal].probability*1.2, 1)
        with open('gpt_interface.json', 'w') as f:
          json.dump(interface_memory, f)
        return interface_memory[input_signal].output
  else:
    interface_memory[input_signal] = []

  
  prompt = f'what is the rgb code for {input_signal}\n#'
  result = default_interface.proxy({
    'prompt': prompt,
    'max_tokens': 40,
    'temperature': .3
  })
  print(result.text)
  output = result.json()['choices'][0]['text'].replace('\n', '')
  output = re.findall(r'#?(\w+).?$', output)[0]

  interface_memory[input_signal].append({
    'input': input_signal,
    'probability': .5,
    'output': output
  })

  with open('gpt_interface.json', 'w') as f:
    json.dump(interface_memory, f)

  return output

