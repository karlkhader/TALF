"""
Cantor encoding for a vector of numbers of a given length:
   cantorenconding(x_1, ..., x_n)

example
  >> cantorencoding(3, 1, 2, 1)
  ans =  5566

Example:
    >>> cantorencoding(3, 1, 2, 1)
    5566
"""

from __future__ import annotations


def cantorencoding(*args: int) -> int:
    """Encode a vector of numbers using Cantor pairing."""
    if len(args) == 1:
        ## case of N
        return int(args[0])
    if len(args) == 2:
        ## case of N^2
        x, y = args
        return int((x + y) * (x + y + 1) / 2 + y)

    ## recursive case of N^p, p > 2
    ## vectors are encoded from left to right
    ## convert to unsigned integer of 64 bits
    return cantorencoding(cantorencoding(*args[:-1]), args[-1])
