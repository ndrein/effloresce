# This module takes a DFA as input, and can be used to parse strings

class Scanner:
    def __init__(self, dfa):
        """
        Create a Scanner

        :param dfa: DFA to use
        :type dfa: DFA
        """
        self.dfa = dfa

    def scan(self, string):
        """
        Parse a string and return an array of the results
        :return: array of Token.{type, lexeme}
        """
        return self.dfa.tokenize(string)
