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

    def simple_test(self):
        tokens = self.dfa.tokenize("b")
        assert(len(tokens) == 1)
        assert(tokens[0].lexeme == "b")

    def assert_failed_tokenization(self, string):
        try:
            self.dfa.tokenize(string)
        except:
            return 0
        raise Exception("Should have failed to tokenize " + string)

    def test_single_failed_tokenize(self):
        self.assert_failed_tokenization("aaabc")

    def test_multiple_failed_tokenize(self):
        # b passes, cac fails
        self.assert_failed_tokenization("b" "cac" "cab")

    def test_tokenize(self):
        tokens = self.dfa.tokenize("aacbab" "b" "cab" "")
        assert(tokens[0].lexeme == "aacbab")
        assert(tokens[1].lexeme == "b")
        assert(tokens[2].lexeme == "cab")

    def test_empty_input(self):
        tokens = self.dfa.tokenize('')
        assert(tokens == [])


# TODO: test token types with a real state_map
