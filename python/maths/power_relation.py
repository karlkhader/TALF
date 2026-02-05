"""
Power n of a relation or its transitive closure.

Examples:
    >>> power_relation([("a", "b"), ("c", "c"), ("b", "a")], 3)
    >>> power_relation([("a", "b"), ("c", "c"), ("b", "a")])
    >>> power_relation(["ab", "cc", "ba"])
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from .pretty_print_relation import pretty_print_relation
from .union_relation import union_relation

Pair = Tuple[str, str]


def power_relation(relation: Sequence[Sequence[str]], n: int | None = None) -> List[Pair]:
    """Return the nth power of a relation or its transitive closure."""
    exponent_symbol = "^"
    infinite_symbol = "∞"

    original = _normalize_relation(relation)

    if n is not None:
        powers: List[List[Pair]] = [original]
        for _ in range(2, n + 1):
            previous = powers[-1]
            current: List[Pair] = []
            for left1, right1 in previous:
                for left2, right2 in original:
                    if right1 == left2:
                        current.append((left1, right2))
            powers.append(current)

        relation_n = _unique_pairs(powers[-1])
        pretty_print_relation(original)
        print(f"{exponent_symbol}{n} = ", end="")
        pretty_print_relation(relation_n, newline=True)
        return relation_n

    exponent = 1
    current_relation = original
    while True:
        exponent += 1
        previous_relation = current_relation
        current_relation = union_relation(current_relation, power_relation(original, exponent))
        print("\n\u2001\n")
        if _unique_pairs(previous_relation) == _unique_pairs(current_relation):
            break

    pretty_print_relation(original)
    print(f"{exponent_symbol}{infinite_symbol} = ", end="")
    pretty_print_relation(_unique_pairs(current_relation), newline=True)
    return _unique_pairs(current_relation)


def _unique_pairs(relation: Sequence[Pair]) -> List[Pair]:
    seen = set()
    result = []
    for pair in relation:
        if pair not in seen:
            seen.add(pair)
            result.append(pair)
    return result


def _normalize_relation(relation: Sequence[Sequence[str]]) -> List[Pair]:
    normalized: List[Pair] = []
    for pair in relation:
        if len(pair) == 2 and not isinstance(pair, str):
            normalized.append((str(pair[0]), str(pair[1])))
        elif isinstance(pair, str) and len(pair) == 2:
            normalized.append((pair[0], pair[1]))
        elif len(pair) == 1 and len(pair[0]) == 2:
            normalized.append((pair[0][0], pair[0][1]))
        else:
            raise ValueError("Invalid relation pair format.")
    return normalized
