"""
Return the Extended WHILE program corresponding to a recursive function.

Examples:
    >>> rec_to_while_ext('<π^1_1|σ(π^3_3)>', 2)
    >>> rec_to_while_ext('predecessor', 1)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

from python.util import label_balanced_symbols


def rec_to_while_ext(recfunction: str, num_var: int, *used_funcs: str) -> str:
    """Return the WHILE-EXT program string for a recursive function."""
    recfunction = recfunction.lower().replace(" ", "")
    recfunction = recfunction.replace("theta", "θ")
    recfunction = recfunction.replace("pi^", "π^")
    recfunction = recfunction.replace("sigma", "σ")
    recfunction = recfunction.replace("mu[", "μ[")

    used_list = list(used_funcs)
    if not used_list:
        current_func = "Q"
        used_list = [current_func]
    else:
        current_func = used_list[-1]

    if "(" not in recfunction and "<" not in recfunction and "[" not in recfunction:
        if recfunction.startswith("θ"):
            if num_var != 0:
                raise ValueError(" θ() cannot be invoked with argument(s).")
            return _wrap_header(current_func, num_var, "\t  (* θ *)\n\t  X1 := 0")
        if recfunction.startswith("σ"):
            if num_var != 1:
                raise ValueError(" σ() cannot be invoked with argument(s).")
            return _wrap_header(current_func, num_var, "\t  (* σ(n) *)\n\t  X1 := X1+1")
        if recfunction.startswith("π"):
            match = re.findall(r"\d+", recfunction)
            if len(match) != 2:
                raise ValueError(" wrong number of arguments for function π.")
            if num_var != int(match[0]):
                raise ValueError(" π^%s_%s() cannot be invoked with %d argument(s)." % (match[0], match[1], num_var))
            return _wrap_header(
                current_func,
                num_var,
                f"\t  (* π^{num_var}_{match[1]} *)\n\t  X1 := X{match[1]}",
            )

        mapping = _load_recursive_functions()
        if recfunction not in mapping:
            raise ValueError("Function not found in database...")
        return rec_to_while_ext(mapping[recfunction], num_var, *used_list)

    if recfunction.endswith("]"):
        minimized_function = recfunction[3:-1]
        min_func_num = _next_available("G", used_list)
        min_func_name = f"G{min_func_num}"

        while_string = f"while {min_func_name}(" + ",".join(f"X{i}" for i in range(1, num_var + 2)) + ") ≠ 0 do \n"
        while_string += f"\t\tX{num_var+1} := X{num_var+1}+1 \n\t  od\n\t  X1 := X{num_var+1}"

        g_function = rec_to_while_ext(minimized_function, num_var + 1, *used_list, min_func_name)
        return _wrap_header(current_func, num_var, f"\t  {while_string}\n \n  where:\n\t{g_function}\n \n")

    if recfunction.endswith(">"):
        separator_position = _avoid_nested(recfunction, "<", ">").find("|")
        if num_var == 0:
            raise ValueError(" wrong number of arguments for primitive recursion.")

        base_func_name = f"G{_next_available('G', used_list)}"
        iter_func_name = f"H{_next_available('H', used_list)}"

        basefunction = recfunction[1:separator_position]
        basefunction_while = rec_to_while_ext(basefunction, num_var - 1, *used_list, iter_func_name, base_func_name)

        iteratedfunction = recfunction[separator_position + 1 : -1]
        iteratedfunction_while = rec_to_while_ext(iteratedfunction, num_var + 1, *used_list, base_func_name, iter_func_name)

        k = num_var - 1
        vars_list = ",".join(f"X{i}" for i in range(1, k + 1))
        vars_rec = f"{vars_list},X{k+3},X{k+2}" if vars_list else f"X{k+3},X{k+2}"

        prim_string = f"\t  X{k+2} := {base_func_name}({vars_list}); \n"
        prim_string += f"\t  while X{k+1}≠0 do \n"
        prim_string += f"\t\tX{k+2} := {iter_func_name}({vars_rec}); \n"
        prim_string += f"\t\tX{k+3} := X{k+3}+1; \n"
        prim_string += f"\t\tX{k+1} := X1-1 \n"
        prim_string += "\t  od \n"
        prim_string += f"\t  X1 := X{k+2}\n \n"
        prim_string += "\t\n  where\n"
        prim_string += f"\t{basefunction_while}\n \n"
        prim_string += f"\t{iteratedfunction_while}\n \n"

        return _wrap_header(current_func, num_var, prim_string)

    if recfunction.endswith(")"):
        symbol_position, nestinglevel = label_balanced_symbols(recfunction, "(", ")")
        separator_first = symbol_position[[i for i, level in enumerate(nestinglevel) if level == 1][-1]]
        separator_last = recfunction.rfind(")") + 1
        separators = [separator_first]
        separators.extend(
            [pos + 1 for pos, char in enumerate(_avoid_nested(recfunction, "(", ")")) if char == ","]
        )
        separators.append(separator_last)

        inner_func_num = _next_available("H", used_list)
        outer_func_num = _next_available("G", used_list)
        outer_func_name = f"G{outer_func_num}"

        k = num_var
        m = len(separators) - 1
        vars_list = ",".join(f"X{i}" for i in range(1, k + 1))

        comp_string = ""
        inner_funcs = []
        for h in range(inner_func_num, inner_func_num + m):
            comp_string += f"\t  X{k+1} := H{h}({vars_list});\n"
            inner_funcs.append(f"H{h}")
            k += 1

        internal_arguments: List[str] = []
        mod_inner_funcs = list(reversed(inner_funcs))
        for idx in range(1, len(separators)):
            innerfunction = recfunction[separators[idx - 1] : separators[idx] - 1]
            internal_arguments.append(rec_to_while_ext(innerfunction, num_var, *used_list, outer_func_name, *mod_inner_funcs))
            mod_inner_funcs = mod_inner_funcs[1:] + mod_inner_funcs[:1]

        vars_g = ",".join(f"X{i}" for i in range(k, k + m))
        comp_string += f"\t  X1 := {outer_func_name}({vars_g}) \n \n"
        comp_string += "  where:\n"
        for inner in internal_arguments:
            comp_string += f"\t{inner}\n \n"

        outer = rec_to_while_ext(recfunction[: separator_first - 1], m, *used_list, *inner_funcs, outer_func_name)
        comp_string += f"\t{outer}"
        return _wrap_header(current_func, num_var, comp_string)

    raise ValueError("Error in function definition...")


def _next_available(prefix: str, used_list: List[str]) -> int:
    number = 1
    while f"{prefix}{number}" in used_list:
        number += 1
    return number


def _avoid_nested(recfunction: str, opensymbol: str, closesymbol: str) -> str:
    filtered = list(recfunction)
    symbol_position, nestinglevel = label_balanced_symbols(recfunction, opensymbol, closesymbol)
    openlevel2 = [i for i, level in enumerate(nestinglevel) if level == 2]
    closelevel2 = [i for i, level in enumerate(nestinglevel) if level == -2]
    for open_idx, close_idx in zip(openlevel2, closelevel2):
        start = symbol_position[open_idx] - 1
        end = symbol_position[close_idx]
        for idx in range(start, end):
            filtered[idx] = " "
    return "".join(filtered)


def _wrap_header(func: str, num_var: int, body: str) -> str:
    return f"\n\t{func}({num_var}, s)\n\ts: \n{body}"


def _load_recursive_functions() -> dict[str, str]:
    path = Path(__file__).with_name("recursivefunctions")
    mapping: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        name, expression = line.split(None, 1)
        mapping[name.strip()] = expression.strip()
    return mapping
