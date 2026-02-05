"""Simulate pushdown automata computations."""

from __future__ import annotations

import random
from typing import Dict, List, Optional, Sequence, Tuple, Union

from python.util import load_representation

Automaton = Dict[str, object]
Configuration = Tuple[str, str, str]


ANY_LABEL = "any"
ACCEPT_LABEL = "accept"
REJECT_LABEL = "reject"
BLOCKED_LABEL = "blocked"


def pushdown_automaton(
    automaton: Union[str, Automaton],
    input_string: str,
    desired_output: str = ANY_LABEL,
    format_option: str = "text",
    random_seed: Optional[float] = None,
    *,
    return_computation: bool = False,
) -> Union[str, Tuple[str, List[Configuration]]]:
    """
    Simulate a pushdown automaton.

    Returns:
        A label describing the outcome (accept/reject/blocked).
    """
    empty_string = "ε"
    transition_symbol = "⊢"
    language_symbol = "𝓛"
    in_symbol = "∈"
    not_in_symbol = "∉"
    empty_string_latex = "\\varepsilon"
    format_option_latex = format_option == "LaTeX"

    if random_seed is not None:
        rng = random.Random(random_seed)
    else:
        rng = random.Random()

    if isinstance(automaton, str):
        automaton = load_representation("pushdownautomata", automaton)
        if automaton is None:
            raise ValueError(f"Automaton '{automaton}' not found.")

    if format_option_latex:
        language_symbol = "\\pazocal{L}"
        in_symbol = "\\in"
        not_in_symbol = "\\notin"

    _print_automaton(automaton, input_string, format_option_latex, empty_string, empty_string_latex)

    initial = (automaton["s"], input_string, "")
    computation = _compute(automaton, initial, desired_output, rng)

    _print_computation(computation, format_option_latex, transition_symbol, empty_string, empty_string_latex)

    outcome = _evaluate(computation[-1], automaton, language_symbol, in_symbol, not_in_symbol, format_option_latex)

    if return_computation:
        return outcome, computation
    return outcome


def _compute(
    automaton: Automaton,
    initial: Configuration,
    desired_output: str,
    rng: random.Random,
) -> List[Configuration]:
    while True:
        computation: List[Configuration] = [initial]
        current = initial
        while True:
            next_config, unable = _transit(automaton["t"], current, rng)
            if unable:
                break
            current = next_config
            computation.append(current)

        outcome = _label_outcome(current, automaton)
        if desired_output in (ANY_LABEL, outcome):
            return computation


def _label_outcome(configuration: Configuration, automaton: Automaton) -> str:
    state, remaining, stack = configuration
    if not remaining and not stack:
        return ACCEPT_LABEL if state in automaton["F"] else REJECT_LABEL
    return BLOCKED_LABEL


def _transit(
    transitions: Sequence[Sequence[Sequence[str]]],
    configuration: Configuration,
    rng: random.Random,
) -> Tuple[Configuration, bool]:
    state, remaining, stack = configuration
    candidates: List[Configuration] = []

    for transition in transitions:
        (current_state, consume_string, consume_stack), (next_state, write_stack) = transition
        consume_string = "" if consume_string == "ε" else consume_string
        consume_stack = "" if consume_stack == "ε" else consume_stack
        write_stack = "" if write_stack == "ε" else write_stack

        if current_state != state:
            continue

        string_ok = _consume_prefix(remaining, consume_string)
        if not string_ok[0]:
            continue

        stack_ok = _consume_prefix(stack, consume_stack)
        if not stack_ok[0]:
            continue

        next_string = string_ok[1]
        next_stack = f"{write_stack}{stack_ok[1]}"
        candidates.append((next_state, next_string, next_stack))

    if not candidates:
        return configuration, True

    return rng.choice(candidates), False


def _consume_prefix(value: str, prefix: str) -> Tuple[bool, str]:
    if not prefix:
        return True, value
    if value.startswith(prefix):
        return True, value[len(prefix) :]
    return False, value


