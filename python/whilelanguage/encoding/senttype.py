"""
Type of a sentence

example
  >>> z = sent2n("while X1=0 do X1≔X1-1; X2≔X2+1 od")
  >>> z
  9325236374
  >>> senttype(z)
  4

"""

from __future__ import annotations


def senttype(z: int) -> int:
    """Return the sentence type from module 5."""
    ## type of sentence from module 5
    return z % 5
