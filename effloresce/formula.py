from lark import Lark, Transformer
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.grammar import GRAMMAR


class Formula:
    def __init__(self, s: str):
        try:
            self.tree = Lark(GRAMMAR).parse(s)
        except (UnexpectedCharacters, ParseError):
            raise InvalidFormula

    def evaluate(self, interpretation):
        tree = self.tree
        if hasattr(tree, "data"):
            tree = tree.children[0]

            if hasattr(tree, "data"):
                tree = tree.children[0]
                return interpretation[tree]

            return not interpretation[tree]

        return interpretation[tree]


class InvalidFormula(Exception):
    pass
