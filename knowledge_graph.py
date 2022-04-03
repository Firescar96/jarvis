#the starter for this file came from https://github.com/bdmarius/python-knowledge-graph/blob/master/knowledgegraph.py
# this is also useful https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/
import spacy
from spacy.lang.en import English
import networkx as nx
import matplotlib.pyplot as plt
nlp = spacy.load('en_core_web_sm')

def getSentences(text):
    # nlp = English()
    nlp.add_pipe('sentencizer')
    document = nlp(text)
    return [sent.text.strip() for sent in document.sents]

def isRelationCandidate(token):
    deps = ['ROOT', 'adj', 'attr', 'agent', 'amod']
    return any(subs in token.dep_ for subs in deps)

def isConstructionCandidate(token):
    deps = ['compound', 'prep', 'conj', 'mod', 'acomp']
    return any(subs in token.dep_ for subs in deps)

def processSubjectObjectPairs(tokens):
    subject = []
    object = []
    relation = []
    subjectConstruction = []
    objectConstruction = []
    for token in tokens:
        print(token.text, '->', token.dep_, '->', token.pos_)
        if 'punct' in token.dep_:
            continue
        if isRelationCandidate(token):
            relation.append(token.lemma_)
        if isConstructionCandidate(token):
            if subjectConstruction:
                subjectConstruction.append(subjectConstruction, token.text)
            if objectConstruction:
                objectConstruction.append(objectConstruction, token.text)
        if 'subj' in token.dep_:
            print('token.dep_', token.dep_)
            subject.append(token.text)
            subjectConstruction.append(subject)
            subjectConstruction = []
        if 'obj' in token.dep_ or token.pos_ == 'ADJ':
            object.append(token.text)
            objectConstruction.append(object)
            objectConstruction = []

    print (subject, ',', relation, ',', object)
    return (' '.join(subject).strip(), ' '.join(relation).strip(), ' '.join(object).strip())

def processSentence(sentence):
    tokens = nlp_model(sentence)
    return processSubjectObjectPairs(tokens)

def printGraph(triples):
    G = nx.Graph()
    for triple in triples:
        G.add_node(triple[0])
        G.add_node(triple[1])
        G.add_node(triple[2])
        G.add_edge(triple[0], triple[1])
        G.add_edge(triple[1], triple[2])

    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='seagreen', alpha=0.9,
            labels={node: node for node in G.nodes()})
    plt.axis('off')
    plt.show()

if __name__ == '__main__':

    text = '''
        Lights take hex color values.
        Lights can turn blue.
    '''
    text = "London is the capital and largest city of England and the United Kingdom. Standing on the River " \
           "Thames in the south-east of England, at the head of its 50-mile (80 km) estuary leading to " \
        #    "the North Sea, London has been a major settlement for two millennia. " \
        #    "Londinium was founded by the Romans. The City of London, " \
        #    "London's ancient core − an area of just 1.12 square miles (2.9 km2) and colloquially known as " \
        #    "the Square Mile − retains boundaries that follow closely its medieval limits." \
        #    "The City of Westminster is also an Inner London borough holding city status. " \
        #    "Greater London is governed by the Mayor of London and the London Assembly." \
        #    "London is located in the southeast of England." \
        #    "Westminster is located in London." \
        #    "London is the biggest city in Britain. London has a population of 7,172,036."
    sentences = getSentences(text)
    nlp_model = spacy.load('en_core_web_sm')

    triples = []
    for sentence in sentences:
        print()
        triples.append(processSentence(sentence))

    printGraph(triples)