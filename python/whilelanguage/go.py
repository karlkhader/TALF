"""
Line number to interpret if not the next one in sequence.

Example:
    >>> go("X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od", 2)
    6
"""

from __future__ import annotations

import re
from typing import List, Tuple

from python.util import label_balanced_symbols
from .line import line


def go(whilecode: str, linenumber: int) -> int:
    """Return the balanced line number for a while head/tail or assignment."""
    normalized = whilecode.replace(";", "")
    normalized = normalized.replace(" ", "")
    normalized = normalized.replace("≔", ":=").replace("≠", "!=")

    _line, start1 = line(normalized, linenumber)
    start2, label = label_balanced_symbols(normalized, "while", "od")

    try:
        position = start2.index(start1)
    except ValueError:
        return 0

    if label[position] > 0:
        headtailmatch = [idx for idx, value in enumerate(label) if value == -label[position]]
        charposition = start2[next(idx for idx in headtailmatch if idx > position)]
        shift_lines = 1
    else:
        headtailmatch = [idx for idx, value in enumerate(label) if value == -label[position]]
        charposition = start2[max(idx for idx in headtailmatch if idx < position)]
        shift_lines = 0

    balanced_line_number = 0
    while True:
        balanced_line_number += 1
        _whileline, lineposition = line(whilecode, balanced_line_number)
        if lineposition == charposition:
            break

    return balanced_line_number + shift_lines
