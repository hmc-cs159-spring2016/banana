# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:49:04 2016

@author: rowan
"""

from nltk.corpus import treebank
from nltk import Nonterminal, nonterminals, Production, CFG, Tree, ProbabilisticTree,PCFG
from nltk import treetransforms
from functools import reduce
from collections import defaultdict
import nltk
import cky_parser
from probabilities import *

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
files = treebank.fileids()
files = files[:100] # make shorter for setup
gram = makeGrammarFromTreebank(files)
myparser = cky_parser.ckyparser(gram,Nonterminal('S'))
chart,mytrees=myparser.probabilistic_parse_from_sent("I saw John with my telescope")



#
#
#
#
### Deterministic parse
#
#import chomsky_converter 
#cfg_grammar = nltk.data.load("project1_grammar.cfg")
#cnf_grammar = chomsky_converter.convert_grammar(cfg_grammar)
#
#
##Check it
#nts = nonterminals('S, NP, VP, PP, N, V, P, DT')
#
##s = '(S (NP (DT the) (NN cat)) (VP (VBD ate) (NP (DT a) (NN cookie))))'
##t = Tree.fromstring(s)
##t.chomsky_normal_form()
#
#myparser = cky_parser.ckyparser(cnf_grammar,Nonterminal('TOP'))
#
#with open('sentences.txt','r') as f:
#    allexamples = f.read().splitlines()
#for ex in allexamples:
#    chart,mytrees=myparser.deterministic_parse(ex)
#    if len(mytrees)>0:
#        print("success")
#    else:
#        print("fail")
#        print(ex)
#        print(nltk.word_tokenize(ex))
#        print(mytrees)
#        
#        