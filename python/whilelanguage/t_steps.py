"""
Temporal complexity of a WHILE program.

Example:
    >>> t_steps("(1, X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od)", [3])
    14
"""

from __future__ import annotations

from typing import List

from .cal import cal
from .next_configuration import next_configuration
from .size import size


def t_steps(whileprogram: str, inputvariables: List[int]) -> int:
    """Return the number of steps until the program halts."""
    time_to_check = 1000
    steps = 0
    halting_line = size(whileprogram) + 1
    configuration = cal(whileprogram, inputvariables, 0)

    while configuration[0] != halting_line:
        steps += 1
        if steps % time_to_check == 0:
            # In Octave this pauses for user input; here we just continue.
            pass
        configuration = next_configuration(whileprogram, configuration)

    return steps
