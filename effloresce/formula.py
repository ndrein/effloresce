from lark import Lark

from effloresce.grammar import GRAMMAR


class Formula:
    def __init__(self, s: str):
        Lark(GRAMMAR).parse(s)