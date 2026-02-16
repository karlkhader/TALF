"""
Left-hand side of an encoded instruction

example
  >>> z = sent2n("while X1≠0 do X1≔X1-1; X2≔X2+1 od")
  >>> z
  9325236374
  >>> lhs(9325236374)
  1

  >>> sent2n("X3≔X2+1")
  37
  >>> lhs(37)
  3

Example:
    >>> lhs(37)
    3
"""

from __future__ import annotations

from .cantordecoding import cantordecoding
from .senttype import senttype


def lhs(z: int) -> int:
    """Return the left-hand side of an encoded instruction."""
    ## type of sentence
    sentence_type = senttype(z)

    if sentence_type == 0:
        ## Xi≔0
        return int(z / 5 + 1)
    else:
        ## Xi≔Xj
        ## Xi≔Xj+1
        ## Xi≔Xj-1
        ## while
        return cantordecoding((z - sentence_type) // 5, 2, 1) + 1
