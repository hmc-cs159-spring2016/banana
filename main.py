"""
Here, we get the training data & evaluate our parsers
"""

from nltk.corpus import treebank

# Get the Penn Treebank corpus
files = treebank.fileids()
parsed_sents = [treebank.parsed_sents(file_id) for file_id in files]
