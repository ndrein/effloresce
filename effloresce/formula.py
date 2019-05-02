from lark import Lark
from operator import or_, and_, eq
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
            """Recursive implementation of evaluate"""

            def _inject_children(bin_op):
                return lambda: bin_op(
                    _evaluate(tree.children[0]), _evaluate(tree.children[1])
                )

            def _implies():
                return not _evaluate(tree.children[0]) or _evaluate(tree.children[1])

            return {
                "literal": lambda: interpretation[tree],
                "not": lambda: not _evaluate(tree.children[0]),
                "or": _inject_children(or_),
                "and": _inject_children(and_),
                "implies": _implies,
                "iff": _inject_children(eq),
            }[getattr(tree, "data", "literal")]()

        return _evaluate(self.tree)


class InvalidFormula(Exception):
    pass
