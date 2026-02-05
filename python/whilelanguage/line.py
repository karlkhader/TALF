"""
Return a line in a WHILE code.

Example:
    >>> line("X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od", 3)
    'X1≔X1+1'
"""

from __future__ import annotations

import re
from typing import Tuple


def line(whilecode: str, linenumber: int) -> Tuple[str, int]:
    """Return the line at the given position and its starting character index."""
    normalized = whilecode.replace(";", "")
    normalized = normalized.replace(" ", "")
    normalized = normalized.replace("≔", ":=")
    normalized = normalized.replace("≠", "!=")

    separators = sorted(
        [
            *[m.start() + 1 for m in re.finditer(r"X\d+:=", normalized)],
            *[m.start() + 1 for m in re.finditer(r"while", normalized)],
            *[m.start() + 1 for m in re.finditer(r"od", normalized)],
            len(normalized) + 1,
        ]
    )

    start = separators[linenumber - 1]
    end = separators[linenumber]
    whileline = normalized[start - 1 : end - 1].strip()

    trimmed_index = start + next(
        (idx for idx, char in enumerate(normalized[start - 1 :]) if not char.isspace()), 0
    )

    return whileline, trimmed_index
