"""
Check the type of a rule, given in the form of a list of two strings.
Optionally, non-terminal and terminal alphabets can be provided as arguments.

Examples:
    >>> rule = rule_type(['A','BC'])
    >>> rule = rule_type(['BA1','110'], N='AB', T='01')
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
        # non-terminal alphabet
        N = [chr(code) for code in range(ord("A"), ord("G") + 1)]
    if T is None:
        # terminal alphabet
        T = [chr(code) for code in range(ord("a"), ord("g") + 1)]

    N_set = set(N)
    T_set = set(T)
    # union of terminals and non-terminals
    V_set = N_set | T_set

    # return variable is a struct, default value is type 0
    left, right = rule
    rule_type_result = RuleType(number=0, name="phrase structure")

    if right == epsilon:
        # case of type 0 epsilon rule
        return rule_type_result

    if len(left) == 1 and left in N_set:
        # leftside is a non-terminal, so type 2 or 3
        if len(right) == 1 and right in T_set:
            return RuleType(number=3, name="terminal-regular")
        if len(right) == 2:
            # it might be left-regular or right regular
            if right[0] in T_set and right[1] in N_set:
                # terminal and non-terminal
                return RuleType(number=3, name="left-regular")
            if right[0] in N_set and right[1] in T_set:
                # non-terminal and terminal
                return RuleType(number=3, name="right-regular")
            # two non-terminals
            return RuleType(number=2, name="context free")
        if all(symbol in V_set for symbol in right):
            # leftside has one non-terminal symbol and all symbols in righside are either terminals or non-terminals
            return RuleType(number=2, name="context free")
    else:
        # leftside has one non-terminal symbol and all symbols in righside are either terminals or non-terminals
        for index, symbol in enumerate(left):
            if symbol not in N_set:
                continue
            alpha = left[:index]
            beta = left[index + 1 :]
            # check if the context is kept
            if len(right) > len(alpha) + len(beta) and right.startswith(alpha) and right.endswith(beta):
                # check that nonterminal is not rewritten by the empty string
                if right != f"{alpha}{beta}":
                    # a context that is kept has been found
                    return RuleType(number=1, name="context sensitive")

    return rule_type_result
