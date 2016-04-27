from nltk.corpus import dependency_treebank
from nltk.grammar import DependencyGrammar, Production, DependencyProduction
from nltk.parse import DependencyGraph, DependencyEvaluator
from nltk.tree import Tree
import nltk
import malt_parser
import random


def dependencyGraphToProductionList(depGraph):
	"""
	Input: A DependencyGraph
	Output: A list of DependencyProduction objects
	"""
	storage = {}
	for subtree in depGraph.tree().subtrees():
		storage[subtree.label()] = [(a.label() if type(a)==nltk.tree.Tree else a) for a in list(subtree)]
	return [DependencyProduction(a, storage[a]) for a in storage.keys()]

def dependencyGraphsToGrammar(depGraphs):
	"""
	Input: A list of DependencyGraph objects
	Output: A DependencyGrammar
	"""
	output = []
	for graph in depGraphs:
		output += dependencyGraphToProductionList(graph)
	return DependencyGrammar(output)

def compareDependencyTrees(testTree, refTree):
	"""
	Input: 2 Trees, the first is the test, the second is the reference
	Output: True if the trees are the same, not dependent on order of subtrees
	"""
	# If the standard comparison says it's true, it's true
	if testTree == refTree:
		return True
	testSubs = list(testTree)
	refSubs = list(refTree)

	# If one of the trees is a string, since they aren't the same by direct comparison,
	# they must not be the same.
	if type(testTree) == str or type(refTree) == str:
		return False

	# If the labels are not the same or the numbers of subtrees
	if testTree.label() != refTree.label() or len(testSubs) != len(refSubs):
		return False

	# If a subtree is not in the other tree, then it should be marked as -1. If it is, mark it with
	# the index
	# Go through every subtree
	foundList = [-1]*len(testSubs)
	for test in range(len(testSubs)):
		for ref in range(len(refSubs)):

			# If one is a string and the other is a Tree
			if (type(testSubs[test]) != type(refSubs[ref])):
				continue

			# If both are strings, do a direct comparison
			elif (type(testSubs[test]) == str):
				if testSubs[test] == refSubs[ref]:
					foundList[test] = ref

			# Otherwise recurse
			elif compareDependencyTrees(refSubs[ref], testSubs[test]):
				foundList[test] = ref

	return not (-1 in foundList)


def crossValidation(numIter, testProp):
	"""
	Input: The number of iterations to run and the proportion of 
	Output: The average proportion of correctly parsed sentences
	"""
	numTest = int(testProp * 1000)
	numList = list(range(1000))
	counter = [0]*numIter

	# repeat numIter times
	for i in range(numIter):
		print("Starting iteration: ", i)

		# Shuffle list of indices of the dependency treebank sentences and set the first numTests
		# as the test sentences.
		random.shuffle(numList)
		tests = numList[:numTest]
		grams = numList[numTest:]
		grammar = dependencyGraphsToGrammar([dependency_treebank.parsed_sents()[sent] for sent in grams])
		parser = malt_parser.maltparser(grammar)

		# try every test sentence. See how the parser does
		for test in tests:
			testSent = parser.parse(dependency_treebank.sents()[test])
			refSent = dependency_treebank.parsed_sents()[test].tree()
			if compareDependencyTrees(testSent,refSent):
				counter[i] += 1

	# return the average score of all of the iterations.
	return sum(counter)/(numTest*numIter)

# Small test from http://www.nltk.org/howto/dependency.html

# grammar0 = DependencyGrammar([Production('taught',['play', 'man']),Production('man',['the']),Production('play',['golf','dog','to']),Production('dog',['his'])])

# a = maltparser(grammar0)
# print(a.parse(['the','man','taught','his','dog','to','play','golf']))

# grammar1 = DependencyGrammar([Production('fell',['price','stock']),Production('price',['of','the']),Production('of',['stock']),Production('stock',['the'])])
# b = maltparser(grammar1)
# print(b.parse(nltk.word_tokenize('the price of the stock fell')))


# grammar = dependencyGraphsToGrammar(dependency_treebank.parsed_sents()[:100])
# parser = malt_parser.maltparser(grammar)
# a = parser.parse(dependency_treebank.sents()[101])
# print(a == dependency_treebank.parsed_sents()[101].tree())
# # print(compareDependencyTrees(a,dependency_treebank.parsed_sents()[0].tree()))
# print(a)
# print(dependency_treebank.parsed_sents()[101].tree())
print(crossValidation(1,.001))
