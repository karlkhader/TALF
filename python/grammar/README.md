# Grammar Module

This module provides functions for creating, analyzing, and manipulating context-free grammars according to the Chomsky hierarchy.

## Functions

### `make_grammar(type_grammar, N=None, T=None)`

Generates a random grammar of a specified Chomsky hierarchy type (0-3).

**Purpose**: Creates grammars for experimentation and testing, ensuring at least one rule of the specified type.

**Parameters**:
- `type_grammar` (int): Chomsky hierarchy type (0=phrase structure, 1=context-sensitive, 2=context-free, 3=regular)
- `N` (Optional[Iterable[str]]): Non-terminal alphabet (default: A-G)
- `T` (Optional[Iterable[str]]): Terminal alphabet (default: a-g)

**Returns**: A grammar structure (dict) with keys 'N', 'T', 'P', and 'S'

**Example**:
```python
from python.grammar import make_grammar

# Generate a context-free grammar (type 2)
grammar = make_grammar(2)

# Generate a type 0 grammar with custom alphabets
grammar = make_grammar(0, N='ABC', T='01')
```

---

### `make_rule(type_rule, N=None, T=None, show_rule=True)`

Generates a random rule of a specified Chomsky hierarchy type.

**Purpose**: Creates individual grammar rules conforming to the Chomsky hierarchy classification.

**Parameters**:
- `type_rule` (int): Rule type (0-3)
- `N` (Optional[Iterable[str]]): Non-terminal alphabet (default: A-G)
- `T` (Optional[Iterable[str]]): Terminal alphabet (default: a-g)
- `show_rule` (bool): Whether to print the rule (default: True)

**Returns**: A Rule object with 'side' (tuple of left and right parts) and 'type' attributes

**Example**:
```python
from python.grammar import make_rule

# Generate a context-free rule (type 2)
rule = make_rule(2)

# Generate a type 0 rule with custom alphabets
rule = make_rule(0, N='ABC', T='01')
```

---

### `rule_type(rule, N=None, T=None)`

Determines the Chomsky hierarchy type of a grammar rule.

**Purpose**: Classifies rules as phrase structure (0), context-sensitive (1), context-free (2), or regular (3).

**Parameters**:
- `rule` (Sequence[str]): A rule as a list of two strings [left_side, right_side]
- `N` (Optional[Iterable[str]]): Non-terminal alphabet (default: A-G)
- `T` (Optional[Iterable[str]]): Terminal alphabet (default: a-g)

**Returns**: A RuleType object with 'number' (0-3) and 'name' attributes

**Example**:
```python
from python.grammar import rule_type

# Check type of a context-free rule
rt = rule_type(['A', 'BC'])

# Check type with custom alphabets
rt = rule_type(['BA1', '110'], N='AB', T='01')
```

---

### `pretty_print_grammar(grammar, output_format='text', database_path='python/grammar/grammars')`

Formats and displays a grammar in various output styles.

**Purpose**: Prints grammars in human-readable or LaTeX format for documentation and presentation.

**Parameters**:
- `grammar` (Union[str, dict]): Grammar name from database or grammar structure
- `output_format` (str): Output format ('text', 'string', 'LaTeX', 'stringLaTeX', 'none')
- `database_path` (str): Path to grammar database (default: 'python/grammar/grammars')

**Returns**: The grammar structure (dict)

**Example**:
```python
from python.grammar import pretty_print_grammar

# Print a grammar from database
pretty_print_grammar('oddlength')

# Print in string format
pretty_print_grammar('oddlength', output_format='string')

# Print in LaTeX format
pretty_print_grammar('palindromes', output_format='LaTeX')
```

---

### `produce(grammar, num_strings=None, max_derivation=None, output_format='text', seed=None, database_path='python/grammar/grammars')`

Generates strings in L(G) through bounded derivations.

**Purpose**: Produces strings by applying grammar rules, showing the derivation process.

**Parameters**:
- `grammar` (Union[str, dict]): Grammar name from database or grammar structure
- `num_strings` (Optional[int]): Number of strings to generate (default: 1)
- `max_derivation` (Optional[int]): Maximum derivation steps (default: 1000)
- `output_format` (str): Output format ('text', 'string', 'LaTeX', 'stringLaTeX', 'none')
- `seed` (Optional[Sequence[float]]): Random seeds for each string
- `database_path` (str): Path to grammar database (default: 'python/grammar/grammars')

**Returns**: List of produced strings (or sentential forms if derivation stops)

**Example**:
```python
from python.grammar import produce

# Generate one string from grammar
produce('oddlength', 1)

# Generate multiple strings with max derivation length
produce('palindromes', num_strings=3, max_derivation=20)
```
