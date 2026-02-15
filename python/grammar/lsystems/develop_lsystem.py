"""
Read more about L-Systems in
 https://riuma.uma.es/xmlui/bitstream/handle/10630/12647/paper%20GECCO09.pdf

Examples:
    >>> develop_lsystem('creeping_plant', 2)
    >>> develop_lsystem('climbing_plant', 3)
"""

from __future__ import annotations

from typing import Dict, Union

from python.util import load_representation
from .draw_tree import draw_tree


LSystem = Dict[str, object]


def develop_lsystem(
    lsystem: Union[str, LSystem],
    iterations: int = 3,
    *,
    database_path: str = "python/grammar/grammars",
    output_path: str | None = None,
) -> str:
    """Develop an L-system for a number of iterations and draw the result."""
    if isinstance(lsystem, str):
        ## read from JSON file (FastArrayParser = 0 avoids replacing '[' by '{')
        loaded = load_representation(database_path, lsystem)
        if loaded is None:
            raise ValueError(f"L-system '{lsystem}' not found.")
        lsystem = loaded

    ## starting string
    string = lsystem["S"]

    ## iterations (choose only from 1 to 7, >= 8 critical,
    ## depends on the string and on the computer !!
    ## rewrite axiom a number of times
    for _ in range(iterations):
        ## start from current string
        ## non-terminal capital letters to small letters
        production = string.lower()
        ## rewrite each small letter with the RHS of the corresponding rule
        for left, right in lsystem["P"]:
            production = production.replace(left.lower(), right)
        string = production

    ## draw resulting structure with turtle method
    draw_tree(string, output_path=output_path)
    return string
