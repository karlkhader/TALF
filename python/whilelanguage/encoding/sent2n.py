"""
Numbering of an individual sentence.

Example:
    >>> sent2n("while X1≠0 do X1≔X1-1; X2≔X2+1 od")
    9325236374
"""

from __future__ import annotations

import re

from .cantorencoding import cantorencoding


def sent2n(sentence: str) -> int:
    """Encode a WHILE sentence into a number."""
    sentence = sentence.replace(" ", "")
    sentence = sentence.replace(":=", "≔")
    sentence = sentence.replace("!=", "≠")

    loophead = "do"
    looptail = "od"

    digits = list(re.finditer(r"\d+", sentence))
    firstnumber = int(digits[0].group(0))

    if sentence.startswith("X"):
        secondnumber = int(digits[1].group(0))
        sentencepattern = (
            sentence[: digits[0].start()] +
            sentence[digits[0].end() : digits[1].start()] +
            sentence[digits[1].end() :]
        )
        if sentencepattern == "X≔":
            return 5 * (firstnumber - 1)
        if sentencepattern == "X≔X":
            return 5 * cantorencoding(firstnumber - 1, secondnumber - 1) + 1
        if sentencepattern == "X≔X+1":
            return 5 * cantorencoding(firstnumber - 1, secondnumber - 1) + 2
        if sentencepattern == "X≔X-1":
            return 5 * cantorencoding(firstnumber - 1, secondnumber - 1) + 3
    else:
        loopbody = sentence[sentence.find(loophead) + len(loophead) : sentence.rfind(looptail)]
        from .code2n import code2n

        return 5 * cantorencoding(firstnumber - 1, code2n(loopbody)) + 4

    raise ValueError("Sentence pattern not recognized.")
