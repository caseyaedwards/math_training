"""Riemann sums: approximating the area under a curve with rectangles."""

from __future__ import annotations

from .. import theme
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough


def f(x: float) -> float:
    return 0.25 * x * x + 1


def exact(a: float, b: float) -> float:
    F = lambda x: x ** 3 / 12 + x
    return F(b) - F(a)


def rectangles(p: Plane, n: int, a=0.0, b=4.0, color=theme.BLUE, rule="mid"):
    dx = (b - a) / n
    total = 0.0
    for i in range(n):
        x0 = a + i * dx
        xs = {"left": x0, "right": x0 + dx, "mid": x0 + dx / 2}[rule]
        h = f(xs)
        total += h * dx
        p.rect(x0, 0, x0 + dx, h, color=color, fill=theme.fill(color, "40"), width=1.5)
        p.c.dot(*p.px(xs, h), r=3.5, color=color)
    return total


@diagram("riemann-sum", "Riemann Sums", "Calculus")
def build() -> Walkthrough:
    wt = Walkthrough(
        "riemann-sum", "Riemann Sums: Area from Rectangles", "Calculus",
        concept="\\int_0^4 (x^2/4 + 1) dx \\approx \\sum f(x_i) \\Delta x",
        summary="Split the area under a curve into thin rectangles, add their areas, and let the rectangles "
                "get thinner. The sums close in on the exact area, which is the definite integral.",
        width=640, height=400, level="301",
    )
    A = exact(0, 4)
    m4 = sum(f(0.5 + i) for i in range(4))

    @wt.setup
    def _(c):
        p = Plane(c, box=(60, 30, 540, 330), x=(-0.5, 4.8), y=(-0.5, 6.2))
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    @wt.step("Draw the curve and the region", "Find the area under y = x²/4 + 1 between x = 0 and x = 4. "
             "No formula from geometry fits this curved shape.", math="area = ?")
    def _(c, p):
        p.shade_under(f, 0, 4, color=theme.GREEN, opacity=0.18)
        p.plot(f, -0.5, 4.6, color=theme.INK, label="y = x^2/4 + 1", label_at=3.2)
        p.vline(0, color=theme.SOFT_INK)
        p.vline(4, color=theme.SOFT_INK)

    @wt.step("Approximate with 4 rectangles", "Cut [0, 4] into 4 strips of width Δx = 1. Make each strip a "
             "rectangle whose height is the curve at the strip midpoint.",
             math=f"area \\approx 1\\cdot(f(0.5) + f(1.5) + f(2.5) + f(3.5)) = {m4:.3f}", fresh=True)
    def _(c, p):
        p.shade_under(f, 0, 4, color=theme.GREEN, opacity=0.12)
        s = rectangles(p, 4)
        p.plot(f, -0.5, 4.6, color=theme.INK)
        c.label_box(470, 70, f"sum = {s:.3f}", border=theme.BLUE, color=theme.BLUE)

    @wt.step("Use thinner rectangles", "With 8 strips of width 0.5 the rectangles hug the curve more "
             "closely. The gaps and overlaps shrink.", fresh=True)
    def _(c, p):
        s = rectangles(p, 8, color=theme.ORANGE)
        p.plot(f, -0.5, 4.6, color=theme.INK)
        c.label_box(470, 70, f"sum = {s:.4f}", border=theme.ORANGE, color=theme.ORANGE)

    @wt.step("Let the width go to zero", "With 32 strips the sum is almost exactly the area. In the limit "
             "as Δx → 0 the sum becomes the definite integral.", fresh=True,
             math=f"\\int_0^4 (x^2/4 + 1) dx = 28/3 \\approx {A:.4f}")
    def _(c, p):
        s = rectangles(p, 32, color=theme.PURPLE)
        p.plot(f, -0.5, 4.6, color=theme.INK)
        c.label_box(470, 70, f"sum = {s:.4f}", border=theme.PURPLE, color=theme.PURPLE)
        c.label_box(470, 104, f"exact = {A:.4f}", border=theme.GREEN, color=theme.GREEN)
    return wt
