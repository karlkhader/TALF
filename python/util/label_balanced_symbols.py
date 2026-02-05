"""Label balanced opening and closing symbols in a string."""

from __future__ import annotations

from typing import List, Tuple


def label_balanced_symbols(
    value: str,
    open_symbol: str,
    close_symbol: str,
) -> Tuple[List[int], List[int]]:
    """
    Label balanced symbols and return their positions and nesting labels.

    Returns 1-based positions and corresponding nesting labels to mirror the
    Octave implementation.
    """
    open_positions = _find_substring_positions(value, open_symbol)
    close_positions = _find_substring_positions(value, close_symbol)

    symbol_positions = sorted(open_positions + close_positions)
    signed_positions = [pos if pos in open_positions else -pos for pos in symbol_positions]

    labels: List[int] = []
    nesting_level = 0
    for position in signed_positions:
        if position > 0:
            nesting_level += 1
            labels.append(nesting_level)
        else:
            labels.append(-nesting_level)
            nesting_level -= 1

    return symbol_positions, labels


def _find_substring_positions(value: str, symbol: str) -> List[int]:
    if not symbol:
        return []
    positions: List[int] = []
    start = 0
    while True:
        idx = value.find(symbol, start)
        if idx == -1:
            break
        positions.append(idx + 1)
        start = idx + len(symbol)
    return positions
