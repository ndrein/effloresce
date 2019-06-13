from effloresce.formula import Formula
from effloresce.proof_checker import check


def test_check_empty_lists():
    assert check([], [])


def test_inference_with_no_assumptions():
    assert not check([], [Formula("r")])


def test_second_inference_not_in_assumptions():
    assert not check([Formula("p")], [Formula("p"), Formula("q")])


def test_valid_inference():
    assert check([Formula("p"), Formula("(p NAND (p NAND q))")], [Formula("q")])


def test_assumption_with_incorrect_tree():
    assert not check([Formula("p"), Formula("(p NAND (p NAND p))")], [Formula("q")])


def test_inference_must_match_both_assumptions():
    assert not check([Formula("q"), Formula("(p NAND (p NAND q))")], [Formula("q")])


def test_a_not_found_in_second_assumption():
    assert not check([Formula("p"), Formula("(q NAND (q NAND q))")], [Formula("q")])


def test_all_inference_cases():
    assert check([Formula("p"), Formula("(p NAND (r NAND p))")], [Formula("p")])
    assert not check([Formula("p"), Formula("(p NAND (r NAND q))")], [Formula("p")])
    assert not check([Formula("p"), Formula("(q NAND (r NAND p))")], [Formula("p")])
    assert not check([Formula("p"), Formula("(q NAND (r NAND q))")], [Formula("p")])
    assert not check([Formula("q"), Formula("(p NAND (r NAND p))")], [Formula("p")])
    assert not check([Formula("q"), Formula("(p NAND (r NAND q))")], [Formula("p")])
    assert check([Formula("q"), Formula("(q NAND (r NAND p))")], [Formula("p")])
    assert not check([Formula("q"), Formula("(q NAND (r NAND q))")], [Formula("p")])


def test_no_args():
    assert check()


def test_only_inferences():
    assert not check(inferences=[Formula("p")])
