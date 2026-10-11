"""Small drawing helpers shared by the algebra diagram modules."""

from __future__ import annotations

from typing import Sequence, Tuple

from .. import theme
from ..svg import Canvas, math_tspans


def colored_math(c: Canvas, cx: float, y: float, parts: Sequence[Tuple[str, str]], size: float = 22,
                 anchor: str = "middle", halo: bool = False):
    """Draws one math line made of (markup, color) pieces, anchored at cx.

    All pieces share one <text> element, so the browser spaces them and nothing overlaps.
    """
    el = c.text(cx, y, "", size=size, math=True, anchor=anchor, halo=halo)
    for s, col in parts:
        before = len(el.children)
        math_tspans(el, s)
        for child in el.children[before:]:
            child.set(fill=col)
    return el


def thick_ray(c: Canvas, x_from: float, x_to: float, y: float, color=theme.ORANGE, width: float = 6,
              arrow: bool = True):
    """Draws a thick shaded ray along a horizontal number line."""
    if arrow:
        c.arrow(x_from, y, x_to, y, color=color, width=width, opacity=0.75)
    else:
        c.line(x_from, y, x_to, y, color=color, width=width, opacity=0.75)


def tile(c: Canvas, x: float, y: float, w: float, h: float, color: str, label: str = "", size: float = 18,
         dashed: bool = False, label_color=None, alpha: str = "40"):
    """Draws an algebra tile: a filled rectangle with a math label in its center."""
    if dashed:
        c.rect(x, y, w, h, color=color, fill="none", width=1.6, dash="5 4", rx=3)
    else:
        c.rect(x, y, w, h, color=color, fill=theme.fill(color, alpha), width=1.8, rx=3)
    if label:
        c.text(x + w / 2, y + h / 2, label, size=size, color=label_color or color, math=True)
