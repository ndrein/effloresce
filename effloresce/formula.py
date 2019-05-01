from lark import Lark, Transformer, Token
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.grammar import GRAMMAR


class Formula:
    def __init__(self, s: str):
        try:
            self.tree = Lark(GRAMMAR).parse(s)
        except (UnexpectedCharacters, ParseError):
            raise InvalidFormula

    def _evaluate(self, tree, interpretation):
        if isinstance(tree, Token):
            return interpretation[tree]

        return not self._evaluate(tree.children[0], interpretation)

    def evaluate(self, interpretation):
        return self._evaluate(self.tree, interpretation)


class InvalidFormula(Exception):
    pass
