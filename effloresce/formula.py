from lark import Lark

from effloresce.logic_grammar import LOGIC_GRAMMAR


class Formula:
    def __init__(self, s: str):
        Lark(LOGIC_GRAMMAR).parse(s)