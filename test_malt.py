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
	if testTree == refTree:
		return True
	testSubs = list(testTree)
	refSubs = list(refTree)

	if type(testTree) == str:
		return False
	if testTree.label() != refTree.label() or len(testSubs) != len(refSubs):
		return False

	foundList = [-1]*len(testSubs)
	for test in range(len(testSubs)):
		for ref in range(len(refSubs)):
			if (type(testSubs[test]) != type(refSubs[ref])):
				continue
			elif (type(testSubs[test]) == str):
				if testSubs[test] == refSubs[ref]:
					foundList[test] = ref
			elif compareDependencyTrees(refSubs[ref], testSubs[test]):
				foundList[test] = ref

	return not (-1 in foundList)


def crossValidation(numIter, testProp):
	"""
	Input: The number of iterations to run and the proportion of 
	Output: The average proportion of correctly parsed sentences
	"""
	numTest = int(testProp * len(dependency_treebank.parsed_sents()))
	numList = list(range(len(dependency_treebank.parsed_sents())))
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
			print(test)
			testSent = parser.parse(dependency_treebank.sents()[test])
			refSent = dependency_treebank.parsed_sents()[test].tree()
			if compareDependencyTrees(testSent,refSent):
				counter[i] += 1

	# return the average score of all of the iterations.
	return sum(counter)/numTest



	# # Go through every subtree one level down in testTree
	# for tree0 in testTree.subtrees(lambda t: t.height() == 2):
	# 	sameTree = False

	# 	# Go through every subtree one level down in refTree
	# 	for tree1 in refTree.subtrees(lambda t: t.height() == 2):
	# 		if compareDependencyTrees(tree0,tree1):
	# 			sameTree = True
	# 			break
	# 	if not sameTree:
	# 		return False
	# return True


grammar = dependencyGraphsToGrammar(dependency_treebank.parsed_sents()[:100])
parser = malt_parser.maltparser(grammar)
a = parser.parse(dependency_treebank.sents()[101])
# print(a == dependency_treebank.parsed_sents()[101].tree())
# # print(compareDependencyTrees(a,dependency_treebank.parsed_sents()[0].tree()))
# print(a)
# print(dependency_treebank.parsed_sents()[101].tree())
crossValidation(2,.001)