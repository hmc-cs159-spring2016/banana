"""
CKY Parser for constituent parsing
"""

from nltk.corpus import treebank
from nltk import Nonterminal, nonterminals, Production, CFG, Tree, ProbabilisticTree,PCFG
from nltk import treetransforms
from functools import reduce
from collections import defaultdict
import nltk
# Get the Penn Treebank corpus
files = treebank.fileids()
files = files[:5] # make shorter for setup

parsed_sents = [sent for sentlist in [treebank.parsed_sents(file_id) for file_id in files] for sent in sentlist]
print(parsed_sents[0])



class ckyparser:
    def __init__(self,rules,success):
        self.rules = rules
        self.success = success
        
    #returns a list of parse trees
    def deterministic_parse(self,sent):
        toks = nltk.word_tokenize(sent)
        #Get the first layer

        n = len(toks)
        
        initlayer = [[p for p in self.rules if p.rhs()[0] == x] for x in toks]
        
        #Fill in initial things along the diagonal
        chart = [[{} for x in range(i+1)] for i in range(n)]
        trees = [[[] for x in range(i+1)] for i in range(n)]
        for i,plist in enumerate(initlayer):
            for p in plist:
                chart[i][i][p] = None
                trees[i][i].append(Tree(p.lhs(),[p.rhs()[0]]))
        
        for depth in range(1,n): #iterate along depth n
            height = n-depth
            for target in range(height):
                i = depth + target
                j = target
                
                #List of all relevant things to look at
                up =  [(i-x,j) for x in range(1,depth+1)][::-1]
                right = [(i,j+x) for x in range(1,depth+1)]
                
                for (i1,j1),(i2,j2) in zip(up,right):
                    for p in self.rules:
                        if (p.rhs()[0] in [k.lhs() for k in chart[i1][j1]]) and (p.rhs()[1] in [k.lhs() for k in chart[i2][j2]]):
                            lefttrees = [t for t in trees[i1][j1] if t.label() == p.rhs()[0]]
                            righttrees = [t for t in trees[i2][j2] if t.label() == p.rhs()[1]]
                            
                            chart[i][j][p] = ((i1,j1),(i2,j2))
                        
                            for lt in lefttrees:
                                for rt in righttrees:
                                    newt = Tree(p.lhs(),[lt,rt])
                                    if newt not in trees[i][j]:
                                        trees[i][j].append(newt)
                            
        #trees that are good
        mytrees = [t for t in trees[-1][0] if t.label() == self.success]
        
        return chart,mytrees

    #returns the best parse
    def probabilistic_parse(self,sent):
        toks = nltk.word_tokenize(sent)
        #Get the first layer

        n = len(toks)
        
        initlayer = [[p for p in self.rules if p.rhs()[0] == x] for x in toks]
        
        #Fill in initial things along the diagonal
        chart = [[{} for x in range(i+1)] for i in range(n)]
        trees = [[[] for x in range(i+1)] for i in range(n)]
        for i,plist in enumerate(initlayer):
            for p in plist:
                chart[i][i][p] = None
                mytree = ProbabilisticTree(p.lhs(),[p.rhs()[0]],prob=p.prob())
                trees[i][i].append(mytree)
        
        for depth in range(1,n): #iterate along depth n
            height = n-depth
            for target in range(height):
                i = depth + target
                j = target
                
                #List of all relevant things to look at
                up =  [(i-x,j) for x in range(1,depth+1)][::-1]
                right = [(i,j+x) for x in range(1,depth+1)]
                #Keep track of the highest probability candidates by label
                maxProb = defaultdict(int)
                bestPointer = {}
                for (i1,j1),(i2,j2) in zip(up,right):
                    for p in self.rules:
                        if (p.rhs()[0] in [k.lhs() for k in chart[i1][j1]]) and (p.rhs()[1] in [k.lhs() for k in chart[i2][j2]]):                            
                            lt = max([t for t in trees[i1][j1] if t.label() == p.rhs()[0]],key=lambda t: t.prob())
                            rt = max([t for t in trees[i2][j2] if t.label() == p.rhs()[1]],key=lambda t: t.prob())
                            
                            prob = lt.prob()*rt.prob()*p.prob()
                            trees[i][j].append(ProbabilisticTree(p.lhs(),[lt,rt],prob=prob))
                            if prob > maxProb[p.lhs()]:
                                modp = nltk.grammar.ProbabilisticProduction(p.lhs(),p.rhs(),prob=prob)
                                
                                bestPointer[p.lhs()] = (modp,((i1,j1),(i2,j2)))
                                maxProb[p.lhs()] = prob
                                
                chart[i][j] = {bp[0]:bp[1] for _,bp in bestPointer.items()}

                                                     
        #trees that are good
        mytrees = [t for t in trees[-1][0] if t.label() == self.success]
        
        return chart,mytrees
    

toy_pcfg1 = PCFG.fromstring("""
    S -> NP VP [1.0]
    NP -> Det N [0.5] | NP PP [0.25] | 'John' [0.1] | 'I' [0.15]
    Det -> 'the' [0.8] | 'my' [0.2]
    N -> 'man' [0.5] | 'telescope' [0.5]
    V -> 'ate' [0.35] | 'saw' [0.65]
    VP -> VP PP [0.1] | V NP [0.7] | 'ate' [0.07] | 'saw' [0.13]
    PP -> P NP [1.0]
    P -> 'with' [0.61] | 'under' [0.39]
    """)
    
#toy_pcfg1 = treetransforms.chomsky_normal_form(toy_pcfg1)
myparser = ckyparser(toy_pcfg1.productions(),Nonterminal('S'))
chart,mytrees=myparser.probabilistic_parse("I saw John with my telescope")







## Deterministic parse

import chomsky_converter 
cfg_grammar = nltk.data.load("project1_grammar.cfg")
cnf_grammar = chomsky_converter.convert_grammar(cfg_grammar)


#Check it
nts = nonterminals('S, NP, VP, PP, N, V, P, DT')

#s = '(S (NP (DT the) (NN cat)) (VP (VBD ate) (NP (DT a) (NN cookie))))'
#t = Tree.fromstring(s)
#t.chomsky_normal_form()

myparser = ckyparser(cnf_grammar.productions(),Nonterminal('TOP'))

with open('sentences.txt','r') as f:
    allexamples = f.read().splitlines()
for ex in allexamples:
    chart,mytrees=myparser.deterministic_parse(ex)
    if len(mytrees)>0:
        print("success")
    else:
        print("fail")
        print(ex)
        print(nltk.word_tokenize(ex))
        print(mytrees)
        
        
