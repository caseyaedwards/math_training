"""Annotation helpers: braces, angle marks, tick marks, callouts, number lines.

All functions take a `Canvas` and pixel coordinates. Convert world
coordinates first with `Plane.px` when working inside a plane.
"""

from __future__ import annotations

import math
from typing import Optional, Sequence

from . import theme
from .svg import Canvas, Point, fmt, text_width


def brace(c: Canvas, x1: float, y1: float, x2: float, y2: float, label: Optional[str] = None,
          color=theme.SOFT_INK, depth: float = 12, math_label: bool = True, size: float = 16):
    """Draws a curly brace from (x1, y1) to (x2, y2), bulging to the left of travel.

    For a brace under a horizontal segment, go right to left: brace(c, x2, y, x1, y).
    """
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L == 0:
        return
    ux, uy = dx / L, dy / L
    nx, ny = uy, -ux  # left normal in screen coordinates
    d = depth

    def P(t, k):
        return (x1 + ux * t + nx * k, y1 + uy * t + ny * k)

    q = min(d, L / 4)

    def xy(t, k):
        X, Y = P(t, k)
        return f"{fmt(X)},{fmt(Y)}"

    h = d / 2
    path = (
        f"M{xy(0, 0)} Q{xy(0, h)} {xy(q, h)} L{xy(L / 2 - q, h)} Q{xy(L / 2, h)} {xy(L / 2, d)} "
        f"Q{xy(L / 2, h)} {xy(L / 2 + q, h)} L{xy(L - q, h)} Q{xy(L, h)} {xy(L, 0)}"
    )
    c.path(path, color=color, width=1.8)
    if label:
        lx, ly = P(L / 2, d + 6)
        # push the label out along the normal by roughly half its size
        w = text_width(label, size, "serif" if math_label else "sans")
        off = abs(nx) * w / 2 + abs(ny) * size / 2 + 2
        c.text(lx + nx * off, ly + ny * off, label, color=color, size=size, math=math_label, halo=True)


def angle_mark(c: Canvas, vertex: Point, p1: Point, p2: Point, r: float = 26, label: Optional[str] = None,
               color=theme.ORANGE, fill: bool = True, count: int = 1, label_r: Optional[float] = None,
               size: float = 16):
    """Marks the angle p1-vertex-p2 (the smaller one) with an arc and optional label.

    count=2 or 3 draws multiple arcs, the usual way to show equal angles.
    """
    vx, vy = vertex
    a1 = math.atan2(-(p1[1] - vy), p1[0] - vx)
    a2 = math.atan2(-(p2[1] - vy), p2[0] - vx)
    sweep = (a2 - a1) % (2 * math.pi)
    if sweep > math.pi:
        a1, a2 = a2, a1
        sweep = 2 * math.pi - sweep
    deg0 = math.degrees(a1)
    deg1 = deg0 + math.degrees(sweep)
    if fill:
        c.arc(vx, vy, r, deg0, deg1, color="none", fill=theme.fill(color, "40"), sector=True)
    for k in range(count):
        c.arc(vx, vy, r - k * 5, deg0, deg1, color=color, width=2)
    if label:
        mid = a1 + sweep / 2
        lr = label_r if label_r is not None else r + 14 + (len(label) > 2) * 6
        c.text(vx + lr * math.cos(mid), vy - lr * math.sin(mid), label, color=color, math=True,
               size=size, halo=True)


def right_angle(c: Canvas, vertex: Point, p1: Point, p2: Point, s: float = 14, color=theme.INK):
    """Draws the small square that marks a 90 degree angle."""
    vx, vy = vertex

    def unit(p):
        dx, dy = p[0] - vx, p[1] - vy
        L = math.hypot(dx, dy) or 1
        return dx / L, dy / L

    u, v = unit(p1), unit(p2)
    a = (vx + u[0] * s, vy + u[1] * s)
    b = (vx + u[0] * s + v[0] * s, vy + u[1] * s + v[1] * s)
    d = (vx + v[0] * s, vy + v[1] * s)
    c.polyline([a, b, d], color=color, width=1.6)


def tick_marks(c: Canvas, p1: Point, p2: Point, count: int = 1, color=theme.INK, size: float = 7):
    """Draws hash marks across the middle of a segment, the usual sign of equal lengths."""
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    for k in range(count):
        off = (k - (count - 1) / 2) * 5
        cx, cy = mx + ux * off, my + uy * off
        c.line(cx - nx * size, cy - ny * size, cx + nx * size, cy + ny * size, color=color, width=1.8)


def segment_label(c: Canvas, p1: Point, p2: Point, label: str, offset: float = 16, color=theme.INK,
                  size: float = 16, side: int = 1, math_label: bool = True):
    """Places a label beside the midpoint of a segment. side=1 is left of travel, -1 right."""
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = dy / L * side, -dx / L * side
    w = text_width(label, size, "serif")
    o = offset + abs(nx) * w / 2
    return c.text(mx + nx * o, my + ny * o, label, color=color, size=size, math=math_label, halo=True)


