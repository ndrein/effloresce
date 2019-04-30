from lark import Lark
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.grammar import GRAMMAR


class Formula:
    def __init__(self, s: str):
        try:
            Lark(GRAMMAR).parse(s)
            self.s = s
        except (UnexpectedCharacters, ParseError):
            raise InvalidFormula

    def evaluate(self, interpretation):
        if self.s not in interpretation:
            raise InvalidInterpretation

        return interpretation[self.s]


class InvalidFormula(Exception):
    pass


class InvalidInterpretation(Exception):
    pass
