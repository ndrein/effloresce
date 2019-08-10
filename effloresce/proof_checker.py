from itertools import product, combinations, permutations
from typing import List

from lark import Tree

from effloresce.formula import Formula


def _is_consequent(f: Formula, antecedents: List[Formula]):
    return any(f.proves(ant_1, ant_2) for ant_1, ant_2 in permutations(antecedents, 2))


def check(assumptions: List[Formula], inferences: List[Formula]) -> bool:
    return all(
        inf.is_axiom() or _is_consequent(inf, assumptions + inferences[:i])
        for i, inf in enumerate(inferences)
    )
