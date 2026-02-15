"""
Check if a string is a regular expression over a given alphabet.

# valid = is_regular_expression(alphabet, expression)
#
# Check if a string is a regular expressions over a given alphabet.
# `alphabet` is a string with the symbols of the alphabet.
# `expression` is a string expression.
#
# Examples:
#
#   is_regular_expression('01','((10)01)')
#   ans = 0
# 
#   is_regular_expression('01','((10)+(01)**)')
#   ans = 1
# 
# ===============================================================
#
#   fjv, 10/10/2023  GNU GPL v3.0
#
# ===============================================================

Examples:
    >>> is_regular_expression('01', '((10)01)')
    False
    >>> is_regular_expression('01', '((10)+(01)**)')
    True
"""

from __future__ import annotations


def is_regular_expression(alphabet: str, expression: str) -> bool:
    """Return True if the expression is a regular expression over alphabet."""
    ## ASCII symbol 0 replaces the Unicode symbol for the empty set
    emptysetalias = "∅"
    extendedalphabet = f"{emptysetalias}{alphabet}"

    if len(expression) == 1:
        ## case of a single-symbol expression (Unicode ∅ replaced by another symbol so it counts as one character)
        return expression in extendedalphabet

    ## case of a concatenation, union or Kleene star of expressions
    if expression.endswith("*"):
        ## case of Kleene star
        return is_regular_expression(alphabet, expression[:-1])

    ## case of concatenation or union
    if expression.startswith("(") and expression.endswith(")"):
        ## remove external parenthesis
        inner = expression[1:-1]
        ## find balanced parenthesis
        depth = 0
        for idx, char in enumerate(inner):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == "+" and depth == 0:
                ## it is a union
                first_expression = inner[:idx]
                second_expression = inner[idx + 1 :]
                ## there are no extra symbols in the expression
                return is_regular_expression(alphabet, first_expression) and is_regular_expression(
                    alphabet, second_expression
                )

        ## case of parentheses not matching or nested expressions
        if "(" in inner or ")" in inner:
            return False

        ## it is a concatenation
        singlesymbols = [idx for idx, char in enumerate(inner) if char in extendedalphabet]
        if len(singlesymbols) == 2:
            ## only two symbols are expected
            first_expression = inner[singlesymbols[0] : singlesymbols[1]]
            second_expression = inner[singlesymbols[1] :]
            if len(first_expression) + len(second_expression) == len(inner):
                ## there are no extra symbols in the expression
                return is_regular_expression(alphabet, first_expression) and is_regular_expression(
                    alphabet, second_expression
                )

    return False
