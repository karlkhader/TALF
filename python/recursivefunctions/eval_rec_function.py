"""
Evaluate a recursive function.

evalrecfunction(recfunction, varargin) returns the computed value

Examples:
    >>> eval_rec_function('addition', 3, 2)
    5
    >>> eval_rec_function('division', 4, 2)
    2
    >>> eval_rec_function('<theta|pi^2_2>', 2)
    0

fjv 20181216 GNU GPL v3.0
fjv 20181217 projection functions with super- and subscripts
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List

from python.util import label_balanced_symbols


def eval_rec_function(recfunction: str, *args: int) -> int:
    """Return the computed value of a recursive function."""
    ## remove spaces and capital letters
    recfunction = recfunction.lower().replace(" ", "")
    ## rewrite Latin names with Greek symbols
    recfunction = recfunction.replace("theta", "θ")
    recfunction = recfunction.replace("pi^", "π^")
    recfunction = recfunction.replace("sigma", "σ")
    recfunction = recfunction.replace("mu[", "μ[")

    ## print recursive function
    sys.stderr.write(f"{_format_function(recfunction)}(")
    if args:
        sys.stderr.write(",".join(str(arg) for arg in args))
    sys.stderr.write(")")

    ## vector or arguments
    arguments = list(args)

    ## check if it is an initial function
    is_initial = "(" not in recfunction and "<" not in recfunction and "[" not in recfunction

    if is_initial:
        ## initial functions
        if recfunction.startswith("θ"):
            ## zero (theta) function =========================================
            if len(args) != 0:
                raise ValueError(" θ() cannot be invoked with argument(s).")
            computed = 0
            sys.stderr.write(f" = {computed}\n")
            return computed
        if recfunction.startswith("σ"):
            ## successor (sigma) function ====================================
            if len(args) != 1:
                raise ValueError(" σ() cannot be invoked with argument(s).")
            computed = args[0] + 1
            sys.stderr.write(f" = {computed}\n")
            return computed
        if recfunction.startswith("π"):
            ## projection (pi) function ======================================
            match = re.findall(r"\d+", recfunction)
            if len(match) != 2:
                raise ValueError(" wrong number of arguments for function π.")
            if len(args) != int(match[0]):
                raise ValueError(_format_function(f" π^{match[0]}_{match[1]}() cannot be invoked with {len(args)} argument(s)."))
            computed = args[int(match[1]) - 1]
            sys.stderr.write(f" = {computed}\n")
            return computed

        ## user-defined function  ========================================
        ## load database of recursive expressions
        mapping = _load_recursive_functions()
        ## find function name
        if recfunction not in mapping:
            ## function not found
            raise ValueError("Function not found in database...")
        ## replace function name by recursive expression
        sys.stderr.write("\n")
        return eval_rec_function(mapping[recfunction], *args)

    if recfunction.endswith("]"):
        ## function defined by minimization ================================
        ## extract the function to be minimized
        ## (μ takes the first two characters and the [ ] are also to be discarded)
        minimized = recfunction[3:-1]
        sys.stderr.write("\n")
        t = 0
        while eval_rec_function(minimized, *args, t) != 0:
            t += 1
        ## value returned by the function
        return t

    if recfunction.endswith(">"):
        ## function defined by primitive recursion =========================
        ## find functions separator (avoiding possible nested primitive recursions)
        separator_pos = _avoid_nested(recfunction, "<", ">" ).find("|")

        ## check that number of arguments > 0
        if len(arguments) == 0:
            raise ValueError(" wrong number of arguments for primitive recursion.")

        ## value returned by the function
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
        ## function defined by composition =================================
        ## find delimiters
        ## position of opening parenthesis as the last one at nesting level 1
        ## (any other parenthesis will be in a deeper level)
        symbol_position, nesting = label_balanced_symbols(recfunction, "(", ")")
        separator_first = symbol_position[[i for i, n in enumerate(nesting) if n == 1][-1]]
        ## position of last parenthesis
        separator_last = recfunction.rfind(")") + 1
        ## position of all function delimiters:  ( , , ... ,  )
        separators = [separator_first]
        ## find comma separators avoiding possible nested compositions
        nested_free = _avoid_nested(recfunction, "(", ")")
        separators.extend([pos + 1 for pos in [i for i, char in enumerate(nested_free) if char == ","]])
        separators.append(separator_last)

        ## evaluate second and further h functions
        internal_args: List[int] = []
        for idx in range(1, len(separators)):
            inner = recfunction[separators[idx - 1] : separators[idx] - 1]
            sys.stderr.write("\n")
            internal_args.append(eval_rec_function(inner, *args))

        ## value returned by the function
        outer = recfunction[: separator_first - 1]
        sys.stderr.write("\n")
        return eval_rec_function(outer, *internal_args)

    raise ValueError("Error in function definition...")


## local functions ===================================================

def _avoid_nested(recfunction: str, opensymbol: str, closesymbol: str) -> str:
    ## erase nested occurrences of the symbols to ease finding internal delimiters
    ## (commas in composition, | in recursion)
    ## "<pi^1_1|<pi^2_2|pi^4_2>>"              ->   "<pi^1_1|               >"
    ## "pi^3_2(pi^1_1(pi^3_1),pi^3_2,pi^3_3)"  ->   "pi^3_2(pi^1_1        ,pi^3_2,pi^3_3)"

    ## filtered name equals original name, and nested substrings will be erased
    filtered = list(recfunction)

    ## find levels of nesting
    symbol_position, nesting = label_balanced_symbols(recfunction, opensymbol, closesymbol)

    ## find opening and closing delimiters for nesting level 2  
    open_level2 = [i for i, level in enumerate(nesting) if level == 2]
    close_level2 = [i for i, level in enumerate(nesting) if level == -2]
    for open_idx, close_idx in zip(open_level2, close_level2):
        ## erase functions with a level of nesting of two or higher
        start = symbol_position[open_idx] - 1
        end = symbol_position[close_idx]
        for idx in range(start, end):
            filtered[idx] = " "
    return "".join(filtered)


def _format_function(recfunction: str) -> str:
    ## super- and subscripts for projection functions
    superscript = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
    subscript = {"0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉"}

    formatted = recfunction

    ## convert normal digits to superscript digits
    for match in re.findall(r"\^\d+", recfunction):
        converted = "".join(superscript[digit] for digit in match[1:])
        formatted = formatted.replace(match, converted)

    ## convert normal digits to subscript digits
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
