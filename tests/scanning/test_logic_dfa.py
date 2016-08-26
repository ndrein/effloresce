"""Test the logic dfa"""
import unittest

from .src import Scanner, Token, logic_dfa

from .common import TestScanner


class TestScannerLogicDFA(TestScanner):
    def test_zero(self):
        self.compare_tokenized_input('0', [Token('NUM', '0')])

    def test_id(self):
        self.compare_tokenized_input('var', [Token('ID', 'var')])

    def test_forall(self):
        self.compare_tokenized_input('forall', [Token('FORALL', 'forall')])

    def test_exists(self):
        self.compare_tokenized_input('exists', [Token('EXISTS', 'exists')])

    def test_num(self):
        self.compare_tokenized_input('00173928570', [Token('NUM', '00173928570')])

    def test_and(self):
        self.compare_tokenized_input('&&', [Token('AND', '&&')])

    def test_or(self):
        self.compare_tokenized_input('||', [Token('OR', '||')])

    def test_not(self):
        self.compare_tokenized_input('!', [Token('NOT', '!')])

    def test_comma(self):
        self.compare_tokenized_input(',', [Token('COMMA', ',')])

    def test_parens(self):
        self.compare_tokenized_input('())(',
                                     [Token('LPAREN', '('),
                                      Token('RPAREN', ')'),
                                      Token('RPAREN', ')'),
                                      Token('LPAREN', '(')])

    def test_implies(self):
        self.compare_tokenized_input('->', [Token('IMPLIES', '->')])

    def test_iff(self):
        self.compare_tokenized_input('<->', [Token('IFF', '<->')])
