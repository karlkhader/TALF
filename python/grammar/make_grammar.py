"""
Make a grammar of a given type (0..3).
Optionally, non-terminal and terminal alphabets can be provided as arguments.

Examples:
    >>> grammar = make_grammar(2)
    >>> grammar = make_grammar(0, N='ABC', T='01')
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
        # non-terminal alphabet
        N = [chr(code) for code in range(ord("A"), ord("G") + 1)]
    if T is None:
        # terminal alphabet
        T = [chr(code) for code in range(ord("a"), ord("g") + 1)]

    # alphabets
    N_list = list(N)
    T_list = list(T)

    # generate random rule types, make sure there is a rule of the lowest type
    while True:
        count = max(1, int(random.random() * max_rules) + 1)
        ruletypes = [int(random.random() * (3 - type_grammar + 1)) + type_grammar for _ in range(count)]
        if type_grammar in ruletypes:
            break

    # case of regular grammar
    type3 = None
    if type_grammar == 3:
        # chose a side, left or right
        type3 = "right-regular" if random.random() < 0.5 else "left-regular"

    # generate random rules
    rules: List[List[str]] = []
    for rule_type_value in ruletypes:
        while True:
            # case of regular grammar
            if type_grammar == 3:
                # make sure the rule fits that type
                rule = make_rule(rule_type_value, N=N_list, T=T_list, show_rule=False)
                if rule.type.name not in {type3, "terminal-regular"}:
                    continue
            else:
                # rules of types 0, 1 and 2
                rule = make_rule(rule_type_value, N=N_list, T=T_list, show_rule=False)
            
            # check if rule already exists
            if not any(existing[0] == rule.side[0] and existing[1] == rule.side[1] for existing in rules):
                rules.append([rule.side[0], rule.side[1]])
                break

    grammar: Grammar = {
        "N": N_list,
        "T": T_list,
        "P": rules,
        "S": random.choice(N_list),  # random axiom
    }

    _pretty_print_grammar(grammar, type_grammar)

    return grammar


def _pretty_print_grammar(grammar: Grammar, type_grammar: int) -> None:
    print(f"type {type_grammar}: (", end="")
    # print N
    print("{", end="")
    print(", ".join(grammar["N"]), end="")
    print("}, ", end="")
    # print T
    print("{", end="")
    print(", ".join(grammar["T"]), end="")
    print("}, ", end="")
    # print P
    print("{", end="")
    for idx, rule in enumerate(grammar["P"]):
        separator = ", " if idx < len(grammar["P"]) - 1 else ""
        print(f"({rule[0]}, {rule[1]}){separator}", end="")
    print("}", end="")
    # print S
    print(f", {grammar['S']})")
