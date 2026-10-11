"""Quadratics: the parts of a parabola and what the discriminant counts."""

from __future__ import annotations

import math

from .. import theme
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._algebra_helpers import colored_math


@diagram("parabola-anatomy", "Anatomy of a Parabola", "Algebra")
def build_parabola() -> Walkthrough:
    wt = Walkthrough(
        "parabola-anatomy", "Anatomy of a Parabola", "Algebra",
        concept="y = x^2 - 2x - 3 = (x + 1)(x - 3) = (x - 1)^2 - 4",
        summary="Every parabola has a y-intercept, up to two roots, an axis of symmetry halfway between the "
                "roots, and a vertex on that axis. Each one is easy to read from the right form of the equation.",
        width=640, height=440, level="201",
    )
    a, b, c0 = 1, -2, -3
    f = lambda x: a * x * x + b * x + c0
    disc = b * b - 4 * a * c0
    r1 = (-b - math.sqrt(disc)) / (2 * a)
    r2 = (-b + math.sqrt(disc)) / (2 * a)
    h = -b / (2 * a)
    k = f(h)
    INT_COL, ROOT_COL, AX_COL, V_COL = theme.PURPLE, theme.RED, theme.GREEN, theme.ORANGE

    def n(v):
        return f"{v:g}".replace("-", "−")

    @wt.setup
    def _(c):
        p = Plane(c, box=(50, 25, 540, 380), x=(-3, 5), y=(-5, 6))
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    @wt.step("Plot the parabola", "The x² term bends the graph into a U. Since its coefficient is positive, "
             "the U opens upward like a cup.", math="y = x^2 - 2x - 3")
    def _(c, p):
        p.plot(f, color=theme.BLUE)
        p.label(3.45, 3.3, "y = x^2 - 2x - 3", color=theme.BLUE, size=18, anchor="end")

    @wt.step("Find the y-intercept", f"Set x = 0 and every x term vanishes. The constant {n(c0)} is where "
             "the curve crosses the y-axis.", math=f"y(0) = {n(c0)}")
    def _(c, p):
        p.point(0, c0, f"y-intercept (0, {n(c0)})", color=INT_COL, r=6, offset=(-12, 16), anchor="end", size=15, math=False)

    @wt.step("Find the roots", f"Factor: (x + 1)(x − 3) = 0 when x = {n(r1)} or x = {n(r2)}. "
             "These are the points where the curve meets the x-axis.",
             math=f"(x + 1)(x - 3) = 0  \\implies  x = {n(r1)}, x = {n(r2)}")
    def _(c, p):
        p.point(r1, 0, f"root ({n(r1)}, 0)", color=ROOT_COL, r=6, offset=(-10, 30), anchor="end", size=15, math=False)
        p.point(r2, 0, f"root ({n(r2)}, 0)", color=ROOT_COL, r=6, offset=(10, 30), anchor="start", size=15, math=False)

    @wt.step("Draw the axis of symmetry", f"The axis sits halfway between the roots, at x = {n(h)}. "
             "Fold the graph along it and the two halves match.",
             math=f"x = ({n(r1)} + {n(r2)}) / 2 = {n(h)}   or   x = -b / 2a = {n(h)}")
    def _(c, p):
        p.vline(h, color=AX_COL, width=2.2)
        p.label(h + 0.1, 5.5, f"axis x = {n(h)}", color=AX_COL, size=15, anchor="start", math=False)

    @wt.step("Find the vertex", f"The vertex is on the axis. Plug in x = {n(h)} to get y = {n(k)}. "
             "It is the lowest point, the bottom of the cup.",
             math=f"y({n(h)}) = 1 - 2 - 3 = {n(k)},   y = (x - 1)^2 - 4")
    def _(c, p):
        p.point(h, k, f"vertex ({n(h)}, {n(k)})", color=V_COL, r=7, offset=(0, 22), anchor="middle", size=15, math=False)

    @wt.step("Use symmetry for a free point", f"The y-intercept is 1 step left of the axis. Its mirror image "
             f"sits 1 step right, at (2, {n(c0)}), with no extra arithmetic.",
             math=f"y(2) = 4 - 4 - 3 = {n(f(2))}")
    def _(c, p):
        X0, Y0 = p.px(0, c0)
        X1, _ = p.px(2 * h, c0)
        c.arrow(X0 + 9, Y0, X1 - 9, Y0, color=INT_COL, width=1.8, both=True, dash="5 4")
        p.point(2 * h, c0, f"mirror (2, {n(c0)})", color=INT_COL, r=6, hollow=True, offset=(12, 16), size=15, math=False)
        c.text((X0 + p.X(h)) / 2, Y0 - 12, "1", size=13, color=INT_COL, weight="bold", halo=True)
        c.text((X1 + p.X(h)) / 2, Y0 - 12, "1", size=13, color=INT_COL, weight="bold", halo=True)

    return wt


