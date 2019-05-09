from lark import Lark, Token, Tree
from operator import or_, and_, eq
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.grammar import GRAMMAR
from typing import Dict, Callable, Any, Union


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

    @classmethod
    def _contains(cls, tree, token):
        if isinstance(tree, Token):
            return token == tree

        return any([cls._contains(t, token) for t in tree.children])

    def _contains_unknown_literal(self, tree: Union[Tree, Token]):
        if isinstance(tree, Token):
            return not self._contains(self.tree, tree)

        if isinstance(tree, Tree):
            return any([self._contains_unknown_literal(t) for t in tree.children])

    def entails(self, formula: "Formula") -> bool:
        if self._contains_unknown_literal(formula.tree):
            raise NoMatchingLiteral

        return True


class InvalidFormula(Exception):
    pass


class NoMatchingLiteral(Exception):
    pass
