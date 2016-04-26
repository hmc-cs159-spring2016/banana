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

	for i in range(0, num_folds):
		train, test = cv.train_test_split(trees, test_size=0.1)
		grammar = probabilities.makeGrammar(train)
		myparser = ckyparser(grammar, ctc.start_symbol)
		for tree in test:
			sentence = tree.leaves()
			chart,mytrees = myparser.probabilistic_parse(sentence)

			# We don't have actual evaluation yet, here they are next to each other.
			if mytrees:
				print("actual:", tree)
				print("gotten:", mytrees)
			else:
				print("could not parse", tree)


# print(cross_validate(fileids=treebank.fileids()[:5], verbose=True))

# http://www.nltk.org/_modules/nltk/parse/evaluate.html
tree_lists = [treebank.parsed_sents(file_id) for file_id in treebank.fileids()]
for i in range(0, len(tree_lists)):
	trees = tree_lists[i]
	print(i)
	cnf_trees = [ctc.convert_tree(t) for t in trees]
	productions = [t.productions() for t in cnf_trees]
	for prod in productions:
		if len(prod) == 1 & is_nonterminal(prod[0]):
			print("bad production:", prod)



# Messing ground for things, will get rid of later
# ##########
# groucho_grammar = nltk.CFG.fromstring(""" 
# S -> NP VP 
# PP -> P NP 
# NP -> Det N | Det N PP | 'I' 
# VP -> V NP | VP PP 
# Det -> 'an' | 'my' 
# N -> 'elephant' | 'pajamas' 
# V -> 'shot' 
# P -> 'in' 
# """)
# sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
# parser = nltk.ChartParser(groucho_grammar)
# for tree in parser.parse(sent):
#     print(tree.flatten())
