"""Simulate finite automata computations."""

from __future__ import annotations

import random
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

from python.util import load_representation

Automaton = Dict[str, object]
Configuration = Tuple[str, str]


def finite_automaton(
    automaton: Union[str, Automaton],
    input_string: str,
    format_option: Optional[str] = None,
    random_seed: Optional[float] = None,
    *,
    return_computation: bool = False,
) -> Union[int, Tuple[int, List[Configuration]]]:
    """
    Simulate a finite automaton (DFA/NFA) for a given input string.

    Returns:
        1 if accepted, 0 if rejected in non-final state, -1 if blocked.
    """
    languagesymbol = "𝓛"
    open_bracket = "{"
    close_bracket = "}"
    empty_string = "ε"
    transition_symbol = "⊢"
    format_option_latex = format_option == "LaTeX"

    if random_seed is None:
        random_seed = random.random()

    if isinstance(automaton, str):
        automaton = load_representation("python/automata/finiteautomata", automaton)
        if automaton is None:
            raise ValueError(f"Automaton '{automaton}' not found.")

    rng = random.Random(random_seed)

    _print_automaton(automaton, input_string, format_option_latex, open_bracket, close_bracket)

    computation: List[Configuration] = []
    current = (automaton["s"], input_string)
    computation.append(current)
    _print_configuration(current, input_string, format_option_latex, empty_string)

    while True:
        next_configuration, unable = _transit(automaton["t"], current, rng)
        if unable:
            break
        print(f" {transition_symbol} ", end="")
        _print_configuration(next_configuration, empty_string, format_option_latex, empty_string)
        current = next_configuration
        computation.append(current)

    print()

    result = _evaluate_result(current, automaton, languagesymbol, format_option_latex)

    if return_computation:
        return result, computation
    return result


def _evaluate_result(
    configuration: Configuration,
    automaton: Automaton,
    language_symbol: str,
    format_option_latex: bool,
) -> int:
    state, remaining = configuration
    if not remaining:
        if state in automaton["F"]:
            print(f"\nw ∈ {language_symbol}(M)")
            return 1
        if _is_dfa(automaton):
            print(f"\nw ∉ {language_symbol}(M)")
        else:
            print("w not accepted by M.")
        return 0

    print("Blocked computation, w not accepted by M.")
    return -1


def _is_dfa(automaton: Automaton) -> bool:
    states = automaton["K"]
    alphabet = automaton["A"]
    coverage = {state: {symbol: 0 for symbol in alphabet} for state in states}
    for source, symbol, _target in automaton["t"]:
        if source in coverage and symbol in coverage[source]:
            coverage[source][symbol] = 1
    return all(all(symbols.values()) for symbols in coverage.values())


def _transit(
    transitions: Sequence[Sequence[str]],
    configuration: Configuration,
    rng: random.Random,
) -> Tuple[Configuration, bool]:
    state, remaining = configuration
    candidates: List[Configuration] = []

    for source, consumed, target in transitions:
        if source != state:
            continue
        if consumed:
            if remaining.startswith(consumed):
                next_string = remaining[len(consumed) :]
                candidates.append((target, next_string))
        else:
            if rng.random() > 0.5:
                candidates.append((target, remaining))

    if not candidates:
        return configuration, True

    return rng.choice(candidates), False


def _print_configuration(
    configuration: Configuration,
    input_string: str,
    format_option_latex: bool,
    empty_string: str,
) -> None:
    state, remaining = configuration
    if not remaining:
        remaining = "\\varepsilon" if format_option_latex else empty_string
    formatted_state = _format_state(state, format_option_latex)
    print(f"({formatted_state}, {remaining})", end="")


def _format_state(state: str, format_option_latex: bool) -> str:
    if not format_option_latex:
        return state
    return f"{state[0]}_{state[1:]}"


def _print_automaton(
    automaton: Automaton,
    input_string: str,
    format_option_latex: bool,
    open_bracket: str,
    close_bracket: str,
) -> None:
    states = ", ".join(_format_state(state, format_option_latex) for state in automaton["K"])
    alphabet = ", ".join(automaton["A"])
    final_states = ", ".join(_format_state(state, format_option_latex) for state in automaton["F"])

    transitions = []
    for source, consumed, target in automaton["t"]:
        consumed_value = consumed or "ε"
        transitions.append(
            f"({_format_state(source, format_option_latex)}, {consumed_value}, {_format_state(target, format_option_latex)})"
        )
    transitions_text = ", ".join(transitions)

    if format_option_latex:
        print(
            f"\n$M = (\\{{{states}\\}}, \\{{{alphabet}\\}}, \\{{{transitions_text}\\}}, "
            f"{_format_state(automaton['s'], format_option_latex)}, \\{{{final_states}\\}})$"
        )
        print(f"\n$w = {input_string}$\n")
    else:
        print(
            f"\nM = ({open_bracket}{states}{close_bracket}, {open_bracket}{alphabet}{close_bracket}, "
            f"{open_bracket}{transitions_text}{close_bracket}, {automaton['s']}, "
            f"{open_bracket}{final_states}{close_bracket})"
        )
        print(f"\nw = {input_string}\n")
