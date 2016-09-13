# This module takes a DFA as input, and can be used to parse strings
import string

from . import DFA


class Scanner:
    DFA = DFA

    def __init__(self, dfa):
        """
        :param dfa: constructed using the Scanner.DFA class
        """
        self.DFA = dfa

    def tokenize(self, input):
        """
        Take a sequence of input and return an array of Tokens

        :param input: iterable of symbols
        :return: iterable of Token.{type, lexeme}
        :raises: CantTokenize
        """
        tokens = []

        input = self.DFA.strip_leading_delimiters(input)
        while len(input) > 0:
            input, token = self.DFA.munch(input)
            tokens.append(token)
            input = self.DFA.strip_leading_delimiters(input)

        return tokens
