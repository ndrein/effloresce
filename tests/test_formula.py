import pytest

from effloresce.formula import Formula


def test_empty_formula():
    with pytest.raises(Exception):
        Formula("")


def test_literal_does_not_raise():
    Formula("p")


def test_two_literals():
    with pytest.raises(Exception):
        Formula("p p")


def test_not():
    Formula("(NOT p)")
