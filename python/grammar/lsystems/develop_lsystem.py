"""
Develop an L-system.

Examples:
    >>> develop_lsystem("creeping_plant", 2)
    >>> develop_lsystem("climbing_plant", 3)
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
        loaded = load_representation(database_path, lsystem)
        if loaded is None:
            raise ValueError(f"L-system '{lsystem}' not found.")
        lsystem = loaded

    string = lsystem["S"]

    for _ in range(iterations):
        production = string.lower()
        for left, right in lsystem["P"]:
            production = production.replace(left.lower(), right)
        string = production

    draw_tree(string, output_path=output_path)
    return string
