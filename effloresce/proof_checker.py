from itertools import product
from typing import List

from lark import Tree

from effloresce.formula import Formula


def check(assumptions: List[Formula] = None, inferences: List[Formula] = None):
    assumptions = assumptions or []
    inferences = inferences or []
    return all((_is_valid_inference(inf, assumptions) for inf in inferences))


def _is_valid_inference(inf: Formula, assumptions):
    return any(
        isinstance(a.tree, Tree) and inf.tree == a.tree.children[1].children[1]
        for a in assumptions
    ) and any(
        isinstance(a2.tree, Tree) and a1.tree == a2.tree.children[0]
        for a1, a2 in product(assumptions, assumptions)
    )
