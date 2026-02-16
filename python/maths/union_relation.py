"""
Union of two relations.

## Union of two relations
##
## examples
##   {(a, b), (c, c)} ∪ {(b, a)}
##   union_relation([("a", "b"), ("c", "c")], [("b", "a")])

Examples:
    >>> union_relation([("a", "b"), ("c", "c")], [("b", "a")])
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from .pretty_print_relation import pretty_print_relation

Pair = Tuple[str, str]


def union_relation(relation1: Sequence[Sequence[str]], relation2: Sequence[Sequence[str]]) -> List[Pair]:
    """Return the union of two relations and print the formatted output."""
    union_symbol = " ∪ "
    result: List[Pair] = []

    seen = set()
    for pair in list(relation1) + list(relation2):
        left, right = _normalize_pair(pair)
        ## this element is already in result, skip
        if (left, right) not in seen:
            seen.add((left, right))
            ## add element if not already in result
            result.append((left, right))

    ## remove repetitions, if any
    pretty_print_relation(relation1)
    print(union_symbol, end="")
    pretty_print_relation(relation2)
    print(" = ", end="")
    pretty_print_relation(result, newline=True)

    return result


def _normalize_pair(pair: Sequence[str]) -> Pair:
    if len(pair) == 2:
        return str(pair[0]), str(pair[1])
    if len(pair) == 1 and len(pair[0]) == 2:
        return pair[0][0], pair[0][1]
    if len(pair) == 2 and isinstance(pair, str):
        return pair[0], pair[1]
    raise ValueError("Invalid relation pair format.")
