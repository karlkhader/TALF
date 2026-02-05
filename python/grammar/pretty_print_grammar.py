"""
Pretty-print a grammar.

Examples:
    >>> pretty_print_grammar("oddlength")
    >>> pretty_print_grammar("oddlength", output_format="string")
"""

from __future__ import annotations

from typing import Dict, List, Optional, Union

from python.util import load_representation

Grammar = Dict[str, object]


def pretty_print_grammar(
    grammar: Union[str, Grammar],
    output_format: str = "text",
    *,
    database_path: str = "software/grammar/grammars",
) -> Grammar:
    """Print a formatted grammar and return the grammar object."""
    arrow = "→"
    epsilon = "ε"

    if isinstance(grammar, str):
        loaded = load_representation(database_path, grammar)
        if loaded is None:
            raise ValueError(f"Grammar '{grammar}' not found.")
        grammar = loaded

    if output_format == "none":
        return grammar

    if output_format == "text":
        print("(")
        _print_alphabet(grammar["N"], indent="  ")
        _print_alphabet(grammar["T"], indent="  ")
        print("  {")
        for left, right in grammar["P"]:
            right_text = right or epsilon
            print(f"    {left} {arrow} {right_text}")
        print("  },")
        print(f"  {grammar['S']}")
        print(")")
    elif output_format == "LaTeX":
        space = "\u2001"
        print("(")
        _print_alphabet(grammar["N"], indent=f"{space}{space}", wrap="\\{")
        _print_alphabet(grammar["T"], indent=f"{space}{space}", wrap="\\{")
        print(f"{space}{space}\\{{")
        for left, right in grammar["P"]:
            right_text = right or epsilon
            print(f"{space}{space}{space}{space}{left} {arrow} {right_text}")
        print(f"{space}{space}\\}},")
        print(f"{space}{space}{grammar['S']}")
        print(")")
    elif output_format == "string":
        n = ", ".join(grammar["N"])
        t = ", ".join(grammar["T"])
        rules = ", ".join(f"({left}, {right or epsilon})" for left, right in grammar["P"])
        print(f"( {{{n}}}, {{{t}}}, {{ {rules} }}, {grammar['S']} )")
    elif output_format == "stringLaTeX":
        n = ", ".join(grammar["N"])
        t = ", ".join(grammar["T"])
        rules = ", ".join(f"({left}, {right or epsilon})" for left, right in grammar["P"])
        print(f"$$( \\{{{n}\\}}, \\{{{t}\\}}, \\{{{rules}\\}}, {grammar['S']} )$$")
    else:
        raise ValueError("Wrong output format...")

    return grammar


def _print_alphabet(symbols: List[str], indent: str, wrap: str = "{") -> None:
    if not symbols:
        print(f"{indent}{wrap}}}")
        return
    opening = wrap
    closing = "}" if wrap == "{" else "\\}"
    items = ", ".join(symbols)
    print(f"{indent}{opening}{items}{closing},")
