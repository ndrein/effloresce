from effloresce.formula import Formula
from effloresce.proof_checker import check


def test_empty():
    assert check([], [])


def test_empty_assumptions():
    assert not check([], [Formula("p")])


def test_valid_inference():
    assert check(
        [],
        [
            Formula(
                "((a NAND (a NAND a)) NAND ((a NAND (a NAND a)) NAND ((a NAND a) NAND ((a NAND a) NAND (a NAND a)))))"
            )
        ],
    )


def test_single_invalid_inference():
    for s in (
        "(a NAND a)",
        "((a NAND a) NAND a)",
        "((a NAND a) NAND (a NAND a))",
        "((a NAND (a NAND a)) NAND (a NAND a))",
        "((a NAND (a NAND a)) NAND ((a NAND a) NAND a))",
        "((a NAND (a NAND a)) NAND ((a NAND a) NAND (a NAND a)))",
        "((a NAND (a NAND a)) NAND ((a NAND (a NAND a)) NAND ((a NAND a) NAND a)))",
        "((a NAND (a NAND a)) NAND ((a NAND (a NAND a)) NAND ((a NAND a) NAND (a NAND a))))",
        "((a NAND (a NAND a)) NAND ((a NAND (a NAND a)) NAND ((a NAND a) NAND ((a NAND a) NAND a))))",
    ):
        assert not check([], [Formula(s)])


def test_second_invalid_inference():
    assert not check(
        [],
        [
            Formula(
                "((a NAND (a NAND a)) NAND ((a NAND (a NAND a)) NAND ((a NAND a) NAND ((a NAND a) NAND (a NAND a)))))"
            ),
            Formula("a"),
        ],
    )


def test_valid_consequent():
    assert check([Formula("a"), Formula("(a NAND (b NAND c))")], [Formula("c")])


def test_invalid_inference_with_name_c():
    assert not check([], [Formula("c")])


def test_invalid_inference_with_two_antecedents():
    assert not check([Formula("a"), Formula("b")], [Formula("c")])


def test_invalid_inference_with_second_antecedent_nand():
    assert not check([Formula("a"), Formula("(a NAND a)")], [Formula("c")])


# def test_invalid_inference_with_correct_structure():
#     assert not check([Formula("a"), Formula("(a NAND (a NAND a))")], [Formula("c")])
