from lark import Lark
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.grammar import GRAMMAR


class Formula:
    def __init__(self, s: str):
        try:
            self.tree = Lark(GRAMMAR).parse(s)
        except (UnexpectedCharacters, ParseError):
            raise InvalidFormula

    def evaluate(self, interpretation):
        try:
            return self._evaluate(interpretation)
        except KeyError:
            raise InvalidInterpretation

    def _evaluate(self, interpretation):
        return interpretation[self.tree]


class InvalidFormula(Exception):
    pass


class InvalidInterpretation(Exception):
    pass
