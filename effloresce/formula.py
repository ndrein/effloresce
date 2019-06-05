from __future__ import annotations
from lark import Lark, Token, Tree
from operator import or_, and_, eq
from itertools import product

from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.grammar import GRAMMAR
from typing import Dict, Callable, Any, Union, Container, Collection, List


class Formula:
    def __init__(self, s: str):
        try:
            self.tree = Lark(GRAMMAR).parse(s)
        except (UnexpectedCharacters, ParseError):
            raise InvalidFormula

    @classmethod
    def _evaluate(cls, tree: Tree, interpretation: Dict) -> bool:
        """Recurses on smaller trees"""

        def _make_nullary_op(bin_op: Callable[[Any, Any], bool]) -> Callable[[], bool]:
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

    @staticmethod
    def _get_literals(node: Union[Tree, Token]) -> List:
        def get_literals(tree):
            for node in tree.children:
                if isinstance(node, Token):
                    yield node
                else:
                    yield from get_literals(node)

        if isinstance(node, Token):
            return [node]

        return list(get_literals(node))

    def entails(self, formula: Formula) -> bool:
        """Determines whether formula is true for every interpretation that satisfies self"""
        literals = self._get_literals(self.tree)
        for booleans in product(*[{False, True}] * len(literals)):
            interpretation = dict(zip(literals, booleans))
            if self._evaluate(self.tree, interpretation) and not self._evaluate(
                formula.tree, interpretation
            ):
                return False

        return True


class InvalidFormula(Exception):
    pass


class NoMatchingLiteral(Exception):
    pass
