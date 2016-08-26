# This module takes a DFA as input, and can be used to parse strings
from . import DFA

class Scanner:
    def __init__(self, dfa):
        """
        :param dfa: DFA object constructed via the DFA class
        """
        self.dfa = dfa

    def tokenize(self, string):
        """
        Parse a string and return an array of the results
        :return: array of Token.{type, lexeme}
        :raises: CantTokenize
        """
        return self.dfa.tokenize(string)
