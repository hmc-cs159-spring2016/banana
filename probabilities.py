from nltk import Nonterminal,FreqDist, ConditionalFreqDist, grammar
from nltk.corpus import treebank
from chomsky_tree_converter import *


def makeGrammarFromTreebank(fileIDs):
    """
    Given the treebank file IDs, which can be accessed from treebank.fileids(),
    create a context free grammar.
    """
    parsed_trees = [tree for treelist in [treebank.parsed_sents(file_id) for file_id in files] for tree in treelist]
    return makeGrammar(parsed_trees)
    


def makeGrammar(trees):
    """
    Given a list of trees, we first convert them into chomsky normal form
    individually. Then, create a list of probabilistic productions and use that
    to to construct a PCFG grammar.
    """
    converted_trees = [convert_tree(tree) for tree in trees]
    # Get Freqdist of productions!
    productions = [p for sent in converted_trees for p in sent.productions()]
    
    myDist = ConditionalFreqDist((p.lhs(), p) for p in productions)
    
    myProductions = []
    for lhs in myDist:
        for p in myDist[lhs]:
            myProductions.append(grammar.ProbabilisticProduction(p.lhs(),p.rhs(),prob=myDist[lhs].freq(p)))
            
    myGrammar = grammar.PCFG(Nonterminal(start_symbol),myProductions)
    
    return myGrammar

#Ex.
# Get the Penn Treebank corpus
#files = treebank.fileids()
#files = files[:5] # make shorter for setup
#makeGrammarFromTreebank(files)