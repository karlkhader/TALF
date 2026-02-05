"""
Bijection ℕ -> CODE.

Example:
    >>> n2code(4)
    'X1≔X1; X1≔0'
"""

from __future__ import annotations

from .godeldecoding import godeldecoding


def n2code(z: int) -> str:
    """Decode a WHILE code from its numeric encoding."""
    from .n2sent import n2sent
    z = z + 1
    sentence = godeldecoding(z)
    code = n2sent(sentence[0])
    for element in sentence[1:]:
        code = f"{code}; {n2sent(element)}"
    return code
