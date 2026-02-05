"""
Build the "egg" Turing machine representation.

Example:
    >>> build_egg()
"""

from __future__ import annotations

from typing import Dict, List


DEFAULT_BINARYSTRING = "1100110001001100000001000101101010010010001100101010001001100010"


def build_egg(binarystring: str = DEFAULT_BINARYSTRING) -> Dict[str, object]:
    """Return the JSON representation for the egg Turing machine."""
    matrix: List[List[str]] = []
    count = 0
    for bit in binarystring:
        count += 1
        matrix.append([f"q{count}", "*", "l", f"q{count}"])
        matrix.append([f"q{count}", "0", "l", f"q{count + 1}"])
        if bit == "1":
            matrix.append([f"q{count}", "1", "l", f"q{count + 1}"])
        else:
            matrix.append([f"q{count}", "1", "0", f"q{count}"])

    count += 1
    matrix.append([f"q{count}", "*", "h", f"q{count}"])
    matrix.append([f"q{count}", "0", "h", f"q{count + 1}"])
    matrix.append([f"q{count}", "1", "h", f"q{count + 1}"])

    return {
        "name": "egg",
        "representation": {"matrix": matrix},
    }
