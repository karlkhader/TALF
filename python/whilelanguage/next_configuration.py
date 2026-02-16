"""
Next configuration of a given configuration for a WHILE program.

Example:
    >>> next_configuration("(1, X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od)", [1, 3, 0])
    [2, 3, 3]
"""

from __future__ import annotations

import re
from typing import List

from .go import go
from .line import line
from .size import size


def next_configuration(whileprogram: str, configuration: List[int]) -> List[int]:
    """Return the next configuration for a WHILE program."""
    ## get line and variables
    linenumber = configuration[0]
    variables = configuration[1:]

    ## get the code
    whilecode = whileprogram[whileprogram.find(",") + 1 : -1]

    if linenumber == size(whilecode) + 1:
        ## halting condition
        return configuration

    whileline, _ = line(whilecode, linenumber)
    if whileline.startswith("w"):
        ## while head
        ## get index of control variable (avoid the second number, the 0)
        index = int(re.findall(r"\d+", whileline)[0])
        if variables[index - 1] != 0:
            ## the condition verifies
            next_line = linenumber + 1
            next_vars = variables
        else:
            ## the condition does not verify, go to tail + 1
            next_line = go(whilecode, linenumber)
            next_vars = variables
    elif whileline == "od":
        ## while tail, go to head
        next_line = go(whilecode, linenumber)
        next_vars = variables
    else:
        ## assignment
        next_line = linenumber + 1
        next_vars = variables[:]
        ## get index of control variable (avoid the second number, the 0)
        #numbers = re.findall(r"\d+", whileline)
        matches = list(re.finditer(r"\d+", whileline))
        numbers = [m.group() for m in matches]  # mismos strings que findall
        positions = [m.start() for m in matches]  # índices iniciales
        i = int(numbers[0])
        if len(numbers) < 2:
            ## Xi:=0
            next_vars[i - 1] = 0
        else:
            j = int(numbers[1])
            if len(numbers) == 2:
                ## Xi:=Xj
                next_vars[i - 1] = next_vars[j - 1]
            else:
                ## Xi:=Xj+1 or Xi:=Xj-1 / get the sign and put everything in a string
                #assignment_sign = whileline[whileline.find(numbers[1]) + len(numbers[1])]
                assignment_sign = whileline[positions[2]-1]
                ## make assignment, considering that 0 - 1 = 0
                delta = 1 if assignment_sign == "+" else -1
                next_vars[i - 1] = max(next_vars[j - 1] + delta, 0)

    return [next_line, *next_vars]
