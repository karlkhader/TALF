"""
Biyection ℕ -> ℕ*
godeldecoding(z, k) returns the kth element of the tuple encoded by z
godeldecoding(z, 0) returns the length of the tuple encoded by z
godeldecoding(z)    returns the tuple encoded by z

example
  >> godeldecoding(1258489)
  ans =

     2    2   43

Example:
    >>> godeldecoding(1258489)
    [2, 2, 43]
"""

from __future__ import annotations

from typing import List

from .cantordecoding import cantordecoding


def godeldecoding(z: int, k: int | None = None):
    """Decode a Gödel number into the kth element or full vector."""
    ## length of the encoded vector
    if z == 0:
        vectorlength = 0
    else:
        vectorlength = cantordecoding(z - 1, 2, 1) + 1

    ## case of returning the length of the encoded vector
    if k == 0:
        return vectorlength

    ## case of returning an element, or the whole vector
    if vectorlength == 0:
        ## N^0
        vector: List[int] = []
    else:
        ## N^k, k>0
        ## Cantor number of the vector
        z = cantordecoding(z - 1, 2, 2)
        if k is not None:
            ## kth element
            return cantordecoding(z, vectorlength, k)
        ## return the vector
        vector = [cantordecoding(z, vectorlength, i + 1) for i in range(vectorlength)]

    return vector
