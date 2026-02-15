"""
Numbering of an individual sentence

example
  >> N2sent(192509)
  ans =  while X2=0 do X2≔X2+1 od

Example:
    >>> n2sent(192509)
    'while X2=0 do X2≔X2+1 od'
"""

from __future__ import annotations

from .lhs import lhs
from .rhs import rhs
from .senttype import senttype


def n2sent(z: int) -> str:
    """Decode a sentence from its numeric encoding."""
    ## type of sentence
    sentence_type = senttype(z)

    if sentence_type == 0:
        ## Xi≔0
        return f"X{lhs(z)}≔0"
    if sentence_type == 1:
        ## Xi≔Xj
        return f"X{lhs(z)}≔X{rhs(z)}"
    if sentence_type == 2:
        ## Xi≔Xj+1
        return f"X{lhs(z)}≔X{rhs(z)}+1"
    if sentence_type == 3:
        ## Xi≔Xj-1
        return f"X{lhs(z)}≔X{rhs(z)}-1"
    if sentence_type == 4:
        from .n2code import n2code

        return f"while X{lhs(z)}≠0 do {n2code(rhs(z))} od"

    raise ValueError("Invalid sentence type.")
