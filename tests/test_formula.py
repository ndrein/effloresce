import pytest

from effloresce.formula import Formula, InvalidFormula


def test_empty_formula():
    with pytest.raises(InvalidFormula):
        Formula("")


def test_literal_does_not_raise():
    Formula("p")


def test_two_literals():
    with pytest.raises(InvalidFormula):
        Formula("p p")


def test_malformed_formula():
    with pytest.raises(InvalidFormula):
        Formula("(NOT p")


def test_invalid_token():
    with pytest.raises(InvalidFormula):
        Formula("NOT")


def test_not():
    Formula("(NOT p)")
