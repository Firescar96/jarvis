import json
import requests;
import json
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