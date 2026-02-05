"""
Pop the first instruction from a Gödel-encoded list.

Example:
    >>> pop(20)
    3
"""

from __future__ import annotations

from python.whilelanguage.encoding.godeldecoding import godeldecoding
from python.whilelanguage.encoding.godelencoding import godelencoding


def pop(value: int) -> int:
    """Return the Gödel encoding of a list without its first element."""
    x2 = 0
    x3 = 0
    x4 = 0

    x4 = value
    if x4 == 1:
        x2 = 0
    else:
        x2 = godelencoding(godeldecoding(value, 2))
        x4 -= 1
        x4 -= 1
        while x4 != 0:
            x2 = godelencoding(x2, godeldecoding(value, x3))
            x3 += 1
            x4 -= 1
    return x2
