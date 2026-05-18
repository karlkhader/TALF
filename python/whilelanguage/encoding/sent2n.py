"""
Numbering of an individual sentence

Example:
    >>> sent2n("while X1!=0 do X1:=X1-1; X2:=X2+1 od")
    9325236374
"""

from __future__ import annotations

import re

from .cantorencoding import cantorencoding


ASSIGNMENT_SYMBOLS = (":=", "\u2254")
COMPARISON_SYMBOLS = ("!=", "\u2260")


def _normalize_sentence(sentence: str) -> str:
    """Normalize accepted WHILE syntax to a canonical ASCII form."""
    sentence = re.sub(r"\s+", "", sentence)
    for symbol in ASSIGNMENT_SYMBOLS[1:]:
        sentence = sentence.replace(symbol, ASSIGNMENT_SYMBOLS[0])
    for symbol in COMPARISON_SYMBOLS[1:]:
        sentence = sentence.replace(symbol, COMPARISON_SYMBOLS[0])
    return sentence


def sent2n(sentence: str) -> int:
    """Encode a WHILE sentence into a number."""
    sentence = _normalize_sentence(sentence)

    ## loop delimiters
    loophead = "do"
    looptail = "od"

    ## identify all numbers in the sentence
    digits = list(re.finditer(r"\d+", sentence))
    ## extract first number
    firstnumber = int(digits[0].group(0))

    ## sort assignments and loops out
    if sentence.startswith("X"):
        ## extract second number
        secondnumber = int(digits[1].group(0))
        ## extract a pattern for the sentence (to identify it by pattern matching)
        sentencepattern = (
            sentence[: digits[0].start()] +
            sentence[digits[0].end() : digits[1].start()] +
            sentence[digits[1].end() :]
        )
        ## encode the assignment
        if sentencepattern == "X:=":
            ## type 0 assignment
            return 5 * (firstnumber - 1)
        if sentencepattern == "X:=X":
            ## type 1 assignment
            return 5 * cantorencoding(firstnumber - 1, secondnumber - 1) + 1
        if sentencepattern == "X:=X+1":
            ## type 2 assignment
            return 5 * cantorencoding(firstnumber - 1, secondnumber - 1) + 2
        if sentencepattern == "X:=X-1":
            ## type 3 assignment
            return 5 * cantorencoding(firstnumber - 1, secondnumber - 1) + 3
    else:
        ## extract loop body
        loopbody = sentence[sentence.find(loophead) + len(loophead) : sentence.rfind(looptail)]
        from .code2n import code2n

        ## encode loop
        return 5 * cantorencoding(firstnumber - 1, code2n(loopbody)) + 4

    raise ValueError("Sentence pattern not recognized.")
