"""
Mathematical function computed by a WHILE program.

In case of error in the WHILE code, it raises the wrong Octave code.

Examples:
    >>> f_emulation("(1, X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od)", 3)
    6
    >>> f_emulation("product", 3, 3)
    9
"""

from __future__ import annotations

import re
from typing import List

from python.util import load_representation


def f_emulation(whileprogram: str, *args: int) -> int:
    """Emulate a WHILE program by translating it into Python code."""
    ## check if the program is given explicitly or as a macrosentence
    if not whileprogram.startswith("("):
        ## case that the program is in the database
        whileprogram = load_representation("python/whilelanguage/Whileprograms", whileprogram)
        if whileprogram is None:
            raise ValueError("While program not found in database.")

    ## extract n
    ## extract all numbers
    numbers = re.findall(r"\d+", whileprogram)
    ## n is the first number
    n = int(numbers[0])
    ## check function arity
    if n != len(args):
        raise ValueError("Function's arity must match the number of arguments...")

    ## extract code
    code = whileprogram.split(",", 1)[1].strip()
    code = code.strip("()")

    ## translate WHILE code into a Python script
    code = code.replace("≔", "=")
    code = code.replace(":=", "=")
    code = code.replace("≠0", "!=0")
    code = code.replace("while", "while")
    code = code.replace("do ", ": ")
    code = code.replace("od", ";end;")

    code = _macrosentence_rep(code)

    ## assign initial values to input variables as new assignments
    for index, value in enumerate(args, start=1):
        code = f"X{index}={value};" + code

    ## variable initialization to avoid error from nested call to eval
    locals_dict = {"X1": 0, "X2": 0, "X3": 0}
    ## run Python script (simulate WHILE program with input variables)
    exec(_to_python(code), globals(), locals_dict)
    #exec(_to_python(code), {}, locals_dict)

    return locals_dict.get("X1", 0)


def _macrosentence_rep(code: str) -> str:
    ## add "f_emulation" to macrosentence calls
    ## e.g. replaces
    ##   X1 = addition(13, 8)
    ##   X1 = f_emulation("addition", 13, 8)
    """Add f_emulation to macro sentence calls."""
    positions = [m.start() for m in re.finditer(r"\(", code)]
    ## replace from the last call to the first, so the replacement does not interfere
    for start in reversed(positions):
        prefix = code[:start]
        assign_index = prefix.rfind("=")
        if assign_index == -1:
            continue
        name = code[assign_index + 1 : start]
        code = f"{code[:assign_index+1]}f_emulation('{name}',{code[start+1:]}"
    return code


def _to_python(code: str) -> str:
    """Translate simplified WHILE code to Python syntax."""
    # Convert statement separators
    lines = [segment.strip() for segment in code.split(";") if segment.strip()]
    python_lines: List[str] = []
    indent = 0
    for segment in lines:
        if segment.startswith("while"):
            divided_line = segment.split(" ")
            python_lines.append("    " * indent + " ".join(divided_line[:-1]))
            indent += 1
            python_lines.append("    " * indent + divided_line[-1])
        elif segment.startswith("end"):
            indent -= 1
        else:
            python_lines.append("    " * indent + segment)
    return "\n".join(python_lines)
