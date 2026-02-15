"""
Numbering of while programs (WHILE -> ℕ)

example
  >> WHILE2N(1, "while X1≠0 do X1≔0 od")
  ans = 134

Example:
    >>> while2n(1, "while X1≠0 do X1≔0 od")
    134
"""

from __future__ import annotations

import re

from .cantorencoding import cantorencoding
from .code2n import code2n


def while2n(n: int, whilecode: str) -> int:
    """Encode a WHILE program into a number."""
    whilecode = whilecode.replace(" ", "")
    ## identify the number of each variable
    ## extract the variable in its context (X, followed by digits, followed by ; or ≔ or ≠ or end of string)
    identifiers = [int(match.group(0)) for match in re.finditer(r"X\d+(?=(;|=|!|:|$))", whilecode)]
    _ = identifiers

    ## encode the while program
    return cantorencoding(n, code2n(whilecode))
