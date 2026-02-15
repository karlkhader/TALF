"""
Produce una cadena de L(G) tras una derivacion de longitud
no superior a maxderivacion. Si no se ha alcanzado una cadena, devuelve
la forma sentencial tras maxderivacion pasos. Si no se asigna valor a maxderivacion,
entonces se impone un limite de 1000 para evitar bucles infinitos.
La semilla se utiliza para la generación de números aleatorios,
si se usa sin límite para la longitud de la derivación, maxderivacion será NaN.

outputformat : "text" (default) / "string" / "stringLaTeX" / "none" 

Ejemplos:

>>> produce('oddlength', 1)
(
  {A, B},
  {@},
  {
    A → @
    A → @B
    B → @A
  },
  A
)

A => @B => @@A => @@@B => @@@@A => @@@@@B => @@@@@@A => @@@@@@@B => @@@@@@@@A =>
@@@@@@@@@B => @@@@@@@@@@A => @@@@@@@@@@@B => @@@@@@@@@@@@A => @@@@@@@@@@@@@
@@@@@@@@@@@@@

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
    ## limite en el numero de pasos de produccion para evitar bucle infinito
    max_steps = 1000

    ## leer gramatica si es el nombre
    if isinstance(grammar, str):
        loaded = load_representation(database_path, grammar)
        if loaded is None:
            raise ValueError(f"Grammar '{grammar}' not found.")
        grammar = loaded

    if num_strings is None:
        num_strings = 1
    if max_derivation is None:
        max_derivation = max_steps

    ## semilla
    if seed is None:
        seed = [random.random() for _ in range(num_strings)]
    elif len(seed) != num_strings:
        raise ValueError("number of strings and seeds not congruent...")

    ## salida en pantalla
    if output_format != "none":
        pretty_print_grammar(grammar, output_format, database_path=database_path)

    ## numero de reglas
    results: List[str] = []
    num_rules = len(grammar["P"])

    for index in range(num_strings):
        rng = random.Random(seed[index])
        print("\u2001")
        ## comenzar a derivar por el axioma
        sentential = grammar["S"]
        print(f"\n{sentential}", end="")
        for _ in range(max_derivation):
            ## la forma sentencial no contiene simbolos no terminales
            ## decidir si producir o continuar la derivacion
            if _is_terminal_string(sentential, grammar["N"]) and rng.choice([True, False]):
                results.append(sentential)
                break

            ## seleccion de las reglas en orden aleatorio
            rule_indices = list(range(num_rules))
            rng.shuffle(rule_indices)
            produced = False
            for rule_index in rule_indices:
                next_sentential = _produce_one_step(sentential, grammar["P"][rule_index], rng)
                ## comprueba variacion en la forma sentencial
                ## la regla produjo en un paso
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
    """
    Produce en un paso una cadena por aplicacion de la regla.

    Ejemplo:
          cadena = producir1paso('123123123', {'123', '456'})

    puede producir directamente '456123123', '123456123' o '123123456'.
    """
    ## conversion del antecedente de la regla en cadena
    antecedent, consequent = rule
    antecedent = "" if antecedent == "ε" else antecedent
    ## conversion del consecuente de la regla en cadena
    consequent = "" if consequent == "ε" else consequent

    ## comparar solo si el antecedente es mayor que la forma cadena
    if len(sentential) < len(antecedent):
        return sentential

    ## encuentra el antecedente en la cadena
    positions = [idx for idx in range(len(sentential) - len(antecedent) + 1) if sentential.startswith(antecedent, idx)]
    ## si el antecedente es subcadena de la cadena
    if not positions:
        return sentential

    ## selecciona una posicion donde realizar la produccion
    index = rng.choice(positions)
    ## prefijo anterior a la subcadena a sustituir
    prefix = sentential[:index]
    ## sufijo posterior a la subcadena a sustituir
    suffix = sentential[index + len(antecedent) :]
    ## concatenacion de las tres subcadenas
    return f"{prefix}{consequent}{suffix}"
