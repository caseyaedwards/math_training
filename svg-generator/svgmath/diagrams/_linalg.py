"""Shared drawing helpers for the linear algebra diagrams.

The registry skips modules whose name starts with an underscore, so this
file holds helpers only and registers no diagrams.

Color roles used across the linear algebra family:
  e1 and the first column      GREEN
  e2 and the second column     RED
  vector u / first input       BLUE
  vector v / second input      ORANGE
  results (sums, images)       PURPLE
"""

from __future__ import annotations

from fractions import Fraction
from typing import Dict, Optional, Sequence, Tuple

from .. import theme
from ..plane import Plane
from ..svg import Canvas, text_width

E1 = theme.GREEN
E2 = theme.RED
U = theme.BLUE
V = theme.ORANGE
RESULT = theme.PURPLE

Matrix2 = Tuple[Tuple[float, float], Tuple[float, float]]


def num(v) -> str:
    """Formats an int, Fraction, or float compactly for math markup."""
    if isinstance(v, Fraction):
        if v.denominator == 1:
            return str(v.numerator)
        return f"{v.numerator}/{v.denominator}"
    if isinstance(v, float):
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return f"{v:.3f}".rstrip("0").rstrip(".")
    return str(v)


def apply(M: Matrix2, x: float, y: float) -> Tuple[float, float]:
    """Returns M times the column vector (x, y)."""
    return (M[0][0] * x + M[0][1] * y, M[1][0] * x + M[1][1] * y)


def matmul(A: Matrix2, B: Matrix2) -> Matrix2:
    return tuple(
        tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2)
    )


def det(M: Matrix2) -> float:
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


class MatrixBox:
    """Geometry of a drawn matrix: cell centers and row and column bands."""

    def __init__(self, x: float, y: float, nrows: int, ncols: int, cw: float, ch: float, pad: float):
        self.x, self.y = x, y
        self.nrows, self.ncols = nrows, ncols
        self.cw, self.ch, self.pad = cw, ch, pad
        self.w = ncols * cw + 2 * pad
        self.h = nrows * ch + 2 * pad

    def cell(self, r: int, k: int) -> Tuple[float, float]:
        return (self.x + self.pad + (k + 0.5) * self.cw, self.y + self.pad + (r + 0.5) * self.ch)

    def row_band(self, r: int) -> Tuple[float, float, float, float]:
        return (self.x + self.pad - 3, self.y + self.pad + r * self.ch + 1, self.ncols * self.cw + 6, self.ch - 2)

    def col_band(self, k: int) -> Tuple[float, float, float, float]:
        return (self.x + self.pad + k * self.cw + 1, self.y + self.pad - 3, self.cw - 2, self.nrows * self.ch + 6)

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2


def draw_matrix(c: Canvas, x: float, y: float, rows: Sequence[Sequence], cw: float = 38, ch: float = 30,
                size: float = 18, color=theme.INK, cell_color: Optional[Dict] = None,
                col_colors: Optional[Sequence] = None, row_colors: Optional[Sequence] = None,
                fills: Optional[Dict] = None, aug: Optional[int] = None, pad: float = 6,
                bracket=theme.INK, weight=None) -> MatrixBox:
    """Draws a bracketed matrix with its top-left corner at (x, y).

    rows holds entries (numbers or math strings). cell_color maps (r, k) to a text color,
    col_colors and row_colors set colors per column or row. fills maps (r, k) to a cell
    background. aug=k draws the augmented-matrix bar before column k.
    """
    nrows, ncols = len(rows), max(len(r) for r in rows)
    box = MatrixBox(x, y, nrows, ncols, cw, ch, pad)
    fills = fills or {}
    cell_color = cell_color or {}
    for (r, k), f in fills.items():
        cx, cy = box.cell(r, k)
        c.rect(cx - cw / 2 + 1, cy - ch / 2 + 1, cw - 2, ch - 2, color="none", fill=f, rx=4)
    t = 7  # bracket serif length
    L, R, T, B = x, x + box.w, y, y + box.h
    c.polyline([(L + t, T), (L, T), (L, B), (L + t, B)], color=bracket, width=1.8)
    c.polyline([(R - t, T), (R, T), (R, B), (R - t, B)], color=bracket, width=1.8)
    if aug is not None:
        ax = x + pad + aug * cw
        c.line(ax, T + 4, ax, B - 4, color=theme.SOFT_INK, width=1.3, dash="4 3")
    for r, row in enumerate(rows):
        for k, v in enumerate(row):
            col = cell_color.get((r, k))
            if col is None and col_colors is not None:
                col = col_colors[k]
            if col is None and row_colors is not None:
                col = row_colors[r]
            cx, cy = box.cell(r, k)
            c.math(cx, cy, v if isinstance(v, str) else num(v), size=size, color=col or color, weight=weight)
    return box


