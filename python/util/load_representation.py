"""Load set representations from a JSON database."""

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

    return None
