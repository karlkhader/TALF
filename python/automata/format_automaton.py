"""Format automata into DOT/Graphviz representations."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Union

from python.util import load_representation

Automaton = Dict[str, object]


def format_automaton(automaton: Union[str, Automaton], output_filename: Optional[str] = None) -> str:
    """
    Generate a Dot/Graphviz representation of an automaton.

    Returns the DOT output and optionally writes it to a file.
    """
    empty_string = "ε"
    font = "times-italic"

    if isinstance(automaton, str):
        description = automaton
        automaton = load_representation("finiteautomata", description)
        if automaton is None:
            automaton = load_representation("pushdownautomata", description)
        if automaton is None:
            raise ValueError(f"Automaton '{description}' not found in databases.")

    dot_lines = [
        "<center>",
        "<DOT>",
        "digraph finite_state_machine {",
        "  rankdir=LR;",
        f"  size=\"{len(automaton['K'])}\"",
        f"  node [fontname=\"{font}\"];",
        f"  edge [fontname=\"{font}\"];",
        "  node [shape = point]; qi",
    ]

    if automaton["F"]:
        finals = ",".join(automaton["F"])
        dot_lines.append(f"  node [shape = doublecircle]; {finals};")

    dot_lines.extend(
        [
            "  node [shape = circle];",
            f"  qi -> {automaton['s']};",
        ]
    )

    for transition in automaton["t"]:
        if len(transition) == 3:
            source, consumed, target = transition
            label = consumed or empty_string
        else:
            (source, consumed_string, consumed_stack), (target, write_stack) = transition
            consumed_string = consumed_string or empty_string
            consumed_stack = consumed_stack or empty_string
            write_stack = write_stack or empty_string
            label = f"{consumed_string}/{consumed_stack}/{write_stack}"
        dot_lines.append(f"  {source} -> {target} [ label = \"{label}\" ];")

    dot_lines.extend(["}", "</DOT>", "</center>"])

    dot_output = "\n".join(dot_lines)

    if output_filename:
        Path(output_filename).write_text(dot_output, encoding="utf-8")

    return dot_output
