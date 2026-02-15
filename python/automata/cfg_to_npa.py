"""Convert a context-free grammar (CFG) to a nondeterministic PDA.

Finds an NPA equivalent to a given CFG.


For example:

   >> finiteautomaton("aa*bb*", "ab")

   M = ( {q0, q1, q2}, {a, b}, {(q0, a, q1), (q1, a, q1), (q1, b, q2), (q2, b, q2)}, q0, {q0, q1, q2} )

   w = ab

   (q0, ab) ⊢ (q1, b) ⊢ (q2, ε)

   w ∈ 𝓛(M)

   >> finiteautomaton("aa*bb*", "ab", "LaTeX")
"""

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

    # STATES
    # STRING ALPHABET
    # STACK ALPHABET
    # INITIAL STATE
    # FINAL STATE
    # TRANSITION RELATION
    # Initial transition pushes the start symbol.
    automaton["t"].append([["q0", "ε", "ε"], ["q1", grammar["S"]]])

    for rule in grammar["P"]:
        head = rule[0]
        body = rule[1]
        automaton["t"].append([["q1", "ε", head], ["q1", body]])

    for symbol in grammar["T"]:
        automaton["t"].append([["q1", symbol, symbol], ["q1", "ε"]])

    return automaton
