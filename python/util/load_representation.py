"""Load set representations from a JSON database.

load the representation of a set (either a language or a function) from a JSON file

Example of a finite automata database:
[
  {
    "name" : "a*bb*aa*",
    "representation" : {
      "K" : ["q0", "q1", "q2", "q3"],
      "A" : ["a", "b"],
      "s" : "q0",
      "F" : ["q2"],
      "t" : [["q0", "a", "q0"],
             ["q0", "b", "q1"],
             ["q1", "a", "q2"],
             ["q1", "b", "q1"],
             ["q2", "a", "q2"],
             ["q2", "b", "q3"],
             ["q3", "a", "q3"],
             ["q3", "b", "q3"]]
      }
  },
  {
    "name" : "aa*bb*",
    "representation" : {
      "K" : ["q0", "q1", "q2"],
      "A" : ["a", "b"],
      "s" : "q0",
      "F" : ["q2"],
      "t" : [["q0", "a", "q1"],
             ["q1", "a", "q1"],
             ["q1", "b", "q2"],
             ["q2", "b", "q2"]]
      }
  }
]

automaton = loadrepresentation(automatadatabasename, automatonname)

fjv, 02/01/2022   GNU GPL v3.0
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional


def load_representation(set_database_name: str, set_name: str) -> Optional[Any]:
    """
    Load the representation of a set (language/function) from a JSON file.

    Args:
        set_database_name: JSON file path without the .json suffix.
        set_name: Name of the set to retrieve.

    Returns:
        The representation object if found, otherwise ``None``.
    """
    database_path = Path(f"{set_database_name}.json")
    if not database_path.exists():
        raise FileNotFoundError(f"Database file not found: {database_path}")

    with database_path.open("r", encoding="utf-8") as handle:
        sets = json.load(handle)

    for current_set in sets:
        if current_set.get("name") == set_name:
            return current_set.get("representation")

    # return empty string and error message if not found
    return None
