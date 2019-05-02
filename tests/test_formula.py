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


def test_evaluate_empty_interpretation():
    with pytest.raises(Exception):
        Formula("p").evaluate({})


def test_evaluate_true_literal():
    assert Formula("p").evaluate({"p": True})


def test_evaluate_false_literal():
    assert not Formula("p").evaluate({"p": False})


def test_evaluate_different_literal():
    assert Formula("q").evaluate({"q": True})


def test_evaluate_non_matching_interpretation():
    with pytest.raises(Exception):
        Formula("q").evaluate({"p": True})


def test_evaluate_longer_literal():
    assert Formula("longliteral").evaluate({"longliteral": True})


def test_evaluate_not():
    assert not Formula("(NOT p)").evaluate({"p": True})


def test_evaluate_not_not():
    assert Formula("(NOT (NOT p))").evaluate({"p": True})


def test_evaluate_or():
    assert Formula("(p OR p)").evaluate(({"p": True}))


def test_evaluate_false_or():
    assert not Formula("(p OR p)").evaluate(({"p": False}))


def test_evaluate_false_true_or():
    assert Formula("(p OR q)").evaluate(({"p": False, "q": True}))


def test_evaluate_nested_or():
    assert Formula("(p OR (NOT p))").evaluate({"p": False})


def test_evaluate_complex_or():
    assert not Formula("((NOT (p OR q)) OR r)").evaluate(
        {"p": False, "q": True, "r": False}
    )


def test_evaluate_false_and():
    assert not Formula("(p AND p)").evaluate({"p": False})


def test_evaluate_true_and():
    assert Formula("(p AND p)").evaluate({"p": True})


def test_evaluate_complex_and():
    assert Formula("((NOT p) AND (q OR p))").evaluate({"p": False, "q": True})
