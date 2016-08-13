# This module takes a DFA as input, and can be used to parse strings

class Parser:
    def __init__(self, dfa):
        """
        Create a Parser

        :param dfa: DFA to use
        :type dfa: DFA
        """
        self.dfa = dfa

    def parse(self, string):
        """
        Parse a string and return an array of the results

        :param string:
            :return: array -- tokens
        """
        raise NotImplemented


    @classmethod
    def fun(cls):
        return cls.dfa
