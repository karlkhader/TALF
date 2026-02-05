"""
Computation for a given Turing machine and tape expression.

Examples:
    >>> turing_machine("add", "*|||*|||*")
    >>> turing_machine("successorbinary", "*11*")
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from .pretty_print import pretty_print, Matrix


@dataclass
class Tape:
    content: List[str]
    index_first_cell: int


def turing_machine(
    turingmachinename: Union[str, Matrix],
    tape: str,
    outputformat: str = "table",
) -> Tuple[Tape, int]:
    """Simulate a deterministic Turing machine and return tape and head position."""
    transitionsymbol = "⊢"

    states, alphabet, instructionfunction, nextstatefunction, initialstate, emptysymbol, matrix = pretty_print(
        turingmachinename, outputformat
    )

    headposition = len(tape)

    tape_state = Tape(content=list(tape), index_first_cell=1)

    current_state = initialstate

    if outputformat != "none":
        print("\u2001")
        _print_configuration(current_state, tape_state, headposition, outputformat)

    steps = 0
    while True:
        next_state, headposition, tape_state, unable = _transit(
            matrix, current_state, tape_state, headposition, emptysymbol
        )
        if unable:
            break
        current_state = next_state
        if outputformat != "none":
            print(f" {transitionsymbol} ", end="")
            _print_configuration(current_state, tape_state, headposition, outputformat)

    if outputformat != "none":
        print()

    return tape_state, headposition


def _transit(
    matrix: Matrix,
    current_state: str,
    tape: Tape,
    headposition: int,
    emptysymbol: str,
) -> Tuple[str, int, Tape, bool]:
    instruction, nextstate = _currentline(matrix, current_state, _tapeexpression(tape, headposition))
    if instruction is None:
        return current_state, headposition, tape, True

    if instruction == "r":
        headposition += 1
        lastcell = len(tape.content) + tape.index_first_cell - 1
        if headposition > lastcell:
            tape.content.append(emptysymbol)
    elif instruction == "l":
        headposition -= 1
        if headposition < tape.index_first_cell:
            tape.content.insert(0, emptysymbol)
            tape.index_first_cell -= 1
    elif instruction == "h":
        return nextstate, headposition, tape, True
    else:
        _write_symbol(tape, headposition, instruction)
        if tape.content[0] != emptysymbol:
            tape.content.insert(0, emptysymbol)
            tape.index_first_cell -= 1
        if tape.content[-1] != emptysymbol:
            tape.content.append(emptysymbol)

    return nextstate, headposition, tape, False


def _currentline(matrix: Matrix, state: str, symbol: str) -> Tuple[str | None, str | None]:
    for row in matrix:
        if row[0] == state and row[1] == symbol:
            return row[2], row[3]
    return None, None


def _tapeexpression(tape: Tape, headposition: int) -> str:
    return tape.content[headposition - tape.index_first_cell]


def _write_symbol(tape: Tape, position: int, symbol: str) -> None:
    tape.content[position - tape.index_first_cell] = symbol


def _print_configuration(state: str, tape: Tape, headposition: int, outputformat: str) -> None:
    head_index = headposition - tape.index_first_cell
    before = "".join(tape.content[:head_index])
    current = tape.content[head_index]
    after = "".join(tape.content[head_index + 1 :])
    if outputformat == "none":
        return
    underline = f"\033[4m{current}\033[0m"
    sys.stdout.write(f"({state}, {before}{underline}{after}, {headposition})")
