"""
Here, we get the training data & evaluate our parsers
"""
import nltk
from nltk.corpus import treebank

# Get the Penn Treebank corpus
files = treebank.fileids()
files = files[:5] # make shorter for setup

parsed_sents = [sent for sentlist in [treebank.parsed_sents(file_id) for file_id in files] for sent in sentlist]
print(parsed_sents[0])

grammar = nltk.data.load("project1_grammar.cfg")
print(grammar)