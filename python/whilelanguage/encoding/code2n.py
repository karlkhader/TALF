"""
Encoding of a while code (CODE -> ℕ)

Example:
    >>> code2n("X1:=0;while X1!=0 do X1:=0 od")
    134
"""

from __future__ import annotations

from typing import List, Tuple

from .godelencoding import godelencoding


def code2n(whilecode: str) -> int:
    """Encode a WHILE code into a number."""
    from .sent2n import sent2n
    ## loop delimiters
    loophead = "while"
    looptail = "od"

    ## segment sentences
    ## find loops at the first nesting level (nx2 - beginning/ends by columns)
    loop = _first_level_loop(whilecode, loophead, looptail)
    if not loop:
        listsentence = _split_sentences(whilecode)
    else:
        ## find assignments where there are no loops
        listsentence = []
        firstchar = 0
        ## add assignments before the loop, and the loop itself
        for head, tail in loop:
            listsentence.extend(_split_sentences(whilecode[firstchar:head]))
            listsentence.append(whilecode[head:tail])
            firstchar = tail + 1
        ## add assignments after the last loop
        listsentence.extend(_split_sentences(whilecode[loop[-1][1] + 1 :]))

    ## make a vector with the encoding of each sentence
    sentencecode = [sent2n(sentence) for sentence in listsentence if sentence]
    ## Gödel number of the code
    return godelencoding(*sentencecode) - 1


def _split_sentences(text: str) -> List[str]:
    return [segment for segment in text.split(";") if segment]


def _first_level_loop(whilecode: str, loophead: str, looptail: str) -> List[Tuple[int, int]]:
    ## find delimiters and assign a +/- sign to heads/tails, resp.
    ##   (first character of head and last character of tail)
    heads = [idx for idx in range(len(whilecode)) if whilecode.startswith(loophead, idx)]
    tails = [idx + len(looptail) - 1 for idx in range(len(whilecode)) if whilecode.startswith(looptail, idx)]
    delimiter = [*heads, *[-tail for tail in tails]]
    if not delimiter:
        ## no loops found in the code
        return []

    ## sort absolute values in ascending order
    delimiter = sorted(delimiter, key=lambda value: abs(value))
    ## first level tails by adding signs cumulatively
    balance = 0
    tail_positions = []
    for value in delimiter:
        balance += 1 if value > 0 else -1
        if balance == 0:
            tail_positions.append(-value)
    ## first level heads positions in the while code
    head_positions = [delimiter[0]] + [delimiter[idx + 1] for idx in range(len(tail_positions) - 1)]
    ## first level loops
    return list(zip(head_positions, tail_positions))
