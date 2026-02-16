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
    ## remove non-ASCII characters to avoid shifts
    normalized = whilecode.replace(";", "")
    normalized = normalized.replace(" ", "")
    normalized = normalized.replace("≔", ":=").replace("≠", "!=")

    ## get the line
    _line, start1 = line(normalized, linenumber)
    ## balance heads and tails
    start2, label = label_balanced_symbols(normalized, "while", "od")

    ## find the relative position of that line
    try:
        position = start2.index(start1)
    except ValueError:
        ## case of an assignment
        return 0

    ## find the balanced head or tail
    if label[position] > 0:
        ## case of a while head
        headtailmatch = [idx for idx, value in enumerate(label) if value == -label[position]]
        charposition = start2[next(idx for idx in headtailmatch if idx > position)]
        shift_lines = 1
    else:
        ## case of a while tail
        headtailmatch = [idx for idx, value in enumerate(label) if value == -label[position]]
        charposition = start2[max(idx for idx in headtailmatch if idx < position)]
        shift_lines = 0

    ## search for the line starting in that character
    balanced_line_number = 0
    while True:
        balanced_line_number += 1
        _whileline, lineposition = line(whilecode, balanced_line_number)
        if lineposition == charposition:
            break

    ## add one more line in case of a head
    return balanced_line_number + shift_lines
