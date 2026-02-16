"""
A line in a While code.

Example:
    >>> line("X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od", 3)
    'X1≔X1+1'
"""

from __future__ import annotations

import re
from typing import Tuple


def line(whilecode: str, linenumber: int) -> Tuple[str, int]:
    """Return the line at the given position and its starting character index."""
    ## delete ;
    normalized = whilecode.replace(";", "")
    ## delete spaces
    normalized = normalized.replace(" ", "")
    ## replace ≔ with :=
    normalized = normalized.replace("≔", ":=")
    ## replace ≠ with !=
    normalized = normalized.replace("≠", "!=")

    ## find line separators, beginning and end
    separators = sorted(
        [
            *[m.start() + 1 for m in re.finditer(r"X\d+:=", normalized)],
            *[m.start() + 1 for m in re.finditer(r"while", normalized)],
            *[m.start() + 1 for m in re.finditer(r"od", normalized)],
            len(normalized) + 1,
        ]
    )

    ## extract line
    start = separators[linenumber - 1]
    end = separators[linenumber]
    whileline = normalized[start - 1 : end - 1].strip()

    ## return separator corrected by the spaces to the next instruction (add blank spaces)
    trimmed_index = start + next(
        (idx for idx, char in enumerate(normalized[start - 1 :]) if not char.isspace()), 0
    )

    return whileline, trimmed_index
