"""
Gödel decoding for vectors of numbers.

Example:
    >>> godeldecoding(1258489)
    [2, 2, 43]
"""

from __future__ import annotations

from typing import List

from .cantordecoding import cantordecoding


def godeldecoding(z: int, k: int | None = None):
    """Decode a Gödel number into the kth element or full vector."""
    if z == 0:
        vectorlength = 0
    else:
        vectorlength = cantordecoding(z - 1, 2, 1) + 1

    if k == 0:
        return vectorlength

    if vectorlength == 0:
        vector: List[int] = []
    else:
        z = cantordecoding(z - 1, 2, 2)
        if k is not None:
            return cantordecoding(z, vectorlength, k)
        vector = [cantordecoding(z, vectorlength, i + 1) for i in range(vectorlength)]

    return vector
