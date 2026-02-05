"""
Formatted print out of a relation.

Examples:
    >>> relation = [("a", "b"), ("c", "c")]
    >>> pretty_print_relation(relation)
    >>> pretty_print_relation(relation, newline=True)
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple


Pair = Tuple[str, str]


def pretty_print_relation(relation: Sequence[Sequence[str]], newline: bool = False) -> None:
    """Pretty-print a relation."""
    open_bracket = "{"
    close_bracket = "}"

    if not relation:
        print("∅", end="\n" if newline else "")
        return

    print(open_bracket, end="")
    for index, pair in enumerate(relation):
        left, right = _normalize_pair(pair)
        print(f"({left},{right})", end="")
        if index != len(relation) - 1:
            print(", ", end="")
    print(close_bracket, end="")
    if newline:
        print()


def _normalize_pair(pair: Sequence[str]) -> Pair:
    if len(pair) == 2:
        return str(pair[0]), str(pair[1])
    if len(pair) == 1 and len(pair[0]) == 2:
        return pair[0][0], pair[0][1]
    if len(pair) == 2 and isinstance(pair, str):
        return pair[0], pair[1]
    raise ValueError("Invalid relation pair format.")
