"""Derivatives as slopes: graphing f', zooming in to see local linearity, and the mean value theorem."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import tick_marks
from ..plane import Plane, tick_label
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._calculus_tools import num, tangent


# ---------------------------------------------------------------------------
# Graphing the derivative
# ---------------------------------------------------------------------------


@diagram("derivative-graph", "Graphing the Derivative", "Calculus")
def derivative_graph() -> Walkthrough:
    f = lambda x: x ** 3 - 3 * x
    df = lambda x: 3 * x * x - 3
    xs = [-2 + 0.5 * i for i in range(9)]

    wt = Walkthrough(
        "derivative-graph", "Graphing the Derivative", "Calculus",
        concept="f(x) = x^3 - 3x \\implies f'(x) = 3x^2 - 3",
        summary="Measure the slope of f at many points and plot each slope as a height. The dots trace a "
                "new graph, the derivative f'.",
        width=660, height=470, level="301",
    )
    ROW = 247  # the slope readout row between the two planes

    @wt.setup
    def _(c):
        top = Plane(c, box=(80, 30, 500, 180), x=(-2.4, 2.4), y=(-3.4, 3.4))
        top.grid(step=0.5, ystep=1)
        top.axes(step=1, ystep=2, ylabel="")
        bot = Plane(c, box=(80, 275, 500, 180), x=(-2.4, 2.4), y=(-4.5, 10.5))
        bot.grid(step=0.5, ystep=3)
        bot.axes(step=1, ystep=3, ylabel="", yfmt=lambda v: "" if v < 0 else tick_label(v))
        c.text(20, top.Y(0), "f", size=20, color=theme.INK, math=True, weight="bold")
        c.text(20, bot.Y(3), "f'", size=20, color=theme.ORANGE, math=True, weight="bold")
        c.text(20, ROW, "slope", size=12, color=theme.ORANGE)
        return top, bot

    @wt.step("Graph the function", "The curve f(x) = x³ − 3x climbs, turns at a peak, falls, turns at a "
             "valley, and climbs again. The empty grid below waits for its slopes.",
             math="f(x) = x^3 - 3x")
    def _(c, pp):
        top, bot = pp
        top.plot(f, -2.15, 2.15, color=theme.INK)
        top.point(-1, 2, "peak (−1, 2)", color=theme.INK, offset=(0, -16), anchor="middle", math=False, size=13)
        top.point(1, -2, "valley (1, −2)", color=theme.INK, offset=(0, 16), anchor="middle", math=False, size=13)
        c.math(top.X(-1.05), top.Y(-2.3), "f(x) = x^3 - 3x", size=16, halo=True)

    @wt.step("Measure the slope at many points", "Lay a short tangent on the curve every half unit and "
             "read its slope. Steep climbs give big positive numbers, the peak and valley give 0.",
             math="slopes at x = -2, -1, 0, 1, 2: 9, 0, -3, 0, 9")
    def _(c, pp):
        top, bot = pp
        for x in xs:
            tangent(top, x, f(x), df(x), half=20, color=theme.ORANGE, width=3)
            c.text(top.X(x), ROW, num(df(x), 2), size=13, color=theme.ORANGE, math=True, halo=True)

    @wt.step("Plot each slope as a height", "Carry each slope straight down and plot it as a point "
             "(x, slope). The slope at x = 0 is −3, so that dot sits at height −3.",
             math="(x, f'(x)): (-2, 9), (-1, 0), (0, -3), (1, 0), (2, 9)")
    def _(c, pp):
        top, bot = pp
        for x in xs:
            if c.is_new:
                c.line(top.X(x), top.Y(f(x)) + 8, bot.X(x), bot.Y(df(x)) - 6, color=theme.ORANGE, width=1,
                       dash="2 4")
            bot.point(x, df(x), None, color=theme.ORANGE, r=5)

    @wt.step("Connect the dots", "The dots lie on a parabola. That parabola is the graph of the "
             "derivative, a new function whose height is the old function's slope.",
             math="f'(x) = 3x^2 - 3")
    def _(c, pp):
        top, bot = pp
        bot.plot(df, -2.4, 2.4, color=theme.ORANGE)
        c.math(bot.X(-0.15), bot.Y(7.5), "f'(x) = 3x^2 - 3", size=16, color=theme.ORANGE, anchor="end", halo=True)

    @wt.step("Read the signs", "Where f' is above the axis, f climbs (green). Where f' dips below, f falls "
             "(red). The zeros of f' line up with the peak and the valley.",
             math="f' > 0: f rises,  f' < 0: f falls,  f' = 0: f is flat")
    def _(c, pp):
        top, bot = pp
        bot.shade_between(df, lambda x: 0.0, -2.4, -1, color=theme.GREEN, opacity=0.25)
        bot.shade_between(df, lambda x: 0.0, -1, 1, color=theme.RED, opacity=0.25)
        bot.shade_between(df, lambda x: 0.0, 1, 2.4, color=theme.GREEN, opacity=0.25)
        for a, b, col in ((-2.15, -1, theme.GREEN), (-1, 1, theme.RED), (1, 2.15, theme.GREEN)):
            top.plot(f, a, b, color=col, width=5)
        c.text(bot.X(-1.85), bot.Y(1.3), "rising", size=13, color=theme.GREEN, halo=True)
        c.text(bot.X(-0.5), bot.Y(-0.95), "falling", size=13, color=theme.RED, halo=True)
        c.text(bot.X(1.85), bot.Y(1.3), "rising", size=13, color=theme.GREEN, halo=True)

    return wt


# ---------------------------------------------------------------------------
# Local linearity: zoom in until the curve looks straight
# ---------------------------------------------------------------------------


@diagram("local-linearity", "Zoom In: Curves Look Straight", "Calculus")
def local_linearity() -> Walkthrough:
    f = lambda x: x * x
    a = 1.0
    halves = [1.0, 0.25, 0.0625]
    colors = [theme.BLUE, theme.PURPLE, theme.RED]

    wt = Walkthrough(
        "local-linearity", "Zoom In: Curves Look Straight", "Calculus",
        concept="f(1 + h) \\approx f(1) + f'(1) h = 1 + 2h  for small h",
        summary="Zoom in on a smooth curve and it straightens out. The line it turns into is the tangent "
                "line, and its slope is the derivative.",
        width=720, height=330, level="301",
    )
    S, TOP = 196, 60
    lefts = [30, 262, 494]

    def panel(c, i):
        h = halves[i]
        p = Plane(c, box=(lefts[i], TOP, S, S), x=(a - h, a + h), y=(f(a) - 2 * h, f(a) + 2 * h))
        c.rect(p.left, p.top, S, S, color=colors[i], fill=theme.PAPER, width=2)
        p.grid(step=h / 2, ystep=h)
        return p

    @wt.setup
    def _(c):
        return None

    def window_box(p, i):
        h = halves[i]
        p.rect(a - h, f(a) - 2 * h, a + h, f(a) + 2 * h, color=colors[i], width=2)

    def caption_under(c, i, s):
        c.text(lefts[i] + S / 2, TOP + S + 22, s, size=14, color=colors[i], math=True)

    def labels(c, i):
        h = halves[i]
        c.text(lefts[i] + S / 2, TOP - 24, f"zoom ×{num(1 / h)}", size=15, color=colors[i], weight="bold")
        caption_under(c, i, f"x from {num(a - h, 4)} to {num(a + h, 4)}")

    @wt.step("Look at the whole curve", "The parabola y = x² bends a lot between x = 0 and x = 2. "
             "Mark the point (1, 1) and draw a smaller window around it.",
             math="f(x) = x^2, point (1, 1)")
    def _(c, _ctx):
        p = panel(c, 0)
        p.plot(f, color=theme.INK, width=3)
        p.point(a, f(a), None, color=theme.INK)
        window_box(p, 1)
        labels(c, 0)
        c.text(lefts[0] + 10, TOP + 18, "y = x²", size=15, color=theme.INK, anchor="start", halo=True)

    @wt.step("Zoom in four times", "Blow up the pink window around (1, 1). The same curve now bends only a little.",
             math="window: 1 \\pm 0.25")
    def _(c, _ctx):
        p = panel(c, 1)
        p.plot(f, color=theme.INK, width=3)
        p.point(a, f(a), None, color=theme.INK)
        window_box(p, 2)
        labels(c, 1)
        if c.is_new:
            c.arrow(lefts[0] + S + 6, TOP + S / 2, lefts[1] - 6, TOP + S / 2, color=colors[1], width=2)

    @wt.step("Zoom in sixteen times", "Blow up the orange window. Now the curve is hard to tell from a "
             "ruler line. Curves are just lines that zoomed out too far.",
             math="window: 1 \\pm 0.0625")
    def _(c, _ctx):
        p = panel(c, 2)
        p.plot(f, color=theme.INK, width=3)
        p.point(a, f(a), None, color=theme.INK)
        labels(c, 2)
        if c.is_new:
            c.arrow(lefts[1] + S + 6, TOP + S / 2, lefts[2] - 6, TOP + S / 2, color=colors[2], width=2)

    @wt.step("Compare with the tangent line", "Lay the line y = 1 + 2(x − 1) over every panel. The gap "
             "between curve and line is h², so it shrinks sixteen times with each zoom while the window "
             "shrinks four times.",
             math="gap = x^2 - (1 + 2h) = h^2, window height = 4h")
    def _(c, _ctx):
        for i in range(3):
            h = halves[i]
            p = Plane(c, box=(lefts[i], TOP, S, S), x=(a - h, a + h), y=(f(a) - 2 * h, f(a) + 2 * h))
            p.line_through(a, f(a), a + 1, f(a) + 2, color=theme.GREEN, width=2.4, dash="7 5")
            X, Y = p.px(a - h, f(a - h))
            X2, Y2 = p.px(a - h, f(a) - 2 * h)
            c.line(X + 5, Y, X + 5, Y2, color=theme.ORANGE, width=4)
            c.text(lefts[i] + S / 2, TOP + S + 44, f"gap {num(h * h, 4)}, {num(100 * h / 4, 1)}% of the window", size=13,
                   color=theme.ORANGE)
        c.text(lefts[0] + S - 10, TOP + S - 14, "slope 2", size=14, color=theme.GREEN, anchor="end", halo=True)

    return wt


# ---------------------------------------------------------------------------
# Mean value theorem
# ---------------------------------------------------------------------------


@diagram("mean-value-theorem", "Mean Value Theorem", "Calculus")
def mean_value_theorem() -> Walkthrough:
    f = math.sqrt
    df = lambda x: 0.5 / math.sqrt(x)
    a, b = 1.0, 9.0
    m = (f(b) - f(a)) / (b - a)
    cc = (0.5 / m) ** 2  # solves f'(c) = m

    wt = Walkthrough(
        "mean-value-theorem", "Mean Value Theorem", "Calculus",
        concept="f'(c) = (f(b) - f(a))/(b - a) for some c in (a, b)",
        summary="On a smooth curve, the average slope between two points equals the exact slope at some "
                "point in between. Somewhere, the tangent is parallel to the secant.",
        width=660, height=380, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(60, 30, 540, 310), x=(-0.3, 10), y=(-0.4, 3.6))
        p.grid(step=1, ystep=0.5)
        p.axes(step=1, ystep=1)
        p.plot(f, 0, 10, color=theme.INK)
        c.math(p.X(1.3), p.Y(2.5), "y = sqrt(x)", size=17, anchor="start", halo=True)
        return p

    @wt.step("Pick two points", "Take the curve y = √x from a = 1 to b = 9. The endpoints are "
             "A = (1, 1) and B = (9, 3).", math="f(1) = 1, f(9) = 3")
    def _(c, p):
        p.point(a, f(a), "A", color=theme.INK, offset=(4, 16), anchor="start")
        p.point(b, f(b), "B", color=theme.INK, offset=(10, 16), anchor="start")

    @wt.step("Draw the secant line", "The line from A to B rises 2 over a run of 8. Its slope 1/4 is the "
             "average slope of the curve on [1, 9].",
             math=f"(f(9) - f(1))/(9 - 1) = 2/8 = {num(m)}")
    def _(c, p):
        p.segment(a, f(a), b, f(b), color=theme.ORANGE, width=3)
        p.segment(a, f(a), b, f(a), color=theme.ORANGE, width=1.5, dash="5 4")
        p.segment(b, f(a), b, f(b), color=theme.ORANGE, width=1.5, dash="5 4")
        c.text(p.X(5), p.Y(f(a)) + 15, "run 8", size=14, color=theme.ORANGE, halo=True)
        c.text(p.X(b) + 8, p.Y(2.0), "rise 2", size=14, color=theme.ORANGE, anchor="start", halo=True)
        c.text(p.X(6.6), p.Y(1 + m * 5.6) + 16, "slope 1/4", size=14, color=theme.ORANGE, halo=True)

    @wt.step("Try some tangent lines", "At x = 2 the tangent is too steep. At x = 8 it is too shallow. "
             "Somewhere between, the slope must pass through 1/4.",
             math=f"f'(2) \\approx {num(df(2))} > 0.25 > f'(8) \\approx {num(df(8))}")
    def _(c, p):
        for x, side in ((2.0, -1), (8.0, 1)):
            if not c.is_new:
                break
            col = theme.PURPLE
            tangent(p, x, f(x), df(x), half=120, color=col, width=2.2, dash="7 4")
            p.point(x, f(x), None, color=col, r=4)
            if c.is_new:
                X, Y = p.px(x, f(x))
                c.text(X - 6, Y - 26 if side < 0 else Y - 20, f"slope {num(df(x))}", size=13, color=col,
                       anchor="end" if side < 0 else "middle", halo=True)

    @wt.step("Find the parallel tangent", "At c = 4 the tangent slope is exactly 1/4, so the tangent runs "
             "parallel to the secant. Drive 8 miles in 32 minutes and at some moment the speedometer reads "
             "exactly your average speed.",
             math=f"f'(c) = 1/(2 sqrt(c)) = 1/4 \\implies c = {num(cc)}")
    def _(c, p):
        y0 = f(cc)
        p.line_through(cc, y0, cc + 1, y0 + m, color=theme.GREEN, width=3)
        p.point(cc, y0, None, color=theme.GREEN)
        p.vline(cc, color=theme.GREEN, dash="4 4", width=1.4, y0=0, y1=y0)
        c.text(p.X(cc), p.Y(0) + 34, "c = 4", size=15, color=theme.GREEN, math=True, halo=True)
        X, Y = p.px(cc, y0)
        c.text(X - 10, Y - 18, "(4, 2)", size=14, color=theme.GREEN, anchor="end", math=True, halo=True)
        # equal-slope marks on both lines
        tick_marks(c, p.px(0.3, y0 - m * 3.7), p.px(0.9, y0 - m * 3.1), count=2, color=theme.GREEN)
        tick_marks(c, p.px(3.0, 1 + m * 2), p.px(3.6, 1 + m * 2.6), count=2, color=theme.ORANGE)
        c.text(p.X(1.4), p.Y(3.25), "tangent, slope 1/4", size=14, color=theme.GREEN, anchor="start", halo=True)

    return wt
