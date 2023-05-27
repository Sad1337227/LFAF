#  Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Telug Anatolie

----

## Theory:
&ensp;&ensp;&ensp;A parser is a crucial component in compilers or interpreters that examines the structure of source code
based on a defined grammar and generates a parse tree or abstract syntax tree (AST) as an intermediate representation. 
By utilizing syntactic rules, the parser analyzes the sequence of tokens produced by the lexer to determine if the code
adheres to the grammar. The resulting parse tree or AST represents the hierarchical structure of the code, capturing the 
relationships between different language constructs such as expressions, statements, and declarations. It provides a 
simplified and higher-level representation of the code, excluding unnecessary details like punctuation or whitespace, 
and serves as a foundation for further analysis, optimization, or code generation.

## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens.
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.
