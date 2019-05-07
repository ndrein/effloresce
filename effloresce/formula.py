from lark import Lark, Token, Tree
from operator import or_, and_, eq
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.grammar import GRAMMAR
from typing import Dict, Callable, Any


class Formula:
    def __init__(self, s: str):
        try:
            self.tree = Lark(GRAMMAR).parse(s)
        except (UnexpectedCharacters, ParseError):
            raise InvalidFormula

    @classmethod
    def _evaluate(cls, tree: Tree, interpretation: Dict) -> bool:
        """Recurses on smaller trees"""

        def _make_nullary_op(bin_op):
            return lambda: bin_op(
                cls._evaluate(tree.children[0], interpretation),
                cls._evaluate(tree.children[1], interpretation),
            )

        if isinstance(tree, Token):
            return interpretation[tree]

        return {
            "not": lambda: not cls._evaluate(tree.children[0], interpretation),
            "or": _make_nullary_op(or_),
            "and": _make_nullary_op(and_),
            "implies": _make_nullary_op(lambda p, q: not p or q),
            "iff": _make_nullary_op(eq),
        }[tree.data]()

    def evaluate(self, interpretation: Dict) -> bool:
        return self._evaluate(self.tree, interpretation)

    def entails(self, formula: "Formula") -> bool:
        raise MismatchedLiteral


class InvalidFormula(Exception):
    pass


class MismatchedLiteral(Exception):
    pass
