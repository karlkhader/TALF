"""
Bijection ℕ -> CODE

example
  >>> n2code(4)
  'X1≔X1; X1≔0'

Example:
    >>> n2code(4)
    'X1≔X1; X1≔0'
"""

from __future__ import annotations

from .godeldecoding import godeldecoding


def n2code(z: int) -> str:
    """Decode a WHILE code from its numeric encoding."""
    from .n2sent import n2sent
    ## add 1 to discard an empty code
    z = z + 1
    ## extract the codes of the sentences
    sentence = godeldecoding(z)

    ## decode the sentences and add separators
    code = n2sent(sentence[0])
    for element in sentence[1:]:
        code = f"{code}; {n2sent(element)}"
    return code
