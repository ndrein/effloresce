import unittest

from .src import DFA


class SimpleDFA(unittest.TestCase):
    def setUp(self):
        alphabet = list('abc')
        states = list(range(5))
        start_state = 0
        accept_states = [1, 4]
        transitions = DFA.init_transitions(alphabet, states)

        transitions[0, 'a'] = 0
        transitions[0, 'b'] = 1
        transitions[0, 'c'] = 2
        transitions[2, 'b'] = 2
        transitions[2, 'a'] = 3
        transitions[3, 'b'] = 4

        state_map = dict.fromkeys(range(5))

        self.dfa = DFA(alphabet, states, start_state, accept_states, transitions, state_map)

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


