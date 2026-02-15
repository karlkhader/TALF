"""Generate a random string based on Octave's randomstring.m logic.

make a string according to a pattern ('N', 'T', 'V+', 'V*')
"""

from __future__ import annotations

import random
import string
from typing import Optional


def _symbol_to_set(symbol: str, middlesymbol: int = 13) -> str:
    """Map a symbol into a target set label (T, N, V+, V*)."""
    if symbol in string.ascii_lowercase[:middlesymbol]:
        # a, b, c, d
        return "T"
    if symbol in string.ascii_lowercase[middlesymbol:]:
        # w, x, y, z
        return "V*"
    if symbol in string.ascii_uppercase[:middlesymbol]:
        # A, B, C, D
        return "N"
    if symbol == "α":
        # α
        return "V+"
    # β, γ
    return "V*"


def random_string(
    targetset: str,
    non_terminals: str,
    terminals: str,
    *,
    max_string_length: int = 5,
    rng: Optional[random.Random] = None,
) -> str:
    """
    Return a random string using Octave's `randomstring.m` convention.

    Args:
        targetset: Target set label ("N", "T", "V+", "V*") or a symbol.
        non_terminals: Available non-terminal symbols.
        terminals: Available terminal symbols.
        max_string_length: Maximum length for generated strings.
        rng: Optional random generator (defaults to `random`).

    Returns:
        A generated string, using the epsilon symbol "ε" for empty strings.
    """
    rng = rng or random
    epsilon = "ε"
    # set of all terminal and non-terminal symbols
    alphabet = ""

    if targetset and targetset[0] not in "NTV":
        # set is given by a letter, instead
        targetset = _symbol_to_set(targetset)

    if targetset.startswith("T"):
        alphabet = terminals
    elif targetset.startswith("N"):
        alphabet = non_terminals
    elif targetset.startswith("V"):
        alphabet = f"{non_terminals}{terminals}"

    # determine output length
    if len(targetset) == 1:
        string_length = 1
    elif len(targetset) > 1 and targetset[1] == "+":
        # empty string is not allowed
        string_length = rng.randint(1, max_string_length)
    else:
        # empty string is allowed
        string_length = rng.randint(0, max_string_length)

    if string_length == 0:
        # empty string
        return epsilon
    if not alphabet:
        raise ValueError("Alphabet is empty; cannot generate a non-empty string.")

    # non-empty string
    return "".join(rng.choice(alphabet) for _ in range(string_length))
