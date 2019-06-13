from __future__ import annotations

from itertools import product, chain
from typing import Dict, List, Iterable, Set, Sized

from lark import Lark, Token
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.evaluate import evaluate
from effloresce.grammar import GRAMMAR


class Formula:
    def __eq__(self, o):
        return isinstance(o, Formula) and self.tree == o.tree

    def __init__(self, s: str):
        try:
            self.tree = Lark(GRAMMAR).parse(s)
        except (UnexpectedCharacters, ParseError):
            raise InvalidFormula

    def evaluate(self, interpretation: Dict[str, bool]) -> bool:
        return evaluate(self.tree, interpretation)

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
    def _get_interpretations(literals: Sized) -> Iterable[Dict]:
        """Generate all possible interpretations"""
        for booleans in product(*[{False, True}] * len(literals)):
            yield dict(zip(literals, booleans))

    def entails(self, formula: Formula) -> bool:
        """Determines whether formula is true for every interpretation that satisfies self"""
        return all(
            (
                evaluate(formula.tree, interp)
                for interp in self._get_interpretations(self._get_literals())
                if evaluate(self.tree, interp)
            )
        )


class InvalidFormula(Exception):
    pass
