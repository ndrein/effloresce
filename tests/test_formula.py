from typing import Sequence
from typing import Union

import pytest
from lark import Lark
from lark import Tree
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.syntax.logic_grammar import LOGIC_GRAMMAR


class Formula:
    def __init__(self, s: str):
        if s == "":
            raise InvalidFormula


class InvalidFormula(Exception):
    pass


# def test_hello_world():
#     Lark(
#         """start: WORD "," WORD "!"
#
#             %import common.WORD   // imports from terminal library
#             %ignore " "           // Disregard spaces in text
#             """
#     ).parse("Hello, World!")
#
#
# def test_parse_literal():
#     assert_matches("p", Lark(LOGIC_GRAMMAR).parse("p"))

# def assert_matches(target: Union[str, Sequence], tree: Tree):
#     if isinstance(target, str):
#         assert target == tree
#     else:
#         assert target[0] == tree.data
#
#         for subtarget, child in zip(target[1:], tree.children):
#             assert_matches(subtarget, child)


def test_empty_formula():
    with pytest.raises(InvalidFormula):
        Formula("")


def test_literal_does_not_raise():
    Formula("p")


def test_not():
    Formula("(NOT p")
