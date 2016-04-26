# nlp-2016-project
Project for Chloe Calvarin, Judge Lee, Rowan Zellers

We are the banana team!

Here is a quick list of files and what they do
- chomsky_converter.py takes in an nltk.grammar CFG, and returns a chomsky normal 
   form grammar equivalent.   
   `convert_grammar(your_cfg)`
- chomsky_tree_converter.py takes in an nltk.tree Tree and returns a Tree that has
   been converted to chomsky normal form. The rules are systematic in such a way
   that we can convert a whole corpus without worrying about having new intermediate 
   rules that get mixed up for each other.   
   `convert_tree(tree)`
- cky_parser.py has both a deterministic and probabilistic CKY parser, with few frills
   added. It does, however, deal with unknown words (provided that there are 
   probabilistic rules that handle unknowns)

   To use, we can run:
   `myparser = cky_parser.ckyparser(grammar,start_symbol)`  
   `chart,mytrees = myparser.probabilistic_parse(sentence)`  
   `chart,mytrees = myparser.deterministic_parse(sentence)`  
- main.py was an initial playground for figuring out the corpus, it became where we 
   run things from different files together.
- malt_parser.py  
   `TODO`
- probabilities.py takes in trees and returns a grammar, with an added shortcut 
   if you prefer using the fileids of the treebank. Since we convert our trees first
   in chomsky_tree_converter, you would feed the resulting list into here  
   `makeGrammar(tree_list)`
- test_cky.py  
   This file contains test code for each of the two CKY parsers (deterministic, and probabilistic).
- transition_parser.py  
   `TODO`


