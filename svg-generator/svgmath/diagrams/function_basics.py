"""What a function is: machines, mapping diagrams, domain and range, symmetry."""

from __future__ import annotations

import math

from .. import theme
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._function_kit import axis_bar, ball, ctable, machine, num, tag

CAT = "Functions"


# ---------------------------------------------------------------------------
# Function machine
# ---------------------------------------------------------------------------


@diagram("function-machine", "Function Machine", CAT)
def build_machine() -> Walkthrough:
    wt = Walkthrough(
        "function-machine", "Function Machine", CAT,
        concept="f(x) = 2x + 1:  3 \\to 7,  0 \\to 1,  -2 \\to -3",
        summary="A function is a machine with one rule. Each input goes in, the rule runs, and exactly one "
                "output comes out. The input and output pairs land on the graph.",
        width=720, height=400, level="201",
    )

    def f(x):
        return 2 * x + 1

    inputs = [3, 0, -2]
    IN, OUT, FN = theme.BLUE, theme.ORANGE, theme.PURPLE
    MX, MY, MW, MH = 190, 50, 170, 120
    CY = MY + MH / 2

    @wt.setup
    def _(c):
        p = Plane(c, box=(500, 34, 190, 340), x=(-3, 4), y=(-4, 8))
        p.grid(step=1, ystep=1)
        p.axes(step=1, ystep=2)
        return p

    def feed(c, p, k):
        x = inputs[k]
        y = f(x)
        if c.is_new:
            ball(c, 80, CY, num(x), IN)
            c.text(80, CY - 38, "input", size=13, color=IN, weight="bold")
            c.arrow(104, CY, 162, CY, color=IN, width=2.5)
            c.math(MX + MW / 2, MY + MH - 24, f"2 \\cdot {num(x) if x >= 0 else '(' + num(x) + ')'} + 1 = {num(y)}", size=16, color=FN)
            c.arrow(MX + MW + 24, CY, MX + MW + 70, CY, color=OUT, width=2.5)
            ball(c, MX + MW + 96, CY, num(y), OUT)
            c.text(MX + MW + 96, CY - 38, "output", size=13, color=OUT, weight="bold")
        rows = [[num(v), num(f(v))] for v in inputs[: k + 1]]
        ctable(c, 140, 220, ["input x", "output f(x)"], rows, [110, 110], [IN, OUT],
               highlight=k if c.is_new else None)
        X, Y = p.px(x, y)
        c.dot(X, Y, r=6, color=FN)
        lab = f"({num(x)}, {num(y)})"
        if x == 3:
            c.text(X - 10, Y + 2, lab, size=14, color=FN, anchor="end", math=True, halo=True)
        else:
            c.text(X + 10, Y + 12, lab, size=14, color=FN, anchor="start", math=True, halo=True)

    @wt.step("Meet the machine", "A function is a machine with one fixed rule. This one doubles what goes "
             "in, then adds one. No moods, no surprises.", math="f(x) = 2x + 1")
    def _(c, p):
        machine(c, MX, MY, MW, MH, FN, "function f", "f(x) = 2x + 1" if c.is_new else None)
        if c.is_new:
            c.text(MX + MW / 2, MY + MH - 24, "double, then add 1", size=14, color=theme.SOFT_INK)
        else:
            c.math(MX + MW / 2, MY + 48, "f(x) = 2x + 1", size=19, color=FN)
        c.text(140 + 110, 206, "input and output pairs", size=13, color=theme.SOFT_INK)
        c.text(595, 392, "pairs as points (x, f(x))", size=12, color=theme.SOFT_INK)

    @wt.step("Feed in 3", "Drop 3 into the machine. It doubles 3 to get 6, adds one, and pushes out 7. "
             "Write the pair in the table and plot it.", math="f(3) = 2 \\cdot 3 + 1 = 7")
    def _(c, p):
        feed(c, p, 0)

    @wt.step("Feed in 0", "Zero goes in. Double zero is still zero, plus one gives 1.",
             math="f(0) = 2 \\cdot 0 + 1 = 1")
    def _(c, p):
        feed(c, p, 1)

    @wt.step("Feed in a negative", "The machine takes negatives too. Double −2 is −4, and −4 + 1 is −3.",
             math="f(-2) = 2 \\cdot (-2) + 1 = -3")
    def _(c, p):
        feed(c, p, 2)

    @wt.step("Connect the pairs", "Each input gives exactly one output, so each x gets one point. Every "
             "input you could feed in fills the line y = 2x + 1: that line is the graph of f.",
             math="graph of f: y = 2x + 1")
    def _(c, p):
        p.plot(f, -2.5, 3.5, color=FN, width=2.5)
        for x in inputs:
            p.point(x, f(x), color=FN, r=6)
        c.math(MX + MW / 2, MY + MH - 24, "any x \\to 2x + 1", size=16, color=FN)
        c.math(p.X(2.0), p.Y(2.6), "y = 2x + 1", size=15, color=FN, anchor="start", halo=True)

    return wt


