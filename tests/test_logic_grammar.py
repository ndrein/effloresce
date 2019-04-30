from typing import Sequence
from typing import Union

import pytest
from lark import Lark
from lark import Tree
from lark.exceptions import UnexpectedCharacters, ParseError

from effloresce.grammar import GRAMMAR


def test_hello_world():
    Lark(
        """start: WORD "," WORD "!"

            %import common.WORD   // imports from terminal library
            %ignore " "           // Disregard spaces in text
            """
    ).parse("Hello, World!")


def test_parse_literal():
    assert_matches("p", Lark(GRAMMAR).parse("p"))


def test_long_literal():
    s = "aweoriquwpeoiuasdfnxcvn"
    assert_matches(s, Lark(GRAMMAR).parse(s))


def test_unexpected_characters():
    for c in ("A", "-", "1"):
        with pytest.raises(UnexpectedCharacters):
            Lark(GRAMMAR).parse(c)


def test_space_gives_parse_error():
    with pytest.raises(ParseError):
        Lark(GRAMMAR).parse(" ")


def test_literal_with_whitespace():
    assert_matches("p", Lark(GRAMMAR).parse("  p "))


def test_not_without_whitespace():
    assert_matches(("not", "p"), Lark(GRAMMAR).parse("(NOTp)"))


def test_not_with_whitespace():
    assert_matches(("not", "p"), Lark(GRAMMAR).parse("  (NOT p ) "))


def test_double_negation():
    assert_matches(("not", ("not", "p")), Lark(GRAMMAR).parse("(NOT (NOT p))"))


def test_or():
    assert_matches(("or", "p", "q"), Lark(GRAMMAR).parse("(p OR q)"))


def test_or_and_not():
    assert_matches(
        ("or", "p", ("not", "q")), Lark(GRAMMAR).parse("(p OR (NOT q))")
    )


def test_and():
    assert_matches(("and", "p", "q"), Lark(GRAMMAR).parse("(p AND q)"))


def test_and_or():
    assert_matches(
        ("and", ("or", "p", "q"), "r"), Lark(GRAMMAR).parse("((p OR q) AND r)")
    )


def test_implies():
    assert_matches(("implies", "p", "q"), Lark(GRAMMAR).parse("(p IMPLIES q)"))


def test_iff():
    assert_matches(("iff", "p", "q"), Lark(GRAMMAR).parse("(p IFF q)"))


def assert_matches(target: Union[str, Sequence], tree: Tree):
    if isinstance(target, str):
        assert target == tree
    else:
        assert target[0] == tree.data

        for subtarget, child in zip(target[1:], tree.children):
            assert_matches(subtarget, child)


def test_and_or_not_implies_iff():
    assert_matches(
        ("and", "a", ("or", ("not", "b"), ("implies", ("iff", "c", "d"), "e"))),
        Lark(GRAMMAR).parse("(a AND ((NOT b) OR ((c IFF d) IMPLIES e)))"),
    )
