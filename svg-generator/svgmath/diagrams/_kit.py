"""Small drawing helpers shared by the arithmetic and fraction diagrams.

The module name starts with an underscore, so the registry skips it.
"""

from __future__ import annotations

from typing import Sequence, Tuple, Union

from .. import theme
from ..svg import Canvas, Element, math_tspans, text_width

Parts = Union[str, Sequence[Tuple[str, str]]]


def _parts(s: Parts, color: str):
    if isinstance(s, str):
        return [(s, color)]
    return list(s)


def parts_width(parts: Parts, size: float, math: bool = True) -> float:
    return sum(text_width(t, size, "serif" if math else "sans") for t, _ in _parts(parts, theme.INK))


def rich(c: Canvas, x: float, y: float, s: Parts, size: float = theme.MATH_SIZE, anchor: str = "middle",
         color: str = theme.INK, math: bool = True, halo: bool = False, weight=None) -> Element:
    """Draws one line of text whose pieces carry their own colors.

    s is a string or a list of (text, color) pairs. With math=True each
    piece uses the math markup (x^2, a_1, \\times).
    """
    el = Element(
        "text", x=x, y=y, font_size=size, fill=color, text_anchor=anchor,
        font_family=theme.SERIF if math else theme.SANS, dominant_baseline="central", font_weight=weight,
    )
    if halo:
        el.set(stroke=theme.PAPER, stroke_width=4, stroke_linejoin="round", paint_order="stroke")
    # Serialize the tspans on one line. Element.render puts a newline between
    # children, which SVG shows as a space between math runs.
    pieces = []
    for text, col in _parts(s, color):
        tmp = Element("text")
        if math:
            math_tspans(tmp, text)
        else:
            tmp.add(Element("tspan", text))
        for ts in tmp.children:
            ts.set(fill=col)
            pieces.append(ts.render(0))
    el.text = "".join(pieces)
    el.raw = True
    return c.add(el)


def frac(c: Canvas, x: float, y: float, num: Parts, den: Parts, size: float = 18, color: str = theme.INK,
         halo: bool = False, weight=None) -> float:
    """Draws a stacked fraction centered at (x, y). Returns its width in px."""
    w = max(parts_width(_parts(num, color), size), parts_width(_parts(den, color), size)) + 6
    gap = size * 0.62
    if halo:
        c.rect(x - w / 2 - 3, y - gap - size * 0.6, w + 6, 2 * gap + size * 1.2, color="none", fill=theme.PAPER,
               rx=4)
    rich(c, x, y - gap, num, size=size, color=color, weight=weight)
    rich(c, x, y + gap + 1, den, size=size, color=color, weight=weight)
    c.line(x - w / 2, y, x + w / 2, y, color=color, width=1.6)
    return w


def fade(c: Canvas, x: float, y: float, w: float, h: float, opacity: float = 0.72):
    """Covers a region with translucent paper, to push used-up marks into the background."""
    c.rect(x, y, w, h, color="none", fill=theme.PAPER, fill_opacity=opacity)


def tag(c: Canvas, x: float, y: float, s: str, color: str, size: float = 14, math: bool = True,
        anchor: str = "middle"):
    """A colored label in a white box with a colored border."""
    return c.label_box(x, y, s, size=size, color=color, border=color, math=math, anchor=anchor)
