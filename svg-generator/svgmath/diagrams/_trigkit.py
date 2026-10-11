"""Shared drawing helpers for the trigonometry and complex number diagrams."""

from __future__ import annotations

import math
from typing import Optional

from .. import theme
from ..svg import Canvas, text_width


def fraction(c: Canvas, cx: float, y: float, top: str, bottom: str, top_color=theme.INK,
             bottom_color=theme.INK, size: float = 18, math_text: bool = True) -> float:
    """Draws a stacked fraction centered at (cx, y), where y is the bar. Returns its width."""
    font = "serif" if math_text else "sans"
    w = max(text_width(top, size, font), text_width(bottom, size, font)) + 10
    c.text(cx, y - size * 0.72, top, size=size, color=top_color, math=math_text)
    c.line(cx - w / 2, y, cx + w / 2, y, color=theme.INK, width=1.6)
    c.text(cx, y + size * 0.78, bottom, size=size, color=bottom_color, math=math_text)
    return w


def polar_px(cx: float, cy: float, r: float, deg: float):
    """Pixel point at radius r and math-style angle deg around (cx, cy)."""
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def arc_label(c: Canvas, cx: float, cy: float, r: float, deg: float, s: str, color=theme.INK,
              size: float = 15, math_text: bool = True, halo: bool = True, anchor: str = "middle"):
    """Places a label at radius r and angle deg around a pixel center."""
    x, y = polar_px(cx, cy, r, deg)
    return c.text(x, y, s, color=color, size=size, math=math_text, halo=halo, anchor=anchor)


def deg_text(v: float, digits: int = 1) -> str:
    """Formats an angle in degrees, dropping a trailing .0."""
    s = f"{v:.{digits}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s + "°"


def num(v: float, digits: int = 3) -> str:
    """Formats a number with at most `digits` decimals, dropping trailing zeros."""
    s = f"{v:.{digits}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", "−0"):
        s = "0"
    return s


def faded(c: Canvas, opacity: float = 0.3):
    """Context manager that draws everything inside at reduced opacity."""
    return c.group(opacity=opacity)


def maybe_faded(c: Canvas, when: bool, opacity: float = 0.3):
    """Fades the drawing inside when `when` is true, otherwise draws it normally."""
    return c.group(opacity=opacity) if when else c.group()


def legend_row(c: Canvas, x: float, y: float, color: str, s: str, size: float = 15,
               math_text: bool = True, swatch: Optional[str] = "line"):
    """Draws a short colored swatch followed by a label, anchored at the left."""
    if swatch == "line":
        c.line(x, y, x + 22, y, color=color, width=3.5)
    elif swatch == "dot":
        c.dot(x + 11, y, r=5, color=color)
    c.text(x + 30, y, s, size=size, color=color, math=math_text, anchor="start")
