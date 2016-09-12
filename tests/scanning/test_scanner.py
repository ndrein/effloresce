#TODO: refactor using TestScanner
import unittest
import string

from .src import Scanner, DFA

from .common import TestScanner

class TestSimpleDFA(TestScanner):
    def setUp(self):
        alphabet = list('abc')
        states = list(range(5))
        start_state = 0
        accept_states = [1, 4]
        transitions = dict()

        transitions[0, 'a'] = 0
        transitions[0, 'b'] = 1
        transitions[0, 'c'] = 2
        transitions[2, 'b'] = 2
        transitions[2, 'a'] = 3
        transitions[3, 'b'] = 4

        state_map = dict.fromkeys(range(5))

        self.scanner = Scanner(DFA(alphabet, states, start_state, accept_states, transitions, state_map))

    def test_simple(self):
        tokens = self.scanner.tokenize('b')
        assert(len(tokens) == 1)
        assert(tokens[0].lexeme == 'b')

    def assert_failed_tokenization(self, string):
        try:
            self.scanner.tokenize(string)
        except:
            return 0
        raise Exception('Should have failed to tokenize ' + string)

    def test_single_failed_tokenize(self):
        self.assert_failed_tokenization('aaabc')

    def test_multiple_failed_tokenize(self):
        # b passes, cac fails
        self.assert_failed_tokenization('b' 'cac' 'cab')

    def test_tokenize(self):
        tokens = self.scanner.tokenize('aacbab' 'b' 'cab' '')
        assert(tokens[0].lexeme == 'aacbab')
        assert(tokens[1].lexeme == 'b')
        assert(tokens[2].lexeme == 'cab')

    def test_empty_input(self):
        tokens = self.scanner.tokenize('')
        assert(tokens == [])


class NumbersAndIDs(unittest.TestCase):
    def setUp(self):
        alphabet = list('0123456789') + list(string.ascii_lowercase)
        states = {'start', 'zero', 'non_zero_numeric', 'id'}
        start_state = 'start'
        accept_states = {'zero', 'non_zero_numeric', 'id'}
        transitions = dict()

        transitions['start', '0'] = 'zero'
        transitions = DFA.build_multiple_transitions(transitions, 'start', '123456789', 'non_zero_numeric')
        transitions = DFA.build_multiple_transitions(transitions, 'non_zero_numeric', '0123456789', 'non_zero_numeric')
        transitions = DFA.build_multiple_transitions(transitions, 'start', string.ascii_lowercase, 'id')
        transitions = DFA.build_multiple_transitions(transitions, 'id', list(string.ascii_lowercase) + list('0123456789'), 'id')

        state_map = dict({
            'zero': 'NUM',
            'non_zero_numeric': 'NUM',
            'id': 'ID'
        })

        self.scanner = Scanner(DFA(alphabet, states, start_state, accept_states, transitions, state_map))

    def test_zero(self):
       tokens = self.scanner.tokenize('0')
       assert(len(tokens) == 1)
       assert(tokens[0].lexeme == '0')
       assert(tokens[0].type == 'NUM')

    def test_simple_num(self):
        tokens = self.scanner.tokenize('102304')
        assert(len(tokens) == 1)
        assert(tokens[0].lexeme == '102304')
        assert(tokens[0].type == 'NUM')

    def test_simple_whitespace(self):
        tokens = self.scanner.tokenize('102 304')
        assert(len(tokens) == 2)
        assert(tokens[0].lexeme == '102')
        assert(tokens[0].type == 'NUM')
        assert(tokens[1].lexeme == '304')
        assert(tokens[1].type == 'NUM')

    def test_all_whitespace(self):
        assert(len(self.scanner.tokenize('          ')) == 0)

    def test_leading_and_trailing_whitespace(self):
        tokens = self.scanner.tokenize(' a123     ')
        assert(len(tokens) == 1)
        assert(tokens[0].lexeme == 'a123')

    def test_ids(self):
        tokens = self.scanner.tokenize('      0' '120\n' '90' 'a999\t' '9990   \n\t' '0')
        assert(len(tokens) == 6)

        assert(tokens[0].lexeme == '0')
        assert(tokens[0].type == 'NUM')

        assert(tokens[1].lexeme == '120')
        assert(tokens[1].type == 'NUM')

        assert(tokens[2].lexeme == '90')

        assert(tokens[3].lexeme == 'a999')
        assert(tokens[3].type == 'ID')

        assert(tokens[4].lexeme == '9990')
        assert(tokens[4].type == 'NUM')

        assert(tokens[5].lexeme == '0')
        assert(tokens[5].type == 'NUM')
