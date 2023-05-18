import re

# Define some regular expressions for our lexer
TOKENS = [
    ('INTEGER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'\/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
]

# A lexer function that takes a string and returns a list of tokens
def lexer(input_string):
    tokens = []
    while len(input_string) > 0:
        match = None
        for token in TOKENS:
            name, pattern = token
            regex = re.compile(pattern)
            match = regex.match(input_string)
            if match:
                text = match.group(0)
                tokens.append((name, text))
                input_string = input_string[len(text):]
                break
        if not match:
            raise ValueError(f"Invalid input: {input_string}")
    return tokens

def main():
    input_string = input("Enter an arithmetic expression: ")
    tokens = lexer(input_string)
    
    # Print the tokens
    print("The tokens are:")
    for token in tokens:
        print(token)

if __name__ == "__main__":
  main()
