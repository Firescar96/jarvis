# background reading in the order I found it
#the starter for this file came from https://github.com/bdmarius/python-knowledge-graph/blob/master/knowledgegraph.py
# this is also useful https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/
# https://www.ijcai.org/Proceedings/15/Papers/273.pdf
# http://graphbrain.net/tutorials/parsing-a-sentence.html
# https://github.com/thomason-jesse/grounded_dialog_agent
# learning papers from Banti
# https://www.cs.cmu.edu/~rsalakhu/papers/oneshot1.pdf
# https://cs330.stanford.edu/slides/lorel5min.pdf
# https://cs330.stanford.edu/slides/Stanford%20LangLfP%20talk.pdf
# https://arxiv.org/pdf/1703.05175.pdf
from hypergraph import Hypergraph
from graphbrain.parsers import create_parser
from graphbrain.cognition.system import run_agent
parser = create_parser(lang='en')

hypergraph = Hypergraph('memory.hg')

# text = "A Light turns on. A Light turns off. A light changes color."

# parses = parser.parse(text)['parses']
# for parse in parses:
#     hypergraph.add(parse['main_edge'])
    
# run_agent('taxonomy', hg=hypergraph)
for edge in hypergraph.search('(light/C)', strict=False):
    print('edge', edge)
    print('\n')
    for subedge in hypergraph.edges_with_edges([edge]):
        print(subedge)
        subedge.match_pattern('* *')
    
    print('\n')
    for subedge in hypergraph.ego(edge):
        print(subedge)


'''
so this is interesting, going to put a pause in it for later
what needs to be done here is to import a library of common sense rules, defining eg. 'change' and 'turn' as
actions that a light can do
then the knowledge graph layer can be used as a sanity check on the validity of instructions
so that 'disintegrate the light' is not understood as valid, but 'change' the light can be understood
even though 'change' might not be in the knowledge graph
'''