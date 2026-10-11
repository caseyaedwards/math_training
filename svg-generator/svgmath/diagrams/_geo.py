"""Small geometry helpers shared by the geometry diagram modules.

The registry skips modules whose names start with an underscore, so this
file registers no diagrams.
"""

from __future__ import annotations

import math
from typing import Sequence, Tuple

from .. import theme
from ..svg import Canvas, Element, math_tspans

Point = Tuple[float, float]


def polar(cx: float, cy: float, r: float, deg: float) -> Point:
    """Returns the pixel point at distance r from (cx, cy), at math-style angle deg (counterclockwise)."""
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy - r * math.sin(a))


def mid(p: Point, q: Point) -> Point:
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def lerp(p: Point, q: Point, t: float) -> Point:
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def dist(p: Point, q: Point) -> float:
    return math.hypot(q[0] - p[0], q[1] - p[1])


def heading(p: Point, q: Point) -> float:
    """Math-style angle in degrees of the ray from p to q, in pixel coordinates."""
    return math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0])) % 360


def away(p: Point, center: Point, d: float) -> Point:
    """Returns the point d pixels from p, on the side away from center."""
    dx, dy = p[0] - center[0], p[1] - center[1]
    L = math.hypot(dx, dy) or 1
    return (p[0] + dx / L * d, p[1] + dy / L * d)


def centroid(pts: Sequence[Point]) -> Point:
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def deg(v: float) -> str:
    """Formats an angle in degrees, dropping a trailing .0."""
    r = round(v, 1)
    return f"{int(r)}°" if r == int(r) else f"{r}°"


def num(v: float, places: int = 2) -> str:
    r = round(v, places)
    if r == int(r):
        return str(int(r))
    return f"{r:.{places}f}".rstrip("0").rstrip(".")


def rich(c: Canvas, x: float, y: float, parts, size: float = 18, anchor: str = "middle", halo: bool = True,
         weight=None):
    """Draws one line of math whose parts have their own colors: parts is [(markup, color), ...]."""
    el = c.text(x, y, "", size=size, anchor=anchor, math=True, halo=halo, weight=weight)
    el.text = None
    for s, col in parts:
        ts = el.add(Element("tspan", fill=col))
        math_tspans(ts, s)
    return el


def solid_face(c: Canvas, pts: Sequence[Point], color: str, alpha: str = "40", width: float = 1.8,
               outline=None):
    """Draws an opaque face: a paper fill under a tinted fill, so faces behind stay hidden."""
    c.polygon(pts, color="none", fill=theme.PAPER)
    c.polygon(pts, color=outline or color, fill=theme.fill(color, alpha), width=width)


class Oblique:
    """Oblique (cabinet) projection: x to the right, y up, depth z drawn up and to the right."""

    def __init__(self, ox: float, oy: float, s: float, k: float = 0.5, angle: float = 35):
        self.ox, self.oy, self.s = ox, oy, s
        self.dx = k * math.cos(math.radians(angle))
        self.dy = k * math.sin(math.radians(angle))

    def __call__(self, x: float, y: float, z: float = 0.0) -> Point:
        return (self.ox + (x + z * self.dx) * self.s, self.oy - (y + z * self.dy) * self.s)


_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def word(n: int) -> str:
    """Writes whole numbers one through ten as words, for captions; larger numbers stay digits."""
    return _WORDS[n] if 0 <= n <= 10 else str(n)
