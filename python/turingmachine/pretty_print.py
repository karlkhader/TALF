"""
Pretty-print a Turing machine table.

Examples:
    >>> pretty_print("add")
    >>> pretty_print("add", "string")
"""

from __future__ import annotations

from typing import List, Sequence, Tuple, Union

from python.util import load_representation

Matrix = List[List[str]]


def pretty_print(
    turingmachinename: Union[str, Matrix],
    outputformat: str = "table",
    *,
    database_path: str = "python/turingmachine/turingmachines",
) -> Tuple[List[str], List[str], List[str], List[str], str, str, Matrix]:
    """Print a formatted table and return machine components."""
    if isinstance(turingmachinename, str):
        representation = load_representation(database_path, turingmachinename)
        if representation is None:
            raise ValueError(f"Turing machine '{turingmachinename}' not found.")
        matrix = representation["matrix"]
    else:
        matrix = turingmachinename

    emptysymbol = matrix[0][1]

    alphabet: List[str] = []
    for row in matrix[1:]:
        if row[1] == emptysymbol:
            break
        alphabet.append(row[1])

    states: List[str] = []
    step = len(alphabet) + 1
    for index in range(0, len(matrix), step):
        states.append(matrix[index][0])

    instructionfunction = [row[2] for row in matrix]
    nextstatefunction = [row[3] for row in matrix]
    initialstate = states[0]

    if outputformat == "string":
        states_text = ",".join(states)
        alphabet_text = ",".join(alphabet)
        instr_text = ",".join(f"({row[0]},{row[1]},{row[2]})" for row in matrix)
        next_text = ",".join(f"({row[0]},{row[1]},{row[3]})" for row in matrix)
        print(f"({{{states_text}}},{initialstate},{{{alphabet_text}}},{{{instr_text}}},{{{next_text}}})")
    elif outputformat == "stringLaTeX":
        states_text = ",".join(states)
        alphabet_text = ",".join(alphabet)
        instr_text = ",".join(f"({row[0]},{row[1]},{row[2]})" for row in matrix)
        next_text = ",".join(f"({row[0]},{row[1]},{row[3]})" for row in matrix)
        print(f"$$(\\{{{states_text}\\}},{initialstate},\\{{{alphabet_text}\\}},\\{{{instr_text}\\}},\\{{{next_text}\\}})$$")
    elif outputformat == "table":
        for row in matrix:
            print(f"{row[0]} {row[1]} {row[2]} {row[3]}")
    elif outputformat == "LaTeX":
        print("$$\\begin{array}{l c c l}")
        for row in matrix:
            state = f"{row[0][0]}_{row[0][1:]}"
            next_state = f"{row[3][0]}_{row[3][1:]}"
            print(f"{state} & {row[1]} & {row[2]} & {next_state} \\")
        print("\\end{array}$$")
    elif outputformat == "graphLaTeX":
        print(_graph_latex(states, alphabet, matrix, initialstate))
    elif outputformat == "none":
        pass
    else:
        raise ValueError("Wrong output format...")

    return states, alphabet, instructionfunction, nextstatefunction, initialstate, emptysymbol, matrix


def _graph_latex(states: List[str], alphabet: List[str], matrix: Matrix, initialstate: str) -> str:
    """Generate a simple TikZ graph representation."""
    lines = []
    lines.append("$$\\begin{tikzpicture}[shorten >=1pt,node distance=4cm,on grid]")
    lines.append(
        f"\\node[state, initial, initial text={{Start}}, initial distance=1cm] ({initialstate}) at (0,0) {{$ {initialstate} $}};"
    )
    for idx, state in enumerate(states[1:], start=1):
        lines.append(f"\\node[state] ({state}) [right of={states[idx-1]}] {{$ {state} $}};")
    lines.append("\\path")
    for row in matrix:
        source, symbol, instruction, target = row
        if instruction == "h":
            target = "H"
        lines.append(f"  ({source}) edge [] node {{$ {symbol},{instruction} $}} ({target})")
    lines.append(";")
    lines.append("\\end{tikzpicture}$$")
    return "\n".join(lines)
