r"""Simulate pushdown automata computations.

Computation for a given pushdown automaton and input string.

  automatonname : name of the automaton as the label in the definition file
  inputstring   : string to be accepted or rejected
  desiredoutput : result to be expected, since the NPA is non-deterministic
                  'any'      anyone of the others (default option)
                  'accept'   accepted string
                  'reject'   rejected string in non final state, or
                  'blocked'  rejected string with blocked computation.
  formatoption  : how the output is generated
                  'text'     ASCII (default option)
                  'LaTeX'    LaTeX code for LN
  randomseed    : seed for the random numbers generator

The automaton is defined in a definition file with JSON format, like this:

 {
   "name" : "0^n1^n",
   "representation" : {
     "K" : ["q0", "q1"],
     "A" : ["0", "1"],
     "s" : "q0",
     "F" : ["q1"],
     "t" : [[["q0", "0", "ε"],["q0", "0"]],
            [["q0", "1", "0"],["q1", "ε"]],
            [["q1", "1", "0"],["q1", "ε"]]]
     }
 }

Examples

   >> pushdownautomaton("|w|0=|w|1", "00011");
   
   M = ({q0}, {0, 1}, q0, {q0}, {((q0, 0, ε), (q0, 0)), ((q0, 1, ε), (q0, 1)), ((q1, 0, 1), (q0, ε)), ((q0, 1, 0), (q0, ε))})
   
   w = 00011
   
   (q0, 00011, ε) ⊢ (q0, 0011, 0) ⊢ (q0, 011, 00) ⊢ (q0, 11, 000) ⊢ (q0, 1, 00) ⊢ (q0, ε, 0)

   w ∉ 𝓛(M) (blocked computation)


   >> pushdownautomaton("0^n1^n", "0011", "accept");

   M = ({q0, q1}, {0, 1}, q0, {q1}, {((q0, 0, ε), (q0, 0)), ((q0, 1, 0), (q1, ε)), ((q1, 1, 0), (q1, ε))})

   w = 0011
   
   (q0, 0011, ε) ⊢ (q0, 011, 0) ⊢ (q0, 11, 00) ⊢ (q1, 1, 0) ⊢ (q1, ε, ε)
   
   w ∈ 𝓛(M)


   >> pushdownautomaton("singleEstate", "a", "blocked", "LaTeX");

   $M = (\{q_0\}, \{a, b\}, \{a, b\}, q_0, \{q0\}, \{((q0, a, ε), (q0, a)), ((q0, b, a), (q0, ε))\})$

   $w = a$

   $(q0, a, \varepsilon) \vdash (q0, \varepsilon, a)$

   w ∉ 𝓛(M) (blocked computation)
"""

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

    ## load automaton definition from JSON file
    if isinstance(automaton, str):
        automaton = load_representation("python/automata/pushdownautomata", automaton)
        if automaton is None:
            raise ValueError(f"Automaton '{automaton}' not found.")

    if format_option_latex:
        language_symbol = "\\pazocal{L}"
        in_symbol = "\\in"
        not_in_symbol = "\\notin"

    _print_automaton(automaton, input_string, format_option_latex, empty_string, empty_string_latex)

    ## define initial configuration
    initial = (automaton["s"], input_string, "")
    ## perform a complete or blocked computation according to the desired output
    computation = _compute(automaton, initial, desired_output, rng)

    ## print computation
    _print_computation(computation, format_option_latex, transition_symbol, empty_string, empty_string_latex)

    ## print acceptance result
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
    ## perform the computation until the desired output is reached
    while True:
        computation: List[Configuration] = [initial]
        current = initial
        ## compute while the automaton can transit to a next configuration
        while True:
            next_config, unable = _transit(automaton["t"], current, rng)
            if unable:
                break
            current = next_config
            computation.append(current)

        ## check if the automaton has done the right thing
        outcome = _label_outcome(current, automaton)
        if desired_output in (ANY_LABEL, outcome):
            return computation


def _label_outcome(configuration: Configuration, automaton: Automaton) -> str:
    state, remaining, stack = configuration
    ## input string and stack are empty
    if not remaining and not stack:
        ## terminal state is a final state
        if state in automaton["F"]:
            return ACCEPT_LABEL
        ## terminal state is not a final state
        return REJECT_LABEL
    ## input string or stack are not empty
    return BLOCKED_LABEL


def _transit(
    transitions: Sequence[Sequence[Sequence[str]]],
    configuration: Configuration,
    rng: random.Random,
) -> Tuple[Configuration, bool]:
    ## transit from current to next configuration, if possible
    state, remaining, stack = configuration
    candidates: List[Configuration] = []

    ## check what are valid transitions from current state and string
    for transition in transitions:
        (current_state, consume_string, consume_stack), (next_state, write_stack) = transition
        consume_string = "" if consume_string == "ε" else consume_string
        consume_stack = "" if consume_stack == "ε" else consume_stack
        write_stack = "" if write_stack == "ε" else write_stack

        ## check if this transition starts from the current state
        if current_state != state:
            continue

        ## check if consumedstring is a prefix of string
        string_ok = _consume_prefix(remaining, consume_string)
        if not string_ok[0]:
            continue

        ## check if consumedstack string is a prefix of stack
        stack_ok = _consume_prefix(stack, consume_stack)
        if not stack_ok[0]:
            continue

        ## the automaton can consume symbols from the string and the stack
        ## (or there is nothing to consume)
        next_string = string_ok[1]
        ## push: add symbols at the top
        next_stack = f"{write_stack}{stack_ok[1]}"
        candidates.append((next_state, next_string, next_stack))

    if not candidates:
        return configuration, True

    ## choose one transition among the valid ones
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
    # print initial configuration
    _print_configuration(computation[0], format_option_latex, empty_string, empty_string_latex)
    # print the next configurations
    for configuration in computation[1:]:
        ## compute while the automaton can transit to a next configuration
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
    ## print formatted configuration, e.g. (q0, 0011, ε)
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
    ## print formatted automaton, e.g.
    ## M = ({q0, q1}, {0, 1}, {((q0, 0, ε), (q0, 0)), ((q0, 1, 0), (q1, ε)), ((q1, 1, 0), (q1, ε))}, q0, {q0, q1})
    ## w = 0011

    ## format states
    states = ", ".join(_format_state(state, format_option_latex) for state in automaton["K"])
    ## format input alphabet
    input_alphabet = ", ".join(automaton["I"])
    ## format stack alphabet
    stack_alphabet = ", ".join(automaton["S"])
    ## format final states
    finals = ", ".join(_format_state(state, format_option_latex) for state in automaton["F"])

    ## format transition relation
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
