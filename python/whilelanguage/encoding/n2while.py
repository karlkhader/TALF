"""
Biyection ℕ -> WHILE

example
  >> N2WHILE(150)
  ans = (2, while X1≠0 do X1≔0 od)

Example:
    >>> n2while(150)
    '(2, while X1≠0 do X1≔0 od)'
"""

from __future__ import annotations

import re

from .cantordecoding import cantordecoding
from .n2code import n2code


def n2while(z: int) -> str:
    """Decode a WHILE program from its number."""
    code = n2code(cantordecoding(z, 2, 2))

    ## identify the number of each variable
    ## extract the variable in its context (X, followed by digits, followed by : or ; ... or end of string
    identifiers = [int(match.group(0)) for match in re.finditer(r"\d+", code)]
    _ = identifiers

    ## extract n
    n = cantordecoding(z, 2, 1)
    ## make while program
    return f"({n}, {code})"
