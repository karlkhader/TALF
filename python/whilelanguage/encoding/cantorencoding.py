"""
Cantor encoding for vectors of numbers.

Example:
    >>> cantorencoding(3, 1, 2, 1)
    5566
"""

from __future__ import annotations


def cantorencoding(*args: int) -> int:
    """Encode a vector of numbers using Cantor pairing."""
    if len(args) == 1:
        return int(args[0])
    if len(args) == 2:
        x, y = args
        return int((x + y) * (x + y + 1) / 2 + y)

    return cantorencoding(cantorencoding(*args[:-1]), args[-1])
