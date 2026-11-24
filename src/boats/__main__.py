"""Command line: python -m boats B UP DOWN TIME"""
from __future__ import annotations

import argparse
import sys

from .core import NoValidStream, _fmt, explain, solve, timeline


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="python -m boats",
        description="Find the stream speed from the boat speed, the distances up and down, and the total time.",
    )
    p.add_argument("boat", help="boat speed in still water, km/h (fractions like 7/2 allowed)")
    p.add_argument("up", help="distance upstream, km")
    p.add_argument("down", help="distance downstream, km")
    p.add_argument("time", help="total time, hours")
    p.add_argument("--timeline", action="store_true", help="also print an ASCII timeline")
    a = p.parse_args(argv)
    try:
        print(explain(a.boat, a.up, a.down, a.time))
        if a.timeline:
            s = solve(a.boat, a.up, a.down, a.time)
            if isinstance(s, float):
                print("(timeline needs an exact stream speed)")
            else:
                print()
                print(timeline(a.boat, a.up, a.down, s))
        s = solve(a.boat, a.up, a.down, a.time)
    except (NoValidStream, ValueError) as e:
        print(f"\nResult: {e}", file=sys.stderr)
        return 1
    print(f"\nAnswer: the stream speed is {_fmt(s)} km/h.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
