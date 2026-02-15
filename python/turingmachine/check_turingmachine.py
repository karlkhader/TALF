"""
checkturingmachine

Example:
    >>> check_turingmachine()
    True
"""

from __future__ import annotations

from .turing_machine import turing_machine


def check_turingmachine() -> bool:
    """Return True if the successor machine passes test cases."""
    machine_name = "successorbinary"
    for inputvaluedecimal in range(0, 101):
        inputvaluebinary = format(inputvaluedecimal, "b")
        tape, _ = turing_machine(machine_name, f"*{inputvaluebinary}*", "none")
        outputvaluebinary = "".join(tape.content[1:-1])
        outputvaluedecimal = int(outputvaluebinary, 2)
        if outputvaluedecimal != inputvaluedecimal + 1:
            return False
    return True
