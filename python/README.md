# Python port (work in progress)

This repository comprises **scripts** (Python code) to simulate several models explained 
in the subject of Theory of Automata and Formal Languages.

You can freely download and modify the Python code.

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

## How to

In order to run the scripts, you have to import the module you want to work with. For example:

`from python.regularexpressions import *`

`from python.whilelanguage.encoding import *`

Then, you can run the examples presented inside each script.