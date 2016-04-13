"""
CKY Parser for constituent parsing
"""

from nltk.corpus import treebank
from nltk import Nonterminal, nonterminals, Production, CFG, Tree, ProbabilisticTree
from functools import reduce
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

        n = len(toks)
        
        initlayer = [[p.lhs() for p in self.rules if p.rhs()[0] == x] for x in toks]
        
        #where 
        chart = [[[] for x in range(i+1)] for i in range(n)]
        bts = [[[] for x in range(i+1)] for i in range(n)]
        for i,elem in enumerate(initlayer):
            chart[i][i] = elem
        
        for depth in range(1,n): #iterate along depth n
            height = n-depth
            for target in range(height):
                i = depth + target
                j = target
                
                #List of all relevant things to look at
                up =  [(i-x,j) for x in range(1,depth+1)]
                right = [(i,j+x) for x in range(1,depth+1)]
                
                allNTs = []
                allBTs = []
                for (i1,j1),(i2,j2) in zip(up,right):
                    
                    thingstoadd = [p.lhs() for p in self.rules if (p.rhs()[0] in chart[i1][j1] and p.rhs()[1] in chart[i2][j2])]
                    if len(thingstoadd) > 0:
                        allBTs.append(((i1,j1),(i2,j2)))
                    allNTs.append(set(thingstoadd))
                chart[i][j] = list(reduce(set.union, allNTs))
                bts[i][j] = allBTs
                
        return chart,bts
        
        




#Check it
nts = nonterminals('S, NP, VP, PP, N, V, P, DT')

s = '(S (NP (DT the) (NN cat)) (VP (VBD ate) (NP (DT a) (NN cookie))))'
t = Tree.fromstring(s)
t.chomsky_normal_form()

myparser = ckyparser(t.productions(),nts)
myparser.parse("the cat ate a cookie")