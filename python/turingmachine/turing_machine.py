"""
Computation for a given Turing machine and tape expression.

The machine behaves deterministically and it is defined
in a JSON file, like this:

{
  "matrix" : [["q0", "*", "*", "q1"],
              ["q0", "|", "l", "q1"],
              ["q1", "*", "r", "q1"],
              ["q1", "|", "h", "q1"]]
}

It is assumed that q0 is the initial state, that the cell with index
0 is the first symbol in the input tape and that the head points to
the last symbol in the input tape.

It works in ANSI/VT100 terminals, where colors are allows as scape
sequences.

The outputformat values can be checked in the prettyprint script.

Examples:
    >>> turing_machine("add", "*|||*|||*")
    ({q0,q1,q2,q3,q4},q0,{|},
     {(q0,*,l),(q0,|,|),(q1,*,|),(q1,|,l),(q2,*,l),(q2,|,r),(q3,*,l),(q3,|,*),(q4,*,h),(q4,|,*)},
     {(q0,*,q1),(q0,|,q0),(q1,*,q2),(q1,|,q1),(q2,*,q3),(q2,|,q2),(q3,*,q4),(q3,|,q3),(q4,*,q4),(q4,|,q4)})
    
    (q0, *|||*|||*, 9) ⊢ (q1, *|||*|||*, 8) ⊢ (q1, *|||*|||*, 7) ⊢ (q1, *|||*|||*, 6) ⊢ (q1, *|||*|||*, 5) ⊢ 
    (q2, *|||||||*, 5) ⊢ (q2, *|||||||*, 6) ⊢ (q2, *|||||||*, 7) ⊢ (q2, *|||||||*, 8) ⊢ (q2, *|||||||*, 9) ⊢ 
    (q3, *|||||||*, 8) ⊢ (q3, *||||||**, 8) ⊢ (q4, *||||||**, 7) ⊢ (q4, *|||||***, 7)
    
    >>> turing_machine("successorbinary", "*11*")
    q0 * l q1
    q0 0 0 q0
    q0 1 1 q0
    q1 * 1 q3
    q1 0 1 q2
    q1 1 l q1
    q2 * h q3
    q2 0 0 q2
    q2 1 r q2
    q3 * l q4
    q3 0 0 q0
    q3 1 r q4
    q4 * h q4
    q4 0 r q4
    q4 1 0 q4
    
    (q0, *11*, 4) ⊢ (q1, *11*, 3) ⊢ (q1, *11*, 2) ⊢ (q1, *11*, 1) ⊢ 
    (q3, 111*, 1) ⊢ (q4, 111*, 2) ⊢ (q4, 101*, 2) ⊢ (q4, 101*, 3) ⊢
    (q4, 100*, 3) ⊢ (q4, 100*, 4)
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

    ## get the machine elements and print it out
    states, alphabet, instructionfunction, nextstatefunction, initialstate, emptysymbol, matrix = pretty_print(
        turingmachinename, outputformat
    )

    ## define initial head position
    headposition = len(tape)

    ## tape stores the expression and the integer index to the first symbol
    tape_state = Tape(content=list(tape), index_first_cell=1)
    ## the first cell of the tape is indexed as 1, this can shift to negative integers

    ## define initial configuration
    current_state = initialstate

    if outputformat != "none":
        print("\u2001")
        _print_configuration(current_state, tape_state, headposition, outputformat)

    steps = 0
    while True:
        ## compute while a transition can be done
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

    ## return tape and cell
    return tape_state, headposition


def _transit(
    matrix: Matrix,
    current_state: str,
    tape: Tape,
    headposition: int,
    emptysymbol: str,
) -> Tuple[str, int, Tape, bool]:
    ## transit from current to next configuration, if possible
    
    ## search for the selected line
    instruction, nextstate = _currentline(matrix, current_state, _tapeexpression(tape, headposition))
    if instruction is None:
        return current_state, headposition, tape, True

    ## execute instruction
    ## 'right' instruction
    if instruction == "r":
        headposition += 1
        ## check boundary condition for the tape
        lastcell = len(tape.content) + tape.index_first_cell - 1
        if headposition > lastcell:
            ## add emptysymbol to the right
            tape.content.append(emptysymbol)
    ## 'left' instruction
    elif instruction == "l":
        headposition -= 1
        ## check boundary condition for the tape
        if headposition < tape.index_first_cell:
            ## add emptysymbol to the left
            tape.content.insert(0, emptysymbol)
            tape.index_first_cell -= 1
    ## 'halt' instruction
    elif instruction == "h":
        return nextstate, headposition, tape, True
    ## 'write' instruction
    else:
        _write_symbol(tape, headposition, instruction)
        ## add empty symbol to the left if the first symbol is not empty
        if tape.content[0] != emptysymbol:
            tape.content.insert(0, emptysymbol)
            tape.index_first_cell -= 1
        ## add empty symbol to the right if the last symbol is not empty
        if tape.content[-1] != emptysymbol:
            tape.content.append(emptysymbol)

    return nextstate, headposition, tape, False


def _currentline(matrix: Matrix, state: str, symbol: str) -> Tuple[str | None, str | None]:
    for row in matrix:
        if row[0] == state and row[1] == symbol:
            return row[2], row[3]
    return None, None


def _tapeexpression(tape: Tape, headposition: int) -> str:
    ## index is mapped as to match current cell with respect to the first cell
    ## example:
    ##     *|||*  indexfirstcell =  1
    ##     12345  tape(5) = 5 - 1 + 1 = 5
    ##   ***|||*  indexfirstcell = -1
    ##  -1012345  tape(5) = 5 + 1 + 1 = 7
    return tape.content[headposition - tape.index_first_cell]


def _write_symbol(tape: Tape, position: int, symbol: str) -> None:
    tape.content[position - tape.index_first_cell] = symbol


def _print_configuration(state: str, tape: Tape, headposition: int, outputformat: str) -> None:
    ## print formatted configuration
    head_index = headposition - tape.index_first_cell
    before = "".join(tape.content[:head_index])
    current = tape.content[head_index]
    after = "".join(tape.content[head_index + 1 :])
    if outputformat == "none":
        return
    underline = f"\033[4m{current}\033[0m"
    sys.stdout.write(f"({state}, {before}{underline}{after}, {headposition})")
