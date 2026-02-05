"""
Determine the type of a grammar rule.

Examples:
    >>> rule_type(["A", "BC"])
    >>> rule_type(["BA1", "110"], N="AB", T="01")
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass
class RuleType:
    number: int
    name: str


def rule_type(rule: Sequence[str], N: Iterable[str] | None = None, T: Iterable[str] | None = None) -> RuleType:
    """Return the type of a rule based on Chomsky hierarchy rules."""
    epsilon = "ε"
    if N is None:
        N = [chr(code) for code in range(ord("A"), ord("G") + 1)]
    if T is None:
        T = [chr(code) for code in range(ord("a"), ord("g") + 1)]

    N_set = set(N)
    T_set = set(T)
    V_set = N_set | T_set

    left, right = rule
    rule_type_result = RuleType(number=0, name="phrase structure")

    if right == epsilon:
        return rule_type_result

    if len(left) == 1 and left in N_set:
        if len(right) == 1 and right in T_set:
            return RuleType(number=3, name="terminal-regular")
        if len(right) == 2:
            if right[0] in T_set and right[1] in N_set:
                return RuleType(number=3, name="left-regular")
            if right[0] in N_set and right[1] in T_set:
                return RuleType(number=3, name="right-regular")
            return RuleType(number=2, name="context free")
        if all(symbol in V_set for symbol in right):
            return RuleType(number=2, name="context free")
    else:
        for index, symbol in enumerate(left):
            if symbol not in N_set:
                continue
            alpha = left[:index]
            beta = left[index + 1 :]
            if len(right) > len(alpha) + len(beta) and right.startswith(alpha) and right.endswith(beta):
                if right != f"{alpha}{beta}":
                    return RuleType(number=1, name="context sensitive")

    return rule_type_result
