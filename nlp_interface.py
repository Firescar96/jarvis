# https://spacy.io/usage/linguistic-features#pos-tagging
from unittest import result
import spacy
import json
nlp = spacy.load('en_core_web_sm')

def process_text(text:str):
  next_stage = {}
  print('process tesc', text)
  parsed_text = nlp(text)

  #get token dependencies
  if 'light' not in text:
    return

  for token in parsed_text:
    #dobj for direct object, attr=attribute prt=particle
    if token.dep_ not in ["dobj", 'ccomp', 'pobj', 'attr', 'prt', 'prep']:
      continue
  
    direct_object_tree = [x.lemma_ for x in token.children]
    print('direct_object_tree', token.text, direct_object_tree)

    full_color_phrase = []
    for child in token.lefts:
      if 'light' in child.lemma_:
        continue
      full_color_phrase += [x.text for x in child.subtree]
    full_color_phrase.append(token.text)
    for child in token.rights:
      if 'light' in child.lemma_:
        continue
      full_color_phrase += [x.text for x in child.subtree]
    full_color_phrase = ' '.join(full_color_phrase)

    if full_color_phrase:
      next_stage = {
        'name': 'hue_interface.output_lights',
        'args': [full_color_phrase]
      }
  return next_stage

result = process_text('jarvis adjust the lights to be a bright purple')
print(result)