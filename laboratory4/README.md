# Regular Grammar
### Course: Formal Languages & Finite Automata
### Author: Telug Anatolie FAF-212
----

## Theory of Infinite Automata

An infinite automaton is a mathematical model used to study computations that involve an infinite sequence of symbols. Unlike finite automata, which can only process a fixed number of input symbols, infinite automata can process an infinite stream of input symbols. Infinite automata have important applications in areas such as computer science, logic, and linguistics.
## Objectives
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