# ---------------------------------------------------------------------------
# Mapping diagram
# ---------------------------------------------------------------------------


def _oval(c, cx, cy, rx, ry, title, color=theme.SOFT_INK):
    c.ellipse(cx, cy, rx, ry, color=color, fill=theme.PANEL, width=2)
    c.text(cx, cy - ry - 14, title, size=13, color=color, weight="bold")


@diagram("mapping-diagram", "Mapping Diagrams", CAT)
def build_mapping() -> Walkthrough:
    wt = Walkthrough(
        "mapping-diagram", "Mapping Diagrams", CAT,
        concept="function: each input has exactly one arrow out",
        summary="Draw the inputs in one oval and the possible outputs in another, then draw an arrow for each "
                "pair. A function sends exactly one arrow out of every input. On a graph this becomes the "
                "vertical line test.",
        width=720, height=400, level="201",
    )
    LX, RX, CY, RY = 95, 270, 215, 118
    dom = [-2, -1, 1, 2]
    dom_y = {v: 140 + i * 50 for i, v in enumerate(dom)}
    cod = [1, 4, 9]
    cod_y = {1: 155, 4: 215, 9: 275}
    # right panel: y^2 = x
    LX2, RX2 = 455, 630
    dom2 = [0, 1, 4]
    dom2_y = {0: 155, 1: 215, 4: 275}
    cod2 = [2, 1, 0, -1, -2]
    cod2_y = {v: 125 + i * 45 for i, v in enumerate(cod2)}

    def elem(c, x, y, v, color=theme.INK):
        c.text(x, y, num(v), size=17, color=color, math=True, weight="bold")

    @wt.step("Draw the inputs and outputs", "Put the inputs in the left oval, the domain. Put the "
             "outputs we allow in the right oval, the codomain. The rule is: square it.",
             math="domain {-2, -1, 1, 2},  codomain {1, 4, 9}")
    def _(c):
        c.math((LX + RX) / 2, 26, "rule: x \\to x^2", size=18, color=theme.BLUE)
        _oval(c, LX, CY, 52, RY, "domain")
        _oval(c, RX, CY, 52, RY, "codomain")
        for v in dom:
            elem(c, LX, dom_y[v], v, theme.BLUE)
        for v in cod:
            elem(c, RX, cod_y[v], v)
        c.line(360, 20, 360, 380, color=theme.GRID, width=1.5)

    @wt.step("Draw one arrow per input", "Each input gets one arrow to its square. Two inputs may share "
             "an output: −2 and 2 both go to 4. That is fine. A function only forbids one input with two "
             "outputs.", math="-2 \\to 4,  -1 \\to 1,  1 \\to 1,  2 \\to 4")
    def _(c):
        for v in dom:
            c.arrow(LX + 22, dom_y[v], RX - 18, cod_y[v * v], color=theme.BLUE, width=2)
        c.text(LX, 362, "1 arrow out of each input", size=13, color=theme.BLUE)

    @wt.step("Read the range", "The range is the outputs that actually get hit: 1 and 4. Nobody sends an "
             "arrow to 9. It sits in the codomain, unused, like a spare chair.",
             math="range = {1, 4} \\subset codomain")
    def _(c):
        for v in (1, 4):
            c.circle(RX, cod_y[v], 16, color=theme.ORANGE, width=2.5)
        c.text(RX, cod_y[9] + 24, "no arrow in", size=12, color=theme.SOFT_INK)
        c.text(RX, 362, "range = {1, 4}", size=13, color=theme.ORANGE, weight="bold")

    @wt.step("Break the rule", "Now pair each x with every y where y² = x. The input 1 sends arrows to 1 "
             "and −1, and 4 sends arrows to 2 and −2. Two arrows from one input: not a function.",
             math="1 \\to \\pm 1,  4 \\to \\pm 2:  two outputs, so no function")
    def _(c):
        c.math((LX2 + RX2) / 2, 26, "rule: x \\to y with y^2 = x", size=18, color=theme.RED)
        _oval(c, LX2, CY, 52, RY, "domain")
        _oval(c, RX2, CY, 52, RY + 10, "codomain")
        for v in dom2:
            elem(c, LX2, dom2_y[v], v, theme.RED if v else theme.INK)
        for v in cod2:
            elem(c, RX2, cod2_y[v], v)
        c.arrow(LX2 + 22, dom2_y[0], RX2 - 18, cod2_y[0], color=theme.SOFT_INK, width=2)
        for v in (1, 4):
            r = int(round(math.sqrt(v)))
            for s in (r, -r):
                c.arrow(LX2 + 22, dom2_y[v], RX2 - 18, cod2_y[s], color=theme.RED, width=2)
        for v in (1, 4):
            c.circle(LX2, dom2_y[v], 15, color=theme.RED, width=2.5)
        c.text((LX2 + RX2) / 2, 372, "1 and 4 each have 2 arrows", size=13, color=theme.RED, weight="bold")

    @wt.step("Turn arrows into a graph", "Plot each arrow as a point (input, output). A vertical line "
             "x = 1 picks one input. It hits y = x² once, but it hits y² = x twice. One hit means function.",
             math="vertical line test: at most one hit per vertical line", fresh=True)
    def _(c):
        p = Plane(c, box=(30, 40, 310, 320), x=(-3, 3), y=(-1, 5), equal=True)
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        p.plot(lambda x: x * x, -2.3, 2.3, color=theme.BLUE)
        for v in dom:
            p.point(v, v * v, color=theme.BLUE, r=5)
        p.vline(1, color=theme.GREEN, width=2.5, dash="7 5")
        p.point(1, 1, color=theme.GREEN, r=8, hollow=True)
        p.label(1.15, 4.4, "x = 1", color=theme.GREEN, anchor="start", size=15)
        c.math(p.X(-2.5), p.Y(4.5), "y = x^2", size=16, color=theme.BLUE, anchor="start", halo=True)
        c.text(p.X(0), 380, "1 hit: function", size=14, color=theme.GREEN, weight="bold")

        q = Plane(c, box=(380, 40, 310, 320), x=(-1, 5), y=(-3, 3), equal=True)
        q.grid(step=1)
        q.axes(step=1, ystep=1)
        q.parametric(lambda t: t * t, lambda t: t, -2.25, 2.25, color=theme.RED)
        for v in cod2:
            q.point(v * v, v, color=theme.RED, r=5)
        q.vline(1, color=theme.RED, width=2.5, dash="7 5")
        for s in (1, -1):
            q.point(1, s, color=theme.RED, r=8, hollow=True)
        q.label(1.15, 2.6, "x = 1", color=theme.RED, anchor="start", size=15)
        c.math(q.X(3.0), q.Y(-2.4), "y^2 = x", size=16, color=theme.RED, anchor="start", halo=True)
        c.text(q.X(2), 380, "2 hits: not a function", size=14, color=theme.RED, weight="bold")

    return wt


