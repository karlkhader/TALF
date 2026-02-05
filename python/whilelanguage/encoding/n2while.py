"""
Bijection ℕ -> WHILE.

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
    identifiers = [int(match.group(0)) for match in re.finditer(r"\d+", code)]
    _ = identifiers
    n = cantordecoding(z, 2, 1)
    return f"({n}, {code})"
