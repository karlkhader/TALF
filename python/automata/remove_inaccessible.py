"""Remove inaccessible states from a DFA.

Transforms an DFA in the database into another DFA without inaccessible states.

 [
  {
    "name" : "a*bb*aa*",
    "representation" : {
      "K" : ["q0", "q1", "q2", "q3"],
      "A" : ["a", "b"],
      "s" : "q0",
      "F" : ["q2"],
      "t" : [["q0", "a", "q0"],
             ["q0", "b", "q1"],
             ["q1", "a", "q2"],
             ["q1", "b", "q1"],
             ["q2", "a", "q2"],
             ["q2", "b", "q3"],
             ["q3", "a", "q3"],
             ["q3", "b", "q3"]]
      }
  },
  {
    "name" : "aa*bb*",
    "representation" : {
      "K" : ["q0", "q1", "q2"],
      "A" : ["a", "b"],
      "s" : "q0",
      "F" : ["q2"],
      "t" : [["q0", "a", "q1"],
             ["q1", "a", "q1"],
             ["q1", "b", "q2"],
             ["q2", "b", "q2"]]
      }
  }
]

Furthermore, json file can contain one automaton or more. That is the reason 
why the input parameters are two: 
  IN:
      automatadatabasename : file's name without file's extension 
                             (FOr example: if it's called "dfa.json", then 
                              we'll introduce automatadatabasename as dfa)
      automatonname : automaton's name. 

  OUT:
"""

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

    ## Take initial state as old and take initial state's successors and initial 
    ## initial state as new
    accessible = _reachable_states(automaton)

    ## Obtain the new values of K, F and t
    new_transitions = [
        transition
        for transition in automaton["t"]
        if transition[0] in accessible and transition[2] in accessible
    ]

    ## Copy new automaton using the previosly defined form in sol
    new_automaton = {
        "K": sorted(accessible),
        "A": automaton["A"],
        "s": automaton["s"],
        "F": [state for state in automaton["F"] if state in accessible],
        "t": new_transitions,
    }

    ## Save in a new json file
    if output_filename:
        Path(output_filename).write_text(
            json.dumps({"name": f"{automaton_name}withoutInaccStates", "representation": new_automaton}, indent=2),
            encoding="utf-8",
        )

    return new_automaton


def _reachable_states(automaton: Automaton) -> Set[str]:
    ## Repeat the last proccess until new = old, looking at the those states' 
    ## successors that we haven't looked up yet. In that way, we would improve the 
    ## performance.
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
