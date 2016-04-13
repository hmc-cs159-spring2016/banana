"""
Converts non-chomsky normal form grammar to CNF
"""

import nltk
from nltk.grammar import is_terminal, is_nonterminal, CFG, Production, Nonterminal

def break_large_rhs(lhs, rhs):
	"""
	Recursively return a list of rules that result in the same production, but have only 
	2 elements on the right hand side
	"""
	# Base case - return as is if short enough
	if len(rhs) < 3:
		return [Production(lhs, rhs)]

	# Break off the tail, making 
	newnonterm = Nonterminal(lhs.symbol()+"_"+rhs[0].symbol())
	newrule = Production(lhs, [rhs[0], newnonterm])
	print("New intermediate rule", newrule)
	return [newrule] + break_large_rhs(newnonterm, rhs[1:])

def remove_empty_productions(cfg_grammar):
	"""
	Remove empties, by making sure all upstream productions can produce none of that
	unfortunately, this is recursive, because you might create emtpies as you're removing things
	"""
	empties = list(cfg_grammar.productions(empty=True))
	if not empties:
		return cfg_grammar

	# Deal with the 1st empty
	empty = empties[0]
	print("running empty for", empty)
	nullable = empty.lhs()

	new_rules = []
	for production in cfg_grammar.productions():
		if nullable in production.rhs():
			# create a new rule for this production without the nullable thing
			lhs = production.lhs()
			rhs = [x for x in production.rhs() if x != nullable]
			print("removing", nullable, "from", production, "yields rhs of", rhs)
			new_rules += [Production(lhs, rhs)]
		
		# Maintain all original productions, except for the empty one we're removing
		if production != empty:
			# we're fine
			new_rules += [production]

	new_cfg = CFG(cfg_grammar.start(), new_rules)
	return remove_empty_productions(new_cfg)


def remove_unitary_productions(cfg_grammar):
	"""
	Remove unitary-productions that aren't terminals, by making sure all 
	downstream productions get trickled up

	unfortunately, this is recursive, because you might create singletons as you're shifting things
	Note, this does NOT detect cycles
	"""
	unary = False
	productions = cfg_grammar.productions()
	for production in productions:
		if len(production) == 1:
			# Identity the first unary productions
			if is_nonterminal(production.rhs()[0]):
				unary = production
				break

	if not unary:
		# Base Case
		return cfg_grammar
	else:
		# get all productions of B, so we can make them all productions of A
		b_prods = cfg_grammar.productions(lhs=unary.rhs()[0])
		b_rhses = [b_prod.rhs() for b_prod in b_prods]

		existing_productions = [prod for prod in productions if prod != unary]
		new_productions = [Production(unary.lhs(), b_rhs) for b_rhs in b_rhses]

		new_grammar = CFG(cfg_grammar.start(), existing_productions+new_productions)
		return remove_unitary_productions(new_grammar)


def convert_grammar(cfg_grammar):
	"""
	Converts to Chomsky_Normal_form
	"""
	if cfg_grammar.is_chomsky_normal_form():
		return cfg_grammar

	# Go through every rule, and do the following conversions:
	# - remove terminals in non-solitary rules
	# - break up greater-than-2 rules
	# Notice that this loop-through will blissfully ignore small productions
	new_productions = []
	for production in cfg_grammar.productions():
		rhs_size = len(production)
		lhs = production.lhs()
		rhs = production.rhs()
		if rhs_size < 2:
			new_productions += [Production(lhs,rhs)]
		else:
			# Go through removing terminals
			term_rules = []
			for i in range(0, rhs_size):
				if is_terminal(rhs[i]):
					newnonterm = Nonterminal(rhs[i])
					term_rules += Production(newnonterm, rhs)
					rhs[i] = newnonterm
					print("terminal in nonsolitary,", production)
			new_productions += term_rules
			# Now break up large groups
			new_productions += break_large_rhs(lhs, rhs)

	# Reset for next loop through
	new_cfg = CFG(cfg_grammar.start(), new_productions)
	assert(new_cfg.is_binarised())

	# Remove empty productions 
	new_cfg = remove_empty_productions(new_cfg)

	# Go through the rules again, removing non-terminals in solitary rules 
	new_cfg = remove_unitary_productions(new_cfg)
	assert(new_cfg.is_chomsky_normal_form())
	return(new_cfg)

cfg_grammar = nltk.data.load("project1_grammar.cfg")
convert_grammar(cfg_grammar)

