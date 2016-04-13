"""
CKY Parser for constituent parsing
"""

from nltk.corpus import treebank
from nltk import Nonterminal, nonterminals, Production, CFG

# Get the Penn Treebank corpus
files = treebank.fileids()
files = files[:5] # make shorter for setup

parsed_sents = [sent for sentlist in [treebank.parsed_sents(file_id) for file_id in files] for sent in sentlist]
print(parsed_sents[0])




class ckyparser:
    def __init__(self,rules,nts):
        self.rules = rules
        self.nts = nts
        

    def parse(self,sent):
        toks = sent.split(' ')
        #Get the first layer
        initlayer = [[p.lhs() for p in self.rules if p.rhs()[0] == x] for x in toks]
        curlayer = initlayer
        laterlayers = [curlayer]
        for i in range(len(initlayer)):
            newlayer = []
            for (bs,cs) in zip(curlayer[:-1],curlayer[1:]):
                for b in bs:
                    for c in cs:
                        print(b,c)
                        newlayer.append([p.lhs() for p in self.rules if p.rhs() == (b,c)])
            laterlayers.append(newlayer)
            curlayer = newlayer
        
        for l in laterlayers[::-1]:
            print(l)
        
        #Unary rules
        





nts = nonterminals('S, NP, VP, PP, N, V, P, DT')
#grammar = CFG.fromstring("""
#... S -> NP VP
#... PP -> P NP
#... NP -> 'the' N | N PP | 'the' N PP
#... VP -> V NP | V PP | V NP PP
#... N -> 'cat'
#... N -> 'dog'
#... N -> 'rug'
#... V -> 'chased'
#... V -> 'sat'
#... P -> 'in'
#... P -> 'on' """)

myparser = ckyparser(grammar.productions(),nts)
myparser.parse("the cat sat on the dog")