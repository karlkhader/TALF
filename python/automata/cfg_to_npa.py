"""Convert a context-free grammar (CFG) to a nondeterministic PDA."""

from __future__ import annotations

from typing import Dict, List, Sequence


Grammar = Dict[str, object]
Automaton = Dict[str, object]


def cfg_to_npa(grammar: Grammar) -> Automaton:
    """
    Build a nondeterministic pushdown automaton from a CFG description.

    Expected grammar keys: N (non-terminals), T (terminals), P (productions), S (start).
    """
    for key in ("N", "T", "P", "S"):
        if key not in grammar:
            raise ValueError(f"Grammar missing required key '{key}'.")

    automaton: Automaton = {
        "K": ["q0", "q1"],
        "I": list(grammar["T"]),
        "S": list(grammar["T"]) + list(grammar["N"]),
        "s": "q0",
        "F": ["q1"],
        "t": [],
    }

    # Initial transition pushes the start symbol.
    automaton["t"].append([["q0", "ε", "ε"], ["q1", grammar["S"]]])

    for rule in grammar["P"]:
        head = rule[0]
        body = rule[1]
        automaton["t"].append([["q1", "ε", head], ["q1", body]])

    for symbol in grammar["T"]:
        automaton["t"].append([["q1", symbol, symbol], ["q1", "ε"]])

    return automaton
