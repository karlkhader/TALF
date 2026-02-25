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

    #matplotlib.use("Agg")
    ## width of lines
    line_width = 0.5
    ## rotation angle in degrees
    ## '+' = rotate anticlockwise;
    ## '-' = rotate clockwise.
    angle = -30
    ## length of each segment
    length_g = 1
    length_f = 2

    ## initial line coordinates and angle (0 = upwards)
    x = 0.0
    y = 0.0
    a = 0.0
    ## convert degrees to radians
    angle = angle / 180 * 3.141592653589793

    ## level of stacking for bracketed expressions
    stack: List[StackState] = []

    ## bounding box limits initialization
    minx = maxx = miny = maxy = 0.0

    ## canvas
    fig, ax = plt.subplots()
    ax.axis("off")

    for symbol in string:
        ## case of a branch
        if symbol == "G":
            ## branch tip
            newx = x + length_g * __import__("math").sin(a)
            newy = y + length_g * __import__("math").cos(a)
            ## plot segment
            ax.plot([x, newx], [y, newy], color="k", linewidth=line_width)
            ## branch tip is the new starting point
            x, y = newx, newy
            ## update bounding box
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, y)
            maxy = max(maxy, y)
        elif symbol == "F":
            ## branch tip
            newx = x + length_f * __import__("math").sin(a)
            newy = y + length_f * __import__("math").cos(a)
            ## plot segment
            ax.plot([x, newx], [y, newy], color="k", linewidth=line_width)
            ## branch tip is the new starting point
            x, y = newx, newy
            ## update bounding box
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, y)
            maxy = max(maxy, y)
        ## rotate anticlockwise
        elif symbol == "+":
            a += angle
        ## rotate clockwise
        elif symbol == "-":
            a -= angle
        ## stack current position
        elif symbol == "[":
            stack.append(StackState(x=x, y=y, angle=a))
        ## restore stacked position
        elif symbol == "]":
            if not stack:
                raise ValueError("Unbalanced stack while drawing the tree...")
            state = stack.pop()
            x, y, a = state.x, state.y, state.angle
        else:
            raise ValueError(f"Symbol {symbol} unknown while drawing the tree...")

    ## sets data aspect ratio
    ax.set_aspect("equal", adjustable="box")
    ## show bounding box only
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    plt.show()

    if output_path:
        fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
