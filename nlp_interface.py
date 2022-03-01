# from nltk.parse.corenlp import CoreNLPParser
# parser = CoreNLPParser()
# parse = next(parser.raw_parse("I put the book in the box on the table."))
import nltk
from nltk import pos_tag, word_tokenize, parse
from nltk.tokenize import sent_tokenize


text = 'jarvis change the lights to purple'
tagged_text = pos_tag(word_tokenize(text))

print(parse)
# print(result)
print(sent_tokenize(text))
# nltk.chunk.conllstr2tree(text, chunk_types=['NP']).draw()

grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and nouns
      {<NNP>+}                # chunk sequences of proper nouns
"""
cp = nltk.RegexpParser(grammar)
print(cp.parse(tagged_text))