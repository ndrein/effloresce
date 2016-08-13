"""Format for a DFA"""

class DFA:
    def __init__(self, alphabet, states, start_state, accept_states, transitions):
        """
        Create a DFA
        States and alphabet are arbitrary, but must have the equality (=) operator defined on them

        :param alphabet: alphabet as a set
        :param states: set of states
        :param start_state: start state \in states
        :param accept_states: set of accepting states
        :param transitions: 2-dimensional array
                            state x symbol -> state
        """
        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def transition(self, state, symbol):
        return self.transitions[state][symbol]

    def is_accepting(self, state):
        return state in self.accept_states
