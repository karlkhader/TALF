"""
Generate a random grammar of a given type.

Examples:
    >>> make_grammar(2)
    >>> make_grammar(0, N="ABC", T="01")
"""

from __future__ import annotations

import random
from typing import Dict, Iterable, List

from .make_rule import make_rule

Grammar = Dict[str, object]


def make_grammar(type_grammar: int, N: Iterable[str] | None = None, T: Iterable[str] | None = None) -> Grammar:
    """Make a grammar of a given type (0..3)."""
    max_rules = 5

    if N is None:
        N = [chr(code) for code in range(ord("A"), ord("G") + 1)]
    if T is None:
        T = [chr(code) for code in range(ord("a"), ord("g") + 1)]

    N_list = list(N)
    T_list = list(T)

    while True:
        count = max(1, int(random.random() * max_rules) + 1)
        ruletypes = [int(random.random() * (3 - type_grammar + 1)) + type_grammar for _ in range(count)]
        if type_grammar in ruletypes:
            break

    type3 = None
    if type_grammar == 3:
        type3 = "right-regular" if random.random() < 0.5 else "left-regular"

    rules: List[List[str]] = []
    for rule_type_value in ruletypes:
        while True:
            rule = make_rule(rule_type_value, N=N_list, T=T_list, show_rule=False)
            if type_grammar == 3 and rule.type.name not in {type3, "terminal-regular"}:
                continue
            if not any(existing[0] == rule.side[0] and existing[1] == rule.side[1] for existing in rules):
                rules.append([rule.side[0], rule.side[1]])
                break

    grammar: Grammar = {
        "N": N_list,
        "T": T_list,
        "P": rules,
        "S": random.choice(N_list),
    }

    _pretty_print_grammar(grammar, type_grammar)

    return grammar


def _pretty_print_grammar(grammar: Grammar, type_grammar: int) -> None:
    print(f"type {type_grammar}: (", end="")
    print("{", end="")
    print(", ".join(grammar["N"]), end="")
    print("}, ", end="")
    print("{", end="")
    print(", ".join(grammar["T"]), end="")
    print("}, ", end="")
    print("{", end="")
    for idx, rule in enumerate(grammar["P"]):
        separator = ", " if idx < len(grammar["P"]) - 1 else ""
        print(f"({rule[0]}, {rule[1]}){separator}", end="")
    print("}", end="")
    print(f", {grammar['S']})")
