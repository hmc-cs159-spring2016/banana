"""
Here, we get the training data & evaluate our parsers
"""
import nltk
from nltk.corpus import treebank
from nltk.grammar import is_nonterminal, Production
from sklearn import cross_validation as cv

import chomsky_tree_converter as ctc
import probabilities 
import evalb
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
	parsed_num = 0
	unparsed_num = 0
	avg_accuracy = 0

	for i in range(0, num_folds):
		if verbose:
			print("Starting cross validation round", i)
		original_trees = []
		resulting_trees = []
		unsuccessful_parses = 0

		# Split the data for this fold, & train, test on 1%, because parsing is so slow
		train, test = cv.train_test_split(trees, test_size=0.01)
		grammar = probabilities.makeGrammar(train)
		myparser = ckyparser(grammar, ctc.start_symbol)

		# Test all the test sentences
		for tree in test:
			sentence = tree.leaves()
			chart, mytree = myparser.probabilistic_parse(sentence)

			if mytree:
				original_trees += [tree]
				resulting_trees += [mytree]
			else:
				unsuccessful_parses += 1

		if original_trees:
			# If we got some successful parses, evaluate these:
			accuracy = evalb.evalb(resulting_trees, original_trees)
			count = len(original_trees)

			if verbose:
				print("In fold", i, "we parsed", count, "sentences with an accuracy of", accuracy)

			# Update the count and averages
			avg_accuracy = (avg_accuracy*parsed_num + accuracy*count)
			parsed_num += count
			avg_accuracy /= parsed_num

		unparsed_num += unsuccessful_parses

	# Aggregate results.
	if verbose:
		print("We parsed", parsed_num, "sentences with an accuracy of", avg_accuracy)
		print("We could not parse", unparsed_num, "sentences")
	return avg_accuracy

print(cross_validate(fileids=treebank.fileids()[:50], verbose=True))