# ---------------------------------------------------------------------------
# Domain and range as shadows
# ---------------------------------------------------------------------------


@diagram("domain-range", "Domain and Range as Shadows", CAT)
def build_domain_range() -> Walkthrough:
    wt = Walkthrough(
        "domain-range", "Domain and Range as Shadows", CAT,
        concept="f(x) = (x - 1)^2 - 3 on [-1, 3]:  domain [-1, 3], range [-3, 1]",
        summary="Shine a light straight down on a graph and its shadow on the x-axis is the domain. Shine a "
                "light from the side and its shadow on the y-axis is the range.",
        width=680, height=400, level="201",
    )
    a, b = -1, 3

    def f(x):
        return (x - 1) ** 2 - 3

    vx, vy = 1, f(1)
    top = max(f(a), f(b))
    D, R = theme.BLUE, theme.ORANGE

    @wt.setup
    def _(c):
        p = Plane(c, box=(50, 34, 560, 336), x=(-3, 5.5), y=(-4.5, 3.5))
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    @wt.step("Draw the graph", "This graph starts at x = −1 and stops at x = 3. The solid dots say both "
             "ends belong to the graph.", math="f(x) = (x - 1)^2 - 3,  -1 \\leq x \\leq 3")
    def _(c, p):
        p.plot(f, a, b, color=theme.INK)
        p.point(a, f(a), "(-1, 1)", color=theme.INK, offset=(-10, -14), anchor="end")
        p.point(b, f(b), "(3, 1)", color=theme.INK, offset=(10, -14))

    @wt.step("Shadow on the x-axis", "Shine a light straight down. The graph throws a shadow on the x-axis "
             "from −1 to 3. That shadow is the domain: every x the graph uses.",
             math="domain: -1 \\leq x \\leq 3")
    def _(c, p):
        p.shade_between(f, lambda x: 0, a, b, color=D, opacity=0.13)
        for x in (a, b):
            p.vline(x, color=D, y0=0, y1=f(x), width=1.8)
        axis_bar(c, p.px(a, 0), p.px(b, 0), D)
        for x in (-0.6, 1, 2.6):
            X = p.X(x)
            c.arrow(X, p.Y(3.3), X, p.Y(2.0), color=D, width=1.8)
        c.text(p.X(1), p.Y(3.3) - 10, "light from above", size=12, color=D)
        c.text(p.X(1), p.Y(0) + 34, "domain", size=14, color=D, weight="bold", halo=True)

    @wt.step("Shadow on the y-axis", "Now shine the light from the side. The shadow on the y-axis runs from "
             "the lowest point, −3, up to 1. The bottom comes from the turning point, not an end.",
             math="range: -3 \\leq y \\leq 1")
    def _(c, p):
        for (x, y) in ((a, f(a)), (b, f(b)), (vx, vy)):
            p.segment(x, y, 0, y, color=R, width=1.6, dash="5 4")
        axis_bar(c, p.px(0, vy), p.px(0, top), R)
        p.point(vx, vy, "lowest (1, -3)", color=R, offset=(12, 4))
        c.text(p.X(0) - 28, p.Y(-1.5), "range", size=14, color=R, weight="bold", anchor="end", halo=True)
        for y in (-2.5, -0.5):
            c.arrow(p.X(5.3), p.Y(y), p.X(4.3), p.Y(y), color=R, width=1.8)
        c.text(p.X(4.8), p.Y(-1.5), "light", size=12, color=R)

    @wt.step("Write both shadows", "Square brackets mean the ends count, because the dots are solid. Each "
             "shadow is one interval. Both ends of the graph sit at height 1, and neither one sets the "
             "bottom.", math="domain [-1, 3],  range [-3, 1]")
    def _(c, p):
        tag(c, 505, 50, "domain = [-1, 3]", D, size=16)
        tag(c, 505, 86, "range = [-3, 1]", R, size=16)

    return wt


