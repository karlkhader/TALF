"""
Prints out a formatted grammar, either a string of plain ASCII or LaTeX,
returns the four elements of the grammar.
  outputformat : "text" (default) / "string" / "stringLaTeX" / "none" 

For example:

   >> prettyprint("add")
   q0 * l q1
   q0 | | q0
   q1 * | q2
   q1 | l q1
   q2 * l q3
   q2 | r q2
   q3 * l q4
   q3 | * q3
   q4 * h q4
   q4 | * q4

   >> prettyprint("add", "string");
   ({q0,q1,q2,q3,q4},q0,{|},
    {(q0,*,l),(q0,|,|),(q1,*,|),(q1,|,l),(q2,*,l),(q2,|,r),(q3,*,l),(q3,|,*),(q4,*,h),(q4,|,*)},
    {(q0,*,q1),(q0,|,q0),(q1,*,q2),(q1,|,q1),(q2,*,q3),(q2,|,q2),(q3,*,q4),(q3,|,q3),(q4,*,q4),(q4,|,q4)})

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
    database_path: str = "python/grammar/grammars",
) -> Grammar:
    """Print a formatted grammar and return the grammar object."""
    arrow = "→"
    epsilon = "ε"

    if isinstance(grammar, str):
        ## load grammar definition from file
        loaded = load_representation(database_path, grammar)
        if loaded is None:
            raise ValueError(f"Grammar '{grammar}' not found.")
        grammar = loaded

    if output_format == "none":
        return grammar

    ## print out grammar
    if output_format == "text":
        print("(")
        ## print N
        _print_alphabet(grammar["N"], indent="  ")
        ## print T
        _print_alphabet(grammar["T"], indent="  ")
        ## print P
        print("  {")
        for left, right in grammar["P"]:
            right_text = right or epsilon
            print(f"    {left} {arrow} {right_text}")
        print("  },")
        ## print S
        print(f"  {grammar['S']}")
        print(")")
    elif output_format == "LaTeX":
        ##   spaces are Em Quad (U+2001) characters here
        space = "\u2001"
        print("(")
        ## print N
        _print_alphabet(grammar["N"], indent=f"{space}{space}", wrap="\\{")
        ## print T
        _print_alphabet(grammar["T"], indent=f"{space}{space}", wrap="\\{")
        ## print P
        print(f"{space}{space}\\{{")
        for left, right in grammar["P"]:
            right_text = right or epsilon
            print(f"{space}{space}{space}{space}{left} {arrow} {right_text}")
        print(f"{space}{space}\\}},")
        ## print S
        print(f"{space}{space}{grammar['S']}")
        print(")")
    elif output_format == "string":
        print("( ", end="")
        ## print N
        n = ", ".join(grammar["N"])
        print(f"{{{n}}}, ", end="")
        ## print T
        t = ", ".join(grammar["T"])
        print(f"{{{t}}}, ", end="")
        ## print P
        rules = ", ".join(f"({left}, {right or epsilon})" for left, right in grammar["P"])
        print(f"{{ {rules} }}, ", end="")
        ## print S
        print(f"{grammar['S']} )")
    elif output_format == "stringLaTeX":
        print("$$( ", end="")
        ## print N
        n = ", ".join(grammar["N"])
        print(f"\\{{{n}\\}}, ", end="")
        ## print T
        t = ", ".join(grammar["T"])
        print(f"\\{{{t}\\}}, ", end="")
        ## print P
        rules = ", ".join(f"({left}, {right or epsilon})" for left, right in grammar["P"])
        print(f"\\{{{rules}\\}}, ", end="")
        ## print S
        print(f"{grammar['S']} )$$")
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
