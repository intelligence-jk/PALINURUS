"""Boats and streams, solved exactly.

A boat has speed b in still water. A stream flows at speed s (0 < s < b).
Going upstream the speed is b - s, downstream it is b + s. The boat goes
d_up km upstream and d_down km downstream and the whole trip takes T hours.

    d_up/(b - s) + d_down/(b + s) = T
    multiply by (b - s)(b + s):  d_up(b + s) + d_down(b - s) = T(b^2 - s^2)
    T s^2 + (d_up - d_down) s + (d_up + d_down) b - T b^2 = 0

All inputs are turned into Fractions, so answers are exact whenever the
discriminant is a perfect square of a rational number.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt, sqrt
from typing import Union

Number = Union[int, str, Fraction]
Root = Union[Fraction, float]


class NoValidStream(ValueError):
    """No stream speed s with 0 < s < b fits the data."""


def _f(x: Number) -> Fraction:
    return Fraction(x)


@dataclass(frozen=True)
class Problem:
    b: Fraction  # boat speed in still water
    d_up: Fraction
    d_down: Fraction
    total: Fraction

    @classmethod
    def make(cls, b: Number, d_up: Number, d_down: Number, total: Number) -> "Problem":
        p = cls(_f(b), _f(d_up), _f(d_down), _f(total))
        if p.b <= 0 or p.d_up <= 0 or p.d_down <= 0 or p.total <= 0:
            raise ValueError("speed, distances and time must all be positive")
        return p


def trip_time(b: Number, d_up: Number, d_down: Number, s: Number) -> Fraction:
    """Total time for the trip with stream speed s (needs 0 <= s < b)."""
    b, d_up, d_down, s = _f(b), _f(d_up), _f(d_down), _f(s)
    if not 0 <= s < b:
        raise ValueError("stream speed must satisfy 0 <= s < b")
    return d_up / (b - s) + d_down / (b + s)


def _sqrt(x: Fraction) -> Root:
    """Exact square root when x is a rational square, else a float."""
    if x < 0:
        raise ValueError("negative")
    n, d = x.numerator, x.denominator
    rn, rd = isqrt(n), isqrt(d)
    if rn * rn == n and rd * rd == d:
        return Fraction(rn, rd)
    return sqrt(x.numerator / x.denominator)


def _quadratic(A: Fraction, B: Fraction, C: Fraction) -> list[Root]:
    disc = B * B - 4 * A * C
    if disc < 0:
        return []
    r = _sqrt(disc)
    if disc == 0:
        return [-B / (2 * A)]
    return sorted([(-B - r) / (2 * A), (-B + r) / (2 * A)], key=float)


def coefficients(p: Problem) -> tuple[Fraction, Fraction, Fraction]:
    return p.total, p.d_up - p.d_down, (p.d_up + p.d_down) * p.b - p.total * p.b**2


def solve_all(b: Number, d_up: Number, d_down: Number, total: Number) -> list[Root]:
    """Every stream speed with 0 < s < b that fits. Usually one; rarely two."""
    p = Problem.make(b, d_up, d_down, total)
    return [r for r in _quadratic(*coefficients(p)) if 0 < r < p.b]


def solve(b: Number, d_up: Number, d_down: Number, total: Number) -> Root:
    """Stream speed s. Only roots with 0 < s < b are kept.

    A negative root would mean the stream flows the other way, which the set
    up (up means against the stream) does not allow. A root s >= b would mean
    the boat cannot move upstream at all. Raises NoValidStream if none is left.
    """
    roots = solve_all(b, d_up, d_down, total)
    if not roots:
        raise NoValidStream("no stream speed between 0 and the boat speed fits these numbers")
    if len(roots) > 1:  # happens when d_up < d_down: the data does not decide
        raise NoValidStream("two valid stream speeds: " + ", ".join(str(r) for r in roots))
    return roots[0]


def wrong_setup(b: Number, d_up: Number, d_down: Number, total: Number) -> Root | None:
    """The classic trap: upstream uses b + s and downstream uses b - s.

    Returns the positive root s (0 < s < b) of that wrong equation, or None
    if it has none. That s makes the wrong equation true, so it "checks out",
    but it is not the real stream speed.
    """
    p = Problem.make(b, d_up, d_down, total)
    # d_up/(b+s) + d_down/(b-s) = T  ->  T s^2 - (d_up - d_down) s + (d_up + d_down) b - T b^2 = 0
    A, B, C = coefficients(p)
    roots = [r for r in _quadratic(A, -B, C) if 0 < r < p.b]
    return roots[0] if roots else None


def _fmt(x: Root) -> str:
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return f"{x:.4f}"


def explain(b: Number, d_up: Number, d_down: Number, total: Number) -> str:
    p = Problem.make(b, d_up, d_down, total)
    A, B, C = coefficients(p)
    lines = [
        f"Boat in still water: {_fmt(p.b)} km/h. Upstream {_fmt(p.d_up)} km, downstream {_fmt(p.d_down)} km, total {_fmt(p.total)} h.",
        "Let the stream speed be s km/h.",
        f"Upstream the stream pushes against the boat: speed {_fmt(p.b)} - s.",
        f"Downstream the stream helps: speed {_fmt(p.b)} + s.",
        f"Time = distance / speed, so {_fmt(p.d_up)}/({_fmt(p.b)} - s) + {_fmt(p.d_down)}/({_fmt(p.b)} + s) = {_fmt(p.total)}.",
        f"Multiply by ({_fmt(p.b)} - s)({_fmt(p.b)} + s): {_fmt(p.d_up)}({_fmt(p.b)} + s) + {_fmt(p.d_down)}({_fmt(p.b)} - s) = {_fmt(p.total)}({_fmt(p.b)}^2 - s^2).",
        f"Rearranged: {_fmt(A)} s^2 + ({_fmt(B)}) s + ({_fmt(C)}) = 0.",
    ]
    roots = _quadratic(A, B, C)
    lines.append("Roots: " + (", ".join(_fmt(r) for r in roots) if roots else "none (negative discriminant)") + ".")
    kept = [r for r in roots if 0 < r < p.b]
    for r in roots:
        if r <= 0:
            lines.append(f"s = {_fmt(r)} is rejected: a speed cannot be negative or zero here (the stream runs against the boat going up).")
        elif r >= p.b:
            lines.append(f"s = {_fmt(r)} is rejected: the stream would be at least as fast as the boat, which could never go upstream.")
    if not kept:
        lines.append("No stream speed fits these numbers.")
        return "\n".join(lines)
    for s in kept:
        up, down = p.b - s, p.b + s
        t = trip_time(p.b, p.d_up, p.d_down, s)
        lines.append(
            f"Check s = {_fmt(s)}: {_fmt(p.d_up)}/{_fmt(up)} + {_fmt(p.d_down)}/{_fmt(down)} = {_fmt(t)} h"
            + (" (matches)." if isinstance(s, Fraction) and t == p.total else ".")
        )
    wrong = wrong_setup(b, d_up, d_down, total)
    if wrong is not None and kept and wrong != kept[0]:
        tw = trip_time(p.b, p.d_up, p.d_down, wrong) if isinstance(wrong, Fraction) else None
        lines.append("")
        lines.append("The trap: swap the two speeds (use b + s going up and b - s going down).")
        lines.append(
            f"That wrong equation also has a clean answer, s = {_fmt(wrong)}, and it checks out in its own wrong equation."
        )
        if tw is not None:
            lines.append(
                f"But with s = {_fmt(wrong)} the real trip takes {_fmt(tw)} h, not {_fmt(p.total)} h. Always check against the story, not against your own equation."
            )
    return "\n".join(lines)


def timeline(b: Number, d_up: Number, d_down: Number, s: Number, width: int = 50) -> str:
    """ASCII timeline: one bar for the upstream leg, one for downstream, scaled to time."""
    b, d_up, d_down, s = _f(b), _f(d_up), _f(d_down), _f(s)
    t_up = d_up / (b - s)
    t_down = d_down / (b + s)
    total = t_up + t_down
    n_up = max(1, round(width * t_up / total))
    n_down = max(1, width - n_up)
    return "\n".join(
        [
            f"|{'<' * n_up}{'>' * n_down}|",
            f" up {_fmt(t_up)} h at {_fmt(b - s)} km/h"
            f"  then  down {_fmt(t_down)} h at {_fmt(b + s)} km/h"
            f"  = {_fmt(total)} h",
        ]
    )
