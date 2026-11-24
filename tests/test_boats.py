from fractions import Fraction as F
import itertools

import pytest

from boats import NoValidStream, explain, solve, solve_all, timeline, trip_time, wrong_setup
from boats.__main__ import main


def test_classic_case():
    assert solve(12, 15, 18, 3) == 4
    assert trip_time(12, 15, 18, 4) == 3


def test_classic_trap():
    assert wrong_setup(12, 15, 18, 3) == 3
    # s = 3 satisfies the swapped equation exactly...
    assert F(15, 15) + F(18, 9) == 3
    # ...but the true trip with s = 3 is 43/15 h
    assert trip_time(12, 15, 18, 3) == F(43, 15)


def test_negative_root_dropped():
    # roots are 4 and -3; only 4 is kept
    assert solve(12, 15, 18, 3) == 4


def test_too_fast_for_any_stream():
    # even s = 0 gives 2/5 h, so no stream speed gives 1/5 h
    with pytest.raises(NoValidStream):
        solve(5, 1, 1, F(1, 5))  # too fast: even s = 0 gives 2/5 h


def test_no_solution_message():
    with pytest.raises(NoValidStream):
        solve(10, 10, 10, 1)


def test_bad_input():
    with pytest.raises(ValueError):
        solve(0, 1, 1, 1)
    with pytest.raises(ValueError):
        solve(10, -1, 1, 1)
    with pytest.raises(ValueError):
        trip_time(10, 1, 1, 10)


def test_generated_cases_round_trip():
    cases = 0
    ambiguous = 0
    for b, s, up, down in itertools.product(
        [F(5), F(12), F(15), F(7, 2), F(20)],
        [F(1), F(2), F(3), F(1, 2), F(5, 2)],
        [F(4), F(15), F(9, 2), F(30)],
        [F(6), F(18), F(7, 3)],
    ):
        if s >= b:
            continue
        T = trip_time(b, up, down, s)
        roots = solve_all(b, up, down, T)
        assert s in roots, (b, s, up, down)
        if len(roots) == 1:
            assert solve(b, up, down, T) == s
        else:
            with pytest.raises(NoValidStream):
                solve(b, up, down, T)
            ambiguous += 1
        cases += 1
    assert cases > 50
    assert ambiguous > 0  # two valid speeds do occur when the upstream leg is shorter


def test_generated_trap_checks_out_in_its_own_equation():
    seen = 0
    for b, s, up, down in itertools.product(
        [F(12), F(15), F(20)], [F(1), F(2), F(3)], [F(15), F(30)], [F(18), F(6)]
    ):
        T = trip_time(b, up, down, s)
        w = wrong_setup(b, up, down, T)
        if w is None or not isinstance(w, F):
            continue
        # exact check in the wrong equation
        assert F(up) / (b + w) + F(down) / (b - w) == T
        if w != s:
            assert trip_time(b, up, down, w) != T
            seen += 1
    assert seen > 0


def test_equal_distances_have_equal_roots_both_ways():
    # with d_up = d_down the two set-ups give the same equation
    assert wrong_setup(10, 12, 12, F(12, 8) + F(12, 12)) == solve(10, 12, 12, F(12, 8) + F(12, 12))


def test_explain_mentions_the_key_steps():
    text = explain(12, 15, 18, 3)
    assert "3 s^2 + (-3) s + (-36) = 0" in text
    assert "s = -3 is rejected" in text
    assert "43/15" in text
    assert "Answer" not in text


def test_timeline_shape():
    t = timeline(12, 15, 18, 4, width=40)
    first, second = t.splitlines()
    assert first.startswith("|") and first.endswith("|")
    assert len(first) == 42
    assert first.count("<") == 25 and first.count(">") == 15  # 15/8 : 9/8 of 40
    assert "15/8 h at 8 km/h" in second and "9/8 h at 16 km/h" in second


def test_cli(capsys):
    assert main(["12", "15", "18", "3", "--timeline"]) == 0
    out = capsys.readouterr().out
    assert "Answer: the stream speed is 4 km/h." in out
    assert "43/15" in out


def test_cli_no_solution(capsys):
    assert main(["10", "10", "10", "1"]) == 1
