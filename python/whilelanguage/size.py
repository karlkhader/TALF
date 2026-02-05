"""
Number of lines of a WHILE program or code.

Example:
    >>> size("X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od")
    5
"""

from __future__ import annotations


def size(whileprogram: str) -> int:
    """Return the number of lines for a WHILE program or code string."""
    if whileprogram.startswith("("):
        whilecode = whileprogram[whileprogram.find(",") + 1 :]
        whilecode = whilecode[:-1] if whilecode.endswith(")") else whilecode
    else:
        whilecode = whileprogram

    whilecode = whilecode.replace(" ", "")
    whilecode = whilecode.replace("≔", ":=")
    whilecode = whilecode.replace("≠", "!=")

    assignment_matches = [m.start() for m in __import__("re").finditer(r"X\d+:=", whilecode)]
    while_matches = [m.start() for m in __import__("re").finditer(r"while", whilecode)]
    od_matches = [m.start() for m in __import__("re").finditer(r"od", whilecode)]
    return len([*assignment_matches, *while_matches, *od_matches])
