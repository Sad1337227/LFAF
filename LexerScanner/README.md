# Lexer & Scanner
### Course: Formal Languages & Finite Automata
### Author: Telug Anatolie FAF-212
----

## Theory of Lexer

&ensp;&ensp;&ensp; The term lexer comes from lexical analysis which, in turn, represents the process of extracting lexical tokens from a string of characters. There are several alternative names for the mechanism called lexer, for example tokenizer or scanner. The lexical analysis is one of the first stages used in a compiler/interpreter when dealing with programming, markup or other types of languages. The tokens are identified based on some rules of the language and the products that the lexer gives are called lexemes. So basically the lexer is a stream of lexemes. Now in case it is not clear what's the difference between lexemes and tokens, there is a big one. The lexeme is just the byproduct of splitting based on delimiters, for example spaces, but the tokens give names or categories to each lexeme. So the tokens don't retain necessarily the actual value of the lexeme, but rather the type of it and maybe some metadata.
## Objectives

1. Understand what lexical analysis [1] is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.
## Implementation
&ensp;&ensp;&ensp; The main goal of lexer is to tokenize the input what breaks string into induvidual tokens or meaningful units and then finds matches.
```
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
```
## The output on screenshot![image](https://user-images.githubusercontent.com/113394083/236165697-425361a1-e933-48b9-8f42-f2fcff3cd3af.png)
## References
[1] [A sample of a lexer implementation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)

[2] [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)
