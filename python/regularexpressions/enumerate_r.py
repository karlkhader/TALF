"""
Enumerate regular expressions over a given alphabet.

Examples:
    >>> enumerate_r('01', 5)
    >>> enumerate_r('01', 10000, 'index')
    >>> enumerate_r('01', '(01)*', 'search', False)
"""

from __future__ import annotations

from typing import List, Optional

from python.whilelanguage.encoding.cantordecoding import cantordecoding
from .is_regular_expression import is_regular_expression


def enumerate_r(
    alphabet: str,
    expression_id=None,
    index_type: str = "list",
    print_expression: bool = True,
):
    """Return or list regular expressions over the alphabet."""
    if any(symbol in alphabet for symbol in "∅()+"):
        raise ValueError("Wrong alphabet...")

    if expression_id is not None and isinstance(expression_id, (int, float)) and expression_id < 0:
        raise ValueError("Wrong limit, it must be a positive integer...")

    if index_type not in ("list", "index", "search"):
        raise ValueError("Wrong index type, it must be 'list', 'index' or 'search'...")

    symbols = ["∅", *alphabet]

    if expression_id is None:
        index_type = "list"
        max_number = None
    elif isinstance(expression_id, str):
        if not is_regular_expression(alphabet, expression_id):
            print(f"\nSorry, '{expression_id}' is not a regular expression over the alphabet '{alphabet}'.\n")
            return None
        print(f"\n'{expression_id}' is a valid regular expression over the alphabet '{alphabet}', let's find its index...\n")
        index_type = "search"
        max_number = None
    elif index_type == "list":
        max_number = int(expression_id)
    else:
        max_number = int(expression_id)

    if index_type == "index":
        expression = _expression_for_index(alphabet, symbols, int(expression_id))
        if print_expression:
            _prettyprint(int(expression_id), expression)
        return expression

    expression = [] if max_number is not None else None
    number_expressions = 0
    searching = index_type == "search"

    while True:
        new_expression = _expression_for_index(alphabet, symbols, number_expressions)
        if searching:
            if new_expression == expression_id:
                if print_expression:
                    _prettyprint(number_expressions, new_expression)
                return number_expressions
        else:
            if max_number is not None:
                expression.append(new_expression)
            if print_expression:
                _prettyprint(number_expressions, new_expression)
        number_expressions += 1
        if index_type == "list" and max_number is not None and number_expressions > max_number:
            break

    return expression


def _expression_for_index(alphabet: str, symbols: List[str], expression_id: int) -> str:
    if expression_id < len(symbols):
        return symbols[expression_id]

    index = expression_id - len(symbols)
    normalized_index = (expression_id - len(symbols)) // 3

    if index % 3 == 0:
        indexes = cantordecoding(normalized_index, 2)
        return f"({_expression_for_index(alphabet, symbols, indexes[0])}{_expression_for_index(alphabet, symbols, indexes[1])})"
    if index % 3 == 1:
        indexes = cantordecoding(normalized_index, 2)
        return f"({_expression_for_index(alphabet, symbols, indexes[0])}+{_expression_for_index(alphabet, symbols, indexes[1])})"

    return f"{_expression_for_index(alphabet, symbols, normalized_index)}*"


def _prettyprint(index: int, expression: str) -> None:
    spacesymbol = " "
    print(f"{spacesymbol * (6 - len(str(index)))}{index}{spacesymbol * 3}{expression}")
