"""Common code that can be used in multiple test case for the Scanner"""
import unittest

from .src import Scanner, logic_scanner


class TestScanner(unittest.TestCase):
    def compare_tokenized_input(self, input, correct_tokens):
        """
        Tokenize the input into a sequence of tokens.
        Compare the computed tokens to the correc_tokens.
        :param input: sequence of symbols
        :param correct_tokens: sequence of Tokens
        :raises: Exception if input is incorrectly tokenized
        """
        computed_tokens = self.scanner.tokenize(input)
        assert(len(computed_tokens) == len(correct_tokens))
        for correct_token, computed_token in zip(correct_tokens, computed_tokens):
            assert(correct_token.type == computed_token.type)
            assert(correct_token.lexeme == computed_token.lexeme)

    def assert_fails_tokenization(self, string):
        try:
            self.scanner.tokenize(string)
        except:
            return
        raise Exception('Should have failed to tokenize ' + string)
