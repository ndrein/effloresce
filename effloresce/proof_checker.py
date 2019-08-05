from itertools import product
from typing import List

from lark import Tree

from effloresce.formula import Formula


def check(assumptions: List[Formula], inferences: List[Formula]) -> bool:
    return all(_is_axiom(inf.tree) for inf in inferences)


def _is_axiom(t: Tree):
    """
    Determine if t follows Lukasiewicz's first axiom system:
    (A | (B | C)) | ((D | (D | D)) | ((D | B) | (A | D))))
    """
    try:
        return all(
            _is_tree(t)
            for t in [
                t.children[0].children[1],
                t.children[1].children[0].children[1],
                t.children[1].children[1],
                t.children[1].children[1].children[0],
                t.children[1].children[1].children[1],
                t.children[1].children[1].children[1].children[0],
                t.children[1].children[1].children[1].children[1],
            ]
        )
    except AttributeError:
        return False


def _is_tree(v):
    return isinstance(v, Tree)
