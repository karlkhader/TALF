# Recursive Functions Module

This module provides functions for evaluating and manipulating primitive recursive functions.

## Functions

### `eval_rec_function(recfunction, *args)`

Evaluates a primitive recursive function with given arguments.

**Purpose**: Computes the value of recursive functions defined using initial functions (θ, σ, π), composition, primitive recursion, and minimization.

**Parameters**:
- `recfunction` (str): Recursive function expression or name from database
- `*args` (int): Variable number of integer arguments

**Returns**: Computed integer value

**Example**:
```python
from python.recursivefunctions import eval_rec_function

# Evaluate predefined functions
eval_rec_function('addition', 3, 2)

# Evaluate division
eval_rec_function('division', 4, 2)

# Evaluate using initial functions
eval_rec_function('<theta|pi^2_2>', 2)
```

**Supported notation**:
- `θ` (theta): Zero function
- `σ` (sigma): Successor function
- `π^n_i` (pi): Projection function (ith component of n arguments)
- `<f|g>`: Primitive recursion
- `μ[f]`: Minimization
- `f(g1,...,gk)`: Composition

---

### `recursive_expression(recfunction, outputformat=None)`

Returns the recursive expression of a function from the database.

**Purpose**: Expands function names into their full recursive expressions using only initial functions and operators.

**Parameters**:
- `recfunction` (str): Function name or expression
- `outputformat` (Optional[str]): Output format (None for default, 'LaTeX' for LaTeX, 'text' for text)

**Returns**: Recursive expression as a string

**Example**:
```python
from python.recursivefunctions import recursive_expression

# Get recursive expression for power function
recursive_expression('power')

# Get expression in LaTeX format
recursive_expression('<π_1^1|π_3^1>', 'LaTeX')
```

---

### `rec_to_while_ext(recfunction, num_var, *used_funcs)`

Translates a recursive function to an Extended WHILE program.

**Purpose**: Converts primitive recursive functions into equivalent WHILE-EXT programs for execution.

**Parameters**:
- `recfunction` (str): Recursive function expression or name
- `num_var` (int): Number of input variables
- `*used_funcs` (str): Optional list of already used function names

**Returns**: WHILE-EXT program as a string

**Example**:
```python
from python.recursivefunctions import rec_to_while_ext

# Convert to WHILE-EXT program
rec_to_while_ext('<π^1_1|σ(π^3_3)>', 2)

# Convert predefined function
rec_to_while_ext('predecessor', 1)
```

**Note**: The output includes the main program and all auxiliary programs (helper functions) needed for the translation.
