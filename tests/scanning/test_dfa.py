import unittest

from .src import DFA, State, Token


class SimpleDFA(unittest.TestCase):
    def setUp(self):
        alphabet = list('abc')
        states = [State(i) for i in range(5)]
        start_state = State(0)
        accept_states = [State(1), State(4)]
        transitions = DFA.init_transitions(alphabet, states)

        transitions[State(0), 'a'] = State(0)
        transitions[State(0), 'b'] = State(1)
        transitions[State(0), 'c'] = State(2)
        transitions[State(2), 'b'] = State(2)
        transitions[State(2), 'a'] = State(3)
        transitions[State(3), 'b'] = State(4)

        self.dfa = DFA(alphabet, states, start_state, accept_states, transitions)

    def test_failed_tokenize(self):
        string = "aaabc"
        try:
            self.dfa.tokenize(string)
        except:
            return 0
        raise Exception("Should have failed to tokenize " + string)

    def test_tokenize(self):
        string = "aacbab"
        self.dfa.tokenize(string)


