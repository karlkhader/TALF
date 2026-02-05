"""
Mathematical function computed by a WHILE program (emulated).

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
    if not whileprogram.startswith("("):
        whileprogram = load_representation("software/Whilelanguage/Whileprograms", whileprogram)
        if whileprogram is None:
            raise ValueError("While program not found in database.")

    numbers = re.findall(r"\d+", whileprogram)
    n = int(numbers[0])
    if n != len(args):
        raise ValueError("Function's arity must match the number of arguments...")

    code = whileprogram.split(",", 1)[1].strip()
    code = code.strip("()")

    code = code.replace("≔", "=")
    code = code.replace(":=", "=")
    code = code.replace("≠0", "!=0 ")
    code = code.replace("while", "while ")
    code = code.replace("do", "")
    code = code.replace("od", ";")

    code = _macrosentence_rep(code)

    for index, value in enumerate(args, start=1):
        code = f"X{index}={value};" + code

    locals_dict = {"X1": 0, "X2": 0, "X3": 0}
    exec(_to_python(code), {}, locals_dict)

    return locals_dict.get("X1", 0)


def _macrosentence_rep(code: str) -> str:
    """Add f_emulation to macro sentence calls."""
    positions = [m.start() for m in re.finditer(r"\(", code)]
    for start in reversed(positions):
        prefix = code[:start]
        assign_index = prefix.rfind("=")
        if assign_index == -1:
            continue
        name = code[assign_index + 1 : start]
        code = f"{code[:assign_index]}f_emulation('{name}', {code[start+1:]}"
    return code


def _to_python(code: str) -> str:
    """Translate simplified WHILE code to Python syntax."""
    # Convert statement separators
    lines = [segment.strip() for segment in code.split(";") if segment.strip()]
    python_lines: List[str] = []
    indent = 0
    for segment in lines:
        if segment.startswith("while"):
            python_lines.append("    " * indent + segment + ":")
            indent += 1
        else:
            python_lines.append("    " * indent + segment)
    return "\n".join(python_lines)
