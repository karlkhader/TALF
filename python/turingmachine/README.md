# Turing Machine Module

This module provides functions for simulating, formatting, and generating Turing machines.

## Functions

### `turing_machine(turingmachinename, tape, outputformat='table')`

Simulates a deterministic Turing machine computation.

**Purpose**: Executes a Turing machine on an input tape, showing the computation trace.

**Parameters**:
- `turingmachinename` (Union[str, Matrix]): Machine name from database or transition matrix
- `tape` (str): Input tape content (head starts at the last symbol)
- `outputformat` (str): Output format ('table', 'string', 'LaTeX', 'stringLaTeX', 'graphLaTeX', 'none')

**Returns**: Tuple of (Tape object, final head position)

**Example**:
```python
from python.turingmachine import turing_machine

# Simulate the "add" Turing machine
turing_machine("add", "*|||*|||*")

# Simulate the "successorbinary" machine
turing_machine("successorbinary", "*11*")
```

---

### `pretty_print(turingmachinename, outputformat='table', database_path='python/turingmachine/turingmachines')`

Formats and displays a Turing machine transition table.

**Purpose**: Prints the Turing machine in various formats and returns machine components.

**Parameters**:
- `turingmachinename` (Union[str, Matrix]): Machine name from database or transition matrix
- `outputformat` (str): Output format ('table', 'string', 'LaTeX', 'stringLaTeX', 'graphLaTeX', 'none')
- `database_path` (str): Path to Turing machine database

**Returns**: Tuple of (states, alphabet, instruction_function, next_state_function, initial_state, empty_symbol, matrix)

**Example**:
```python
from python.turingmachine import pretty_print

# Print machine in table format
pretty_print("add")

# Print in string format
pretty_print("add", "string")

# Print in LaTeX format
pretty_print("add", "LaTeX")
```

---

### `random_turingmachine(numberstates, alphabet, emptysymbol='*', randomseed=None)`

Generates a random Turing machine transition matrix.

**Purpose**: Creates random Turing machines for experimentation and testing.

**Parameters**:
- `numberstates` (int): Number of states in the machine
- `alphabet` (str): Tape alphabet (excluding empty symbol)
- `emptysymbol` (str): Symbol representing empty cells (default: '*')
- `randomseed` (Optional[int]): Seed for random number generator

**Returns**: Transition matrix as a list of lists

**Example**:
```python
from python.turingmachine import random_turingmachine, turing_machine

# Generate a random Turing machine with 2 states
random_turingmachine(2, "|")

# Generate and simulate a random machine
matrix = random_turingmachine(3, "|")
turing_machine(matrix, "*")
```

---

### `build_egg(binarystring=DEFAULT_BINARYSTRING)`

Builds a special "egg" Turing machine from a binary string.

**Purpose**: Constructs a Turing machine that processes a specific binary pattern.

**Parameters**:
- `binarystring` (str): Binary string to encode in the machine (default: predefined 64-bit string)

**Returns**: Dictionary with 'name' and 'representation' keys containing the machine definition

**Example**:
```python
from python.turingmachine import build_egg

# Build the default egg machine
build_egg()

# Build with custom binary string
build_egg("110011")
```

---

### `check_turingmachine()`

Tests the successor Turing machine on binary numbers 0-100.

**Purpose**: Validates that the "successorbinary" machine correctly computes n+1 for all test cases.

**Parameters**: None

**Returns**: True if all tests pass, False otherwise

**Example**:
```python
from python.turingmachine import check_turingmachine

# Verify the successor machine works correctly
check_turingmachine()
```
