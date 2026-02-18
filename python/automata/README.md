# Automata Module

This module provides functions for simulating and manipulating finite automata and pushdown automata.

## Functions

### `finite_automaton(automaton, input_string, format_option=None, random_seed=None)`

Simulates a finite automaton (DFA/NFA) computation for a given input string.

**Purpose**: Tests whether a string is accepted by a finite automaton, showing the computation trace.

**Parameters**:
- `automaton` (Union[str, dict]): Automaton name from database or automaton structure
- `input_string` (str): The input string to test
- `format_option` (Optional[str]): Output format ('LaTeX' for LaTeX formatting, None for text)
- `random_seed` (Optional[float]): Seed for random number generator (for NFA transitions)

**Returns**: 
- `1` if string is accepted
- `0` if string is rejected (non-final state)
- `-1` if computation is blocked

**Example**:
```python
from python.automata import finite_automaton

# Test if "ab" is accepted by automaton "aa*bb*"
finite_automaton("aa*bb*", "ab")

# Use LaTeX formatting
finite_automaton("aa*bb*", "ab", "LaTeX")
```

---

### `pushdown_automaton(automaton, input_string, desired_output='any', format_option='text', random_seed=None)`

Simulates a pushdown automaton (PDA) computation for a given input string.

**Purpose**: Tests whether a string is accepted by a pushdown automaton, showing stack operations.

**Parameters**:
- `automaton` (Union[str, dict]): Automaton name from database or automaton structure
- `input_string` (str): The input string to test
- `desired_output` (str): Expected result ('any', 'accept', 'reject', 'blocked')
- `format_option` (str): Output format ('text' or 'LaTeX')
- `random_seed` (Optional[float]): Seed for random number generator

**Returns**: A label describing the outcome ('accept', 'reject', or 'blocked')

**Example**:
```python
from python.automata import pushdown_automaton

# Test if "0011" is accepted by automaton "0^n1^n"
pushdown_automaton("0^n1^n", "0011", "accept")

# Test with LaTeX formatting
pushdown_automaton("singleEstate", "a", "blocked", "LaTeX")
```

---

### `cfg_to_npa(grammar)`

Converts a context-free grammar (CFG) to a nondeterministic pushdown automaton (NPDA).

**Purpose**: Constructs a pushdown automaton that accepts the same language as the given grammar.

**Parameters**:
- `grammar` (dict): Grammar with keys 'N' (non-terminals), 'T' (terminals), 'P' (productions), 'S' (start symbol)

**Returns**: A pushdown automaton structure (dict)

**Example**:
```python
from python.automata import cfg_to_npa

# Convert a grammar to NPDA
grammar = {
    'N': ['S', 'A'],
    'T': ['a', 'b'],
    'P': [['S', 'aA'], ['A', 'b']],
    'S': 'S'
}
npda = cfg_to_npa(grammar)
```

---

### `format_automaton(automaton, output_filename=None)`

Generates a DOT/Graphviz representation of an automaton for visualization.

**Purpose**: Creates a graph visualization of the automaton in DOT format.

**Parameters**:
- `automaton` (Union[str, dict]): Automaton name from database or automaton structure
- `output_filename` (Optional[str]): Optional file to save the DOT output

**Returns**: DOT format string representation

**Example**:
```python
from python.automata import format_automaton, random_automaton

# Format an automaton from database
format_automaton('a*bb*aa*')

# Format a random automaton and save to file
fa = random_automaton(['0', '1'], 5, 'NFA')
format_automaton(fa, 'DOT_file')
```

---

### `random_automaton(alphabet, number_states, options=None)`

Generates a random automaton (DFA, NFA, or NPDA).

**Purpose**: Creates random automata for experimentation and testing.

**Parameters**:
- `alphabet` (Sequence[str]): Alphabet symbols
- `number_states` (int): Number of states in the automaton
- `options` (Optional[RandomAutomatonOptions]): Configuration options (automaton_type, probability_final_state, etc.)

**Returns**: An automaton structure (dict)

**Example**:
```python
from python.automata import random_automaton

# Generate a random DFA with 5 states
random_automaton(['0', '1'], 5)

# Generate a random NFA
random_automaton(['a', 'b', 'c'], 8, RandomAutomatonOptions(automaton_type='NFA'))

# Generate a random NPDA
random_automaton(['|'], 10, RandomAutomatonOptions(automaton_type='NPDA', probability_final_state=0.3))
```

---

### `save_random_automaton(automaton, filename)`

Saves an automaton structure to a JSON file.

**Purpose**: Persists automaton definitions for later use.

**Parameters**:
- `automaton` (dict): The automaton structure to save
- `filename` (str): Path to the output JSON file

**Example**:
```python
from python.automata import random_automaton, save_random_automaton

# Generate and save a random automaton
automaton = random_automaton(['a', 'b'], 5)
save_random_automaton(automaton, 'my_automaton.json')
```

---

### `dfa_without_inaccessible_states(database_name, automaton_name, output_filename=None)`

Removes inaccessible (unreachable) states from a DFA.

**Purpose**: Simplifies a DFA by removing states that cannot be reached from the initial state.

**Parameters**:
- `database_name` (str): Name of the automata database (without .json extension)
- `automaton_name` (str): Name of the automaton in the database
- `output_filename` (Optional[str]): Optional file to save the simplified automaton

**Returns**: A simplified automaton structure (dict)

**Example**:
```python
from python.automata import dfa_without_inaccessible_states

# Remove inaccessible states from a DFA
simplified = dfa_without_inaccessible_states('finiteautomata', 'a*bb*aa*')

# Remove and save to file
dfa_without_inaccessible_states('finiteautomata', 'a*bb*aa*', 'simplified.json')
```
