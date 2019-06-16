from __future__ import annotations

from itertools import product, chain
from operator import or_, and_, eq
from typing import Dict, Iterable, Sized, Callable, Any

from lark import Lark, Token, Tree
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.grammar import GRAMMAR


class Formula:
    """Represents a formula in propositional logic"""

    @classmethod
    def _evaluate(cls, tree: Tree, interpretation: Dict[str, bool]) -> bool:
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
            "nand": _make_nullary_op(lambda p, q: not (p and q)),
        }[tree.data]()

    def __init__(self, s: str):
        """
        :param s: Must be a string admitted by the propositional logic grammar
        :raises InvalidFormula if s is not described by the grammar
        """
        try:
            self.tree = Lark(GRAMMAR).parse(s)
        except (UnexpectedCharacters, ParseError):
            raise InvalidFormula

    def evaluate(self, interpretation: Dict[str, bool]) -> bool:
        """Evaluate the syntax tree from the bottom up,
        substituting true or false for literals according to the given interpretation

        :param interpretation: dict mapping from literal name to bool
        """
        return self._evaluate(self.tree, interpretation)

    def _get_literals(self) -> Sized:
        """Return all literals in self.tree"""
        if isinstance(self.tree, Token):
            return {self.tree}

        return {
            t
            for t in chain(*(tree.children for tree in self.tree.iter_subtrees()))
            if isinstance(t, Token)
        }

    @staticmethod
    def _get_interpretations(literals: Sized[str]) -> Iterable[Dict]:
        """Generate all possible interpretations"""
        for booleans in product(*[{False, True}] * len(literals)):
            yield dict(zip(literals, booleans))

    def entails(self, formula: Formula) -> bool:
        """Determines whether formula is true for every interpretation that satisfies self"""
        return all(
            (
                self._evaluate(formula.tree, interp)
                for interp in self._get_interpretations(self._get_literals())
                if self._evaluate(self.tree, interp)
            )
        )


class InvalidFormula(Exception):
    pass
