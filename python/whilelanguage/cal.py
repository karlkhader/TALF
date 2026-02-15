"""
Configuration after a number of steps.

Example:
    >>> cal("(1, X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od)", 3, 1)
    [2, 3, 3]
"""

from __future__ import annotations

import re
from typing import List

from .next_configuration import next_configuration


def cal(whileprogram: str, inputvariables: int | List[int], steps: int) -> List[int]:
    """Return the configuration after a number of steps."""
    transition_symbol = "⊢"

    if isinstance(inputvariables, int):
        input_list = [inputvariables]
    else:
        input_list = list(inputvariables)

    if steps == 0:
        ## initial configuration
        ## find out the number of input variables
        numbers = re.findall(r"\d+", whileprogram)
        n = int(numbers[0])
        ## find out the total number of variables
        p = max(int(value) for value in numbers)
        configuration = [1, *input_list, *([0] * (p - n))]
        return configuration

    previous = cal(whileprogram, input_list, steps - 1)
    return next_configuration(whileprogram, previous)