def band(c: Canvas, rect: Tuple[float, float, float, float], color: str, alpha: str = "30"):
    """Fills a row or column band of a matrix with a translucent color and outlines it."""
    x, y, w, h = rect
    c.rect(x, y, w, h, color=color, fill=theme.fill(color, alpha), width=1.6, rx=6)


def warped_grid(p: Plane, M: Matrix2, lo: int = -12, hi: int = 12, color=theme.SKY, width: float = 1.3,
                opacity: float = 1.0, dash=None):
    """Draws the image of the integer grid under M, clipped to the plane."""
    with p.c.group(clip_path=p.clip, opacity=opacity):
        for k in range(lo, hi + 1):
            a = apply(M, k, lo * 3)
            b = apply(M, k, hi * 3)
            p.c.line(*p.px(*a), *p.px(*b), color=color, width=width, dash=dash)
            a = apply(M, lo * 3, k)
            b = apply(M, hi * 3, k)
            p.c.line(*p.px(*a), *p.px(*b), color=color, width=width, dash=dash)


def vec(p: Plane, x1: float, y1: float, x2: float, y2: float, color, width: float = 3.2, dash=None):
    """Draws an arrow in world coordinates without a label."""
    return p.vector(x1, y1, x2, y2, color=color, width=width, dash=dash)


def tip(p: Plane, x: float, y: float, s: str, color, dx: float = 0, dy: float = -16, size: float = 17,
        anchor: str = "middle"):
    """Labels the point (x, y) with math text offset by (dx, dy) pixels."""
    X, Y = p.px(x, y)
    return p.c.text(X + dx, Y + dy, s, color=color, size=size, math=True, halo=True, anchor=anchor)


def light_axes(p: Plane, step: float = 1, labels: bool = True):
    """Draws a light grid and axes with unit ticks."""
    p.grid(step=step)
    p.axes(step=step, ystep=step, labels=labels)


def boxed(c: Canvas, x: float, y: float, s: str, color, size: float = 16, math: bool = True,
          fill=theme.PAPER, anchor: str = "middle"):
    """Draws a label in a rounded box centered at (x, y), sized generously for math text.

    Canvas.label_box sizes its box from an estimate that runs short for serif math with
    superscripts, so this helper adds a little extra width.
    """
    w = text_width(s, size, "serif" if math else "sans") * 1.08 + 20
    h = size + 14
    left = {"middle": x - w / 2, "start": x, "end": x - w}[anchor]
    c.rect(left, y - h / 2, w, h, color=color, fill=fill, width=1.5, rx=5)
    c.text(left + w / 2, y, s, size=size, color=color, math=math)
    return w, h


def offset_segment(p: Plane, a, b, off: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Returns the pixel endpoints of segment ab moved off pixels to the right of travel."""
    import math as _m

    A, B = p.px(*a), p.px(*b)
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = _m.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    return (A[0] + nx * off, A[1] + ny * off), (B[0] + nx * off, B[1] + ny * off)
