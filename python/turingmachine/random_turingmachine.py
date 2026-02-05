"""
Generate a random Turing machine.

Examples:
    >>> random_turingmachine(2, "|")
    >>> turing_machine(random_turingmachine(3, "|"), "*")
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

    alphabet = f"{emptysymbol}{alphabet}"

    matrix: List[List[str]] = []
    for state_index in range(numberstates):
        state = f"q{state_index}"
        for symbol in alphabet:
            matrix.append([state, symbol, _make_instruction(alphabet), _make_state(numberstates)])

    return matrix


def _make_instruction(alphabet: str) -> str:
    return random.choice(f"hlr{alphabet}")


def _make_state(numberstates: int) -> str:
    return f"q{random.randrange(numberstates)}"
