"""Draw an L-system tree using turtle-like interpretation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class StackState:
    x: float
    y: float
    angle: float


def draw_tree(string: str, *, output_path: str | None = None) -> None:
    """Draw the tree encoded in the L-system string."""
    try:
        import matplotlib
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError("matplotlib is required to draw L-systems.") from exc

    matplotlib.use("Agg")
    line_width = 0.5
    angle = -30
    length_g = 1
    length_f = 2

    x = 0.0
    y = 0.0
    a = 0.0
    angle = angle / 180 * 3.141592653589793

    stack: List[StackState] = []

    minx = maxx = miny = maxy = 0.0

    fig, ax = plt.subplots()
    ax.axis("off")

    for symbol in string:
        if symbol == "G":
            newx = x + length_g * __import__("math").sin(a)
            newy = y + length_g * __import__("math").cos(a)
            ax.plot([x, newx], [y, newy], color="k", linewidth=line_width)
            x, y = newx, newy
        elif symbol == "F":
            newx = x + length_f * __import__("math").sin(a)
            newy = y + length_f * __import__("math").cos(a)
            ax.plot([x, newx], [y, newy], color="k", linewidth=line_width)
            x, y = newx, newy
        elif symbol == "+":
            a += angle
        elif symbol == "-":
            a -= angle
        elif symbol == "[":
            stack.append(StackState(x=x, y=y, angle=a))
        elif symbol == "]":
            if not stack:
                raise ValueError("Unbalanced stack while drawing the tree...")
            state = stack.pop()
            x, y, a = state.x, state.y, state.angle
        else:
            raise ValueError(f"Symbol {symbol} unknown while drawing the tree...")

        minx = min(minx, x)
        maxx = max(maxx, x)
        miny = min(miny, y)
        maxy = max(maxy, y)

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    if output_path:
        fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
