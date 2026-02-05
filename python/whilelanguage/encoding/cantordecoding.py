"""
Cantor decoding for vectors of numbers.

Example:
    >>> cantordecoding(313613413, 4)
    [1, 0, 10, 24967]
"""

from __future__ import annotations

import math
from typing import List


def cantordecoding(z: int, n: int, k: int | None = None):
    """Decode a Cantor-encoded number into the n-tuple, optionally returning element k."""
    if n < 1:
        raise ValueError("n must be >= 1")

    if n == 1:
        vector = [z]
    elif n == 2:
        diagonal = int(math.floor((math.sqrt(8 * z + 1) - 1) / 2))
        element2 = z - diagonal * (diagonal + 1) / 2
        element1 = diagonal - element2
        vector = [int(element1), int(element2)]
    else:
        vector = [0] * n
        current = z
        for idelement in range(n - 1, 0, -1):
            pair = cantordecoding(current, 2)
            vector[idelement] = pair[1]
            current = pair[0]
        vector[0] = current

    if k is None:
        return vector
    return vector[k - 1]
