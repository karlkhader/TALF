# Maths Module

This module provides functions for relation operations including power, union, and formatted printing.

## Functions

### `power_relation(relation, n=None)`

Computes the nth power of a relation or its transitive closure.

**Purpose**: Calculates R^n (relation composed with itself n times) or R^∞ (transitive closure) if n is not specified.

**Parameters**:
- `relation` (Sequence[Sequence[str]]): Relation as list of pairs, e.g., [("a", "b"), ("c", "c")] or ["ab", "cc"]
- `n` (Optional[int]): Power to compute (if None, computes transitive closure)

**Returns**: List of pairs representing the resulting relation

**Example**:
```python
from python.maths import power_relation

# Compute R^3
power_relation([("a", "b"), ("c", "c"), ("b", "a")], 3)

# Compute transitive closure R^∞
power_relation([("a", "b"), ("c", "c"), ("b", "a")])

# Can also use string format for pairs
power_relation(["ab", "cc", "ba"])
```

---

### `pretty_print_relation(relation, newline=False)`

Formats and displays a relation in set notation.

**Purpose**: Prints relations in the format {(a,b), (c,d)} for readability.

**Parameters**:
- `relation` (Sequence[Sequence[str]]): Relation as list of pairs
- `newline` (bool): Whether to add a newline after printing (default: False)

**Returns**: None (prints to console)

**Example**:
```python
from python.maths import pretty_print_relation

# Print relation
relation = [("a", "b"), ("c", "c")]
pretty_print_relation(relation)

# Print with newline
pretty_print_relation(relation, newline=True)
```

---

### `union_relation(relation1, relation2)`

Computes the union of two relations.

**Purpose**: Combines two relations, removing duplicates, and displays the operation.

**Parameters**:
- `relation1` (Sequence[Sequence[str]]): First relation as list of pairs
- `relation2` (Sequence[Sequence[str]]): Second relation as list of pairs

**Returns**: List of pairs representing the union

**Example**:
```python
from python.maths import union_relation

# Compute union of two relations
union_relation([("a", "b"), ("c", "c")], [("b", "a")])
```
