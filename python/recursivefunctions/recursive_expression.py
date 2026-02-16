"""
Return the recursive expression of a recursive function.

expression = recursiveexpression(recfunction, outputformat) is the recursive expression 
(only initial functions, composition, recursion and minimization) of a recursive function

Examples:
    >>> recursive_expression('power')
    <σ(<θ|π^2_2>)|<<θ|π^2_2>|<π^1_1|σ(π^3_3)>(π^3_1,π^3_3)>(π^3_1,π^3_3)>
    >>> recursive_expression('<π_1^1|π_3^1>', 'LaTeX')
    $<π_1^1|π_3^1>$
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict


def recursive_expression(recfunction: str, outputformat: str | None = None) -> str:
    """Return the recursive expression for a given function name."""
    ## remove spaces and capital letters
    recfunction = recfunction.lower().replace(" ", "")
    ## rewrite Latin names with Greek symbols
    recfunction = recfunction.replace("theta", "θ")
    recfunction = recfunction.replace("pi^", "π^")
    recfunction = recfunction.replace("sigma", "σ")
    recfunction = recfunction.replace("mu[", "μ[")

    ## replace function names by recursive expressions
    ## load database of recursive expressions
    mapping = _load_recursive_functions()

    while True:
        ## find function names
        match = re.search(r"[a-z]+[0-9^_]*", recfunction)
        if not match:
            break
        name = match.group(0)
        ## find function name in database
        if name not in mapping:
            ## function not found
            raise ValueError(f"Function '{name}' not found in database...")
        ## replace name by expression
        recfunction = f"{recfunction[:match.start()]}{mapping[name]}{recfunction[match.end():]}"

    if outputformat == "LaTeX":
        ## rewrite Greek symbols with LaTeX commands
        ## TBD: add {} to sub and superscripts: \pi^{3}_{2}
        recfunction = recfunction.replace("θ", "\\theta")
        recfunction = recfunction.replace("π^", "\\pi^")
        recfunction = recfunction.replace("σ", "\\sigma")
        recfunction = recfunction.replace("μ[", "\\mu[")
        recfunction = recfunction.replace("[", "\\left[")
        recfunction = recfunction.replace("]", "\\right]")
        recfunction = recfunction.replace("(", "\\left(")
        recfunction = recfunction.replace(")", "\\right)")
        recfunction = f"${recfunction}$"
    elif outputformat == "text":
        ## rewrite Greek symbols with LaTeX commands
        ## TBD: add {} to sub and superscripts: \pi^{3}_{2}
        recfunction = recfunction.replace("θ", "\\theta")
        recfunction = recfunction.replace("π^", "\\pi^")
        recfunction = recfunction.replace("σ", "\\sigma")
        recfunction = recfunction.replace("μ", "\\mnz")
        recfunction = recfunction.replace("<", "\\rec{")
        recfunction = recfunction.replace(">", "}")
        recfunction = recfunction.replace("|", "}{")
        recfunction = recfunction.replace("[", "{")
        recfunction = recfunction.replace("]", "}")
        recfunction = f"${recfunction}$"

    return recfunction


def _load_recursive_functions() -> Dict[str, str]:
    path = Path(__file__).with_name("recursivefunctions")
    mapping: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        name, expression = line.split(None, 1)
        mapping[name.strip()] = expression.strip()
    return mapping