def _print_computation(
    computation: List[Configuration],
    format_option_latex: bool,
    transition_symbol: str,
    empty_string: str,
    empty_string_latex: str,
) -> None:
    math_mode = "$" if format_option_latex else ""
    print(math_mode, end="")
    _print_configuration(computation[0], format_option_latex, empty_string, empty_string_latex)
    for configuration in computation[1:]:
        if format_option_latex:
            print(" \\vdash ", end="")
        else:
            print(f" {transition_symbol} ", end="")
        _print_configuration(configuration, format_option_latex, empty_string, empty_string_latex)
    print(math_mode)
    print()


def _evaluate(
    configuration: Configuration,
    automaton: Automaton,
    language_symbol: str,
    in_symbol: str,
    not_in_symbol: str,
    format_option_latex: bool,
) -> str:
    state, remaining, stack = configuration
    math_mode = "$" if format_option_latex else ""
    if not remaining and not stack:
        if state in automaton["F"]:
            print(f"{math_mode}w {in_symbol} {language_symbol}(M){math_mode}")
            return ACCEPT_LABEL
        print("w not accepted by M.")
        return REJECT_LABEL

    print("Blocked computation, w not accepted by M.")
    return BLOCKED_LABEL


def _print_configuration(
    configuration: Configuration,
    format_option_latex: bool,
    empty_string: str,
    empty_string_latex: str,
) -> None:
    state, remaining, stack = configuration
    remaining_display = _format_empty(remaining, format_option_latex, empty_string, empty_string_latex)
    stack_display = _format_empty(stack, format_option_latex, empty_string, empty_string_latex)
    print(f"({_format_state(state, format_option_latex)}, {remaining_display}, {stack_display})", end="")


def _format_empty(
    value: str,
    format_option_latex: bool,
    empty_string: str,
    empty_string_latex: str,
) -> str:
    if not value:
        return empty_string_latex if format_option_latex else empty_string
    if value == empty_string and format_option_latex:
        return empty_string_latex
    return value


def _format_state(state: str, format_option_latex: bool) -> str:
    if not format_option_latex:
        return state
    return f"{state[0]}_{state[1:]}"


def _print_automaton(
    automaton: Automaton,
    input_string: str,
    format_option_latex: bool,
    empty_string: str,
    empty_string_latex: str,
) -> None:
    states = ", ".join(_format_state(state, format_option_latex) for state in automaton["K"])
    input_alphabet = ", ".join(automaton["I"])
    stack_alphabet = ", ".join(automaton["S"])
    finals = ", ".join(_format_state(state, format_option_latex) for state in automaton["F"])

    transitions = []
    for (source, consume_string, consume_stack), (target, write_stack) in automaton["t"]:
        consume_string = consume_string or empty_string
        consume_stack = consume_stack or empty_string
        write_stack = write_stack or empty_string
        if format_option_latex:
            consume_string = empty_string_latex if consume_string == empty_string else consume_string
            consume_stack = empty_string_latex if consume_stack == empty_string else consume_stack
            write_stack = empty_string_latex if write_stack == empty_string else write_stack
        transitions.append(
            f"(({_format_state(source, format_option_latex)}, {consume_string}, {consume_stack}), "
            f"({_format_state(target, format_option_latex)}, {write_stack}))"
        )

    transitions_text = ", ".join(transitions)

    if format_option_latex:
        print(
            f"\n$M = (\\{{{states}\\}}, \\{{{input_alphabet}\\}}, \\{{{stack_alphabet}\\}}, "
            f"\\{{{transitions_text}\\}}, {_format_state(automaton['s'], format_option_latex)}, \\{{{finals}\\}})$"
        )
        print(f"\n$w = {input_string}$\n")
    else:
        print(
            f"\nM = ({{{states}}}, {{{input_alphabet}}}, {{{stack_alphabet}}}, {{{transitions_text}}}, "
            f"{automaton['s']}, {{{finals}}})"
        )
        print(f"\nw = {input_string}\n")
