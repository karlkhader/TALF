"""
Evaluate a recursive function.

Examples:
    >>> eval_rec_function('addition', 3, 2)
    >>> eval_rec_function('division', 4, 2)
    >>> eval_rec_function('<theta|pi^2_2>', 2)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List

from python.util import label_balanced_symbols


def eval_rec_function(recfunction: str, *args: int) -> int:
    """Return the computed value of a recursive function."""
    recfunction = recfunction.lower().replace(" ", "")
    recfunction = recfunction.replace("theta", "θ")
    recfunction = recfunction.replace("pi^", "π^")
    recfunction = recfunction.replace("sigma", "σ")
    recfunction = recfunction.replace("mu[", "μ[")

    sys.stderr.write(f"{_format_function(recfunction)}(")
    if args:
        sys.stderr.write(",".join(str(arg) for arg in args))
    sys.stderr.write(")")

    arguments = list(args)
    is_initial = "(" not in recfunction and "<" not in recfunction and "[" not in recfunction

    if is_initial:
        if recfunction.startswith("θ"):
            if len(args) != 0:
                raise ValueError(" θ() cannot be invoked with argument(s).")
            computed = 0
            sys.stderr.write(f" = {computed}\n")
            return computed
        if recfunction.startswith("σ"):
            if len(args) != 1:
                raise ValueError(" σ() cannot be invoked with argument(s).")
            computed = args[0] + 1
            sys.stderr.write(f" = {computed}\n")
            return computed
        if recfunction.startswith("π"):
            match = re.findall(r"\d+", recfunction)
            if len(match) != 2:
                raise ValueError(" wrong number of arguments for function π.")
            if len(args) != int(match[0]):
                raise ValueError(_format_function(f" π^{match[0]}_{match[1]}() cannot be invoked with {len(args)} argument(s)."))
            computed = args[int(match[1]) - 1]
            sys.stderr.write(f" = {computed}\n")
            return computed

        mapping = _load_recursive_functions()
        if recfunction not in mapping:
            raise ValueError("Function not found in database...")
        sys.stderr.write("\n")
        return eval_rec_function(mapping[recfunction], *args)

    if recfunction.endswith("]"):
        minimized = recfunction[3:-1]
        sys.stderr.write("\n")
        t = 0
        while eval_rec_function(minimized, *args, t) != 0:
            t += 1
        return t

    if recfunction.endswith(">"):
        separator_pos = _avoid_nested(recfunction, "<", ">" ).find("|")
        if len(arguments) == 0:
            raise ValueError(" wrong number of arguments for primitive recursion.")
        if arguments[-1] == 0:
            base_function = recfunction[1:separator_pos]
            sys.stderr.write("\n")
            return eval_rec_function(base_function, *args[:-1])
        iterated_function = recfunction[separator_pos + 1 : -1]
        sys.stderr.write("\n")
        return eval_rec_function(
            iterated_function,
            *args[:-1],
            args[-1] - 1,
            eval_rec_function(recfunction, *args[:-1], args[-1] - 1),
        )

    if recfunction.endswith(")"):
        symbol_position, nesting = label_balanced_symbols(recfunction, "(", ")")
        separator_first = symbol_position[[i for i, n in enumerate(nesting) if n == 1][-1]]
        separator_last = recfunction.rfind(")") + 1
        separators = [separator_first]
        nested_free = _avoid_nested(recfunction, "(", ")")
        separators.extend([pos + 1 for pos in [i for i, char in enumerate(nested_free) if char == ","]])
        separators.append(separator_last)

        internal_args: List[int] = []
        for idx in range(1, len(separators)):
            inner = recfunction[separators[idx - 1] : separators[idx] - 1]
            sys.stderr.write("\n")
            internal_args.append(eval_rec_function(inner, *args))

        outer = recfunction[: separator_first - 1]
        sys.stderr.write("\n")
        return eval_rec_function(outer, *internal_args)

    raise ValueError("Error in function definition...")


def _avoid_nested(recfunction: str, opensymbol: str, closesymbol: str) -> str:
    filtered = list(recfunction)
    symbol_position, nesting = label_balanced_symbols(recfunction, opensymbol, closesymbol)
    open_level2 = [i for i, level in enumerate(nesting) if level == 2]
    close_level2 = [i for i, level in enumerate(nesting) if level == -2]
    for open_idx, close_idx in zip(open_level2, close_level2):
        start = symbol_position[open_idx] - 1
        end = symbol_position[close_idx]
        for idx in range(start, end):
            filtered[idx] = " "
    return "".join(filtered)


def _format_function(recfunction: str) -> str:
    superscript = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
    subscript = {"0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉"}

    formatted = recfunction
    for match in re.findall(r"\^\d+", recfunction):
        converted = "".join(superscript[digit] for digit in match[1:])
        formatted = formatted.replace(match, converted)
    for match in re.findall(r"_\d+", recfunction):
        converted = "".join(subscript[digit] for digit in match[1:])
        formatted = formatted.replace(match, converted)
    return formatted


def _load_recursive_functions() -> Dict[str, str]:
    path = Path(__file__).with_name("recursivefunctions")
    mapping: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        name, expression = line.split(None, 1)
        mapping[name.strip()] = expression.strip()
    return mapping
