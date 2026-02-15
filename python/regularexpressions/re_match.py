"""
Find strings matching a given regular-expression pattern (no overlaps).

# strings = re_match(strings, pattern)
#
# Finds the strings that match a given pattern (without overlap).
# The strings can be represented in three different ways:
#   {'10001', '0000', '111111101101'}  # as a list of strings
#   '10001 0000 111111101101'          # as space-separated strings
#   filename                           # the string is loaded from filename
#
# Examples:
#
#    re_match('10001 0000 100000001 11 11', '10*1');
#    
#    10001 ∈ 10*1
#    
#    100000001 ∈ 10*1
#    
#    11 ∈ 10*1
#    
#
#    re_match('10001 0000 01010100010001 11101', '(0*+1*)10*1');
#    
#    10001 ∈ (0*+1*)10*1
#    
#    11101 ∈ (0*+1*)10*1
#    
#
#    To generate a random string over an alphabet, this line will suffice:
#
#    >> import random; ''.join(random.choice('01') for _ in range(5))
#    ans = 10110
#    >> import random; ''.join(random.choice('ATCG') for _ in range(10))
#    ans = TTTATGGGCA
#
#   It can also be invoked with a textfile name (newline characters are ignored).

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
    ## if in a single string, individual strings are delimited by one or more spaces
    separator = ' '
    
    original_pattern = pattern
    ## replace '+' (or) symbol of theoretical model by '|' of Python re model
    ## include word anchors and parenthesis to match whole words
    compiled_pattern = f"^({pattern.replace('+', '|')})$"

    if isinstance(strings, str):
        ## the string might be a textfile name
        path = Path(strings)
        if path.exists():
            ## read textfile discarding newline characters
            strings = path.read_text(encoding="utf-8").replace("\n", "")
        if isinstance(strings, str):
            ## convert space-separated strings into an array of strings
            liststrings: List[str] = []
            for token in strings.split():
                ## add to list removing leading and trailing spaces
                token = token.strip()
                if token:
                    liststrings.append(token)
            strings = liststrings

    ## find strings matching the expression
    # extract only the strings that match, not the substrings
    filtered: List[str] = []
    for value in strings:
        if re.search(compiled_pattern, value):
            filtered.append(value)

    ## remove duplicates
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
