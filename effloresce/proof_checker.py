from itertools import product, combinations, permutations
from typing import List

from lark import Tree

from effloresce.formula import Formula


def _try_consequent(ant_1: Tree, ant_2: Tree, consequent: Tree):
    try:
        return (
            ant_2.children[1].children[1] == consequent and ant_2.children[0] == ant_1
        )
    except (AttributeError, IndexError):
        return False


def _is_consequent(f: Formula, antecedents: List[Formula]):
    return any(
        _try_consequent(ant_1.tree, ant_2.tree, f.tree)
        for ant_1, ant_2 in permutations(antecedents, 2)
    )


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
