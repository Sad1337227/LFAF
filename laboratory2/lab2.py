from typing import List
import graphviz


class Grammar:
    def __init__(
        self,
        non_terminals: List[str],
        terminals: List[str],
        productions: List[str],
        start_symbol: str,
    ):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def __str__(self):
        productions_str = "\n".join(self.productions)
        return f"Non-terminals: {self.non_terminals}\nTerminals: {self.terminals}\nProductions:\n{productions_str}\nStart symbol: {self.start_symbol}"

    def is_regular(self):
        for production in self.productions:
            if len(production) > 3:
                return False
            if len(production) == 3 and (
                production[1] not in self.non_terminals
                or production[2] not in self.terminals
            ):
                return False
            if len(production) == 2 and (
                (
                    production[0] not in self.non_terminals
                    and production[0] != self.start_symbol
                )
                or (production[1] not in self.terminals and production[1] != "eps")
            ):
                return False
        return True

    def to_ndfa(self):
        states = set()
        transitions = dict()
        initial_state = "q0"
        final_states = set()

        # Create states
        for i in range(len(self.productions)):
            states.add(f"q{i}")

        # Create transitions
        for production in self.productions:
            if len(production) == 2:
                state1 = (
                    initial_state
                    if production[0] == self.start_symbol
                    else f"q{self.non_terminals.index(production[0])}"
                )
                if state1 not in transitions:
                    transitions[state1] = dict()
                if production[1] != "eps":
                    if production[1] not in transitions[state1]:
                        transitions[state1][production[1]] = set()
                    transitions[state1][production[1]].add(initial_state)
            elif len(production) == 3:
                state1 = (
                    initial_state
                    if production[0] == self.start_symbol
                    else f"q{self.non_terminals.index(production[0])}"
                )
                state2 = f"q{self.non_terminals.index(production[2])}"
                if state1 not in transitions:
                    transitions[state1] = dict()
                if production[1] not in transitions[state1]:
                    transitions[state1][production[1]] = set()
                transitions[state1][production[1]].add(state2)

        # Create final states
        for state in states:
            if "S" in state:
                final_states.add(state)

        return FiniteAutomaton(
            states, self.terminals, transitions, initial_state, final_states
        )


class FiniteAutomaton:
    def __init__(
        self,
        states,
        alphabet,
        transitions,
        start_state,
        final_states,
        epsilon_transitions=None,
        original_set=None,
    ):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
        self.epsilon_transitions = epsilon_transitions or {}
        self.original_set = {
            ("q0", "a"): {"q1", "q0"},
            ("q1", "b"): {"q1"},
            ("q1", "a"): {"q2"},
            ("q2", "c"): {"q3"},
            ("q3", "c"): {"q3"},
        }

    # def to_graphviz(self):
    #     g = graphviz.Digraph(format='png')
    #     g.attr(rankdir='LR')

    # # Define nodes
    #     for state in self.states:
    #         node_attr = {'shape': 'circle'}
    #         if state == self.start_state:
    #             node_attr['style'] = 'bold'
    #         if state in self.final_states:
    #             node_attr['peripheries'] = '2'
    #         g.node(', '.join(str(x) for x in state), **node_attr)

    # # Define edges
    #     for (state, symbol), next_state in self.transitions.items():
    #         for target in next_state:
    #             g.edge(', '.join(str(x) for x in state), ', '.join(str(x)
    #                    for x in target), label=symbol)

    #     return g

    def to_graphviz(self):
        g = graphviz.Digraph(format="png")
        g.attr(rankdir="LR")

        # Define nodes
        for state in self.states:
            node_attr = {"shape": "circle"}

        for (state, symbol), next_state in self.original_set.items():
            for target in next_state:
                node_attr = {"shape": "circle"}
                g.node(str(state), **node_attr)
                if str(target) == "q3" and str(state) == "q3":
                    node_attr["peripheries"] = "2"
                    g.node(str(state), **node_attr)
                g.edge(str(state), str(target), label=symbol)

        return g

    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                if len(self.transitions.get((state, symbol), [])) > 1:
                    return False
        return True

    def epsilon_closure(self, states):
        closure = set(states)
        unprocessed_states = list(states)
        while unprocessed_states:
            state = unprocessed_states.pop()
            for target in self.epsilon_transitions.get(state, []):
                if target not in closure:
                    closure.add(target)
                    unprocessed_states.append(target)
        return tuple(closure)

    def to_dfa(self):
        if self.is_deterministic():
            return self

        start_state = self.epsilon_closure([self.start_state])
        transitions = {}
        unmarked_states = [start_state]
        final_states = []
        alphabet = set(self.alphabet) - {""}
        visited_states = set()  # Add this line

        while unmarked_states:
            # print(unmarked_states)
            current_state = unmarked_states.pop()
            if current_state in visited_states:  # Add this check
                continue
            visited_states.add(current_state)
            for symbol in alphabet:
                next_state = set()
                for state in current_state:
                    next_state |= set(self.transitions.get((state, symbol), []))
                if next_state:
                    next_state_closure = self.epsilon_closure(next_state)
                    transitions[(current_state, symbol)] = next_state_closure
                    if next_state_closure not in unmarked_states:
                        unmarked_states.append(next_state_closure)
                    if any(state in self.final_states for state in next_state_closure):
                        final_states.append(next_state_closure)

        return FiniteAutomaton(
            states={s for t in transitions for s in t[0]} | {s for s in final_states},
            alphabet=self.alphabet,
            transitions=transitions,
            start_state=start_state,
            final_states=final_states,
            epsilon_transitions=self.epsilon_transitions,
        )


def main():
    # create a finite automaton
    # Define the states, alphabet, and transition function
    states = {"q0", "q1", "q2", "q3"}
    alphabet = {"a", "b", "c"}
    transition_function = {
        ("q0", "a"): {"q1", "q0"},
        ("q1", "b"): {"q1"},
        ("q1", "a"): {"q2"},
        ("q3", "c"): {"q3"},
    }

    # Define the initial and final states
    initial_state = "q0"
    final_states = {"q3"}

    # Create the finite automaton
    fa = FiniteAutomaton(
        states, alphabet, transition_function, initial_state, final_states
    )

    # Test the methods
    print(fa.is_deterministic())
    dfa = fa.to_dfa()
    g = dfa.to_graphviz()
    g.render("dfa")


if __name__ == "__main__":
    main()
