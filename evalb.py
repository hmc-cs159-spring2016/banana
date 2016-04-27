# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 17:10:11 2016

Computes the distance between two trees. Adapted from 
http://www.isi.edu/natural-language/teaching/cs562/2009/hw5/hw5.pdf

@author: rowan
"""

import sys
import itertools, collections
from nltk.tree import Tree

def _brackets_helper(node, i, result):
    i0 = i
    
    children = [x for x in node if not isinstance(x,str)]    
    if len(children) > 0: #If there are any children
        for child in children:
            i = _brackets_helper(child, i, result)
        j0 = i
        cchildren = [x for x in node[0] if not isinstance(x,str)]
        if len(cchildren) > 0: # don't count preterminals
            result[node.label(), i0, j0] += 1
    else:
        j0 = i0 + 1
    return j0

def brackets(t):
    result = collections.defaultdict(int)
    _brackets_helper(t, 0, result)
    return result

def evalb(test_trees,gold_trees):
    """
    Call this on two list of trees
    """
    matchcount = testcount = goldcount = 0
    
    for test_tree,gold_tree in zip(test_trees,gold_trees):
        goldbrackets = brackets(gold_tree)
        goldcount += len(goldbrackets)
    
        testbrackets = brackets(test_tree)
        testcount += len(testbrackets)
    
        for bracket,count in testbrackets.items():
            matchcount += min(count,goldbrackets[bracket])

    #print("{}\t{} brackets".format(' '.join(test_tree.leaves()), testcount))
    #print("{}\t{} brackets".format(' '.join(gold_tree.leaves()), goldcount))
    #print("matching\t{} brackets".format(matchcount))
    return(matchcount/goldcount)
    
    