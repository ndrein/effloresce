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


def test_evaluate_complex_implies():
    assert Formula("((NOT p) IMPLIES (p OR r))").evaluate(
        {"p": False, "q": False, "r": True}
    )


def test_evaluate_4_implies_cases():
    assert Formula("(p IMPLIES q)").evaluate({"p": False, "q": False})
    assert Formula("(p IMPLIES q)").evaluate({"p": False, "q": True})
    assert not Formula("(p IMPLIES q)").evaluate({"p": True, "q": False})
    assert Formula("(p IMPLIES q)").evaluate({"p": True, "q": True})


def test_evaluate_complex_iff():
    assert not Formula("((p IMPLIES p) IFF (p AND q))").evaluate(
        {"p": True, "q": False}
    )


def test_entails_same_literals():
    assert Formula("p").entails(Formula("p"))


def test_entails_not():
    assert not Formula("p").entails(Formula("(NOT p)"))


def test_entails_different_literal_raises_error():
    assert Formula("q").entails(Formula("q"))


def test_bottom_entails_anything():
    assert Formula("(p AND (NOT p))").entails(Formula("(p AND (NOT p))"))


def test_entails_tautology():
    assert Formula("p").entails(Formula("(p OR (NOT p))"))


def test_unknown_literal_entails():
    assert Formula("(p AND q)").entails(Formula("p"))


def test_or_does_not_entail():
    assert not Formula("(p OR q)").entails(Formula("p"))


def test_complex_entails():
    assert Formula("(NOT (p IFF q))").entails(
        Formula("((NOT (p IMPLIES q)) OR (NOT (q IMPLIES p)))")
    )
