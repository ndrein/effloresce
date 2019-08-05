from itertools import product
from typing import List

from lark import Tree

from effloresce.formula import Formula


def check(assumptions: List[Formula], inferences: List[Formula]) -> bool:
    if not inferences:
        return True

    return _is_axiom(inferences[0].tree)


def _is_axiom(t: Tree):
    try:
        trees = [
            t.children[0].children[1],
            t.children[1].children[0].children[1],
            t.children[1].children[1],
            t.children[1].children[1].children[0],
            t.children[1].children[1].children[1],
            t.children[1].children[1].children[1].children[0],
            t.children[1].children[1].children[1].children[1],
        ]
        return all(_is_tree(t) for t in trees)
    except AttributeError:
        return False


def _is_tree(v):
    return isinstance(v, Tree)