# ---------------------------------------------------------------------------
# Even and odd functions
# ---------------------------------------------------------------------------


@diagram("even-odd-functions", "Even and Odd Functions", CAT)
def build_even_odd() -> Walkthrough:
    wt = Walkthrough(
        "even-odd-functions", "Even and Odd Functions", CAT,
        concept="even: f(-x) = f(x)    odd: g(-x) = -g(x)",
        summary="An even function looks the same in a mirror held on the y-axis. An odd function looks the "
                "same after a half turn about the origin.",
        width=720, height=400, level="201",
    )
    E, O = theme.BLUE, theme.GREEN

    def f(x):
        return x * x / 2 - 1

    def g(x):
        return x ** 3 / 4 - x / 2

    @wt.setup
    def _(c):
        p = Plane(c, box=(25, 62, 320, 300), x=(-3.5, 3.5), y=(-3, 3.5), equal=True)
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        q = Plane(c, box=(385, 62, 320, 300), x=(-3.5, 3.5), y=(-3, 3.5), equal=True)
        q.grid(step=1)
        q.axes(step=1, ystep=1)
        return p, q

    @wt.step("Plot an even function", "Here is f(x) = x²/2 − 1. The left half looks like the right half "
             "in a mirror.", math="f(x) = x^2/2 - 1")
    def _(c, pq):
        p, _ = pq
        p.plot(f, -3, 3, color=E)
        c.math(p.X(-3.3), p.Y(-1.9), "f(x) = x^2/2 - 1", size=16, color=E, anchor="start", halo=True)

    @wt.step("Mirror on the y-axis", "Pick x = 2 and x = −2. Both give 1, so the two points sit at the same "
             "height, the same distance from the y-axis. That is the mirror rule.",
             math="f(-2) = f(2) = 1")
    def _(c, pq):
        p, _ = pq
        p.vline(0, color=E, width=3, dash="2 5")
        y = f(2)
        for s in (1, -1):
            p.vector(0, y, 2 * s, y, color=theme.SOFT_INK, width=1.6)
            p.point(2 * s, y, color=E)
        p.label(1, y + 0.3, "2", color=theme.SOFT_INK, size=14)
        p.label(-1, y + 0.3, "2", color=theme.SOFT_INK, size=14)
        p.label(2.15, y - 0.35, "(2, 1)", color=E, anchor="start", size=14)
        p.label(-2.15, y - 0.35, "(-2, 1)", color=E, anchor="end", size=14)
        c.text(p.X(1.9), p.Y(-2.5), "mirror: y-axis", size=13, color=E, weight="bold", halo=True)

    @wt.step("Plot an odd function", "Here is g(x) = x³/4 − x/2. Its left half is the right half flipped "
             "upside down as well as left to right.", math="g(x) = x^3/4 - x/2")
    def _(c, pq):
        _, q = pq
        q.plot(g, -3, 3, color=O)
        c.math(q.X(0.2), q.Y(-2.3), "g(x) = x^3/4 - x/2", size=16, color=O, anchor="start", halo=True)

    @wt.step("Half turn about the origin", "Pick x = 2: g(2) = 1. Then g(−2) = −1. The segment between the "
             "two points passes through the origin, and the origin is its midpoint.",
             math="g(-2) = -g(2) = -1")
    def _(c, pq):
        _, q = pq
        q.segment(2, g(2), -2, g(-2), color=theme.SOFT_INK, width=1.4, dash="4 4")
        q.point(2, g(2), color=O)
        q.point(-2, g(-2), color=O)
        q.point(0, 0, color=theme.INK, r=4)
        q.label(2.2, g(2) - 0.4, "(2, 1)", color=O, anchor="start", size=14)
        q.label(-2.2, g(-2) - 0.35, "(-2, -1)", color=O, anchor="end", size=14)
        X0, Y0 = q.px(0, 0)
        r = q.length(1.4)
        c.arc(X0, Y0, r, 25, 200, color=theme.ORANGE, width=2, arrow=True)
        c.text(X0 - r - 8, Y0 - r + 6, "180°", size=13, color=theme.ORANGE, anchor="end", halo=True)

    @wt.step("Check with algebra", "Swap x for −x. Squares hide the sign, so f does not change. Cubes and "
             "plain x keep the sign, so g flips. Most functions are neither, and that is allowed.",
             math="f(-x) = (-x)^2/2 - 1 = f(x),   g(-x) = -x^3/4 + x/2 = -g(x)")
    def _(c, pq):
        p, q = pq
        tag(c, p.X(0), 22, "even: f(-x) = f(x)", E, size=15)
        tag(c, q.X(0), 22, "odd: g(-x) = -g(x)", O, size=15)

    return wt
