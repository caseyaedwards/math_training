"""Math coordinates on a canvas: axes, grids, function plots, and shading.

A `Plane` maps a world rectangle [xmin, xmax] x [ymin, ymax] onto a pixel
box of the canvas, with y pointing up. Every drawing method takes world
coordinates.

    p = Plane(c, box=(40, 20, 520, 360), x=(-4, 4), y=(-2, 6))
    p.grid(); p.axes()
    p.plot(lambda x: x**2, color=theme.BLUE, label="y = x^2")
"""

from __future__ import annotations

import math
from typing import Callable, Iterable, List, Optional, Sequence, Tuple

from . import theme
from .svg import Canvas, Point, fmt

Func = Callable[[float], float]


def nice_step(span: float, target: int = 8) -> float:
    """Returns a 1-2-5 tick step that yields about `target` ticks across span."""
    raw = span / max(target, 1)
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 5, 10):
        if raw <= m * mag:
            return m * mag
    return 10 * mag


def tick_label(v: float) -> str:
    if abs(v - round(v)) < 1e-9:
        s = str(int(round(v)))
    else:
        s = f"{v:.3f}".rstrip("0").rstrip(".")
    return s.replace("-", "−")


def pi_label(v: float, denom: int = 2) -> str:
    """Formats a multiple of pi, for example 3.14159 -> 'π', 1.5708 -> 'π/2'."""
    k = round(v / math.pi * denom)
    if k == 0:
        return "0"
    from fractions import Fraction

    f = Fraction(k, denom)
    sign = "−" if f < 0 else ""
    f = abs(f)
    num = "" if f.numerator == 1 else str(f.numerator)
    if f.denominator == 1:
        return f"{sign}{num}π"
    return f"{sign}{num}π/{f.denominator}"


