"""
Gödel numbering for vectors of numbers (ℕ* -> ℕ).

Example:
    >>> godelencoding(4, 10, 2)
    23863684
"""

from __future__ import annotations

from .cantorencoding import cantorencoding


def godelencoding(*args: int) -> int:
    """Encode a vector of numbers using Gödel numbering."""
    if len(args) == 0:
        return 0
    return int(cantorencoding(len(args) - 1, cantorencoding(*args)) + 1)
