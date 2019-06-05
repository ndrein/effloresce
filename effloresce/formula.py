from __future__ import annotations

from itertools import product, chain
from operator import or_, and_, eq
from typing import Dict, Callable, Any, List, Iterable

from lark import Lark, Token, Tree
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.grammar import GRAMMAR


class Formula:
    def __init__(self, s: str):
        try:
            self.tree = Lark(GRAMMAR).parse(s)
        except (UnexpectedCharacters, ParseError):
            raise InvalidFormula

    @classmethod
    def _eval(cls, tree: Tree, interpretation: Dict) -> bool:
        """Recurses on smaller trees"""

        def _make_nullary_op(bin_op: Callable[[Any, Any], bool]) -> Callable[[], bool]:
            return lambda: bin_op(
                cls._eval(tree.children[0], interpretation),
                cls._eval(tree.children[1], interpretation),
            )

        if isinstance(tree, Token):
            return interpretation[tree]

        return {
            "not": lambda: not cls._eval(tree.children[0], interpretation),
            "or": _make_nullary_op(or_),
            "and": _make_nullary_op(and_),
            "implies": _make_nullary_op(lambda p, q: not p or q),
            "iff": _make_nullary_op(eq),
        }[tree.data]()

    def evaluate(self, interpretation: Dict[str, bool]) -> bool:
        return self._eval(self.tree, interpretation)

    def _get_literals(self) -> List:
        """Return all literals in self.tree"""

        def get_literals(node):
            if isinstance(node, Token):
                yield node
            else:
                yield from chain(*(get_literals(n) for n in node.children))

        return list(get_literals(self.tree))

    @staticmethod
    def _get_interpretations(literals: List) -> Iterable[Dict]:
        """Generate all possible interpretations"""
        for booleans in product(*[{False, True}] * len(literals)):
            yield dict(zip(literals, booleans))

    def entails(self, formula: Formula) -> bool:
        """Determines whether formula is true for every interpretation that satisfies self"""
        return all(
            (
                self._eval(formula.tree, interp)
                for interp in self._get_interpretations(self._get_literals())
                if self._eval(self.tree, interp)
            )
        )


class InvalidFormula(Exception):
    pass
