"""Test the logic dfa"""

from lib.syntax.tests import TestScanner
from lib.syntax.syntax.scanner import Token

# TODO: fix imports with nose2
from effloresce.syntax.scanning import logic_scanner


class TestScannerLogicDFA(TestScanner):
    def setUp(self):
        self.scanner = logic_scanner

    def test_zero(self):
        self.compare_tokenized_input('0', [Token('NUM', '0')])

    def test_double_zero(self):
        self.compare_tokenized_input('00', [Token('NUM', '00')])

    def test_id(self):
        self.compare_tokenized_input('var', [Token('ID', 'var')])

    def test_T(self):
        self.compare_tokenized_input('T', [Token('BOOL', 'T')])

    def test_F(self):
        self.compare_tokenized_input('F', [Token('BOOL', 'F')])

    def test_TF(self):
        self.compare_tokenized_input('TF', [Token('ID', 'TF')])

    def test_bool_id(self):
        self.compare_tokenized_input('TF T F f', [Token('ID', 'TF'),
                                                  Token('BOOL', 'T'),
                                                  Token('BOOL', 'F'),
                                                  Token('ID', 'f')])

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

    def test_simple_sequence(self):
        self.compare_tokenized_input('forall' ' forallx' ' \n   forallforallx' '01' '||' '!',
                                     [Token('FORALL', 'forall'),
                                      Token('ID', 'forallx'),
                                      Token('ID', 'forallforallx'),
                                      Token('NUM', '01'),
                                      Token('OR', '||'),
                                      Token('NOT', '!')])

    def test_partial_forall(self):
        self.compare_tokenized_input('for', [Token('ID', 'for')])

    def test_partial_exists(self):
        self.compare_tokenized_input('e', [Token('ID', 'e')])

    def test_formula(self):
        self.compare_tokenized_input('forall x ((exists y (P(y) && Q(x, y))) || !exist(x))',
                                     [Token('FORALL', 'forall'),
                                      Token('ID', 'x'),
                                      Token('LPAREN', '('),
                                      Token('LPAREN', '('),
                                      Token('EXISTS', 'exists'),
                                      Token('ID', 'y'),
                                      Token('LPAREN', '('),
                                      Token('ID', 'P'),
                                      Token('LPAREN', '('),
                                      Token('ID', 'y'),
                                      Token('RPAREN', ')'),
                                      Token('AND', '&&'),
                                      Token('ID', 'Q'),
                                      Token('LPAREN', '('),
                                      Token('ID', 'x'),
                                      Token('COMMA', ','),
                                      Token('ID', 'y'),
                                      Token('RPAREN', ')'),
                                      Token('RPAREN', ')'),
                                      Token('RPAREN', ')'),
                                      Token('OR', '||'),
                                      Token('NOT', '!'),
                                      Token('ID', 'exist'),
                                      Token('LPAREN', '('),
                                      Token('ID', 'x'),
                                      Token('RPAREN', ')'),
                                      Token('RPAREN', ')')])

    def test_bad_alphabet_characters(self):
        self.assert_fails_tokenization('@')
        self.assert_fails_tokenization('#')
        self.assert_fails_tokenization('$')
        self.assert_fails_tokenization('&')
        self.assert_fails_tokenization('|')

    def test_underscore_fail(self):
        self.assert_fails_tokenization('_')

    def test_percent_fail(self):
        self.assert_fails_tokenization('%')

    def test_caret_fail(self):
        self.assert_fails_tokenization('^')

    def test_star_fail(self):
        self.assert_fails_tokenization('*')

    def test_curly_fail(self):
        self.assert_fails_tokenization('{')
        self.assert_fails_tokenization('}')

    def test_square_fail(self):
        self.assert_fails_tokenization('[')
        self.assert_fails_tokenization(']')
