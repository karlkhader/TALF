# Regular Expressions Module

This module provides functions for validating, enumerating, and matching regular expressions.

## Functions

### `is_regular_expression(alphabet, expression)`

Validates if a string is a valid regular expression over a given alphabet.

**Purpose**: Checks if an expression follows the formal definition of regular expressions (single symbols, concatenation, union, Kleene star).

**Parameters**:
- `alphabet` (str): String containing alphabet symbols
- `expression` (str): String expression to validate

**Returns**: True if valid, False otherwise

**Example**:
```python
from python.regularexpressions import is_regular_expression

# Check if expression is valid
is_regular_expression('01', '((10)01)')

# Check valid expression with union and star
is_regular_expression('01', '((10)+(01)**)')
```

---

### `enumerate_r(alphabet, expression_id=None, index_type='list', print_expression=True)`

Enumerates regular expressions over a given alphabet using Cantor encoding.

**Purpose**: Lists all regular expressions, finds the index of a specific expression, or retrieves an expression by index.

**Parameters**:
- `alphabet` (str): String containing alphabet symbols
- `expression_id` (Optional): Number of expressions to list, expression to search, or index to retrieve
- `index_type` (str): Mode ('list' to enumerate, 'index' to get by index, 'search' to find index)
- `print_expression` (bool): Whether to print expressions (default: True)

**Returns**: List of expressions, single expression, or index depending on mode

**Example**:
```python
from python.regularexpressions import enumerate_r

# List first 5 regular expressions
enumerate_r('01', 5)

# Get expression at index 10000
enumerate_r('01', 10000, 'index')

# Find index of a specific expression
enumerate_r('01', '(01)*', 'search', False)

# Get list without printing
enumerate_r('01', 5, 'list', False)
```

---

### `re_match(strings, pattern)`

Finds strings that match a given regular expression pattern (whole-string matches).

**Purpose**: Filters strings that match a pattern, supporting multiple input formats.

**Parameters**:
- `strings` (Union[str, Sequence[str]]): Strings to test (list, space-separated string, or filename)
- `pattern` (str): Regular expression pattern using '+' for union and '*' for Kleene star

**Returns**: List of matching strings

**Example**:
```python
from python.regularexpressions import re_match

# Match strings against pattern
re_match('10001 0000 100000001 11 11', '10*1')

# Match with union
re_match('10001 0000 01010100010001 11101', '(0*+1*)10*1')

# Can also use a list of strings
re_match(['10001', '0000', '111111101101'], '10*1')
```
