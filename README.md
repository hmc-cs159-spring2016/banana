# nlp-2016-project
Project for Chloe Calvarin, Judge Lee, Rowan Zellers

We are the banana team!

Here is a quick list of files and what they do
- chomsky_converter takes in an nltk.grammar CFG, and returns a chomsky normal 
   form grammar equivalent.   
   `convert_grammar(your_cfg)`
- chomsky_tree_converter takes in an nltk.tree Tree and returns a Tree that has
   been converted to chomsky normal form. The rules are systematic in such a way
   that we can convert a whole corpus without worrying about having new intermediate 
   rules that get mixed up for each other.   
   `convert_tree(tree)`
