from nltk.corpus import treebank, conll2007
from nltk.grammar import DependencyGrammar, Production
from nltk.tree import Tree
import nltk

class maltparser:
	def __init__(self, grammar):
		# the grammar
		self.grammar = grammar

	def parse(self, sent):
		"""
		Input: A sentence as a string
		Output: An nltk.tree.Tree object of the dependency parse of the sentence
		"""
		toks = nltk.word_tokenize(sent)
		headlist = []
		wordlist = []
		arcset   = set()
		headFound = False

		for word in toks:

			# see if word is the head of anything in headlist
			delList = []
			for needHead in range(len(headlist)):
				if self.grammar.contains(word,headlist[needHead]):
					arcset.add((word,headlist[needHead]))
					delList.append(needHead)

				# remove words 
			for rem in delList[::-1]:
				headlist.pop(rem)

			# see if anything in wordlist is head of word
			for isHead in wordlist:

				if self.grammar.contains(isHead,word):
					arcset.add((isHead,word))
					headFound = True
					break # Can't have more than one head

			# Add word to list of words without heads if haven't found head
			if not headFound:
				headlist.append(word)
			wordlist.append(word)

		# List of words without a head should be 1 if everything has a relation
		if len(headlist) > 1:
			print("WARNING: SOME WORDS DID NOT FIND A HEAD")

		return self.relations(arcset, toks, headlist[0])

	def relations(self, arcset, toks, head):
		"""
		Input: A set of relations, a tokenized sentence, and the head of the sentence
		Output: An nltk.tree.Tree object of the dependency parsed sentence
		"""
		children = {}
		for word in toks:
			children[word] = []
			for rel in arcset:
				if word == rel[0]:
					children[word].append(rel[1])
		return self.makeTree(children,head)


	def makeTree(self, children, head):
		"""
		Input: A dictionary of heads (keys) and modfiers and the root head
		Output: An nltk.tree.Tree object of the dependency parsed sentence
		"""
		if len(children[head]) == 0:
			return head
		return Tree(head, [self.makeTree(children, word) for word in children[head]])

# g = DependencyGrammar([Production('world',['hello']),Production('hello',['hi','bye'])])
# print(g.contains('world','hello'))
# a = maltparser(g)
# b = a.parse('bye hello world hi')
# print(b)

grammar = DependencyGrammar([Production('taught',['play', 'man']),Production('man',['the']),Production('play',['golf','dog','to']),Production('dog',['his'])])

a = maltparser(grammar)
print(a.parse('the man taught his dog to play golf'))
