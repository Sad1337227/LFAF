# Regular Grammar
### Course: Formal Languages & Finite Automata
### Author: Telug Anatolie FAF-212
----

## Theory of Infinite Automata

An infinite automaton is a mathematical model used to study computations that involve an infinite sequence of symbols. Unlike finite automata, which can only process a fixed number of input symbols, infinite automata can process an infinite stream of input symbols. Infinite automata have important applications in areas such as computer science, logic, and linguistics.
&ensp;&ensp;&ensp; 


## Objectives:
1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
    4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.
## Implementation
&ensp;&ensp;&ensp; 
1. Step 1: In this step, the code is adding a new start symbol to the grammar by appending a prime symbol (') to the existing start symbol. It ensures that the new start symbol is not already present in the set of nonterminal symbols (vn). The original start symbol is then replaced with the new start symbol.

2. Step 2: This step deals with the removal of epsilon productions, which are productions that derive the empty string (""). The code iteratively removes epsilon productions from each production in the grammar until no epsilon productions are left. It uses a set called epsilon_productions to keep track of symbols that have epsilon productions. For each symbol in the grammar, it checks if it has an epsilon production and modifies the production by replacing the epsilon symbol with an empty string. The modified production is added back to the set of productions for that symbol.

3. Step 3: Here, the code eliminates unit productions, which are productions of the form A -> B, where A and B are nonterminal symbols. It initializes a dictionary called unit_productions to store the unit productions for each nonterminal symbol. The code then iterates over each production in the grammar and checks if it is a unit production. If it is, the code removes the unit production and replaces it with the productions derived from the nonterminal symbol B. The process continues until there are no more unit productions left.

4. Step 4: This step introduces new nonterminal symbols for productions with more than two symbols on the right-hand side. It iterates over each production in the grammar and if the length of the production is greater than 2, it creates a new nonterminal symbol by appending a prime symbol (') to the original symbol. It ensures that the new symbol is not already present in vn. The code then modifies the production by splitting it into two parts, where the last two symbols form a new production with the new symbol, and the rest of the production is concatenated with the new symbol.

5. Step 5: In this step, the code eliminates all non-2-sized right-hand sides. It iterates over each production in the grammar and checks if the length of the production is 2. If it is, the production is kept as it is. Otherwise, the code creates new productions by pairing adjacent symbols in the original production and appending a prime symbol (') to the pair. These new productions replace the original production.

Overall, this code implements the conversion of a context-free grammar to Chomsky normal form (CNF) by applying a series of transformations to the grammar. Each step addresses a specific aspect of the grammar and modifies it accordingly.
```
 def to_cnf(self):
        # Step 1: eliminate the start symbol from right-hand sides
        new_start_symbol = f"{self.start_symbol}'"
        while new_start_symbol in self.vn:
            new_start_symbol += "'"
        self.p[new_start_symbol] = [self.start_symbol]
        self.start_symbol = new_start_symbol

        # Step 2: remove epsilon productions
        epsilon_productions = {symbol for symbol, productions in self.p.items() if "" in productions}
        while epsilon_productions:
            for symbol in self.p:
                self.p[symbol] = [
                    production.replace(epsilon_symbol, "")
                    for production in self.p[symbol]
                    for epsilon_symbol in epsilon_productions
                    if epsilon_symbol in production and (new_production := production.replace(epsilon_symbol, ""))
                ] + self.p[symbol]
            epsilon_productions = {symbol for symbol, productions in self.p.items() if "" in productions}
        
        # Step 3: eliminate unit productions
        unit_productions = {symbol: set() for symbol in self.vn}
        for symbol, productions in self.p.items():
            for production in productions:
                if len(production) == 1 and production in self.vn:
                    symbol=symbol[:-1]
                    print(symbol)
                    print(unit_productions)
                    unit_productions[symbol].add(production)
        while any(unit_productions.values()):
            for symbol, productions in unit_productions.items():
                while productions:
                    production = productions.pop()
                    if production in self.p[symbol]:
                        self.p[symbol].remove(production)
                        self.p[symbol].extend(self.p[production])
                    
        # Step 4: introduce new nonterminal symbols for long right-hand sides
        new_symbols_counter = 0
        for symbol, productions in self.p.items():
            for i, production in enumerate(productions):
                if len(production) > 2:
                    new_symbol = f"{symbol}{i+1}'"
                    while new_symbol in self.vn:
                        new_symbol += "'"
                    self.vn.append(new_symbol)
                    self.p[new_symbol] = [production[-2:]]
                    self.p[symbol][i] = f"{production[:-2]}{new_symbol}"
        
        # Step 5: eliminate all non-2-sized right-hand sides
        for symbol, productions in self.p.items():
            new_productions = []
            for production in productions:
                if len(production) == 2:
                    new_productions.append(production)
                else:
                    new_productions.extend([f"{production[i]}{production[i+1]}'" for i in range(len(production)-1)])
            self.p[symbol] = new_productions
```
## The output on screenshot![image](https://user-images.githubusercontent.com/113394083/230783934-bf31334a-9838-4dfd-9743-f6df2dbe67f9.png) 
## References
[1] [Chomsky Normal Form Wiki](https://en.wikipedia.org/wiki/Chomsky_normal_form)
