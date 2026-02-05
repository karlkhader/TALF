"""
Generate a rule of a given type.

Examples:
    >>> make_rule(2)
    >>> make_rule(0, N="ABC", T="01")
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, Tuple

from python.util import random_string
from .rule_type import RuleType, rule_type


@dataclass
class Rule:
    side: Tuple[str, str]
    type: RuleType


def make_rule(
    type_rule: int,
    N: Iterable[str] | None = None,
    T: Iterable[str] | None = None,
    show_rule: bool = True,
) -> Rule:
    """Return a rule of the given type (0..3)."""
    separator = "->"
    epsilon = "ε"

    if N is None:
        N = [chr(code) for code in range(ord("A"), ord("G") + 1)]
    if T is None:
        T = [chr(code) for code in range(ord("a"), ord("g") + 1)]

    N_str = "".join(N)
    T_str = "".join(T)

    if type_rule == 1:
        alpha = random_string("V*", N_str, T_str)
        beta = random_string("V*", N_str, T_str)
        alpha = "" if alpha == epsilon else alpha
        beta = "" if beta == epsilon else beta
        left = f"{alpha}{random_string('N', N_str, T_str)}{beta}"
        right = f"{alpha}{random_string('V+', N_str, T_str)}{beta}"
        current_rule = Rule(side=(left, right), type=rule_type([left, right], N_str, T_str))
    else:
        while True:
            left = random_string("V+", N_str, T_str)
            right = random_string("V*", N_str, T_str)
            current_type = rule_type([left, right], N_str, T_str)
            if current_type.number == type_rule:
                current_rule = Rule(side=(left, right), type=current_type)
                break

    if show_rule:
        print(
            f"type {current_rule.type.number} - {current_rule.type.name}: "
            f"{current_rule.side[0]} {separator} {current_rule.side[1]}"
        )

    return current_rule
