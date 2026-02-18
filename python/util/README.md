# Util Module

This module provides utility functions for string manipulation, JSON database loading, and random string generation.

## Functions

### `label_balanced_symbols(value, open_symbol, close_symbol)`

Labels balanced opening and closing symbols in a string with nesting levels.

**Purpose**: Identifies matched pairs of opening/closing symbols (like parentheses, brackets) and assigns nesting level labels.

**Parameters**:
- `value` (str): The input string to analyze
- `open_symbol` (str): The opening symbol (e.g., '(', '[')
- `close_symbol` (str): The closing symbol (e.g., ')', ']')

**Returns**: A tuple of (positions, labels) where:
- `positions` (List[int]): 1-based positions of symbols
- `labels` (List[int]): Nesting levels (positive for opening, negative for closing)

**Example**:
```python
from python.util import label_balanced_symbols

# Label parentheses
label_balanced_symbols('()()()', '(', ')')

# Label nested brackets
label_balanced_symbols('[[][]]', '[', ']')
```

---

### `load_representation(set_database_name, set_name)`

Loads the representation of a set (language or function) from a JSON database file.

**Purpose**: Retrieves automata, grammars, or other representations from JSON database files.

**Parameters**:
- `set_database_name` (str): Path to the JSON file (without .json extension)
- `set_name` (str): Name of the set/representation to retrieve

**Returns**: The representation object if found, otherwise `None`

**Example**:
```python
from python.util import load_representation

# Load a finite automaton from database
automaton = load_representation('python/automata/finiteautomata', 'a*bb*aa*')

# Load a grammar from database
grammar = load_representation('python/grammar/grammars', 'palindromes')
```

---

### `random_string(targetset, non_terminals, terminals, max_string_length=5, rng=None)`

Generates a random string according to a pattern specification.

**Purpose**: Creates random strings following Octave's convention using terminal/non-terminal alphabets and pattern types.

**Parameters**:
- `targetset` (str): Target set label ("N" for non-terminals, "T" for terminals, "V+" for non-empty strings, "V*" for any string)
- `non_terminals` (str): Available non-terminal symbols
- `terminals` (str): Available terminal symbols
- `max_string_length` (int): Maximum length for generated strings (default: 5)
- `rng` (Optional[random.Random]): Optional random generator

**Returns**: A generated string, using "ε" for empty strings

**Example**:
```python
from python.util import random_string

# Generate a random terminal string
random_string('T', 'ABCD', 'abcd')

# Generate a random non-empty string from both alphabets
random_string('V+', 'ABCD', 'abcd', max_string_length=10)

# Generate a random non-terminal string
random_string('N', 'ABCD', 'abcd')
```
