"""
Here, we get the training data & evaluate our parsers
"""
import nltk
import chomsky_converter as cc
from nltk.corpus import treebank
from nltk import FreqDist

# Get the Penn Treebank corpus
files = treebank.fileids()
files = files[:5] # make shorter for setup

parsed_sents = [sent for sentlist in [treebank.parsed_sents(file_id) for file_id in files] for sent in sentlist]

# Get Freqdist of productions!
productions = [p for sent in parsed_sents for p in sent.productions()]
freqs = FreqDist(productions)
print(freqs.items())
			


