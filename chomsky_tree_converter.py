"""
Converts non-chomsky normal form tree to a chomsky-tree
"""

import nltk
from nltk.tree import Tree

start_symbol = 'START'

def add_start_symbol(tree_parse):
    """
    START - add a new start symbol that won't ever be produced
    """
    return Tree(start_symbol, [tree_parse])

def singularize_terminals(tree_parse, allowed_to_be_terminal=True):
    """
    TERM - recursively remove terminals in non-terminal positions, inserting intermediate
    Argument:
    - allowed_to_be_terminal - a boolean that marks whether this is
      "allowed" to be a word, a leaf, because in CNF, terminals can only be
      only children.
    """
    if type(tree_parse) == str:
        # We've got a leaf!
        # This is a terminal - but if we have siblings, then we aren't in an 
        # A -> word rule, so we need to inject a non-terminal wrapper.
        if allowed_to_be_terminal:
            return tree_parse
        else:
            # Insert wrapper parent for non terminal
            return Tree(tree_parse, [tree_parse])
    else:
        # Call recursively on children, marking them either as single children 
        # or multiples
        has_single_child = len(tree_parse) == 1
        children = [singularize_terminals(t, has_single_child) for t in tree_parse]
        return Tree(tree_parse.label(), children)

def split_large_families(tree_parse):
    """ 
    BIN - split productions with too many children 
    """
    if type(tree_parse) == str:
        # Terminal here - base case
        return tree_parse

    if len(tree_parse) > 2:
        # We have too many children! Oh no
        nonterminal_label = tree_parse.label()
        first_child_tree = tree_parse[0]
        remaining_tree_label = nonterminal_label + "_" + first_child_tree.label()
        remaining_tree = Tree(remaining_tree_label, tree_parse[1:])

        # We're going to make a tree with the first child and this synthetic 
        # "remaining" subtree list. We have to first convert both to CNF
        child1 = split_large_families(first_child_tree)
        child2 = split_large_families(remaining_tree)
        return Tree(nonterminal_label, [child1, child2])

    else:
        # No splitting necessary here, but we still need to check the children
        children = [split_large_families(t) for t in tree_parse]
        return Tree(tree_parse.label(), children)


def eliminate_units(tree_parse):
    """
    UNIT - eliminate unit rules by replacing the child with its child[ren]
    """
    if type(tree_parse) == str:
        # Base Case, return this leaf!
        return tree_parse

    if len(tree_parse) == 1:
        # We've got a singleton!
        if type(tree_parse[0]) == str:
            # We've got a terminal child, we're fine
            return tree_parse
        else:
            # Bypass the single child, point straight to the grandchildren
            # Don't forget to check grandchildren recursively.
            child = tree_parse[0]

            grandchildren = [eliminate_units(t) for t in child]
            return Tree(tree_parse.label(), grandchildren)


    else:
        # No unit to remove, check children recursively
        children = [eliminate_units(t) for t in tree_parse]
        return Tree(tree_parse.label(), children)


def convert_tree(tree_parse):
    """
    Converts to Chomsky_Normal_form
    
    Args:
        - tree_parse - the nltk.tree Tree parse structure
        
    Traverses the tree recursively, adding intermediaries where needed, for 
    terminals in the wrong place, or for >2 numbers of children, in a consistent
    way that will maintain naming for the same rule sequence.

    It also removes nodes that lead to a single non-terminal, shortening the 
    tree where it would expand on single A->B->[] paths by eliminating B

    Unfortunately, because these removal and addition actions are not commutative,
    we have to iterate through the tree iteratively. The order chosen is the
    one outline on Wikipedia:
        1. START - add a new start symbol that won't ever be produced
        2. TERM - remove terminals in non-terminal positions, inserting intermediate
        3. BIN - split productions with too many children
        X. DEL - eliminate epsilon rules - Not necessary, we're working with 
            real parse trees, empty rules shouldn't occur
        4. UNIT - eliminate unit rules by replacing the child with its child[ren]
    """
    tree_START = add_start_symbol(tree_parse)
    tree_TERM  = singularize_terminals(tree_START)
    tree_BIN   = split_large_families(tree_TERM)
    tree_UNIT  = eliminate_units(tree_BIN)

    return tree_UNIT
 
  

