from nltk import Nonterminal,FreqDist, ConditionalFreqDist, grammar
from nltk.tree import Tree
from nltk.corpus import treebank
from chomsky_tree_converter import *



def makeGrammarFromTreebank(fileIDs,cutoff=3):
    """
    Given the treebank file IDs, which can be accessed from treebank.fileids(),
    create a context free grammar.
    """
    parsed_trees = [tree for treelist in [treebank.parsed_sents(file_id) 
                            for file_id in fileIDs] 
                            for tree in treelist]
    
    raw_productions = [p for sent in parsed_trees for p in sent.productions()]
    prods_to_word = [p for p in raw_productions if (p.lhs() != Nonterminal('-NONE-')
                                                and (len(p.rhs()) == 1)
                                                and isinstance(p.rhs()[0],str))]

    #Find words that occur less than 5 times. Replace them with "Unknown"
    myDist = FreqDist([p.rhs()[0] for p in prods_to_word])
    unknowns = {k: "UNK" for k in myDist if myDist[k] <= cutoff}

    #Filters all unknown words out
    def f_tree(t):
        #Check if we're next to a node
        if (len(t) == 1) and (isinstance(t[0],str)):
            if t[0] in unknowns:
                return Tree(t.label(),[unknowns[t[0]]])
            return Tree(t.label(),[t[0]])
        return Tree(t.label(),[f_tree(st) for st in t])
        
    filtered_trees = [f_tree(tree) for tree in parsed_trees]
    
    
    return makeGrammar(filtered_trees)
    


def makeGrammar(trees):
    """
    Given a list of trees, we first convert them into chomsky normal form
    individually. Then, create a list of probabilistic productions and use that
    to to construct a PCFG grammar.
    
    The cutoff field (defaulted to 5) allows us to filter out things that occur
    fewer than 5 times.
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
#files = files[:100] # make shorter for setup
#makeGrammarFromTreebank(files)
