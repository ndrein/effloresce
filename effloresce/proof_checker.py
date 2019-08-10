from itertools import product
from typing import List

from lark import Tree

from effloresce.formula import Formula


def _is_consequent(f: Formula, antecedents: List[Formula]):
    try:
        ant_2 = antecedents[1]
        return (
            ant_2.tree.children[1].children[1] == f.tree
            and ant_2.tree.children[0] == antecedents[0].tree
        )
    except (AttributeError, IndexError):
        return False


def check(assumptions: List[Formula], inferences: List[Formula]) -> bool:
    return all(
        _is_axiom(inf) or _is_consequent(inf, assumptions + inferences[:i])
        for i, inf in enumerate(inferences)
    )


def _is_axiom(f: Formula):
    """
    Determine if f follows Lukasiewicz's first axiom system:
    (A | (B | C)) | ((D | (D | D)) | ((D | B) | (A | D))))
    """
    tree = f.tree
    try:
        return all(
            _is_tree(t)
            for t in [
                tree.children[0].children[1],
                tree.children[1].children[0].children[1],
                tree.children[1].children[1],
                tree.children[1].children[1].children[0],
                tree.children[1].children[1].children[1],
                tree.children[1].children[1].children[1].children[0],
                tree.children[1].children[1].children[1].children[1],
            ]
        )
    except AttributeError:
        return False


def _is_tree(v):
    return isinstance(v, Tree)
