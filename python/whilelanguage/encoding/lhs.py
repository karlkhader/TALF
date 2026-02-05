"""
Left-hand side of an encoded instruction.

Example:
    >>> lhs(37)
    3
"""

from __future__ import annotations

from .cantordecoding import cantordecoding
from .senttype import senttype


def lhs(z: int) -> int:
    """Return the left-hand side of an encoded instruction."""
    sentence_type = senttype(z)
    if sentence_type == 0:
        return int(z / 5 + 1)
    return cantordecoding((z - sentence_type) // 5, 2, 1) + 1
