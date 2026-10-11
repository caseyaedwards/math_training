"""Straight lines: slope, intercept, and systems of two linear equations."""

from __future__ import annotations

from fractions import Fraction

from .. import theme
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._algebra_helpers import colored_math

RUN_COL = theme.ORANGE
RISE_COL = theme.PURPLE
B_COL = theme.GREEN
M_COL = theme.RED


def _slope_triangle(c, p, x0, y0, run, rise, place_ratio):
    """Draws a run-then-rise triangle under a line, with labels and the ratio inside."""
    p.region([(x0, y0), (x0 + run, y0), (x0 + run, y0 + rise)], color=RISE_COL, opacity=0.10)
    p.vector(x0, y0, x0 + run, y0, color=RUN_COL, width=3)
    p.vector(x0 + run, y0, x0 + run, y0 + rise, color=RISE_COL, width=3)
    X, Y = p.px(x0 + run / 2, y0)
    c.text(X, Y + 16, f"run {run}", size=14, color=RUN_COL, weight="bold", halo=True)
    X, Y = p.px(x0 + run, y0 + rise / 2)
    c.text(X + 10, Y, f"rise {rise}", size=14, color=RISE_COL, weight="bold", anchor="start", halo=True)
    fr = Fraction(rise, run)
    X, Y = p.px(*place_ratio)
    s = f"{rise}/{run}" + ("" if (rise, run) == (fr.numerator, fr.denominator) else f" = {fr}")
    c.math(X, Y, s, size=17, color=M_COL, halo=True)


@diagram("slope-intercept", "Slope and Intercept: y = mx + b", "Algebra")
def build_slope() -> Walkthrough:
    wt = Walkthrough(
        "slope-intercept", "Slope and Intercept: y = mx + b", "Algebra",
        concept="y = mx + b,   m = rise / run",
        summary="The slope m says how much y climbs per step right, and b says where the line crosses the y-axis. "
                "Any slope triangle on the line, big or small, gives the same rise over run.",
        width=680, height=440, level="201",
    )
    m = Fraction(2, 3)
    b = 1
    f = lambda x: float(m) * x + b
    pts = [(x, int(f(x))) for x in (0, 3, 6, 9)]

    @wt.setup
    def _(c):
        p = Plane(c, box=(50, 30, 600, 380), x=(-1, 10), y=(-1, 8), equal=True)
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    @wt.step("Draw the line", "These points all sit on one straight line. Every 3 steps right, the line "
             "climbs 2.", math="(0, 1), (3, 3), (6, 5), (9, 7)")
    def _(c, p):
        p.plot(f, color=theme.BLUE)
        for x, y in pts[1:]:
            p.point(x, y, f"({x}, {y})", color=theme.BLUE, offset=(-10, -16), anchor="end", size=15)
        p.point(*pts[0], color=theme.BLUE)

    @wt.step("Find the y-intercept b", f"The line crosses the y-axis at height {b}. That starting height is b.",
             math=f"x = 0 \\implies y = {b},   so b = {b}")
    def _(c, p):
        p.point(0, b, f"(0, {b}): b = {b}", color=B_COL, r=7, offset=(-12, -20), anchor="end", size=15)

    @wt.step("Measure rise over run", "Walk 3 right along the orange run, then 2 up along the purple rise to "
             "get back to the line. The slope is rise divided by run.", math="m = rise / run = 2/3")
    def _(c, p):
        _slope_triangle(c, p, 0, 1, 3, 2, (2.1, 1.55))

    @wt.step("Try a bigger triangle", "Start at (3, 3) and walk 6 right and 4 up. The triangle is twice as big, "
             "but the ratio is the same, because a straight line has one steady slope.",
             math="4/6 = 2/3")
    def _(c, p):
        _slope_triangle(c, p, 3, 3, 6, 4, (7.0, 4.1))

    @wt.step("Write the equation", "Start at b and add m for every step right. That recipe is the whole "
             "equation of the line.", math="y = (2/3)x + 1")
    def _(c, p):
        X, Y = p.px(0.35, 6.7)
        colored_math(c, X, Y, [("y = ", theme.BLUE), ("(2/3)", M_COL), ("x", theme.BLUE), (" + 1", B_COL)],
                     size=24, anchor="start", halo=True)
        c.text(X + 4, Y + 32, "m = 2/3: the slope, rise per run", size=14, color=M_COL, anchor="start", halo=True)
        c.text(X + 4, Y + 54, "b = 1: the starting height", size=14, color=B_COL, anchor="start", halo=True)

    return wt


