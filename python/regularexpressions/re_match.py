"""
Find strings matching a given regular-expression pattern (no overlaps).

Examples:
    >>> re_match('10001 0000 100000001 11 11', '10*1')
    >>> re_match('10001 0000 01010100010001 11101', '(0*+1*)10*1')
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Sequence, Union


def re_match(strings: Union[str, Sequence[str]], pattern: str) -> List[str]:
    """Return strings that match a given pattern (whole-string match)."""
    original_pattern = pattern
    compiled_pattern = f"^({pattern.replace('+', '|')})$"

    if isinstance(strings, str):
        path = Path(strings)
        if path.exists():
            strings = path.read_text(encoding="utf-8").replace("\n", "")
        if isinstance(strings, str):
            liststrings: List[str] = []
            for token in strings.split():
                token = token.strip()
                if token:
                    liststrings.append(token)
            strings = liststrings

    filtered: List[str] = []
    for value in strings:
        if re.search(compiled_pattern, value):
            filtered.append(value)

    seen = set()
    unique_strings: List[str] = []
    for value in filtered:
        if value not in seen:
            seen.add(value)
            unique_strings.append(value)

    if unique_strings:
        maxlength = max(len(value) for value in unique_strings)
    else:
        maxlength = 0

    for value in unique_strings:
        filling = " " * (maxlength - len(value) + 1)
        print(f"\n\u2001\u2001{value}{filling}∈ {original_pattern}")

    return unique_strings
