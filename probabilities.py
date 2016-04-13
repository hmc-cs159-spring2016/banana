from nltk import FreqDist, ConditionalProbDist, MLEProbDist, grammar, CFG, production
from nltk.corpus import treebank

def getProdProb(parsedTree, freqdist):
	"""
	Input: nltk.tree.Tree object, FreqDist object
	Output: nothing
	"""
	prodList = parsedTree.productions()

	for prod in prodList:
		if prod in freqdist:
			freqdist[prod] += 1
		else:
			freqdist[prod] = 1
	return
	



