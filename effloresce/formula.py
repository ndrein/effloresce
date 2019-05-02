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
        def _evaluate(tree):
            """Recursive implementation of tree evaluation"""
            return {
                "literal": lambda: interpretation[tree],
                "not": lambda: not _evaluate(tree.children[0]),
                "or": lambda: _evaluate(tree.children[0])
                or _evaluate(tree.children[1]),
                "and": lambda: _evaluate(tree.children[0])
                and _evaluate(tree.children[1]),
            }[getattr(tree, "data", "literal")]()

        return _evaluate(self.tree)


class InvalidFormula(Exception):
    pass
