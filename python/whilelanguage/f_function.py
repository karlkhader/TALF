"""
Mathematical function computed by a WHILE program.

In case of error in the WHILE code, it raises the wrong Octave code.

Example:
    >>> f_function("(1, X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od)", [10])
    20
"""

from __future__ import annotations

from typing import List

from .cal import cal
from .t_steps import t_steps


def f_function(whileprogram: str, inputvariables: List[int]) -> int:
    """Return the computed value of the WHILE program."""
    configuration = cal(whileprogram, inputvariables, t_steps(whileprogram, inputvariables))
    return configuration[1]
