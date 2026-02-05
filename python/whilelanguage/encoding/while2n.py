"""
Numbering of WHILE programs (WHILE -> ℕ).

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
    identifiers = [int(match.group(0)) for match in re.finditer(r"X\d+(?=(;|=|!|:|$))", whilecode)]
    _ = identifiers
    return cantorencoding(n, code2n(whilecode))
