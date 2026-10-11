"""Small drawing helpers shared by the function diagrams (not a diagram module)."""

from __future__ import annotations

from typing import Optional, Sequence

from .. import theme
from ..svg import Canvas, Point, text_width


def num(v: float, digits: int = 4) -> str:
    """Formats a number for labels: trims zeros and uses a real minus sign."""
    r = round(v, digits)
    if abs(r - round(r)) < 1e-9:
        s = str(int(round(r)))
    else:
        s = f"{r:.{digits}f}".rstrip("0").rstrip(".")
    return s.replace("-", "−")


def ball(c: Canvas, x: float, y: float, s: str, color: str, r: float = 21, size: float = 17):
    """Draws a value as a filled disc with the number inside."""
    c.circle(x, y, r, color=color, fill=theme.fill(color, "26"), width=2.5)
    c.text(x, y + 1, s, size=size, color=color, weight="bold", math=True)


def machine(c: Canvas, x: float, y: float, w: float, h: float, color: str, name: str,
            rule: Optional[str] = None, rule_size: float = 19):
    """Draws a function machine: a rounded box with an input funnel and an output chute."""
    cy = y + h / 2
    c.polygon([(x - 20, cy - 24), (x + 2, cy - 13), (x + 2, cy + 13), (x - 20, cy + 24)],
              color=color, fill=theme.PAPER, width=2)
    c.polygon([(x + w - 2, cy - 13), (x + w + 20, cy - 13), (x + w + 20, cy + 13), (x + w - 2, cy + 13)],
              color=color, fill=theme.PAPER, width=2)
    c.rect(x, y, w, h, color=color, fill=theme.fill(color, "14"), width=3, rx=14)
    c.text(x + w / 2, y + 18, name, size=13, color=color, weight="bold")
    if rule:
        c.math(x + w / 2, y + h / 2 + 2, rule, size=rule_size, color=color)


def ctable(c: Canvas, x: float, y: float, headers: Sequence[str], rows: Sequence[Sequence[str]],
           col_w: Sequence[float], colors: Sequence[str], row_h: float = 28, size: float = 15,
           highlight: Optional[int] = None):
    """Draws a table whose columns each have their own text color.

    highlight is the index of a body row to fill with the highlight color.
    """
    cx = x
    for k, hd in enumerate(headers):
        c.rect(cx, y, col_w[k], row_h, color=theme.MUTED, fill=theme.PANEL, width=1)
        c.text(cx + col_w[k] / 2, y + row_h / 2, hd, size=13, weight="bold", color=colors[k], math=True)
        cx += col_w[k]
    for r, row in enumerate(rows):
        cx = x
        top = y + (r + 1) * row_h
        for k, val in enumerate(row):
            fill = theme.HIGHLIGHT if highlight == r else theme.PAPER
            c.rect(cx, top, col_w[k], row_h, color=theme.MUTED, fill=fill, width=1)
            c.text(cx + col_w[k] / 2, top + row_h / 2, val, size=size, color=colors[k], math=True)
            cx += col_w[k]


def axis_bar(c: Canvas, a: Point, b: Point, color: str, closed_a: bool = True, closed_b: bool = True,
             width: float = 7):
    """Draws a thick interval bar between two pixel points with end dots (hollow = open end)."""
    c.line(a[0], a[1], b[0], b[1], color=color, width=width)
    c.dot(a[0], a[1], r=6, color=color, hollow=not closed_a)
    c.dot(b[0], b[1], r=6, color=color, hollow=not closed_b)



def tag(c: Canvas, x: float, y: float, s: str, color: str, size: float = 15, anchor: str = "middle",
        math: bool = True, fill: str = theme.PAPER):
    """Draws a bordered label box in a color, for results and equations.

    The box is a little wider than Canvas.label_box, whose width estimate runs short for serif math.
    """
    w = text_width(s, size, "serif" if math else "sans") * 1.12 + 16
    h = size + 12
    left = {"middle": x - w / 2, "start": x, "end": x - w}[anchor]
    c.rect(left, y - h / 2, w, h, color=color, fill=fill, width=1.5, rx=5)
    c.text(left + w / 2, y, s, size=size, color=color, math=math)
    return w


def width_of(s: str, size: float, math: bool = True) -> float:
    return text_width(s, size, "serif" if math else "sans")
