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

## Implementation description
### Parser class
The class Parser defines methods for parsing a sequence of tokens into an abstract syntax tree 
(AST) representation of a Python expression or statement. The class initializes with an output tokens of the lexer with 
 which then works on, makes all the operations and the output is then saved into a .json file. The class uses the following methods. 

### peek() and get()
The peek() method returns the next token in the list without consuming it, or None if there are no more tokens. 
The get() method returns and consumes the next token in the list, or None if there are no more tokens.

### parse_expression()
This method parses a sequence of tokens into an AST node representing a Python expression. It handles multiple 
expressions separated by semicolons and returns either a single expression node or a block node containing a list of expressions.

```
def parse_expression(self):
        expressions = []
        while True:
            expression = self.parse_comparison()
            expressions.append(expression)
            next_token = self.peek()
            if next_token is None or next_token['type'] != 'SEMICOLON':
                break
            self.get()
        if len(expressions) == 1:
            return expressions[0]
        else:
            return {'type': 'block', 'expressions': expressions}  
```

### parse_comparison()
This method parses a sequence of tokens into an AST node representing a Python comparison expression. It handles operators
such as equals, not equals, less than, and greater than, and returns an operation node with the operator and the left 
and right operands.

```
def parse_comparison(self):
        left = self.parse_term()
        while True:
            op = self.peek()
            if op is None or op['type'] not in ['EQUALS', 'NOT_EQUALS', 'LESS_THAN', 'GREATER_THAN']:
                break
            self.get()
            right = self.parse_term()
            left = {'type': 'operation', 'operator': op['type'], 'left': left, 'right': right}
        return left
```

### parse_term()
It handles operators such as plus and minus, and returns an operation node with the operator and the left and right operands.

### parse_factor()
This method handles operators such as times and divide, and returns an operation node with the operator and the left and right operands.

```
def parse_factor(self):
        left = self.parse_unary()
        while True:
            op = self.peek()
            if op is None or op['type'] not in ['TIMES', 'DIVIDE']:
                break
            self.get()
            right = self.parse_unary()
            left = {'type': 'operation', 'operator': op['type'], 'left': left, 'right': right}
        return left
```

### parse_unary()
This method handles operators such as plus, minus, and not, and returns an operation node with the operator and the operand.

```
def parse_unary(self):
        op = self.peek()
        if op is not None and op['type'] in ['PLUS', 'MINUS', 'NOT']:
            self.get()
            operand = self.parse_unary()
            return {'type': 'operation', 'operator': op['type'], 'operand': operand}
        else:
            return self.parse_primary()
```

### parse_primary()
This method parses a sequence of tokens into an AST node representing a Python primary expression. It handles literals 
such as numbers and strings, identifiers, parentheses, and if-else expressions, and returns the corresponding node type.

```
def parse_primary(self):
        token = self.get()
        if token['type'] == 'NUMBER':
            return {'type': 'number', 'value': float(token['value'])}
        elif token['type'] == 'IDENTIFIER':
            return {'type': 'identifier', 'value': token['value']}
        ...
        elif token['type'] == 'IF':
            ...
            return {'type': 'if-else', 'condition': condition, 'if_expression': if_expr, 'else_expression': else_expr}
        else:
            raise ValueError('Invalid token: ' + token['type'])
```
## Conclusions / Results

### Conclusion

To summarize, it is crucial to incorporate a parser that can accept tokens generated by a lexer and produce an Abstract Syntax Tree (AST) when constructing a robust and efficient compiler or interpreter.

To begin with, the lexer's role is to convert a sequence of characters into tokens, which represent meaningful units within the programming language. This process entails identifying language-specific elements like keywords, identifiers, and literals. Implementing a dependable lexer is vital to ensure a consistent token stream for the parser.

Next, the parser takes the token stream as input and constructs an Abstract Syntax Tree (AST), which is a hierarchical structure. The parser applies a set of grammar rules to determine the structure and relationships among the tokens. Designing a grammar that accurately reflects the language's syntax is essential to achieve correct parsing.

Furthermore, the AST serves as a representation of the source code's syntactic structure, capturing hierarchical relationships and operator precedence. Each node in the AST corresponds to a language construct, such as a conditional statement or variable assignment. Constructing the AST involves creating and connecting nodes based on the grammar rules and token relationships.

Ultimately, implementing a parser that can accept tokens from a lexer and generate an AST is a crucial aspect of the compilation or interpretation process. It encompasses tokenization, parsing based on grammar, AST construction, semantic analysis, and more. By designing and implementing an effective parser, we can create powerful language tools that facilitate efficient execution or evaluation of programming code.

### Results
input1:``` 'if (2 > x) : 0 else x / 2'```
output1:
```
{'type': 'if-else', 'condition': {'type = operation', 'operator = GREATER_THAN', "left = {'type': 'number', 'value': 2.0}", "right = {'type': 'identifier', 'value': 'x'}"}, 'if_expression': {'type': 'number', 'value': 0.0}, 
'else_expression': {"left = {'type': 'identifier', 'value': 'x'}", "right = {'type': 'number', 'value': 2.0}", 'type = operation', 'operator = DIVIDE'}}
```
input2:``` "hello" + "world"```
output2:
```
{'operator = PLUS', "left = {'type': 'str', 'value': 'hello'}", "right = {'type': 'str', 'value': 'world'}", 'type = operation'}
```
input3: ```'a + 5 != !a / 3'```
output3:
```
{'right = {"right = {'type': 'number', 'value': 3.0}", 
'left = {'operator = NOT', "operand = {'type': 'identifier', 'value': 'a'}", 'type = operation'}', 'operator = DIVIDE', 'type = operation'}',
'left = {"right = {'type': 'number', 'value': 5.0}", "left = {'type': 'identifier', 'value': 'a'}", 'operator = PLUS', 'type = operation'}', 'operator = NOT_EQUALS', 'type = operation'}
```
## References
https://github.com/DrVasile/FLFA-Labs/blob/master/5_ParserASTBuild/task.md
