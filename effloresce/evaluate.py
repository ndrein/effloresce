from operator import or_, and_, eq
from typing import Dict, Callable, Any

from lark import Tree, Token


def evaluate(tree: Tree, interpretation: Dict[str, bool]) -> bool:
    """Recurses on smaller trees"""

    def _make_nullary_op(bin_op: Callable[[Any, Any], bool]) -> Callable[[], bool]:
        return lambda: bin_op(
            evaluate(tree.children[0], interpretation),
            evaluate(tree.children[1], interpretation),
        )

    if isinstance(tree, Token):
        return interpretation[tree]

    return {
        "not": lambda: not evaluate(tree.children[0], interpretation),
        "or": _make_nullary_op(or_),
        "and": _make_nullary_op(and_),
        "implies": _make_nullary_op(lambda p, q: not p or q),
        "iff": _make_nullary_op(eq),
        "nand": _make_nullary_op(lambda p, q: not (p and q)),
    }[tree.data]()
