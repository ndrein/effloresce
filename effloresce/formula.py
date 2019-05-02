from lark import Lark, Token
from operator import or_, and_, eq
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.grammar import GRAMMAR
from typing import Dict, Callable


class Formula:
    def __init__(self, s: str):
        try:
            self.tree = Lark(GRAMMAR).parse(s)
        except (UnexpectedCharacters, ParseError):
            raise InvalidFormula

    def evaluate(self, interpretation: Dict):
        def _evaluate(tree):
            """Recursive implementation of evaluate"""

            def _make_nullary_op(bin_op: Callable):
                return lambda: bin_op(
                    _evaluate(tree.children[0]), _evaluate(tree.children[1])
                )

            if isinstance(tree, Token):
                return interpretation[tree]

            return {
                "not": lambda: not _evaluate(tree.children[0]),
                "or": _make_nullary_op(or_),
                "and": _make_nullary_op(and_),
                "implies": _make_nullary_op(lambda p, q: not p or q),
                "iff": _make_nullary_op(eq),
            }[tree.data]()

        return _evaluate(self.tree)


class InvalidFormula(Exception):
    pass
