# Python port (work in progress)

This directory mirrors the thematic structure in `software/` with Python modules.
The goal is to preserve a 1:1 mapping folder-by-folder so examples remain easy to
locate while transitioning from GNU Octave to Python.

## Status

- `util/`: initial helpers ported from Octave (random string generation, JSON
  representation loader, balanced symbol labeling).
- `automata/`: initial finite automaton, pushdown automaton, CFG-to-NPA,
  random automaton generation, DOT formatting, and inaccessible state removal
  utilities.
- `grammar/`: grammar utilities (pretty printing, rule typing, rule/grammar
  generation, production), plus L-system development and drawing.
- `whilelanguage/`: WHILE language utilities (execution, complexity, encoding).
- `turingmachine/`: Turing machine simulators, printers, and generators.
- `regularexpressions/`: regular-expression enumeration and matching helpers.
- `maths/`: relations utilities (union, powers, printing).
- `recursivefunctions/`: recursive function expressions, evaluation, and WHILE-EXT output.

Future folders will be added following the same naming and layout convention.