class Plane:
    def __init__(
        self,
        canvas: Canvas,
        box: Tuple[float, float, float, float],
        x: Tuple[float, float] = (-5, 5),
        y: Tuple[float, float] = (-5, 5),
        equal: bool = False,
    ):
        """box is (left, top, width, height) in pixels.

        equal=True shrinks the box so one unit has the same length on both axes,
        which keeps circles round and angles true.
        """
        self.c = canvas
        left, top, w, h = box
        self.xmin, self.xmax = x
        self.ymin, self.ymax = y
        if equal:
            sx = w / (self.xmax - self.xmin)
            sy = h / (self.ymax - self.ymin)
            s = min(sx, sy)
            nw, nh = s * (self.xmax - self.xmin), s * (self.ymax - self.ymin)
            left += (w - nw) / 2
            top += (h - nh) / 2
            w, h = nw, nh
        self.left, self.top, self.w, self.h = left, top, w, h
        self.sx = w / (self.xmax - self.xmin)
        self.sy = h / (self.ymax - self.ymin)
        self._clip = None

    # -- mapping -----------------------------------------------------------

    def px(self, x: float, y: float) -> Point:
        """Converts world (x, y) to pixel coordinates."""
        return (self.left + (x - self.xmin) * self.sx, self.top + (self.ymax - y) * self.sy)

    def X(self, x: float) -> float:
        return self.left + (x - self.xmin) * self.sx

    def Y(self, y: float) -> float:
        return self.top + (self.ymax - y) * self.sy

    def length(self, d: float) -> float:
        """Converts a world distance along x to pixels."""
        return d * self.sx

    @property
    def clip(self) -> str:
        if self._clip is None:
            self._clip = self.c.clip_rect(self.left, self.top, self.w, self.h)
        return self._clip

    def contains(self, x: float, y: float) -> bool:
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax

    # -- background --------------------------------------------------------

    def grid(self, step: Optional[float] = None, ystep: Optional[float] = None, color=theme.GRID,
             minor: Optional[int] = None):
        """Draws grid lines. minor=n adds n subdivisions per step in a lighter tone."""
        step = step or nice_step(self.xmax - self.xmin)
        ystep = ystep or (step if abs((self.ymax - self.ymin) / step) < 30 else nice_step(self.ymax - self.ymin))
        if minor:
            for v in _ticks(self.xmin, self.xmax, step / minor):
                self.c.line(self.X(v), self.top, self.X(v), self.top + self.h, color="#f1f3f5", width=1)
            for v in _ticks(self.ymin, self.ymax, ystep / minor):
                self.c.line(self.left, self.Y(v), self.left + self.w, self.Y(v), color="#f1f3f5", width=1)
        for v in _ticks(self.xmin, self.xmax, step):
            self.c.line(self.X(v), self.top, self.X(v), self.top + self.h, color=color, width=1)
        for v in _ticks(self.ymin, self.ymax, ystep):
            self.c.line(self.left, self.Y(v), self.left + self.w, self.Y(v), color=color, width=1)

    def axes(self, xlabel: str = "x", ylabel: str = "y", step: Optional[float] = None,
             ystep: Optional[float] = None, ticks: bool = True, labels: bool = True,
             xfmt: Callable[[float], str] = tick_label, yfmt: Callable[[float], str] = tick_label,
             color=theme.INK, arrows: bool = True):
        """Draws the x- and y-axes with tick marks and numbers.

        Axes sit at x=0 and y=0 when visible, otherwise on the box edge.
        """
        step = step or nice_step(self.xmax - self.xmin)
        ystep = ystep or nice_step(self.ymax - self.ymin)
        ax_y = 0 if self.ymin <= 0 <= self.ymax else self.ymin
        ax_x = 0 if self.xmin <= 0 <= self.xmax else self.xmin
        c = self.c
        y0 = self.Y(ax_y)
        x0 = self.X(ax_x)
        draw = c.arrow if arrows else c.line
        draw(self.left - 4, y0, self.left + self.w + 6, y0, color=color, width=1.6)
        draw(x0, self.top + self.h + 4, x0, self.top - 6, color=color, width=1.6)
        if xlabel:
            c.math(self.left + self.w + 14, y0, xlabel, size=17, anchor="start", color=color)
        if ylabel:
            c.math(x0, self.top - 18, ylabel, size=17, color=color)
        if not ticks:
            return
        for v in _ticks(self.xmin, self.xmax, step):
            if abs(v - ax_x) < 1e-9 and self.xmin < ax_x:
                continue
            X = self.X(v)
            c.line(X, y0 - 4, X, y0 + 4, color=color, width=1.4)
            if labels:
                c.text(X, y0 + 16, xfmt(v), size=theme.SMALL_SIZE, color=theme.SOFT_INK, halo=True)
        for v in _ticks(self.ymin, self.ymax, ystep):
            if abs(v - ax_y) < 1e-9:
                continue
            Y = self.Y(v)
            c.line(x0 - 4, Y, x0 + 4, Y, color=color, width=1.4)
            if labels:
                c.text(x0 - 8, Y, yfmt(v), size=theme.SMALL_SIZE, color=theme.SOFT_INK, anchor="end", halo=True)
        if labels and self.xmin < 0 < self.xmax and self.ymin < 0 < self.ymax:
            c.text(x0 - 8, y0 + 14, "0", size=theme.SMALL_SIZE, color=theme.SOFT_INK, anchor="end")

    # -- curves ------------------------------------------------------------

    def sample(self, f: Func, a: Optional[float] = None, b: Optional[float] = None, n: int = 400,
               jump: Optional[float] = None) -> List[List[Point]]:
        """Samples f on [a, b] into pixel polylines, splitting at gaps and asymptotes."""
        a = self.xmin if a is None else a
        b = self.xmax if b is None else b
        jump = jump if jump is not None else (self.ymax - self.ymin) * 1.5
        pieces: List[List[Point]] = [[]]
        prev = None
        lo, hi = self.ymin - (self.ymax - self.ymin), self.ymax + (self.ymax - self.ymin)
        for i in range(n + 1):
            x = a + (b - a) * i / n
            try:
                y = f(x)
                ok = y is not None and math.isfinite(y)
            except (ValueError, ZeroDivisionError, OverflowError):
                ok = False
            if not ok or (prev is not None and abs(y - prev) > jump):
                if pieces[-1]:
                    pieces.append([])
                prev = y if ok else None
                if not ok:
                    continue
            y = max(lo, min(hi, y))
            pieces[-1].append(self.px(x, y))
            prev = y
        return [p for p in pieces if len(p) > 1]

    def plot(self, f: Func, a: Optional[float] = None, b: Optional[float] = None, color=theme.BLUE,
             width=theme.THICK - 0.5, dash=None, label: Optional[str] = None, label_at: Optional[float] = None,
             label_side: str = "above", n: int = 400):
        """Plots y = f(x) on [a, b], clipped to the plane."""
        with self.c.group(clip_path=self.clip):
            for pts in self.sample(f, a, b, n):
                self.c.polyline(pts, color=color, width=width, dash=dash)
        if label:
            lx = label_at if label_at is not None else (b if b is not None else self.xmax) - (self.xmax - self.xmin) * 0.12
            try:
                ly = f(lx)
            except (ValueError, ZeroDivisionError):
                ly = None
            if ly is not None and math.isfinite(ly):
                X, Y = self.px(lx, max(self.ymin, min(self.ymax, ly)))
                off = -16 if label_side == "above" else 18
                self.c.math(X, Y + off, label, color=color, size=17, halo=True)

    def parametric(self, fx: Func, fy: Func, t0: float, t1: float, color=theme.BLUE, width=theme.THICK - 0.5,
                   n: int = 600, dash=None, arrow: bool = False):
        pts = [self.px(fx(t0 + (t1 - t0) * i / n), fy(t0 + (t1 - t0) * i / n)) for i in range(n + 1)]
        with self.c.group(clip_path=self.clip):
            el = self.c.polyline(pts, color=color, width=width, dash=dash)
            if arrow:
                el.set(marker_end=self.c.marker(color))
        return el

    def polar(self, r: Func, t0: float = 0, t1: float = 2 * math.pi, **kw):
        return self.parametric(lambda t: r(t) * math.cos(t), lambda t: r(t) * math.sin(t), t0, t1, **kw)

    # -- regions -----------------------------------------------------------

    def shade_between(self, f: Func, g: Func, a: float, b: float, color=theme.BLUE, opacity=0.22, n=200):
        """Fills the region between y=f(x) and y=g(x) for x in [a, b]."""
        top = [self.px(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)]
        bot = [self.px(a + (b - a) * i / n, g(a + (b - a) * i / n)) for i in range(n, -1, -1)]
        with self.c.group(clip_path=self.clip):
            return self.c.polygon(top + bot, color="none", fill=color, fill_opacity=opacity)

    def shade_under(self, f: Func, a: float, b: float, color=theme.BLUE, opacity=0.22, n=200):
        return self.shade_between(f, lambda x: 0.0, a, b, color=color, opacity=opacity, n=n)

    def region(self, pts: Sequence[Point], color=theme.BLUE, opacity=0.22, outline: Optional[str] = None,
               width=theme.STROKE, dash=None):
        """Fills a polygon given in world coordinates."""
        return self.c.polygon([self.px(x, y) for x, y in pts], color=outline or "none", fill=color,
                              fill_opacity=opacity, width=width, dash=dash)

    def polygon(self, pts: Sequence[Point], color=theme.INK, fill="none", width=theme.STROKE, dash=None, **kw):
        return self.c.polygon([self.px(x, y) for x, y in pts], color=color, fill=fill, width=width, dash=dash, **kw)

    def rect(self, x0: float, y0: float, x1: float, y1: float, color=theme.INK, fill="none", width=theme.STROKE,
             **kw):
        """Draws the axis-aligned rectangle with corners (x0, y0) and (x1, y1)."""
        X0, Y0 = self.px(x0, y0)
        X1, Y1 = self.px(x1, y1)
        return self.c.rect(min(X0, X1), min(Y0, Y1), abs(X1 - X0), abs(Y1 - Y0), color=color, fill=fill,
                           width=width, **kw)

    # -- marks -------------------------------------------------------------

    def point(self, x: float, y: float, label: Optional[str] = None, color=theme.INK, r=5,
              hollow=False, offset: Tuple[float, float] = (10, -14), anchor="start", math=True, size=16):
        X, Y = self.px(x, y)
        self.c.dot(X, Y, r=r, color=color, hollow=hollow)
        if label:
            self.c.text(X + offset[0], Y + offset[1], label, color=color, anchor=anchor, math=math,
                        size=size, halo=True)

    def segment(self, x1, y1, x2, y2, color=theme.INK, width=theme.STROKE, dash=None, **kw):
        a, b = self.px(x1, y1), self.px(x2, y2)
        return self.c.line(*a, *b, color=color, width=width, dash=dash, **kw)

    def vector(self, x1, y1, x2, y2, color=theme.BLUE, width=theme.THICK - 0.5, label=None,
               label_offset=(0, -14), dash=None):
        """Draws an arrow from (x1, y1) to (x2, y2). The label sits near the midpoint."""
        a, b = self.px(x1, y1), self.px(x2, y2)
        el = self.c.arrow(*a, *b, color=color, width=width, dash=dash)
        if label:
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            self.c.math(mx + label_offset[0], my + label_offset[1], label, color=color, halo=True)
        return el

    def line_through(self, x1, y1, x2, y2, color=theme.INK, width=theme.STROKE, dash=None):
        """Draws the full line through two points, clipped to the plane."""
        if abs(x2 - x1) < 1e-12:
            return self.vline(x1, color=color, width=width, dash=dash)
        m = (y2 - y1) / (x2 - x1)
        f = lambda x: y1 + m * (x - x1)
        with self.c.group(clip_path=self.clip):
            return self.c.line(*self.px(self.xmin, f(self.xmin)), *self.px(self.xmax, f(self.xmax)),
                               color=color, width=width, dash=dash)

    def vline(self, x: float, color=theme.MUTED, width=1.5, dash="6 5", y0=None, y1=None):
        y0 = self.ymin if y0 is None else y0
        y1 = self.ymax if y1 is None else y1
        return self.c.line(self.X(x), self.Y(y0), self.X(x), self.Y(y1), color=color, width=width, dash=dash)

    def hline(self, y: float, color=theme.MUTED, width=1.5, dash="6 5", x0=None, x1=None):
        x0 = self.xmin if x0 is None else x0
        x1 = self.xmax if x1 is None else x1
        return self.c.line(self.X(x0), self.Y(y), self.X(x1), self.Y(y), color=color, width=width, dash=dash)

    def label(self, x: float, y: float, s: str, color=theme.INK, size=16, math=True, **kw):
        X, Y = self.px(x, y)
        return self.c.text(X, Y, s, color=color, size=size, math=math, halo=True, **kw)

    def circle(self, cx: float, cy: float, r: float, color=theme.INK, fill="none", width=theme.STROKE, **kw):
        X, Y = self.px(cx, cy)
        return self.c.circle(X, Y, r * self.sx, color=color, fill=fill, width=width, **kw)


def _ticks(lo: float, hi: float, step: float) -> Iterable[float]:
    start = math.ceil(lo / step - 1e-9)
    end = math.floor(hi / step + 1e-9)
    for k in range(start, end + 1):
        yield round(k * step, 10)
