# WHILE Language Module

This module provides functions for simulating and analyzing WHILE programs, a simple imperative programming language.

## Functions

### `size(whileprogram)`

Counts the number of lines in a WHILE program.

**Purpose**: Determines the total number of instruction lines (assignments, while heads, and od tails).

**Parameters**:
- `whileprogram` (str): WHILE program as a string (can be a full program or just code)

**Returns**: Number of lines (int)

**Example**:
```python
from python.whilelanguage import size

# Count lines in a WHILE program
size("X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od")
```

---

### `line(whilecode, linenumber)`

Extracts a specific line from WHILE code.

**Purpose**: Retrieves the instruction at a given line number and its starting position.

**Parameters**:
- `whilecode` (str): WHILE code as a string
- `linenumber` (int): Line number to extract (1-indexed)

**Returns**: Tuple of (line_text, starting_position)

**Example**:
```python
from python.whilelanguage import line

# Get line 3 from WHILE code
line("X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od", 3)
```

---

### `go(whilecode, linenumber)`

Finds the balanced line number for while loops.

**Purpose**: For a while head, returns the line after the matching od. For an od tail, returns the matching while head. For assignments, returns 0.

**Parameters**:
- `whilecode` (str): WHILE code as a string
- `linenumber` (int): Line number to check

**Returns**: Balanced line number (int)

**Example**:
```python
from python.whilelanguage import go

# Find matching od for while at line 2
go("X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od", 2)
```

---

### `next_configuration(whileprogram, configuration)`

Computes the next configuration from the current configuration.

**Purpose**: Executes one step of the WHILE program, updating the line number and variable values.

**Parameters**:
- `whileprogram` (str): Full WHILE program with arity specification
- `configuration` (List[int]): Current configuration as [line_number, var1, var2, ...]

**Returns**: Next configuration as a list of integers

**Example**:
```python
from python.whilelanguage import next_configuration

# Compute next configuration
next_configuration("(1, X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od)", [1, 3, 0])
```

---

### `cal(whileprogram, inputvariables, steps)`

Returns the configuration after N execution steps.

**Purpose**: Executes a WHILE program for a specified number of steps.

**Parameters**:
- `whileprogram` (str): Full WHILE program with arity specification
- `inputvariables` (Union[int, List[int]]): Input variable value(s)
- `steps` (int): Number of steps to execute

**Returns**: Configuration after N steps as a list of integers

**Example**:
```python
from python.whilelanguage import cal

# Get configuration after 3 steps
cal("(1, X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od)", 3, 1)

# Get initial configuration (0 steps)
cal("(1, X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od)", 3, 0)
```

---

### `t_steps(whileprogram, inputvariables)`

Calculates the temporal complexity (number of steps until halting).

**Purpose**: Determines how many execution steps are needed for the program to halt.

**Parameters**:
- `whileprogram` (str): Full WHILE program with arity specification
- `inputvariables` (List[int]): Input variable values

**Returns**: Number of steps until halting (int)

**Example**:
```python
from python.whilelanguage import t_steps

# Calculate steps to halt
t_steps("(1, X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od)", [3])
```

---

### `f_function(whileprogram, inputvariables)`

Computes the mathematical function result of a WHILE program.

**Purpose**: Executes a WHILE program until halting and returns the value of X1.

**Parameters**:
- `whileprogram` (str): Full WHILE program with arity specification
- `inputvariables` (List[int]): Input variable values

**Returns**: Value of X1 after halting (int)

**Example**:
```python
from python.whilelanguage import f_function

# Compute function value
f_function("(1, X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od)", [10])
```

---

### `f_emulation(whileprogram, *args)`

Translates and emulates WHILE code as Python for faster execution.

**Purpose**: Converts WHILE programs to Python code and executes them natively for improved performance.

**Parameters**:
- `whileprogram` (str): WHILE program string or name from database
- `*args` (int): Variable number of input arguments

**Returns**: Value of X1 after execution (int)

**Example**:
```python
from python.whilelanguage import f_emulation

# Emulate WHILE program directly
f_emulation("(1, X2≔X1; while X2≠0 do X1≔X1+1; X2≔X2-1 od)", 3)

# Load and emulate from database
f_emulation("product", 3, 3)
```
