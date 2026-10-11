"""Small drawing helpers shared by the calculus and differential equation diagrams.

The registry skips modules whose names start with an underscore, so this
file registers no diagrams.
"""

from __future__ import annotations

import math
from typing import Optional, Sequence

from .. import theme
from ..plane import Plane


def slope_dir(p: Plane, slope: float):
    """Returns the unit pixel direction of a line with the given world slope."""
    dx, dy = p.sx, -slope * p.sy
    L = math.hypot(dx, dy)
    return dx / L, dy / L


def tangent(p: Plane, x0: float, y0: float, slope: float, half: float = 40, color=theme.ORANGE,
            width: float = theme.STROKE, dash=None):
    """Draws a segment through (x0, y0) with the given slope, `half` pixels to each side."""
    X, Y = p.px(x0, y0)
    ux, uy = slope_dir(p, slope)
    return p.c.line(X - ux * half, Y - uy * half, X + ux * half, Y + uy * half, color=color,
                    width=width, dash=dash)


def tangent_line(p: Plane, x0: float, y0: float, slope: float, color=theme.GREEN, width: float = theme.STROKE,
                 dash=None):
    """Draws the full line through (x0, y0) with the given slope, clipped to the plane."""
    return p.line_through(x0, y0, x0 + 1, y0 + slope, color=color, width=width, dash=dash)


def num(v: float, digits: int = 3) -> str:
    """Formats a number with at most `digits` decimals and a true minus sign."""
    s = f"{v:.{digits}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace("-", "−")


def table_rows(c, x: float, y: float, col_w: Sequence[float], rows: Sequence[Sequence[str]],
               row_h: float = 30, colors: Optional[Sequence[str]] = None, header: bool = False,
               size: float = 15, fill: Optional[str] = None):
    """Draws table rows at top-left (x, y), one row per entry, with optional per-row text colors."""
    for r, row in enumerate(rows):
        cx = x
        top = y + r * row_h
        color = (colors[r] if colors else None) or theme.INK
        for k, cell in enumerate(row):
            bg = theme.PANEL if header else (fill or "none")
            c.rect(cx, top, col_w[k], row_h, color=theme.MUTED, fill=bg, width=1)
            c.text(cx + col_w[k] / 2, top + row_h / 2, cell, size=size, color=theme.INK if header else color,
                   math=not header, weight="bold" if header else None)
            cx += col_w[k]
