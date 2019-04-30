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


def test_malformed_formula():
    with pytest.raises(Exception):
        Formula("(NOT p")


def test_invalid_token():
    with pytest.raises(Exception):
        Formula("NOT")


def test_not():
    Formula("(NOT p)")
