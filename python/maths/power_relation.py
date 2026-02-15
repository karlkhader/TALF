"""
Power n of a relation or its transitive closure.

## Power n of a relation R1, or its transitive closure (if n undefined)
##
## examples
##   power_relation([("a", "b"), ("c", "c"), ("b", "a")], 3)
##   {(a,b), (c,c), (b,a)}^3 = {(a,b), (b,a), (c,c)}
##
##   power_relation([("a", "b"), ("c", "c"), ("b", "a")]);
##   {(a,b), (c,c), (b,a)}^2 = {(a,a), (b,b), (c,c)}
##   {(a,b), (c,c), (b,a)} ∪ {(a,a), (b,b), (c,c)} = {(a,a), (a,b), (b,a), (b,b), (c,c)}
##   
##   {(a,b), (c,c), (b,a)}^3 = {(a,b), (b,a), (c,c)}
##   {(a,a), (a,b), (b,a), (b,b), (c,c)} ∪ {(a,b), (b,a), (c,c)} = {(a,a), (a,b), (b,a), (b,b), (c,c)}
##   
##   {(a,b), (c,c), (b,a)}^∞ = {(a,a), (a,b), (b,a), (b,b), (c,c)}
##   
##   Ordered pairs can also be formatted like this:
##   power_relation(["ab", "cc", "ba"]);
##
## 2023/01/31 version 0.1 - fjvico@uma.es  GNU GPL v3.0
## 2018/09/29 version 0.0 - fjvico@uma.es  GNU GPL v3.0

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
        ## case of finite exponent (R^n)
        
        ## store the input R1 as a cell array, and further powers likewise
        powers: List[List[Pair]] = [original]
        for _ in range(2, n + 1):
            previous = powers[-1]
            current: List[Pair] = []
            ## browser all pairs in the previous power relation
            for left1, right1 in previous:
                ## search for pairs in the original relation
                for left2, right2 in original:
                    if right1 == left2:
                        ## add a new element
                        current.append((left1, right2))
            powers.append(current)

        ## return last power
        ## remove repetitions, in any
        relation_n = _unique_pairs(powers[-1])
        pretty_print_relation(original)
        print(f"{exponent_symbol}{n} = ", end="")
        pretty_print_relation(relation_n, newline=True)
        return relation_n

    ## case of transitive closure (R1^∞)
    exponent = 1
    current_relation = original
    while True:
        ## increase exponent
        exponent += 1
        previous_relation = current_relation
        ## compute power n and add
        current_relation = union_relation(current_relation, power_relation(original, exponent))
        # character U+2001 (Em Quad) allows an empty line between printed powers
        print("\n\u2001\n")
        if _unique_pairs(previous_relation) == _unique_pairs(current_relation):
            break

    ## return the result of the union
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
