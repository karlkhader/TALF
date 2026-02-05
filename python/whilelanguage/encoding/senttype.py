"""
Type of a sentence.

Example:
    >>> senttype(9325236374)
    4
"""

from __future__ import annotations


def senttype(z: int) -> int:
    """Return the sentence type from module 5."""
    return z % 5
