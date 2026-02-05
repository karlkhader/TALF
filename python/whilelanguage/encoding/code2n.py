"""
Encoding of a WHILE code (CODE -> ℕ).

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
    loophead = "while"
    looptail = "od"

    loop = _first_level_loop(whilecode, loophead, looptail)
    if not loop:
        listsentence = _split_sentences(whilecode)
    else:
        listsentence = []
        firstchar = 0
        for head, tail in loop:
            listsentence.extend(_split_sentences(whilecode[firstchar:head]))
            listsentence.append(whilecode[head:tail])
            firstchar = tail + 1
        listsentence.extend(_split_sentences(whilecode[loop[-1][1] + 1 :]))

    sentencecode = [sent2n(sentence) for sentence in listsentence if sentence]
    return godelencoding(*sentencecode) - 1


def _split_sentences(text: str) -> List[str]:
    return [segment for segment in text.split(";") if segment]


def _first_level_loop(whilecode: str, loophead: str, looptail: str) -> List[Tuple[int, int]]:
    heads = [idx for idx in range(len(whilecode)) if whilecode.startswith(loophead, idx)]
    tails = [idx + len(looptail) - 1 for idx in range(len(whilecode)) if whilecode.startswith(looptail, idx)]
    delimiter = [*heads, *[-tail for tail in tails]]
    if not delimiter:
        return []

    delimiter = sorted(delimiter, key=lambda value: abs(value))
    balance = 0
    tail_positions = []
    for value in delimiter:
        balance += 1 if value > 0 else -1
        if balance == 0:
            tail_positions.append(-value)
    head_positions = [delimiter[0]] + [delimiter[idx + 1] for idx in range(len(tail_positions) - 1)]
    return list(zip(head_positions, tail_positions))
