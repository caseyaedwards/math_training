"""First-order differential equations: slope fields, Euler's method, and exponential growth and decay."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import brace
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._calculus_tools import num, slope_dir, table_rows, tangent

CAT = "Differential Equations"


# ---------------------------------------------------------------------------
# Slope field
# ---------------------------------------------------------------------------


@diagram("slope-field", "Slope Fields", CAT)
def slope_field() -> Walkthrough:
    wt = Walkthrough(
        "slope-field", "Slope Fields", CAT,
        concept="dy/dx = y, y(0) = 1 \\implies y = e^x",
        summary="A differential equation gives a slope at every point. Draw those slopes as short dashes and "
                "a solution is any curve that follows the dashes.",
        width=660, height=440, level="301",
    )
    xs = [-2 + 0.4 * i for i in range(11) if i != 5]  # skip x = 0 so dashes stay off the y-axis
    ys = [-1.5 + 0.5 * i for i in range(10)]
    rows = {2.0: theme.RED, 1.0: theme.ORANGE, 0.0: theme.BLUE, -1.0: theme.PURPLE}

    @wt.setup
    def _(c):
        p = Plane(c, box=(60, 28, 500, 370), x=(-2.3, 2.3), y=(-2.3, 3.8))
        p.grid(step=0.5, ystep=0.5)
        p.axes(step=1, ystep=1)
        return p

    def dash(p, x, y, col, width=2):
        X, Y = p.px(x, y)
        ux, uy = slope_dir(p, y)
        p.c.line(X - ux * 11, Y - uy * 11, X + ux * 11, Y + uy * 11, color=col, width=width)

    @wt.step("Read the rule", "The equation dy/dx = y says the slope at any point equals its height. "
             "At height 2 the slope is 2, at height 0 it is flat, and below the axis it points down.",
             math="slope at (x, y) = y")
    def _(c, p):
        for y, col in rows.items():
            for x in xs:
                dash(p, x, y, col, width=2.6)
            c.text(p.X(2.3) + 8, p.Y(y) - (12 if y == 0 else 0), f"slope {num(y)}", size=13, color=col,
                   anchor="start")

    @wt.step("Fill in the field", "Draw a dash at every grid point. The slope only depends on y, so each "
             "row repeats the same dash. Up high, the dashes get steep fast.",
             math="dy/dx = y")
    def _(c, p):
        for y in ys:
            if y in rows:
                continue
            for x in xs:
                dash(p, x, y, theme.SOFT_INK, width=1.6)

    @wt.step("Pick a starting point", "An initial condition picks one solution out of the crowd. Start at "
             "(0, 1), where the dash has slope 1.",
             math="y(0) = 1")
    def _(c, p):
        p.point(0, 1, "(0, 1)", color=theme.GREEN, r=7, offset=(-12, -16), anchor="end", size=15)

    @wt.step("Follow the dashes", "Walk forward and backward along the dashes from (0, 1). The path is "
             "y = eˣ, the function that is its own slope.",
             math="y = e^x, dy/dx = e^x = y")
    def _(c, p):
        p.plot(math.exp, -2.3, math.log(3.8), color=theme.GREEN, width=3.5)
        c.math(p.X(math.log(3.8)) + 8, p.Y(3.55), "y = e^x", size=17, color=theme.GREEN, anchor="start",
               halo=True)

    @wt.step("Try other starts", "Other starting heights give other members of the family y = C eˣ. "
             "Start at 0 and you stay at 0 forever, the calmest solution there is.",
             math="y = C e^x for C = 2, 1/2, 0, -1/2")
    def _(c, p):
        for C, col in ((2.0, theme.SKY), (0.5, theme.SKY), (-0.5, theme.PURPLE)):
            p.plot(lambda x, C=C: C * math.exp(x), color=col, width=2.2)
            edge = 3.55 if C > 0 else -2.1
            x_exit = math.log(edge / C)
            c.text(p.X(x_exit) + 8, p.Y(edge), f"C = {num(C)}", size=13, color=col, anchor="start", halo=True)
        p.hline(0, color=theme.BLUE, dash=None, width=2.6)
        c.text(p.X(1.4), p.Y(0) + 13, "C = 0", size=13, color=theme.BLUE, halo=True)

    return wt


# ---------------------------------------------------------------------------
# Euler's method
# ---------------------------------------------------------------------------


def _euler(h: float, n: int):
    pts = [(0.0, 1.0)]
    for _ in range(n):
        x, y = pts[-1]
        pts.append((x + h, y + h * y))
    return pts


@diagram("eulers-method", "Euler's Method", CAT)
def eulers_method() -> Walkthrough:
    pts = _euler(0.5, 4)
    fine = _euler(0.25, 8)
    true2 = math.exp(2)

    wt = Walkthrough(
        "eulers-method", "Euler's Method", CAT,
        concept="y_{n+1} = y_n + h \\cdot f(x_n, y_n), here f(x, y) = y",
        summary="Euler's method walks along a slope field in straight steps: read the slope, step forward h, "
                "repeat. Smaller steps track the true solution more closely.",
        width=700, height=430, level="301",
    )
    TX, TY, COLS, RH = 528, 40, (44, 58, 62), 28

    @wt.setup
    def _(c):
        p = Plane(c, box=(60, 30, 430, 360), x=(-0.2, 2.3), y=(-0.5, 8))
        p.grid(step=0.25, ystep=1)
        p.axes(step=0.5, ystep=1)
        table_rows(c, TX, TY, COLS, [["x", "Euler", "exact"]], row_h=RH, header=True, size=14)
        return p

    def cell(c, row, col, s, color):
        x = TX + sum(COLS[:col])
        table_rows(c, x, TY + RH * row, COLS[col:col + 1], [[s]], row_h=RH, colors=[color], size=14)

    def tally(c, row, x, yv):
        cell(c, row, 0, num(x), theme.INK)
        cell(c, row, 1, num(yv, 4), theme.ORANGE)

    @wt.step("Start with a point and a slope", "Solve dy/dx = y starting from (0, 1). At the start "
             "the slope is the height, 1.",
             math="(x_0, y_0) = (0, 1), slope = 1")
    def _(c, p):
        p.point(0, 1, "(0, 1)", color=theme.ORANGE, offset=(-10, -19), anchor="end", size=14)
        if c.is_new:
            tangent(p, 0, 1, 1, half=40, color=theme.ORANGE, dash="5 4")
        tally(c, 1, 0, 1)

    @wt.step("Take one step", "Move h = 0.5 to the right along that slope. The height rises by "
             "h times slope = 0.5, landing at (0.5, 1.5).",
             math="y_1 = 1 + 0.5 \\cdot 1 = 1.5")
    def _(c, p):
        (x0, y0), (x1, y1) = pts[0], pts[1]
        p.segment(x0, y0, x1, y1, color=theme.ORANGE, width=3)
        p.point(x1, y1, None, color=theme.ORANGE)
        if c.is_new:
            p.segment(x0, y0, x1, y0, color=theme.ORANGE, width=1.4, dash="4 3")
            p.segment(x1, y0, x1, y1, color=theme.ORANGE, width=1.4, dash="4 3")
            c.text(p.X(0.25), p.Y(y0) + 14, "h = 0.5", size=13, color=theme.ORANGE, math=True, halo=True)
            c.text(p.X(x1) + 6, p.Y(1.25), "0.5", size=13, color=theme.ORANGE, math=True, anchor="start", halo=True)
        tally(c, 2, x1, y1)

    @wt.step("Repeat", "At each new point, read the new slope and step again. The slopes 1.5, 2.25, and "
             "3.375 grow with the height, so the path bends upward.",
             math="y_{n+1} = y_n + 0.5 y_n = 1.5 y_n")
    def _(c, p):
        for (x0, y0), (x1, y1) in zip(pts[1:], pts[2:]):
            p.segment(x0, y0, x1, y1, color=theme.ORANGE, width=3)
            p.point(x1, y1, None, color=theme.ORANGE)
        for i, (x, y) in enumerate(pts[2:], start=3):
            tally(c, i, x, y)
        X, Y = p.px(*pts[-1])
        c.text(X + 10, Y + 4, num(pts[-1][1], 4), size=14, color=theme.ORANGE, anchor="start", math=True,
               halo=True)

    @wt.step("Compare with the true solution", "The exact solution is y = eˣ, which reaches about 7.389 "
             "at x = 2. Euler falls short by about 2.33, because each step uses a slope that is already "
             "out of date.",
             math=f"e^2 \\approx {num(true2)}, Euler gives {num(pts[-1][1], 4)}")
    def _(c, p):
        p.plot(math.exp, -0.2, 2.15, color=theme.GREEN, width=3)
        X, Y = p.px(2, true2)
        c.dot(X, Y, r=5, color=theme.GREEN)
        c.text(X + 10, Y, num(true2), size=14, color=theme.GREEN, anchor="start", math=True, halo=True)
        c.math(p.X(1.6) - 10, p.Y(math.exp(1.6)) - 6, "y = e^x", size=16, color=theme.GREEN, anchor="end",
               halo=True)
        for i, (x, _y) in enumerate(pts, start=1):
            cell(c, i, 2, num(math.exp(x)), theme.GREEN)

    @wt.step("Halve the step", "With h = 0.25 the path takes eight shorter steps and ends at about 5.96. "
             "The error drops from 2.33 to 1.43, and it keeps shrinking as h does.",
             math=f"h = 0.25: y(2) \\approx 1.25^8 \\approx {num(fine[-1][1], 2)}")
    def _(c, p):
        c.polyline([p.px(x, y) for x, y in fine], color=theme.PURPLE, width=2.4)
        for x, y in fine[1:]:
            p.point(x, y, None, color=theme.PURPLE, r=3.5)
        X, Y = p.px(*fine[-1])
        c.text(X + 10, Y, num(fine[-1][1], 2), size=14, color=theme.PURPLE, anchor="start", math=True, halo=True)
        c.text(TX, TY + RH * 6 + 22, f"h = 0.25 ends at {num(fine[-1][1], 2)}", size=14, color=theme.PURPLE,
               anchor="start")

    return wt


# ---------------------------------------------------------------------------
# Exponential growth and decay
# ---------------------------------------------------------------------------

Y0 = 80.0
HALF = 2.0
K = -math.log(2) / HALF


@diagram("exponential-decay", "Exponential Decay and Half-Life", CAT)
def exponential_decay() -> Walkthrough:
    y = lambda t: Y0 * math.exp(K * t)

    wt = Walkthrough(
        "exponential-decay", "Exponential Decay and Half-Life", CAT,
        concept="dy/dt = ky \\implies y = y_0 e^{kt}, half-life T = ln 2/|k|",
        summary="When something shrinks at a rate proportional to how much is left, it loses the same "
                "fraction in every equal stretch of time. The time to lose half is the half-life.",
        width=680, height=420, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(60, 34, 560, 340), x=(-0.3, 8.8), y=(-6, 92))
        p.grid(step=1, ystep=10)
        p.axes(step=1, ystep=20, xlabel="t")
        return p

    @wt.step("Rate follows amount", "Start with 80 grams of a substance that decays with k = −0.347 per "
             "hour. The rate dy/dt = ky is steep when there is a lot and gentle when there is little.",
             math=f"at y = 80: dy/dt \\approx {num(K * 80, 1)}; at y = 20: dy/dt \\approx {num(K * 20, 1)}")
    def _(c, p):
        for t in (0.0, 4.0):
            if c.is_new:
                if t == 0:
                    X, Y = p.px(t, y(t))
                    ux, uy = slope_dir(p, K * y(t))
                    c.line(X, Y, X + 60 * ux, Y + 60 * uy, color=theme.ORANGE, width=3)
                else:
                    tangent(p, t, y(t), K * y(t), half=55, color=theme.ORANGE, width=3)
                X, Y = p.px(t, y(t))
                c.text(X + 14, Y - 18, f"slope {num(K * y(t), 1)}", size=13, color=theme.ORANGE, anchor="start",
                       halo=True)
            p.point(t, y(t), None, color=theme.BLUE, r=5)

    @wt.step("Draw the solution", "The curve y = 80 e^(−0.347t) has exactly those slopes. It drops fast "
             "at first and then slows, but never quite reaches zero.",
             math=f"y = 80 e^{{{num(K)} t}}")
    def _(c, p):
        p.plot(y, 0, 8.8, color=theme.BLUE)
        c.math(p.X(1.2) + 10, p.Y(y(1.2)) - 6, "y = 80e^{-0.347t}", size=16, color=theme.BLUE, anchor="start",
               halo=True)

    @wt.step("Find the half-life", "Ask when 80 grams becomes 40. Solve e^(kT) = 1/2 to get T = ln 2/0.347 = 2 "
             "hours.", math="T = ln 2/|k| = 0.693/0.347 = 2")
    def _(c, p):
        p.segment(0, 40, HALF, 40, color=theme.GREEN, dash="5 4", width=1.6)
        p.segment(HALF, 0, HALF, 40, color=theme.GREEN, dash="5 4", width=1.6)
        p.point(HALF, 40, "40", color=theme.GREEN, offset=(10, -12), size=14)
        if c.is_new:
            X0, X1, Yb = p.X(0), p.X(HALF), p.Y(0)
            brace(c, X1, Yb + 26, X0, Yb + 26, "T = 2 hours", color=theme.GREEN, size=15)

    @wt.step("Halve again and again", "Every 2 hours the amount halves: 40, then 20, then 10, then 5. "
             "The same time always cuts the same fraction, no matter how much is left.",
             math="80 \\to 40 \\to 20 \\to 10 \\to 5 at t = 0, 2, 4, 6, 8")
    def _(c, p):
        for i in range(1, 5):
            t = HALF * i
            v = Y0 / 2 ** i
            p.segment(t - HALF, Y0 / 2 ** (i - 1), t, Y0 / 2 ** (i - 1), color=theme.GREEN, dash="2 3", width=1.2)
            if i > 1:
                p.segment(t, 0, t, v, color=theme.GREEN, dash="5 4", width=1.4)
                p.point(t, v, num(v), color=theme.GREEN, offset=(8, -12), size=14)
            if c.is_new:
                X, Ya = p.px(t - HALF / 2, Y0 / 2 ** (i - 1))
                c.text(X, Ya - 12, "÷2", size=13, color=theme.GREEN, halo=True)

    @wt.step("Flip the sign for growth", "With k = +0.347 the same equation describes growth: 10 grams "
             "of yeast doubles every 2 hours, 10, 20, 40, 80. Decay is growth running backward in time.",
             math="k > 0: doubling time = ln 2/k = 2")
    def _(c, p):
        g = lambda t: 10 * math.exp(-K * t)
        p.plot(g, 0, 8.8, color=theme.ORANGE, dash="8 5")
        for i in range(4):
            p.point(HALF * i, 10 * 2 ** i, None, color=theme.ORANGE, r=4)
        c.math(p.X(5.4) - 12, p.Y(g(5.4)), "y = 10e^{0.347t}", size=16, color=theme.ORANGE, anchor="end",
               halo=True)

    return wt


# ---------------------------------------------------------------------------
# The same decay on a log scale
# ---------------------------------------------------------------------------


@diagram("exponential-log-scale", "Exponential Decay on a Log Scale", CAT)
def exponential_log_scale() -> Walkthrough:
    y = lambda t: Y0 * math.exp(K * t)
    ts = [0, 2, 4, 6, 8]

    wt = Walkthrough(
        "exponential-log-scale", "Exponential Decay on a Log Scale", CAT,
        concept="y = y_0 e^{kt} \\iff ln y = ln y_0 + kt",
        summary="Take the logarithm of an exponential and it turns into a straight line. The slope of that "
                "line is the rate constant k.",
        width=720, height=380, level="301",
    )

    @wt.setup
    def _(c):
        left = Plane(c, box=(56, 50, 280, 280), x=(-0.4, 8.8), y=(-6, 90))
        left.grid(step=1, ystep=10)
        left.axes(step=2, ystep=20, xlabel="t")
        right = Plane(c, box=(420, 50, 260, 280), x=(-0.4, 8.8), y=(-0.3, 4.9))
        right.grid(step=1, ystep=0.5)
        right.axes(step=2, ystep=1, xlabel="t", ylabel="ln y")
        c.text(196, 18, "amount y", size=15, color=theme.BLUE, weight="bold")
        c.text(550, 18, "log of the amount, ln y", size=15, color=theme.PURPLE, weight="bold")
        return left, right

    @wt.step("Measure every 2 hours", "Weigh the sample every 2 hours: 80, 40, 20, 10, 5 grams. "
             "Each reading is half the one before.",
             math="y: 80, 40, 20, 10, 5")
    def _(c, pp):
        left, right = pp
        for t in ts:
            left.point(t, y(t), num(y(t)), color=theme.BLUE, offset=(8, -12), size=13)

    @wt.step("The curve bends", "Joined up, the readings make a curve that keeps flattening. The slope "
             "changes everywhere, so k is hard to read off by eye.",
             math="y = 80 e^{kt}")
    def _(c, pp):
        left, right = pp
        left.plot(y, 0, 8.8, color=theme.BLUE, width=2.6)

    @wt.step("Take the log of each reading", "Plot ln y instead of y. Halving always subtracts the same "
             "amount, ln 2 ≈ 0.693, so the dots fall in equal steps.",
             math="ln 80 \\approx 4.38, ln 40 \\approx 3.69, ln 20 \\approx 3.00, ...")
    def _(c, pp):
        left, right = pp
        for t in ts:
            right.point(t, math.log(y(t)), f"{math.log(y(t)):.2f}", color=theme.PURPLE, offset=(8, -12), size=13)

    @wt.step("Read k as a slope", "The dots lie on a straight line. Its slope is −0.693/2 = −0.347, which is k, "
             "and it crosses the axis at ln 80. Straight lines are much easier to read than curves.",
             math=f"ln y = ln 80 + kt, k = -0.693/2 \\approx {num(K)}")
    def _(c, pp):
        left, right = pp
        right.plot(lambda t: math.log(Y0) + K * t, -0.4, 8.8, color=theme.PURPLE, width=2.6)
        a, b = 4.0, 6.0
        la, lb = math.log(y(a)), math.log(y(b))
        right.segment(a, la, a, lb, color=theme.ORANGE, width=2)
        right.segment(a, lb, b, lb, color=theme.ORANGE, width=2)
        c.text(right.X(5), right.Y(lb) + 14, "run 2", size=13, color=theme.ORANGE, halo=True)
        c.text(right.X(a) - 6, right.Y((la + lb) / 2), "−0.693", size=13, color=theme.ORANGE, anchor="end",
               halo=True)
    return wt
