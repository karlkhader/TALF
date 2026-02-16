"""
cantordecoding(z, n, k) returns the kth element of the n-tuple encoded by z
cantordecoding(z, n)    returns the n-tuple encoded by z

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
        ## N -> N
        vector = [z]
    elif n == 2:
        ## N^2 -> N
        ## diagonal where the pair is sitting
        diagonal = int(math.floor((math.sqrt(8 * z + 1) - 1) / 2))
        ## the second element is the distance to the beginning of the diagonal
        ##   cantorencoding(diagonal, 0)) = diagonal * (diagonal + 1) / 2
        element2 = z - diagonal * (diagonal + 1) / 2
        ## first element
        element1 = diagonal - element2
        ## diagonal = first element + second element
        vector = [int(element1), int(element2)]
    else:
        ## N^k -> N, k > 2
        vector = [0] * n
        current = z
        for idelement in range(n - 1, 0, -1):
            ## at each level, z encodes a pair of numbers
            pair = cantordecoding(current, 2)
            ## the first element of a pair decodes the elements of the vector
            vector[idelement] = pair[1]
            ## the second element of the pair encodes the rest of the vector
            current = pair[0]
        ## the second element of the pair decodes the last element of the vector
        vector[0] = current

    if k is None:
        ## vector as output
        return vector
    else:
        ## element as output
        return vector[k - 1]