@diagram("system-of-equations", "Solving a System by Graphing", "Algebra")
def build_system() -> Walkthrough:
    wt = Walkthrough(
        "system-of-equations", "Solving a System by Graphing", "Algebra",
        concept="y = 2x - 1,  x + y = 5 \\implies (x, y) = (2, 3)",
        summary="Each equation is a line of points that satisfy it. The point on both lines satisfies both "
                "equations, so the crossing point is the solution.",
        width=640, height=440, level="201",
    )
    A_COL, B2_COL, S_COL = theme.BLUE, theme.ORANGE, theme.GREEN
    f = lambda x: 2 * x - 1
    g = lambda x: 5 - x
    xs = 2  # 2x - 1 = 5 - x  ->  3x = 6
    ys = f(xs)
    assert f(xs) == g(xs)

    @wt.setup
    def _(c):
        p = Plane(c, box=(40, 25, 560, 390), x=(-2, 7), y=(-2, 7), equal=True)
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    @wt.step("Graph the first equation", "Every point on the blue line makes y = 2x − 1 true. "
             "Start at −1 on the y-axis and climb 2 for each step right.", math="y = 2x - 1")
    def _(c, p):
        p.plot(f, color=A_COL)
        for x in (0, 1, 3):
            p.point(x, f(x), f"({x}, {f(x)})", color=A_COL, offset=(10, 14), size=14)
        p.label(2.6, 6.3, "y = 2x - 1", color=A_COL, size=18, anchor="end")

    @wt.step("Graph the second equation", "Every point on the orange line makes x + y = 5 true. "
             "It hits both axes at 5.", math="x + y = 5")
    def _(c, p):
        p.plot(g, color=B2_COL)
        p.point(0, 5, "(0, 5)", color=B2_COL, offset=(10, -14), size=14)
        p.point(5, 0, "(5, 0)", color=B2_COL, offset=(8, -14), size=14)
        p.label(4.3, 1.6, "x + y = 5", color=B2_COL, size=18, anchor="start")

    @wt.step("Find the crossing point", f"The lines meet at ({xs}, {ys}). It is the only point on both lines, "
             "so it is the only pair that satisfies both equations.", math=f"(x, y) = ({xs}, {ys})")
    def _(c, p):
        p.vline(xs, color=S_COL, y0=0, y1=ys)
        p.hline(ys, color=S_COL, x0=0, x1=xs)
        p.point(xs, ys, f"({xs}, {ys})", color=S_COL, r=7, offset=(14, 4), size=18)

    @wt.step("Check by substitution", "Plug x = 2 and y = 3 into each equation. Both come out true, so the "
             "graph did not lie.", math=f"3 = 2 \\cdot 2 - 1   and   2 + 3 = 5")
    def _(c, p):
        X, Y = p.px(4.3, 6.3)
        c.label_box(X, Y, "y = 2x - 1:  3 = 2 \\cdot 2 - 1  ✓", color=A_COL, border=A_COL, math=True,
                    size=16, anchor="start")
        c.label_box(X, Y + 40, "x + y = 5:  2 + 3 = 5  ✓", color=B2_COL, border=B2_COL, math=True,
                    size=16, anchor="start")
        c.math(X + 4, Y + 80, "x = 2, y = 3", size=17, color=S_COL, anchor="start")

    return wt
