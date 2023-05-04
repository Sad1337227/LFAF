import random

class Grammar:
    def __init__(self):
        self.vn = ["S", "A", "B", "C"]
        self.vt = ["a", "b", "c", "d"]
        self.p = {
            "S": ["dA"],
            "A": ["aB", "b"],
            "B": ["bC", "d"],
            "C": ["cB", "aA"],
        }
        self.start_symbol = "S"

    # dA -> daB -> dabC -> dabcB -> dabcd
    # dA -> daB -> dabC -> dabaA -> dabab
    # dA -> daB -> dad

    # dA -> daB -> dabC -> dabcB -> dabcbC || dabcd
    # dA -> daB -> dabC -> dabcB -> dabcbC -> dabcbcB || dabcbaA -> dabcbaaB -> dabcbaabC -> dabcbaabaA->

    def generate_string(self):
        string = ""
        stack = [self.start_symbol]
        while stack:
            symbol = stack.pop()
            if symbol in self.vt:
                string += symbol
            else:
                productions = self.p[symbol]
                chosen_production = random.choice(productions)
                for s in reversed(chosen_production):
                    stack.append(s)
        return string

    def to_finite_automaton(self):
        states = set(self.vn + ["S"])
        alphabet = set(self.vt)
        transitions = {}
        initial_state = "S"
        final_states = set()
        iteration = 0
        for symbol in self.vn:
            state1 = symbol
            if iteration > len(self.vn) - 1:
                iteration = 0
            iteration = +1
            state2 = self.vn[iteration]
            if state1 not in transitions:
                transitions[state1] = {}
            for production in self.p[symbol]:
                if len(production) == 1:
                    transitions[state1][production] = {state2}
                elif len(production) == 2:
                    symbol2 = production[1]
                    if symbol2 not in transitions:
                        transitions[symbol2] = {}
                    transitions[state1][production[0]] = {symbol2}
                    if symbol2 in self.vn:
                        final_states.add(symbol2)
        return FiniteAutomaton(
            states, alphabet, transitions, initial_state, final_states
        )

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

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def string_belongs_to_language(self, input_string):
        if input_string[len(input_string) - 1] == "a":
            # print("ends with 'a'")
            return False
        current_state = self.initial_state

        for symbol in input_string:
            if symbol not in self.alphabet:
                print("not in alphabet")
                return False
            if current_state not in self.transitions:
                print("not in TRANSITIONS")
                return False
            if symbol not in self.transitions[current_state]:
                return False
            current_state = next(iter(self.transitions[current_state][symbol]))
            print(current_state)
        print(current_state + " " + str(self.final_states))
        print(self.transitions)
        return current_state in self.final_states


def main():
    grammar = Grammar()
    grammar.to_cnf()
    finite_automaton = grammar.to_finite_automaton()

    grammar = Grammar()
    finite_automaton = grammar.to_finite_automaton()

    # Generate a string

    input_array = []
    while len(input_array) < 5:
        input_string = grammar.generate_string()
        if input_string not in input_array:
            input_array.append(input_string)

    # Test if the string matches the rules
    for i in range(len(input_array)):
        print(input_array[i])
        if finite_automaton.string_belongs_to_language(input_array[i]):
            print("String", input_string, "matches the grammar rules")
        else:
            print("String", input_string, "does not match the grammar rules")


if __name__ == "__main__":
    main()
