"""
randomturingmachine(numberstates, alphabet, emptysymbol, randomseed)

Generates a table for a random Turing Machine

Examples:
    >>> random_turingmachine(2, "|")
    [[q0, *, h, q1],
     [q0, |, |, q1],
     [q1, *, |, q1],
     [q1, |, *, q0]]

    >>> turing_machine(random_turingmachine(3, "|"), "*")
    q0 * r q2
    q0 | l q1
    q1 * r q0
    q1 | | q0
    q2 * | q1
    q2 | h q1
    
    (q0, *, 1) ⊢ (q2, **, 2) ⊢ (q1, *|*, 2) ⊢ (q0, *|*, 2) ⊢ (q1, *|*, 1) ⊢ (q0, *|*, 2) ...

    >>> savejson("matrix", random_turingmachine(2, "|"), "test.json")
    >>> turing_machine("test", "*|||*")
"""

from __future__ import annotations

import random
from typing import List


def random_turingmachine(
    numberstates: int,
    alphabet: str,
    emptysymbol: str = "*",
    randomseed: int | None = None,
) -> List[List[str]]:
    """Generate a random Turing machine transition matrix."""
    if randomseed is not None:
        random.seed(randomseed)

    ## define the empty symbol
    
    ## add empty symbol to the alphabet
    alphabet = f"{emptysymbol}{alphabet}"

    ## create table
    matrix: List[List[str]] = []
    for state_index in range(numberstates):
        state = f"q{state_index}"
        for symbol in alphabet:
            matrix.append([state, symbol, _make_instruction(alphabet), _make_state(numberstates)])

    return matrix


def _make_instruction(alphabet: str) -> str:
    ## random instruction
    return random.choice(f"hlr{alphabet}")


def _make_state(numberstates: int) -> str:
    ## random state
    return f"q{random.randrange(numberstates)}"
