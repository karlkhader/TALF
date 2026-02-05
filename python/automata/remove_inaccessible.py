"""Remove inaccessible states from a DFA."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Set

from python.util import load_representation

Automaton = Dict[str, object]


def dfa_without_inaccessible_states(
    database_name: str,
    automaton_name: str,
    *,
    output_filename: Optional[str] = None,
) -> Automaton:
    """Return a DFA equivalent to the input, without inaccessible states."""
    automaton = load_representation(database_name, automaton_name)
    if automaton is None:
        raise ValueError(f"Automaton '{automaton_name}' not found in '{database_name}'.")

    accessible = _reachable_states(automaton)

    new_transitions = [
        transition
        for transition in automaton["t"]
        if transition[0] in accessible and transition[2] in accessible
    ]

    new_automaton = {
        "K": sorted(accessible),
        "A": automaton["A"],
        "s": automaton["s"],
        "F": [state for state in automaton["F"] if state in accessible],
        "t": new_transitions,
    }

    if output_filename:
        Path(output_filename).write_text(
            json.dumps({"name": f"{automaton_name}withoutInaccStates", "representation": new_automaton}, indent=2),
            encoding="utf-8",
        )

    return new_automaton


def _reachable_states(automaton: Automaton) -> Set[str]:
    transitions = automaton["t"]
    reachable = {automaton["s"]}
    queue = [automaton["s"]]

    while queue:
        current = queue.pop(0)
        for source, _symbol, target in transitions:
            if source == current and target not in reachable:
                reachable.add(target)
                queue.append(target)

    return reachable