@diagram("discriminant", "The Discriminant: Counting Real Roots", "Algebra")
def build_disc() -> Walkthrough:
    wt = Walkthrough(
        "discriminant", "The Discriminant: Counting Real Roots", "Algebra",
        concept="x = (-b \\pm sqrt(b^2 - 4ac)) / 2a,   D = b^2 - 4ac",
        summary="The part under the square root, D = b² − 4ac, decides how many times a parabola meets the "
                "x-axis: twice when D is positive, once when D is zero, never when D is negative.",
        width=700, height=420, level="201",
    )
    a, b = 1, -4
    cases = [(3, theme.BLUE), (4, theme.ORANGE), (5, theme.PURPLE)]
    D_COL = theme.RED
    PX = 470  # left edge of the right panel

    def n(v):
        return f"{v:g}".replace("-", "−")

    @wt.setup
    def _(c):
        p = Plane(c, box=(40, 30, 375, 360), x=(-0.5, 4.5), y=(-2, 6))
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    @wt.step("Read the quadratic formula", "The formula solves any ax² + bx + c = 0. The red part under "
             "the root is the discriminant D, and it runs the show.",
             math="x = (-b \\pm sqrt(D)) / 2a,   D = b^2 - 4ac")
    def _(c, p):
        cx = PX + 105
        colored_math(c, cx, 52, [("-b \\pm sqrt(", theme.INK), ("b^2 - 4ac", D_COL), (")", theme.INK)], size=20)
        c.line(cx - 95, 70, cx + 95, 70, color=theme.INK, width=1.6)
        c.math(cx, 88, "2a", size=20)
        c.math(PX - 10, 70, "x =", size=20, anchor="end")
        c.text(cx, 112, "D = b² − 4ac", size=14, color=D_COL, weight="bold")

    def row(c, i, cc, col):
        D = b * b - 4 * a * cc
        y = 150 + i * 88
        c.circle(PX + 6, y, 6, color="none", fill=col)
        c.math(PX + 18, y, f"y = x^2 - 4x + {cc}", size=17, color=col, anchor="start")
        c.math(PX + 18, y + 26, f"D = 16 - {4 * cc} = {n(D)}", size=16, color=D_COL, anchor="start")
        if D > 0:
            s = math.sqrt(D)
            res = f"x = (4 \\pm {s:g}) / 2 = {(4 - s) / 2:g}, {(4 + s) / 2:g}"
        elif D == 0:
            res = "x = (4 \\pm 0) / 2 = 2"
        else:
            res = f"sqrt({n(D)}): no real number"
        c.math(PX + 18, y + 52, res, size=16, color=theme.INK, anchor="start")
        return D

    @wt.step("Positive D: two roots", "With c = 3 the vertex dips below the x-axis, so the curve crosses "
             "it twice. D = 4 is positive, and ± sqrt(4) gives two different answers.",
             math="D = (-4)^2 - 4 \\cdot 1 \\cdot 3 = 4 > 0")
    def _(c, p):
        cc, col = cases[0]
        p.plot(lambda x: x * x - 4 * x + cc, color=col)
        row(c, 0, cc, col)
        for r in (1, 3):
            p.point(r, 0, f"({r}, 0)", color=col, r=6, offset=(-8 if r == 1 else 8, 20),
                    anchor="end" if r == 1 else "start", size=14)

    @wt.step("Zero D: one root", "With c = 4 the vertex just touches the axis. D = 0, so ± 0 adds nothing "
             "and both answers collapse into one.", math="D = 16 - 16 = 0")
    def _(c, p):
        cc, col = cases[1]
        p.plot(lambda x: x * x - 4 * x + cc, color=col)
        row(c, 1, cc, col)
        p.point(2, 0, "(2, 0)", color=col, r=6, offset=(-8, 28), anchor="end", size=14)

    @wt.step("Negative D: no real roots", "With c = 5 the whole cup floats above the axis. D = −4, and no "
             "real number squares to a negative, so the formula has nothing real to offer.",
             math="D = 16 - 20 = -4 < 0")
    def _(c, p):
        cc, col = cases[2]
        p.plot(lambda x: x * x - 4 * x + cc, color=col)
        row(c, 2, cc, col)

    @wt.step("See D in the vertex height", "All three cups share the axis x = 2. The vertex height is "
             "−D / 4a, so a positive D means the vertex sits below the axis and the curve must cross.",
             math="vertex y = -D / 4a:   -1,  0,  1")
    def _(c, p):
        p.vline(2, color=theme.GREEN, width=1.8)
        for cc, col in cases:
            D = b * b - 4 * a * cc
            vy = -D / (4 * a)
            p.point(2, vy, None, color=col, r=6)
            X, Y = p.px(2, vy)
            c.text(X + 8, Y + 15, f"y = {n(vy)}", size=13, color=col, weight="bold", anchor="start", halo=True)

    return wt
