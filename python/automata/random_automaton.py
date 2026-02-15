"""Generate random automata for experiments.

optional: automatontype, probabilityfinalstate

Generates a random automaton and its graph in DOT format.
The automaton can be either DFA, NFA or NPDA, and it is
defined in a JSON file (for further use), like this:

  {
    "K" : ["q0", "q1", "q2"],
    "A" : ["a", "b"],
    "s" : "q0",
    "F" : ["q2"],
    "t" : [["q0", "a", "q1"],
           ["q1", "a", "q1"],
           ["q1", "b", "q2"],
           ["q2", "b", "q2"]]
  }

examples
  randomautomaton({'0', '1'}, 5)
  randomautomaton({'a', 'b', 'c'}, 8, 'NFA')
  randomautomaton({'|'}, 10, 'DFA', 0.3)
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Dict, List, Sequence


@dataclass
class RandomAutomatonOptions:
    automaton_type: str = "DFA"
    probability_final_state: float = 0.5
    mean_transitions_factor: int = 2
    mean_string_length: int = 2
    empty_string: str = "*"


def random_automaton(
    alphabet: Sequence[str],
    number_states: int,
    options: RandomAutomatonOptions | None = None,
) -> Dict[str, object]:
    """Generate a random DFA/NFA/NPDA automaton description."""
    if number_states < 1:
        raise ValueError("number_states must be >= 1")

    options = options or RandomAutomatonOptions()
    automaton_type = options.automaton_type

    # determine if DFA (default), NFA or NPDA
    if automaton_type not in {"DFA", "NFA", "NPDA"}:
        raise ValueError("automaton_type must be 'DFA', 'NFA', or 'NPDA'")

    # create list of states and final states
    states = [f"q{idx}" for idx in range(number_states)]
    final_states = [state for state in states if random.random() > options.probability_final_state]
    # make the first final if no one selected
    if not final_states:
        final_states = [states[0]]

    # create transitions
    transitions: List[List[str]] = []

    if automaton_type == "DFA":
        # DFA's transition function
        for state in states:
            for symbol in alphabet:
                transitions.append([state, symbol, random.choice(states)])
    elif automaton_type == "NFA":
        # NFA's transition application
        # transitions as a Poissonian function of number of states
        number_transitions = _poisson(options.mean_transitions_factor * len(states))
        for _ in range(number_transitions):
            transitions.append(
                [
                    random.choice(states),
                    _random_string(alphabet, options),
                    random.choice(states),
                ]
            )
    else:
        # NPDA's transition application
        # transitions as a Poissonian function of number of states
        number_transitions = _poisson(options.mean_transitions_factor * len(states))
        for _ in range(number_transitions):
            transitions.append(
                [
                    random.choice(states),
                    f"{_random_string(alphabet, options)}/{_random_string(alphabet, options)}/{_random_string(alphabet, options)}",
                    random.choice(states),
                ]
            )

    # create automaton
    automaton = {
        "K": states,
        "A": list(alphabet),
        "s": "q0",
        "F": final_states,
        "t": transitions,
    }

    return automaton


def save_random_automaton(automaton: Dict[str, object], filename: str) -> None:
    """Save an automaton to JSON."""
    with open(filename, "w", encoding="utf-8") as handle:
        json.dump(automaton, handle, ensure_ascii=False, indent=2)


def _random_string(alphabet: Sequence[str], options: RandomAutomatonOptions) -> str:
    # generate a random string
    # length of string with Poissonian distribution
    length = _poisson(options.mean_string_length)
    if length == 0:
        return options.empty_string
    # generate random indexes and get symbols from alphabet
    return "".join(random.choice(alphabet) for _ in range(length))


def _poisson(lam: float) -> int:
    if lam <= 0:
        return 0
    l = pow(2.718281828459045, -lam)
    k = 0
    p = 1.0
    while p > l:
        k += 1
        p *= random.random()
    return k - 1
