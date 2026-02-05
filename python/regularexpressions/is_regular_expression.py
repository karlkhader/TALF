"""
Check if a string is a regular expression over a given alphabet.

Examples:
    >>> is_regular_expression('01', '((10)01)')
    False
    >>> is_regular_expression('01', '((10)+(01)**)')
    True
"""

from __future__ import annotations


def is_regular_expression(alphabet: str, expression: str) -> bool:
    """Return True if the expression is a regular expression over alphabet."""
    emptysetalias = "∅"
    extendedalphabet = f"{emptysetalias}{alphabet}"

    if len(expression) == 1:
        return expression in extendedalphabet

    if expression.endswith("*"):
        return is_regular_expression(alphabet, expression[:-1])

    if expression.startswith("(") and expression.endswith(")"):
        inner = expression[1:-1]
        depth = 0
        for idx, char in enumerate(inner):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == "+" and depth == 0:
                first_expression = inner[:idx]
                second_expression = inner[idx + 1 :]
                return is_regular_expression(alphabet, first_expression) and is_regular_expression(
                    alphabet, second_expression
                )

        if "(" in inner or ")" in inner:
            return False

        singlesymbols = [idx for idx, char in enumerate(inner) if char in extendedalphabet]
        if len(singlesymbols) == 2:
            first_expression = inner[singlesymbols[0] : singlesymbols[1]]
            second_expression = inner[singlesymbols[1] :]
            if len(first_expression) + len(second_expression) == len(inner):
                return is_regular_expression(alphabet, first_expression) and is_regular_expression(
                    alphabet, second_expression
                )

    return False
