"""
Right-hand side of an encoded instruction

example
  >> sent2N("while X1≠0 do X1≔X1-1; X2≔X2+1 od")
  ans =  9325236374
  >> rhs(9325236374)
  ans =  61073
  >> N2CODE(61073)
  ans = X1≔X1-1; X2≔X2+1

  >> sent2N("X3≔X2+1")
  ans =  37
  >> rhs(37)
  ans =  2

Example:
    >>> rhs(37)
    2
"""

from __future__ import annotations

from .cantordecoding import cantordecoding
from .senttype import senttype


def rhs(z: int) -> int:
    """Return the right-hand side of an encoded instruction."""
    ## type of sentence
    sentence_type = senttype(z)

    if sentence_type == 4:
        ## while Xi≠0 do b od
        return cantordecoding((z - sentence_type) // 5, 2, 2)
    else:
        ## Xi≔Xj
        ## Xi≔Xj+1
        ## Xi≔Xj-1
        return cantordecoding((z - sentence_type) // 5, 2, 2) + 1
