"""
CKY Parser for constituent parsing
"""

from nltk.corpus import treebank
from nltk import Nonterminal, nonterminals, Production, CFG, Tree, ProbabilisticTree,PCFG
from nltk import treetransforms
from functools import reduce
from collections import defaultdict
import nltk

class ckyparser:
    def __init__(self,grammar,success):
        self.rules = grammar.productions()
        self.success = success
        
        
    def getInit(self,x):
        """
        Tries to get a rule that matches x. if no such rule exists,
        produces UNK.
        
        Returns a tuple of (all rules matching x, x or UNK)
        """     
        first_try = [p for p in self.rules if p.rhs()[0] == x]
        if len(first_try)>0:
            return (first_try,x)
        return ([p for p in self.rules if p.rhs()[0] == "UNK"],"UNK")
        
        
    #returns a list of parse trees
    def deterministic_parse(self,sent):
        toks = nltk.word_tokenize(sent)
        #Get the first layer

        n = len(toks)
        inittoks = [self.getInit(x) for x in toks]
        initlayer = [x[0] for x in inittoks]
        newtoks = [x[1] for x in inittoks]

        
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

    def probabilistic_parse_from_sent(self, sent):
        toks = nltk.word_tokenize(sent)
        return self.probabilistic_parse(toks)

    #returns the best parse
    def probabilistic_parse(self,toks):
        n = len(toks)
        inittoks = [self.getInit(x) for x in toks]
        initlayer = [x[0] for x in inittoks]
        newtoks = [x[1] for x in inittoks]
        
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
                
                #A list of all trees we come up with. Not necessarily just
                #the highest ones!
                allTrees = []                
                
                #This dictionary keeps track of the highest probability trees
                #by label that could go in the [i][j] location
                maxProb = defaultdict(float)

                #This dictionary will keep track of the parent for each
                #highest probability tree we see per label.
                bestPointer = {}
                
                
                for (i1,j1),(i2,j2) in zip(up,right):
                    for p in self.rules:
                        if (p.rhs()[0] in [k.lhs() for k in chart[i1][j1]]) and (p.rhs()[1] in [k.lhs() for k in chart[i2][j2]]):                            
                            lt = max([t for t in trees[i1][j1] if t.label() == p.rhs()[0]],key=lambda t: t.prob())
                            rt = max([t for t in trees[i2][j2] if t.label() == p.rhs()[1]],key=lambda t: t.prob())
                            
                            #Construct the tree and add it to the list
                            prob = lt.prob()*rt.prob()*p.prob()
                            allTrees.append(ProbabilisticTree(p.lhs(),[lt,rt],prob=prob))
                            
                            #If the probability is higher than it is for other
                            #trees with the same node, it goes here.
                            if prob > maxProb[p.lhs()]:
                                
                                modp = nltk.grammar.ProbabilisticProduction(p.lhs(),p.rhs(),prob=prob)
                                bestPointer[p.lhs()] = (modp,((i1,j1),(i2,j2)))
                                maxProb[p.lhs()] = prob
                                
                #Filter out all extra trees that don't have the highest probability
                trees[i][j] = [t for t in allTrees if t.prob() == maxProb[t.label()]]
                chart[i][j] = {bp[0]:bp[1] for _,bp in bestPointer.items()}

                                                     
        #trees that are good
        mytrees = [t for t in trees[-1][0] if t.label() == self.success]
       # if len(mytrees) > 0:
       #     print("more than 1 best candidate found")
        if len(mytrees) == 0:
            # print("No trees found")
            return chart,None
        
        return chart,mytrees[0]
