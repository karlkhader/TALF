"""
Enumerate regular expressions over a given alphabet.

# strings = enumerate_r(alphabet, expression_id, index_type, print_expression)
#
# Return regular expressions over a given alphabet.
# `alphabet` is a string with the symbols of the alphabet.
# If `expression_id` is undefined then all expressions are enumerated.
# If `expression_id` is a valid regular expression then it returns its index.
# If `index_type` == 'list' or undefined, then it generates the range 0..expression_id.
# If `index_type` == 'index', then it generates the regular expression with index `expression_id`.
# If `print_expression` is false, then the expressions are not printed out, default is true.
#
# Examples:
#
#   list all regular expressions (take your time!)
#   enumerate_r('01');
#        0   ∅
#        1   0
#        2   1
#        3   (∅∅)
#        4   (∅+∅)
#        5   ∅*
#        6   (0∅)
#        7   (0+∅)
#        8   0*
#        9   (∅0)
#       10   (∅+0)
#       11   1*
#       ...
#   
#   list the first n regular expressions
#   enumerate_r('01', 5);
#      0   ∅
#      1   0
#      2   1
#      3   (∅∅)
#      4   (∅+∅)
#      5   ∅*
# 
#   find the index of a regular expression
#   enumerate_r('01', '((∅∅)+(∅+∅))');
#   100   ((∅∅)+(∅+∅))
#
#   enumerate_r('01', '(01)*', 'search', False)
#   ans = 86
#
#   regular expression with index 10000
#   enumerate_r('01', 10000, 'index');
#   10000   ((0*+0)+(∅∅)*)
#
#   enumerate_r('01', 10000, 'index', False)
#   ans = ((0*+0)+(∅∅)*)
#
#   return the first 5 regular expressions, do not print them
#   enumerate_r('01', 5, 'list', False)
#   ans = ['∅', '0', '1', '(∅∅)', '(∅+∅)', '∅*']

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
    ## check arguments
    ## reserved symbols
    if any(symbol in alphabet for symbol in "∅()+"):
        raise ValueError("Wrong alphabet...")

    ## numeric limit
    if expression_id is not None and isinstance(expression_id, (int, float)) and expression_id < 0:
        raise ValueError("Wrong limit, it must be a positive integer...")

    ## correct index_type value
    if index_type not in ("list", "index", "search"):
        raise ValueError("Wrong index type, it must be 'list', 'index' or 'search'...")

    ## add empty set symbol to the alphabet
    symbols = ["∅", *alphabet]

    ## check possible arguments values
    ## expressions are printed by default
    if expression_id is None:
        ## enumerate regular expressions
        index_type = "list"
        max_number = None
    elif isinstance(expression_id, str):
        ## it is a regular expression
        ## return index
        if not is_regular_expression(alphabet, expression_id):
            print(f"\nSorry, '{expression_id}' is not a regular expression over the alphabet '{alphabet}'.\n")
            return None
        print(f"\n'{expression_id}' is a valid regular expression over the alphabet '{alphabet}', let's find its index...\n")
        index_type = "search"
        max_number = None
    elif index_type == "list":
        ## it is a numeric index
        ## default value: return a list of regular expressions
        max_number = int(expression_id)
    else:
        ## otherwise, it has an input value
        max_number = int(expression_id)

    ## check if only one indexed expression, or a finite or infinite list of them
    if index_type == "index":
        ## an indexed regular expression
        ##   expression_id mod 3 the index is mapped to any possible combination
        ##   0      maps onto ∅
        ##   1      maps onto alphabet(1)
        ##   ...
        ##   |Σ|    maps onto alphabet(|Σ|)
        ##   |Σ|+1  maps onto (00)
        ##   |Σ|+2  maps onto (0+0)
        ##   |Σ|+3  maps onto 0*
        ##   |Σ|+4  maps onto (10)
        ##   |Σ|+5  maps onto (1+0)
        ##   |Σ|+6  maps onto 1*
        ##   |Σ|+7  maps onto (01)
        ##   |Σ|+8  maps onto (0+1)
        ##   |Σ|+9  maps onto 2*
        ##   |Σ|+10 maps onto (20)
        ##   |Σ|+11 maps onto (2+0)
        ##   |Σ|+12 maps onto 3*
        ##   and so on, according to Cantor encoding of ℕ²
        expression = _expression_for_index(alphabet, symbols, int(expression_id))
        if print_expression:
            _prettyprint(int(expression_id), expression)
        return expression

    ## enumerate expressions (either finite or infinite)
    expression = [] if max_number is not None else None
    number_expressions = 0
    searching = index_type == "search"

    while True:
        new_expression = _expression_for_index(alphabet, symbols, number_expressions)
        if searching:
            if new_expression == expression_id:
                ## the regular expression has been found
                if print_expression:
                    _prettyprint(number_expressions, new_expression)
                return number_expressions
        else:
            ## not searching
            if max_number is not None:
                ## only if there is a limit
                expression.append(new_expression)
            if print_expression:
                _prettyprint(number_expressions, new_expression)
        number_expressions += 1
        if index_type == "list" and max_number is not None and number_expressions > max_number:
            break

    return expression


def _expression_for_index(alphabet: str, symbols: List[str], expression_id: int) -> str:
    if expression_id < len(symbols):
        ## base cases are 0..|Σ| for ∅ and the symbols of the alphabet
        return symbols[expression_id]

    ## general case include concatenation, union and Kleen star of regular expressions
    ##   mapping:
    ##     |Σ|+1 -> 0 -> (0,0)
    ##     |Σ|+2 -> 1 -> (1,0)
    ##     |Σ|+3 -> 0
    ##     |Σ|+4 -> 2 -> (0,1)
    ##     |Σ|+5 -> 3 -> (2,0)
    ##     |Σ|+6 -> 1
    index = expression_id - len(symbols)
    normalized_index = (expression_id - len(symbols)) // 3

    if index % 3 == 0:
        # union of expressions
        indexes = cantordecoding(normalized_index, 2)
        return f"({_expression_for_index(alphabet, symbols, indexes[0])}{_expression_for_index(alphabet, symbols, indexes[1])})"
    if index % 3 == 1:
        # concatenation of expressions
        indexes = cantordecoding(normalized_index, 2)
        return f"({_expression_for_index(alphabet, symbols, indexes[0])}+{_expression_for_index(alphabet, symbols, indexes[1])})"

    # Kleene star of an expression
    return f"{_expression_for_index(alphabet, symbols, normalized_index)}*"


def _prettyprint(index: int, expression: str) -> None:
    spacesymbol = " "
    print(f"{spacesymbol * (6 - len(str(index)))}{index}{spacesymbol * 3}{expression}")
