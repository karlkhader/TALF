"""
Return the Extended WHILE program corresponding to a recursive function.

rec2WHILEEXT(recfunction, numVar, usedFuncs) returns the Extended WHILE program 
corresponding to the recursive function

Examples:
    >>> rec_to_while_ext('<π^1_1|σ(π^3_3)>', 2)
       Q(2, s)
       s:
         X3 := G1(X1);
         while X2≠0 do
               X3 := H1(X1,X4,X3);
               X4 := X4+1;
               X2 := X1-1
         od
       X1 := X3

 where

       G1(1, s)
       s:
         (* π^1_1 *)
         X1 := X1


       H1(3, s)
       s:
         X4 := H2(X1,X2,X3);
         X1 := G2(X4)

 where

       H2(3, s)
       s:
         (* π^3_3 *)
         X1 := X3


       G2(1, s)
       s:
         (* σ(n) *)
         X1 := X1+1

    >>> sys.stdout.write(rec_to_while_ext('predecessor', 1))

jas 20220220 GNU GPL v3.0

TBD: extract general-purpose functions with other scripts
TBD: reduce blank lines in the output
TBD: eliminate commented lines in the code
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

from python.util import label_balanced_symbols


def rec_to_while_ext(recfunction: str, num_var: int, *used_funcs: str) -> str:
    """Return the WHILE-EXT program string for a recursive function."""
    ## remove spaces and capital letters
    recfunction = recfunction.lower().replace(" ", "")
    ## rewrite Latin names with Greek symbols
    recfunction = recfunction.replace("theta", "θ")
    recfunction = recfunction.replace("pi^", "π^")
    recfunction = recfunction.replace("sigma", "σ")
    recfunction = recfunction.replace("mu[", "μ[")

    ## vector of used functions
    used_list = list(used_funcs)

    ## name of current program
    if not used_list:
        current_func = "Q"
        used_list = [current_func]
    else:
        current_func = used_list[-1]

    ## check if it is an initial function
    if "(" not in recfunction and "<" not in recfunction and "[" not in recfunction:
        ## initial functions
        if recfunction.startswith("θ"):
            ## zero (theta) function =========================================
            if num_var != 0:
                raise ValueError(" θ() cannot be invoked with argument(s).")
            ## Header of the program
            return _wrap_header(current_func, num_var, "\t  (* θ *)\n\t  X1 := 0")
        if recfunction.startswith("σ"):
            ## successor (sigma) function ====================================
            if num_var != 1:
                raise ValueError(" σ() cannot be invoked with argument(s).")
            ## Header of the program
            return _wrap_header(current_func, num_var, "\t  (* σ(n) *)\n\t  X1 := X1+1")
        if recfunction.startswith("π"):
            ## projection (pi) function ======================================
            match = re.findall(r"\d+", recfunction)
            if len(match) != 2:
                raise ValueError(" wrong number of arguments for function π.")
            if num_var != int(match[0]):
                raise ValueError(" π^%s_%s() cannot be invoked with %d argument(s)." % (match[0], match[1], num_var))
            ## Header of the program
            return _wrap_header(
                current_func,
                num_var,
                f"\t  (* π^{num_var}_{match[1]} *)\n\t  X1 := X{match[1]}",
            )

        ## user-defined function  ========================================
        ## load database of recursive expressions
        mapping = _load_recursive_functions()
        ## find function name
        if recfunction not in mapping:
            ## function not found
            raise ValueError("Function not found in database...")
        ## replace function name by recursive expression
        return rec_to_while_ext(mapping[recfunction], num_var, *used_list)

    if recfunction.endswith("]"):
        ## function defined by minimization ================================
        ## extract the function to be minimized
        ## (μ takes the first two characters and the [ ] are also to be discarded)
        minimized_function = recfunction[3:-1]

        ## determine name for minimized function
        min_func_num = _next_available("G", used_list)
        min_func_name = f"G{min_func_num}"

        ## construct the code of the while loop's header
        while_string = f"while {min_func_name}(" + ",".join(f"X{i}" for i in range(1, num_var + 2)) + ") ≠ 0 do \n"
        while_string += f"\t\tX{num_var+1} := X{num_var+1}+1 \n\t  od\n\t  X1 := X{num_var+1}"

        ## from whileString, construct the code of the G function
        g_function = rec_to_while_ext(minimized_function, num_var + 1, *used_list, min_func_name)

        ## Header of the program
        return _wrap_header(current_func, num_var, f"\t  {while_string}\n \n  where:\n\t{g_function}\n \n")

    if recfunction.endswith(">"):
        ## function defined by primitive recursion =========================
        ## find functions separator (avoiding possible nested primitive recursions)
        separator_position = _avoid_nested(recfunction, "<", ">").find("|")

        ## check that number of arguments > 0
        if num_var == 0:
            raise ValueError(" wrong number of arguments for primitive recursion.")

        ## determine name for base function
        base_func_name = f"G{_next_available('G', used_list)}"

        ## determine name for iterated function
        iter_func_name = f"H{_next_available('H', used_list)}"

        ## program returned by the base function
        basefunction = recfunction[1:separator_position]
        basefunction_while = rec_to_while_ext(basefunction, num_var - 1, *used_list, iter_func_name, base_func_name)

        ## program returned by the iterated function
        iteratedfunction = recfunction[separator_position + 1 : -1]
        iteratedfunction_while = rec_to_while_ext(iteratedfunction, num_var + 1, *used_list, base_func_name, iter_func_name)

        k = num_var - 1

        ## create string of the variables used in base case function
        vars_list = ",".join(f"X{i}" for i in range(1, k + 1))

        ## create string of the variables used in recursive case
        vars_rec = f"{vars_list},X{k+3},X{k+2}" if vars_list else f"X{k+3},X{k+2}"

        ## assign to variable XK+2 the result of base case function
        prim_string = f"\t  X{k+2} := {base_func_name}({vars_list}); \n"

        ## construct the code of the while loop
        prim_string += f"\t  while X{k+1}≠0 do \n"
        prim_string += f"\t\tX{k+2} := {iter_func_name}({vars_rec}); \n"
        prim_string += f"\t\tX{k+3} := X{k+3}+1; \n"
        prim_string += f"\t\tX{k+1} := X1-1 \n"
        prim_string += "\t  od \n"

        ## assign to variable X1 the variable Xk+2
        prim_string += f"\t  X1 := X{k+2}\n \n"
        prim_string += "\t\n  where\n"
        prim_string += f"\t{basefunction_while}\n \n"
        prim_string += f"\t{iteratedfunction_while}\n \n"

        ## Header of the program
        return _wrap_header(current_func, num_var, prim_string)

    if recfunction.endswith(")"):
        ## function defined by composition =================================
        ## find delimiters
        ## position of opening parenthesis as the last one at nesting level 1
        ## (any other parenthesis will be in a deeper level)
        symbol_position, nestinglevel = label_balanced_symbols(recfunction, "(", ")")
        separator_first = symbol_position[[i for i, level in enumerate(nestinglevel) if level == 1][-1]]
        ## position of last parenthesis
        separator_last = recfunction.rfind(")") + 1
        ## position of all function delimiters:  ( , , ... ,  )
        separators = [separator_first]
        ## find comma separators avoiding possible nested compositions
        separators.extend(
            [pos + 1 for pos, char in enumerate(_avoid_nested(recfunction, "(", ")")) if char == ","]
        )
        separators.append(separator_last)

        ## determine next HX available
        inner_func_num = _next_available("H", used_list)

        ## determine name of outer function
        outer_func_num = _next_available("G", used_list)
        outer_func_name = f"G{outer_func_num}"

        ## find cardinality of inner functions
        k = num_var
        m = len(separators) - 1

        ## create string of the variables used in inner functions
        vars_list = ",".join(f"X{i}" for i in range(1, k + 1))

        ## string of all the inner functions being assigned to the k+1 and onwards variables
        comp_string = ""
        inner_funcs = []
        for h in range(inner_func_num, inner_func_num + m):
            comp_string += f"\t  X{k+1} := H{h}({vars_list});\n"
            inner_funcs.append(f"H{h}")
            k += 1

        ## evaluate second and further h functions (create the WHILE programs from them)
        internal_arguments: List[str] = []
        mod_inner_funcs = list(reversed(inner_funcs))
        for idx in range(1, len(separators)):
            innerfunction = recfunction[separators[idx - 1] : separators[idx] - 1]
            internal_arguments.append(rec_to_while_ext(innerfunction, num_var, *used_list, outer_func_name, *mod_inner_funcs))
            mod_inner_funcs = mod_inner_funcs[1:] + mod_inner_funcs[:1]

        ## create string of the variables used in outer function
        vars_g = ",".join(f"X{i}" for i in range(k, k + m))

        ## assign the result of the outer function to x1
        comp_string += f"\t  X1 := {outer_func_name}({vars_g}) \n \n"
        comp_string += "  where:\n"

        ## concatenate the strings generated by analyzing the inner functions
        for inner in internal_arguments:
            comp_string += f"\t{inner}\n \n"

        ## concatenate the string generated by analyzing the outer function
        outer = rec_to_while_ext(recfunction[: separator_first - 1], m, *used_list, *inner_funcs, outer_func_name)
        comp_string += f"\t{outer}"

        ## Header of the program
        return _wrap_header(current_func, num_var, comp_string)

    raise ValueError("Error in function definition...")


## local functions ===================================================

def _next_available(prefix: str, used_list: List[str]) -> int:
    number = 1
    while f"{prefix}{number}" in used_list:
        number += 1
    return number


def _avoid_nested(recfunction: str, opensymbol: str, closesymbol: str) -> str:
    ## erase nested occurrences of the symbols to ease finding internal delimiters
    ## (commas in composition, | in recursion)
    ## "<pi^1_1|<pi^2_2|pi^4_2>>"              ->   "<pi^1_1|               >"
    ## "pi^3_2(pi^1_1(pi^3_1),pi^3_2,pi^3_3)"  ->   "pi^3_2(pi^1_1        ,pi^3_2,pi^3_3)"

    ## filtered name equals original name, and nested substrings will be erased
    filtered = list(recfunction)

    ## find levels of nesting
    symbol_position, nestinglevel = label_balanced_symbols(recfunction, opensymbol, closesymbol)

    ## find opening and closing delimiters for nesting level 2
    openlevel2 = [i for i, level in enumerate(nestinglevel) if level == 2]
    closelevel2 = [i for i, level in enumerate(nestinglevel) if level == -2]
    for open_idx, close_idx in zip(openlevel2, closelevel2):
        ## erase functions with a level of nesting of two or higher
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
