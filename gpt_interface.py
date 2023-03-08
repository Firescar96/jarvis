import json
import requests;
import json
import re
import random
from jarvis_secrets import gpt3_key

class GPT3Interface():
  def __init__(self):
    self.headers = {
      'Authorization': f'Bearer {gpt3_key}',
      'Content-Type': 'application/json'
    }

  def proxy(self, data):
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
      if possible_output['probability'] > random.random():
        return possible_output['output']
  else:
    interface_memory[input_signal] = []

  
  prompt = f'what is the rgb code for {input_signal}\n#'
  print('prompt', prompt)
  result = default_interface.proxy({
    'prompt': prompt,
    'max_tokens': 40,
    'temperature': .3
  })
  output = result.json()['choices'][0]['text'].replace('\n', '')
  print('output', output)
  output = re.findall(r'#?(\w+).?$', output)[0]

  for possible_output in interface_memory[input_signal]:
    if possible_output['output'] == output:
        possible_output['probability'] = min(possible_output['probability']*1.2, 1)
  else:
    interface_memory[input_signal].append({
      'input': input_signal,
      'probability': .5,
      'output': output
    })

  with open('gpt_interface.json', 'w') as f:
    json.dump(interface_memory, f)

  return output

