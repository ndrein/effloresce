"""Test the logic dfa"""
import unittest

from .src import Scanner, Token, logic_dfa

from .common import compare_token_sequences

class ScannerTest(unittest.TestCase):
    def setUp(self):
        self.scanner = Scanner(logic_dfa)

    def test_zero(self):
        computed_tokens = self.scanner.tokenize('0')
        correct_tokens = [Token('NUM', '0')]
        compare_token_sequences(computed_tokens, correct_tokens)

    def test_id(self):
        computed_tokens = self.scanner.tokenize('var')
        correct_tokens = [Token('ID', 'var')]
        compare_token_sequences(computed_tokens, correct_tokens)

    def test_forall(self):
        compare_token_sequences(self.scanner.tokenize('forall'), [Token('FORALL', 'forall')])

    def test_exists(self):
        compare_token_sequences(self.scanner.tokenize('exists'), [Token('EXISTS', 'exists')])

    def test_num(self):
        compare_token_sequences(self.scanner.tokenize('00173928570'), [Token('NUM', '00173928570')])
