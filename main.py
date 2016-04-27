"""
Here, we get the training data & evaluate our parsers
"""
import nltk
from nltk.corpus import treebank
from nltk.grammar import is_nonterminal, Production
from sklearn import cross_validation as cv

import chomsky_tree_converter as ctc
import probabilities 
from cky_parser import ckyparser

def get_trees(fileids=None, verbose=False):
	""" 
	Get the CNF trees for the treebank fileids given, or for the entire treebank
	"""
	if not fileids:
		# Get the Penn Treebank corpus
		fileids = treebank.fileids()

	# Get the sentence-trees in each file
	tree_lists = [treebank.parsed_sents(file_id) for file_id in fileids]
	trees = [sent for sent_list in tree_lists for sent in sent_list]
	if verbose:
		print("obtained", len(trees), "trees from the corpus.")

	cnf_trees = [ctc.convert_tree(t) for t in trees]
	if verbose:
		print("converted", len(trees), "trees to cnf.")

	return cnf_trees


def cross_validate(fileids=None, num_folds=10, verbose=False):
	"""
	Test the CKY parser using cross-validation 
	"""
	trees = get_trees(fileids, verbose)

	original_trees = []
	resulting_trees = []
	for i in range(0, num_folds):
		if verbose:
			print("Starting cross validation round,",i)
		train, test = cv.train_test_split(trees, test_size=0.1)
		grammar = probabilities.makeGrammar(train)
		myparser = ckyparser(grammar, ctc.start_symbol)
		for tree in test:
			sentence = tree.leaves()
			chart,mytree = myparser.probabilistic_parse(sentence)

			# We don't have actual evaluation yet, here they are next to each other.
			if mytree:
				print("actual:", tree)
				print("gotten:", mytree)
			else:
				print("could not parse", tree.leaves())


print(cross_validate(fileids=treebank.fileids()[:50], verbose=True))
