"""
Right-hand side of an encoded instruction.

Example:
    >>> rhs(37)
    2
"""

from __future__ import annotations

from .cantordecoding import cantordecoding
from .senttype import senttype


def rhs(z: int) -> int:
    """Return the right-hand side of an encoded instruction."""
    sentence_type = senttype(z)
    if sentence_type == 4:
        return cantordecoding((z - sentence_type) // 5, 2, 2)
    return cantordecoding((z - sentence_type) // 5, 2, 2) + 1
