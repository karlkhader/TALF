"""
Produce strings from a grammar.

Examples:
    >>> produce("oddlength", 1)
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional, Sequence, Tuple, Union

from python.util import load_representation
from .pretty_print_grammar import pretty_print_grammar

Grammar = Dict[str, object]


def produce(
    grammar: Union[str, Grammar],
    num_strings: Optional[int] = None,
    max_derivation: Optional[int] = None,
    output_format: str = "text",
    seed: Optional[Sequence[float]] = None,
    *,
    database_path: str = "python/grammar/grammars",
) -> List[str]:
    """
    Produce strings in L(G) after derivations bounded by max_derivation.

    Returns the list of produced strings (or sentential forms if derivation stops).
    """
    max_steps = 1000

    if isinstance(grammar, str):
        loaded = load_representation(database_path, grammar)
        if loaded is None:
            raise ValueError(f"Grammar '{grammar}' not found.")
        grammar = loaded

    if num_strings is None:
        num_strings = 1
    if max_derivation is None:
        max_derivation = max_steps

    if seed is None:
        seed = [random.random() for _ in range(num_strings)]
    elif len(seed) != num_strings:
        raise ValueError("number of strings and seeds not congruent...")

    if output_format != "none":
        pretty_print_grammar(grammar, output_format, database_path=database_path)

    results: List[str] = []
    num_rules = len(grammar["P"])

    for index in range(num_strings):
        rng = random.Random(seed[index])
        print("\u2001")
        sentential = grammar["S"]
        print(f"\n{sentential}", end="")
        for _ in range(max_derivation):
            if _is_terminal_string(sentential, grammar["N"]) and rng.choice([True, False]):
                results.append(sentential)
                break

            rule_indices = list(range(num_rules))
            rng.shuffle(rule_indices)
            produced = False
            for rule_index in rule_indices:
                next_sentential = _produce_one_step(sentential, grammar["P"][rule_index], rng)
                if next_sentential != sentential:
                    sentential = next_sentential
                    print(f" => {sentential}", end="")
                    produced = True
                    break

            if not produced:
                results.append(sentential)
                break
        else:
            results.append(sentential)

        print()

    return results


def _is_terminal_string(sentential: str, non_terminals: Sequence[str]) -> bool:
    return all(symbol not in sentential for symbol in non_terminals)


def _produce_one_step(sentential: str, rule: Sequence[str], rng: random.Random) -> str:
    antecedent, consequent = rule
    antecedent = "" if antecedent == "ε" else antecedent
    consequent = "" if consequent == "ε" else consequent

    if len(sentential) < len(antecedent):
        return sentential

    positions = [idx for idx in range(len(sentential) - len(antecedent) + 1) if sentential.startswith(antecedent, idx)]
    if not positions:
        return sentential

    index = rng.choice(positions)
    prefix = sentential[:index]
    suffix = sentential[index + len(antecedent) :]
    return f"{prefix}{consequent}{suffix}"