def dimension(c: Canvas, p1: Point, p2: Point, label: str, offset: float = 22, color=theme.SOFT_INK,
              size: float = 15):
    """Draws an engineering-style dimension line with arrows at both ends."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = dy / L, -dx / L
    a = (p1[0] + nx * offset, p1[1] + ny * offset)
    b = (p2[0] + nx * offset, p2[1] + ny * offset)
    c.line(p1[0] + nx * 4, p1[1] + ny * 4, a[0] + nx * 5, a[1] + ny * 5, color=color, width=1)
    c.line(p2[0] + nx * 4, p2[1] + ny * 4, b[0] + nx * 5, b[1] + ny * 5, color=color, width=1)
    c.arrow(*a, *b, color=color, width=1.3, both=True)
    segment_label(c, a, b, label, offset=12, color=color, size=size)


def callout(c: Canvas, x: float, y: float, text: str, target: Optional[Point] = None, color=theme.INK,
            border=theme.MUTED, fill=theme.PAPER, size: float = 14, width: float = 200, math: bool = False):
    """Draws a boxed note at top-left (x, y), with an optional pointer line to target."""
    from .svg import wrap

    lines = wrap(text, width - 16, size)
    h = len(lines) * size * 1.35 + 12
    w = max(text_width(ln, size) for ln in lines) + 18
    if target:
        tx, ty = target
        cx = min(max(tx, x), x + w)
        cy = min(max(ty, y), y + h)
        c.line(cx, cy, tx, ty, color=border, width=1.4)
        c.dot(tx, ty, r=3, color=border)
    c.rect(x, y, w, h, color=border, fill=fill, width=1.4, rx=6)
    for i, ln in enumerate(lines):
        c.text(x + 9, y + 7 + i * size * 1.35, ln, size=size, color=color, anchor="start", baseline="hanging",
               math=math)
    return w, h


def number_line(c: Canvas, x0: float, y: float, x1: float, lo: float, hi: float, step: float = 1,
                label_every: int = 1, color=theme.INK, minor: int = 0, fmt_label=None, size: float = 14):
    """Draws a horizontal number line from value lo to hi. Returns a value->x function."""
    def X(v: float) -> float:
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    c.arrow(x0 - 14, y, x1 + 18, y, color=color, width=2, both=True)
    n = int(round((hi - lo) / step))
    for i in range(n + 1):
        v = lo + i * step
        c.line(X(v), y - 7, X(v), y + 7, color=color, width=1.8)
        if i % label_every == 0:
            s = fmt_label(v) if fmt_label else (str(int(v)) if abs(v - round(v)) < 1e-9 else f"{v:g}")
            c.text(X(v), y + 22, s.replace("-", "−"), size=size, color=color)
        if minor and i < n:
            for k in range(1, minor):
                vv = v + k * step / minor
                c.line(X(vv), y - 4, X(vv), y + 4, color=color, width=1)
    return X


def hop(c: Canvas, xa: float, xb: float, y: float, label: Optional[str] = None, color=theme.BLUE,
        height: float = 36, size: float = 14, below: bool = False):
    """Draws a jump arc over a number line from xa to xb, labeled at its peak.

    below=True draws the arc under the line, which keeps a second hop readable.
    """
    mx = (xa + xb) / 2
    s = 1 if below else -1
    k = height * 1.3 * s
    d = f"M{fmt(xa)},{fmt(y)} C{fmt(xa)},{fmt(y + k)} {fmt(xb)},{fmt(y + k)} {fmt(xb)},{fmt(y + 2 * s)}"
    c.path(d, color=color, width=2.4, marker_end=c.marker(color))
    if label:
        c.text(mx, y + s * (height * 0.975 + 14), label, color=color, size=size, math=True, halo=True)


def table(c: Canvas, x: float, y: float, rows: Sequence[Sequence[str]], col_w: Sequence[float] = None,
          row_h: float = 30, header: bool = True, size: float = 15, highlight: dict = None,
          math: bool = True, border=theme.MUTED):
    """Draws a simple grid table at top-left (x, y).

    highlight maps (row, col) to a fill color; use (r, None) for a whole row.
    """
    ncols = max(len(r) for r in rows)
    col_w = list(col_w or [80] * ncols)
    highlight = highlight or {}
    total_w = sum(col_w)
    for r, row in enumerate(rows):
        cx = x
        top = y + r * row_h
        for k in range(ncols):
            fill = highlight.get((r, k)) or highlight.get((r, None)) or (theme.PANEL if header and r == 0 else "none")
            c.rect(cx, top, col_w[k], row_h, color=border, fill=fill, width=1)
            if k < len(row):
                c.text(cx + col_w[k] / 2, top + row_h / 2, row[k], size=size, math=math and not (header and r == 0),
                       weight="bold" if header and r == 0 else None)
            cx += col_w[k]
    return total_w, row_h * len(rows)
