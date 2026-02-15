"""
Godel numbering for vectors of numbers of arbitrary length (ℕ* -> ℕ)

example
  >> godelencoding(4, 10, 2)
  ans =  6674029

Example:
    >>> godelencoding(4, 10, 2)
    23863684
"""

from __future__ import annotations

from .cantorencoding import cantorencoding


def godelencoding(*args: int) -> int:
    """Encode a vector of numbers using Gödel numbering."""
    if len(args) == 0:
        ## case of empty vector
        return 0
    else:
        ## length of the vector plus Cantor encoding of the vector
        return int(cantorencoding(len(args) - 1, cantorencoding(*args)) + 1)
