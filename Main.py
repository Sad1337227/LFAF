import json
import os
from lexer.Lexer import Lexer
from lexer.Token import Token
from parser.Parser import Parser

if __name__ == '__main__':
    # Input strings
    input_string1 = 'if (2 > x) : 0 else x / 2'
    input_string2 = 'a + 5 != !a / 3'
    input_string3 = '"hello" + "world"'
    input_string4 = 'a * 3; b - 9; !p < 2'

    # Initialize lexer and parser
    lexer = Lexer(input_string2, Token.tokens)
    parser = Parser(lexer.lex())

    # Parse input string
    ast = parser.parse_expression()
    ast = str(ast).replace('\\', '')
    ast = str(ast).replace('\'left = ', "\n\'left = ")

    print(ast)
