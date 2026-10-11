"""Families of functions: piecewise, rational, polynomial, logarithmic, and periodic."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import brace, hop
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._function_kit import ctable, num, tag

CAT = "Functions"


# ---------------------------------------------------------------------------
# Piecewise functions
# ---------------------------------------------------------------------------


def _cases(c, x, y, name, rows, active, row_gap=46):
    """Draws f(x) = { cases } with each row colored; rows are (expr, cond, color)."""
    n = len(rows)
    top, bot = y - 22, y + (n - 1) * row_gap + 22
    mid = (top + bot) / 2
    c.math(x, mid, name, size=19, anchor="start")
    bx = x + 80
    h = (bot - top) / 2
    d = (f"M{bx + 8},{top} Q{bx},{top} {bx},{top + 10} L{bx},{mid - 10} Q{bx},{mid} {bx - 8},{mid} "
         f"Q{bx},{mid} {bx},{mid + 10} L{bx},{bot - 10} Q{bx},{bot} {bx + 8},{bot}")
    c.path(d, color=theme.INK, width=2)
    for i, (expr, cond, col) in enumerate(rows):
        ry = y + i * row_gap
        if i in active:
            if i == max(active):
                c.rect(bx + 6, ry - 17, 162, 34, color=col, fill=theme.fill(col, "1a"), width=1.5, rx=5)
            c.math(bx + 14, ry, expr, size=17, color=col, anchor="start")
            c.math(bx + 66, ry, cond, size=15, color=col, anchor="start")
        else:
            c.math(bx + 14, ry, expr, size=17, color=theme.MUTED, anchor="start")
            c.math(bx + 66, ry, cond, size=15, color=theme.MUTED, anchor="start")
    return h


@diagram("piecewise-function", "Piecewise Functions", CAT)
def build_piecewise() -> Walkthrough:
    wt = Walkthrough(
        "piecewise-function", "Piecewise Functions", CAT,
        concept="f(x) = x + 4 (x < -1),  1 (-1 \\leq x \\leq 2),  x - 3 (x > 2)",
        summary="A piecewise function uses different rules on different stretches of x. Solid dots mark "
                "endpoints that belong to a piece, and hollow dots mark endpoints that do not.",
        width=720, height=420, level="201",
    )
    C1, C2, C3 = theme.BLUE, theme.ORANGE, theme.GREEN
    rows = [("x + 4", "if x < -1", C1), ("1", "if -1 \\leq x \\leq 2", C2), ("x - 3", "if x > 2", C3)]

    def f(x):
        if x < -1:
            return x + 4
        if x <= 2:
            return 1
        return x - 3

    @wt.setup
    def _(c):
        p = Plane(c, box=(40, 30, 400, 370), x=(-5.5, 6.5), y=(-3, 5.5))
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    def panel(c, active):
        c.text(588, 52, "three rules, one function", size=12, color=theme.SOFT_INK)
        _cases(c, 460, 100, "f(x) =", rows, active)

    @wt.step("Split the x-axis", "The rule changes at x = −1 and at x = 2. Those two cuts split the x-axis "
             "into three stretches, and each stretch gets its own rule.",
             math="cuts at x = -1 and x = 2")
    def _(c, p):
        for x in (-1, 2):
            p.vline(x, color=theme.SOFT_INK, width=1.5)
        p.label(-3.3, 5.0, "x < -1", color=C1, size=15)
        p.label(0.5, 3.5, "-1 \\leq x \\leq 2", color=C2, size=13)
        p.label(4.3, 5.0, "x > 2", color=C3, size=15)
        panel(c, [])

    @wt.step("Draw the first piece", "Left of −1, f(x) = x + 4. The line would reach 3 at x = −1, but −1 "
             "is not in this piece, so the end gets a hollow dot.", math="x + 4 \\to 3 at x = -1, open end")
    def _(c, p):
        p.plot(lambda x: x + 4, -5.5, -1, color=C1)
        p.point(-1, 3, "(-1, 3)", color=C1, hollow=True, r=6, offset=(-10, -16), anchor="end")
        panel(c, [0])

    @wt.step("Draw the middle piece", "From −1 to 2 the function is flat at 1. Both ends belong to this "
             "piece, so both get solid dots.", math="f(x) = 1 on -1 \\leq x \\leq 2")
    def _(c, p):
        p.segment(-1, 1, 2, 1, color=C2, width=3)
        p.point(-1, 1, "(-1, 1)", color=C2, r=6, offset=(-16, 20), anchor="end")
        p.point(2, 1, "(2, 1)", color=C2, r=6, offset=(10, -16))
        panel(c, [0, 1])

    @wt.step("Draw the last piece", "Right of 2, f(x) = x − 3. It starts just above x = 2 at height −1, "
             "so that end is hollow too.", math="x - 3 \\to -1 at x = 2, open end")
    def _(c, p):
        p.plot(lambda x: x - 3, 2, 6.5, color=C3)
        p.point(2, -1, "(2, -1)", color=C3, hollow=True, r=6, offset=(10, 16))
        panel(c, [0, 1, 2])

    @wt.step("Read values at the cuts", "At a cut, use the solid dot. So f(−1) = 1, not 3, and f(2) = 1, "
             "not −1. A vertical line at a cut hits one solid dot, so f is still a function.",
             math="f(-1) = 1,  f(2) = 1,  f(5) = 2")
    def _(c, p):
        for x in (-1, 2):
            X, Y = p.px(x, f(x))
            c.circle(X, Y, 12, color=theme.RED, width=2.5)
        p.point(5, 2, "f(5) = 2", color=C3, offset=(-12, -16), anchor="end")
        tag(c, 575, 300, "f(-1) = 1", C2, size=16)
        tag(c, 575, 340, "f(2) = 1", C2, size=16)
        c.text(575, 376, "solid dot wins", size=13, color=theme.RED, weight="bold")

    return wt


@diagram("absolute-value-piecewise", "Absolute Value as a Piecewise Function", CAT)
def build_abs() -> Walkthrough:
    wt = Walkthrough(
        "absolute-value-piecewise", "Absolute Value as a Piecewise Function", CAT,
        concept="|x| = -x (x < 0),  x (x \\geq 0)",
        summary="The absolute value is two lines glued at the origin. Keep the right half of y = x and the "
                "left half of y = −x, and the V shape appears.",
        width=720, height=400, level="201",
    )
    L, R = theme.ORANGE, theme.BLUE
    rows = [("-x", "if x < 0", L), ("x", "if x \\geq 0", R)]

    @wt.setup
    def _(c):
        p = Plane(c, box=(40, 30, 400, 350), x=(-4.5, 4.5), y=(-4, 4.5), equal=True)
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    @wt.step("Draw two lines", "Start with y = x and y = −x. Each one is a full line, and each one is "
             "wrong half the time.", math="y = x,  y = -x")
    def _(c, p):
        p.plot(lambda x: x, color=R, width=1.6, dash="6 5")
        p.plot(lambda x: -x, color=L, width=1.6, dash="6 5")
        p.label(3.6, 4.0, "y = x", color=R, anchor="end", size=15)
        p.label(-3.6, 4.0, "y = -x", color=L, anchor="start", size=15)
        _cases(c, 470, 120, "|x| =", rows, [], row_gap=56)

    @wt.step("Keep the right half of y = x", "For x ≥ 0 the number is already positive, so |x| = x. Keep "
             "that half and drop the rest.", math="|3| = 3")
    def _(c, p):
        p.plot(lambda x: x, 0, 4.5, color=R)
        p.point(3, 3, "(3, 3)", color=R, offset=(12, 10))
        _cases(c, 470, 120, "|x| =", rows, [1], row_gap=56)

    @wt.step("Keep the left half of y = -x", "For x < 0 the minus sign flips a negative into a positive: "
             "−(−3) = 3. Keep the left half of y = −x.", math="|-3| = -(-3) = 3")
    def _(c, p):
        p.plot(lambda x: -x, -4.5, 0, color=L)
        p.point(-3, 3, "(-3, 3)", color=L, offset=(-12, 10), anchor="end")
        _cases(c, 470, 120, "|x| =", rows, [0, 1], row_gap=56)

    @wt.step("Read the V", "The two halves meet at the origin, the corner of the V. The graph never dips "
             "below the x-axis, because distance from zero is never negative.",
             math="|x| \\geq 0 for every x")
    def _(c, p):
        p.point(0, 0, color=theme.INK)
        p.segment(1.0, 0.45, 0.1, 0.03, color=theme.INK, width=1)
        p.label(1.05, 0.62, "corner (0, 0)", color=theme.INK, size=15, anchor="start")
        p.segment(-3, 3, 3, 3, color=theme.SOFT_INK, width=1.4, dash="4 4")
        p.label(1.5, 3.35, "same height 3", color=theme.SOFT_INK, size=13, math=False)
        tag(c, 580, 300, "|-3| = |3| = 3", theme.PURPLE, size=16)

    return wt


# ---------------------------------------------------------------------------
# Rational functions and asymptotes
# ---------------------------------------------------------------------------


def _rat(x):
    return 1 / (x - 2) + 1


@diagram("rational-asymptotes", "Asymptotes of a Rational Function", CAT)
def build_rational() -> Walkthrough:
    wt = Walkthrough(
        "rational-asymptotes", "Asymptotes of y = 1/(x − 2) + 1", CAT,
        concept="y = 1/(x - 2) + 1:  vertical asymptote x = 2,  horizontal asymptote y = 1",
        summary="Near x = 2 the denominator shrinks to zero and the graph shoots off to infinity. Far from the "
                "origin the fraction fades to zero and the graph settles toward y = 1.",
        width=720, height=430, level="201",
    )
    VA, HA, CV = theme.RED, theme.PURPLE, theme.BLUE
    near = [1.5, 1.9, 1.99, 2.01, 2.1, 2.5]
    far = [-100, -10, -2, 6, 10, 100]

    @wt.setup
    def _(c):
        p = Plane(c, box=(40, 30, 420, 380), x=(-3, 7), y=(-4, 6))
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    @wt.step("Find where the formula breaks", "At x = 2 the denominator is 0, and nobody divides by 0. "
             "The graph cannot touch the line x = 2.", math="x - 2 = 0 \\implies x = 2")
    def _(c, p):
        p.vline(2, color=VA, width=2.2, dash="8 5")
        p.label(2.15, -3.6, "x = 2", color=VA, anchor="start", size=16)
        c.math(p.X(3.0), p.Y(5.4), "y = 1/(x - 2) + 1", size=17, color=CV, anchor="start", halo=True)

    @wt.step("Creep up on x = 2", "Try x values closer and closer to 2. Just right of 2 the outputs blow "
             "up, just left of 2 they plunge. That is a vertical asymptote.",
             math="x \\to 2^+: y \\to \\infty,   x \\to 2^-: y \\to −\\infty")
    def _(c, p):
        c.text(590, 22, "near x = 2", size=13, color=VA, weight="bold")
        ctable(c, 520, 34, ["x", "y"], [[num(x), num(_rat(x))] for x in near], [70, 70], [VA, CV],
               row_h=26)
        for x in (1.5, 2.5):
            p.point(x, _rat(x), color=CV)
        c.arrow(p.X(2.35), p.Y(3.6), p.X(2.35), p.Y(5.6), color=CV, width=2.2)
        c.arrow(p.X(1.65), p.Y(-1.6), p.X(1.65), p.Y(-3.6), color=CV, width=2.2)
        p.label(2.55, 4.6, "up to \\infty", color=CV, anchor="start", size=14)
        p.label(2.15, -2.6, "down to −\\infty", color=CV, anchor="start", size=14)

    @wt.step("Walk far away", "Now try huge x values. The fraction 1/(x − 2) shrinks toward 0, so y "
             "settles toward 1 from above on the right and from below on the left.",
             math="x \\to \\pm\\infty: 1/(x - 2) \\to 0, y \\to 1")
    def _(c, p):
        p.hline(1, color=HA, width=2.2, dash="8 5")
        p.label(-2.9, 1.35, "y = 1", color=HA, anchor="start", size=16)
        c.text(590, 228, "far away", size=13, color=HA, weight="bold")
        ctable(c, 520, 240, ["x", "y"], [[num(x), num(_rat(x))] for x in far], [70, 70], [theme.SOFT_INK, HA],
               row_h=26)
        for x in (-2, 6):
            p.point(x, _rat(x), color=CV)

    @wt.step("Draw the curve", "Join the points without crossing the asymptotes. The graph has two "
             "branches. It crosses the x-axis at 1 and the y-axis at 0.5.",
             math="y = 0: 1/(x - 2) = -1 \\implies x = 1;   x = 0: y = 0.5")
    def _(c, p):
        p.plot(_rat, -3, 1.98, color=CV)
        p.plot(_rat, 2.02, 7, color=CV)
        for (x, y), (lx, ly), lab in (((1, 0), (0.8, -2.2), "(1, 0)"), ((0, _rat(0)), (-1.5, -1.2), "(0, 0.5)")):
            p.point(x, y, color=theme.INK)
            p.segment(lx, ly + 0.25, x, y, color=theme.INK, width=1)
            p.label(lx, ly, lab, color=theme.INK, size=15)

    return wt


@diagram("rational-shift", "Rational Function as a Shifted 1/x", CAT)
def build_rational_shift() -> Walkthrough:
    wt = Walkthrough(
        "rational-shift", "y = 1/(x − 2) + 1 as a Shifted 1/x", CAT,
        concept="y = 1/(x - h) + k:  center (h, k), asymptotes x = h and y = k",
        summary="The graph of y = 1/(x − 2) + 1 is the graph of y = 1/x moved right 2 and up 1. The "
                "asymptotes ride along, so their crossing point lands at (2, 1).",
        width=680, height=420, level="201",
    )
    stages = [
        ("y = 1/x", theme.SOFT_INK, 0, 0),
        ("y = 1/(x - 2)", theme.ORANGE, 2, 0),
        ("y = 1/(x - 2) + 1", theme.BLUE, 2, 1),
    ]

    @wt.setup
    def _(c):
        p = Plane(c, box=(40, 30, 600, 370), x=(-4, 7), y=(-4, 5), equal=True)
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    def draw(c, p, k):
        eq, col, h, kk = stages[k]
        if k > 0:
            _, pc, ph, pk = stages[k - 1]
            p.plot(lambda x: 1 / (x - ph) + pk, color=theme.MUTED, width=1.8, dash="6 5")
        p.vline(h, color=theme.RED, width=1.8, dash="8 5")
        p.hline(kk, color=theme.PURPLE, width=1.8, dash="8 5")
        p.plot(lambda x: 1 / (x - h) + kk if abs(x - h) > 1e-9 else None, color=col)
        p.point(h, kk, f"center ({h}, {kk})", color=theme.INK, offset=(12, 30))
        p.point(h + 1, kk + 1, f"({h + 1}, {kk + 1})", color=col, offset=(10, -12))
        if k > 0:
            _, _, ph, pk = stages[k - 1]
            for (a, b) in (((ph, pk), (h, kk)), ((ph + 1, pk + 1), (h + 1, kk + 1))):
                A, B = p.px(*a), p.px(*b)
                c.arrow(A[0], A[1], B[0] - (B[0] - A[0]) * 0.1, B[1] - (B[1] - A[1]) * 0.1, color=theme.INK,
                        width=1.8)
        tag(c, 520, 50, eq, col, size=17)
        if k > 0:
            p.label(h + 0.15, -3.6, f"x = {h}", color=theme.RED, anchor="start", size=14)
            p.label(-3.9, kk + 0.45, f"y = {kk}", color=theme.PURPLE, anchor="start", size=14)

    @wt.step("Start with 1/x", "The parent y = 1/x has two branches. Its asymptotes are the two axes, "
             "and they cross at the center (0, 0).", math="y = 1/x", fresh=True)
    def _(c, p):
        draw(c, p, 0)

    @wt.step("Shift right 2", "Replace x with x − 2. The whole picture slides 2 to the right, and the "
             "vertical asymptote moves to x = 2.", math="y = 1/(x - 2)", fresh=True)
    def _(c, p):
        draw(c, p, 1)

    @wt.step("Shift up 1", "Add 1. The picture rises 1, and the horizontal asymptote moves to y = 1. "
             "The center is now (2, 1).", math="y = 1/(x - 2) + 1", fresh=True)
    def _(c, p):
        draw(c, p, 2)

    @wt.step("Read h and k off the formula", "In y = 1/(x − h) + k, the number subtracted from x is the "
             "vertical asymptote and the number added at the end is the horizontal one. No table needed.",
             math="h = 2: x = 2,   k = 1: y = 1")
    def _(c, p):
        tag(c, 520, 88, "x = h = 2", theme.RED, size=15)
        tag(c, 520, 124, "y = k = 1", theme.PURPLE, size=15)

    return wt


# ---------------------------------------------------------------------------
# Polynomial roots and end behavior
# ---------------------------------------------------------------------------


def _poly(x):
    return (x + 2) * (x - 1) ** 2 * (x - 3)


@diagram("polynomial-roots", "Polynomial Roots: Touch or Cross", CAT)
def build_poly() -> Walkthrough:
    wt = Walkthrough(
        "polynomial-roots", "Polynomial Roots: Touch or Cross", CAT,
        concept="y = (x + 2)(x - 1)^2(x - 3):  cross at -2 and 3, touch at 1",
        summary="Read a factored polynomial without plotting a hundred points. The factors give the zeros, "
                "the degree gives the ends, and an even power makes the graph touch instead of cross.",
        width=700, height=440, level="201",
    )
    ONE, TWO = theme.BLUE, theme.ORANGE
    SY = 404  # sign chart row

    @wt.setup
    def _(c):
        p = Plane(c, box=(56, 26, 590, 340), x=(-3.2, 4.2), y=(-18, 12))
        p.grid(step=1, ystep=4)
        p.axes(step=1, ystep=4)
        return p

    @wt.step("Find the zeros", "Each factor is zero at one x: x + 2 at −2, x − 1 at 1, x − 3 at 3. The "
             "factor x − 1 appears twice, so 1 is a double root.",
             math="zeros: -2,  1 (twice),  3")
    def _(c, p):
        for r, col, lab, anc, dx in ((-2, ONE, "x = -2, once", "start", 0.12),
                                     (1, TWO, "x = 1, twice", "middle", 0),
                                     (3, ONE, "x = 3, once", "end", -0.12)):
            p.point(r, 0, color=col, r=6)
            p.label(r + dx, 2.8, lab, color=col, anchor=anc, size=15)

    @wt.step("Check the ends", "Multiply the x parts: x · x² · x = x⁴. An even power with a plus sign "
             "sends both ends up, like a smile at the edges.",
             math="degree 1 + 2 + 1 = 4,  leading term +x^4")
    def _(c, p):
        for x in (-2.85, 3.85):
            c.arrow(p.X(x), p.Y(4), p.X(x), p.Y(10.5), color=theme.PURPLE, width=3)
        p.label(-2.85, 2.4, "up", color=theme.PURPLE, size=14, math=False)
        p.label(3.85, 2.4, "up", color=theme.PURPLE, size=14, math=False)
        p.label(1.9, 10.2, "far out, x⁴ wins: both ends rise", color=theme.PURPLE, size=14, math=False)

    @wt.step("Build a sign chart", "Test one x in each stretch. The sign flips at −2 and at 3, but not at "
             "1, because (x − 1)² is never negative.",
             math=", ".join(f"f({num(x)}) = {num(_poly(x))}" for x in (-3, 0, 2, 4)))
    def _(c, p):
        x0, x1 = p.X(-3.2), p.X(4.2)
        c.line(x0, SY, x1, SY, color=theme.SOFT_INK, width=1.5)
        c.text(x0 - 6, SY, "sign", size=12, color=theme.SOFT_INK, anchor="end")
        for r, col in ((-2, ONE), (1, TWO), (3, ONE)):
            c.line(p.X(r), SY - 12, p.X(r), SY + 12, color=col, width=2)
            c.text(p.X(r), SY + 22, num(r), size=12, color=col)
        for (a, b, test) in ((-3.2, -2, -3), (-2, 1, 0), (1, 3, 2), (3, 4.2, 4)):
            s = _poly(test)
            col = theme.GREEN if s > 0 else theme.RED
            c.text((p.X(a) + p.X(b)) / 2, SY - 1, "+" if s > 0 else "−", size=22, color=col, weight="bold")
            c.text((p.X(a) + p.X(b)) / 2, SY + 22, f"f({num(test)}) = {num(s)}", size=12, color=col,
                   math=True)

    @wt.step("Cross at single roots", "At −2 and 3 the sign flips, so the graph passes straight through "
             "the axis, like a train through a station.", math="(x + 2)^1,  (x - 3)^1:  cross")
    def _(c, p):
        p.plot(_poly, -2.22, -1.75, color=ONE, width=4)
        p.plot(_poly, 2.6, 3.39, color=ONE, width=4)

    @wt.step("Touch at the double root", "At 1 the sign stays negative on both sides. The graph rises to "
             "touch the axis and turns back down, a bounce, not a crossing.",
             math="(x - 1)^2 \\geq 0:  touch and turn")
    def _(c, p):
        p.plot(_poly, 0.35, 1.65, color=TWO, width=4)

    @wt.step("Join the pieces", "Connect the pieces, falling from the left, bouncing at 1, and rising on "
             "the right. The y-intercept is f(0) = 2 · 1 · (−3) = −6.",
             math="f(0) = (0 + 2)(0 - 1)^2(0 - 3) = -6")
    def _(c, p):
        p.plot(_poly, -3.2, 4.2, color=theme.INK, width=2)
        p.point(0, _poly(0), "(0, -6)", color=theme.INK, offset=(10, 14))

    return wt


# ---------------------------------------------------------------------------
# Logarithms as exponents
# ---------------------------------------------------------------------------


@diagram("logarithm-scale", "Logarithms on a Number Line", CAT)
def build_log_scale() -> Walkthrough:
    wt = Walkthrough(
        "logarithm-scale", "Logarithms on a Number Line", CAT,
        concept="log_{10} x = the power of 10 that gives x;  log(ab) = log a + log b",
        summary="On a log scale each step of the same length multiplies by 10. The logarithm of a number "
                "is how far along that scale it sits, which is the exponent on 10.",
        width=720, height=400, level="201",
    )
    VAL, LOG, MUL = theme.BLUE, theme.ORANGE, theme.GREEN
    L0, L1 = 70, 650
    TY, BY = 92, 270  # linear line, log line

    def LX(v):  # linear scale 0..1000
        return L0 + v / 1000 * (L1 - L0)

    def GX(v):  # log scale 1..1000
        return L0 + math.log10(v) / 3 * (L1 - L0)

    @wt.setup
    def _(c):
        c.text(16, TY - 52, "linear scale: equal steps add 200", size=13, color=theme.SOFT_INK, anchor="start")
        c.arrow(L0 - 12, TY, L1 + 22, TY, color=theme.INK, width=2)
        for k in range(6):
            v = k * 200
            c.line(LX(v), TY - 6, LX(v), TY + 6, color=theme.INK, width=1.6)
            c.text(LX(v), TY + 20, str(v), size=12, color=theme.SOFT_INK)
        return None

    @wt.step("Mark powers of 10 on a normal ruler", "Put 1, 10, 100, and 1000 on an ordinary number line. "
             "The 1000 hogs the line while 1 and 10 get squashed together near 0.",
             math="1, 10, 100, 1000")
    def _(c):
        linear_marks(c)

    def linear_marks(c):
        for v, lx in ((1, LX(1) - 14), (10, LX(10) + 18), (100, LX(100) + 12), (1000, LX(1000))):
            c.dot(LX(v), TY, r=5, color=VAL)
            c.line(LX(v), TY - 6, lx, TY - 22, color=VAL, width=1)
            c.text(lx, TY - 30, str(v), size=14, color=VAL, weight="bold")
        c.text(LX(300), TY - 30, "1 and 10 are nearly on top of 0", size=12, color=theme.SOFT_INK)

    def log_line(c):
        c.text(16, BY - 92, "log scale: equal steps multiply by 10", size=13, color=theme.SOFT_INK,
               anchor="start")
        c.arrow(L0 - 12, BY, L1 + 22, BY, color=theme.INK, width=2)
        for e in range(4):
            v = 10 ** e
            c.line(GX(v), BY - 8, GX(v), BY + 8, color=theme.INK, width=2)
            c.dot(GX(v), BY, r=5, color=VAL)
            c.text(GX(v), BY + 22, str(v), size=14, color=VAL, weight="bold")
            c.math(GX(v), BY + 48, f"10^{e}", size=16, color=LOG)
            c.text(GX(v), BY + 72, f"log = {e}", size=12, color=LOG)

    def between(c, skip=()):
        for e in range(3):
            for m in range(2, 10):
                v = m * 10 ** e
                c.line(GX(v), BY - 5, GX(v), BY + 5, color=theme.INK, width=1)
                if m in (2, 5) and v not in skip:
                    c.text(GX(v), BY + 22, str(v), size=12, color=theme.SOFT_INK)
        c.text(GX(2), BY + 48, num(math.log10(2), 3), size=12, color=LOG)
        c.text(GX(5), BY + 48, num(math.log10(5), 3), size=12, color=LOG)

    @wt.step("Space the powers evenly", "On a log scale, 1, 10, 100, and 1000 sit at equal gaps. The "
             "position of each number is its exponent: 1000 = 10³ sits at 3.",
             math="position = log_{10} x")
    def _(c):
        log_line(c)

    @wt.step("A log counts the times-10 steps", "To get from 1 to 100 takes two steps of ×10, so the "
             "log of 100 is 2. A logarithm is an exponent in disguise.",
             math="log_{10} 100 = 2  because  10^2 = 100")
    def _(c):
        for e in range(3):
            hop(c, GX(10 ** e), GX(10 ** (e + 1)), BY, "\\times 10", color=LOG, height=26)

    @wt.step("Fill in the numbers between", "The numbers 2 to 9 crowd toward the next power of 10. The "
             "number 2 sits about 0.3 of the way, and 5 about 0.7.",
             math="log_{10} 2 \\approx 0.301,   log_{10} 5 \\approx 0.699")
    def _(c):
        between(c)

    @wt.step("Multiply by adding lengths", "Logs turn times into plus. Walk the length for 2, then the "
             "length for 50, and you land on 100. This is how a slide rule multiplies.",
             math=f"log 2 + log 50 = {math.log10(2):.3f} + {math.log10(50):.3f} = 2 = log 100", fresh=True)
    def _(c):
        linear_marks(c)
        log_line(c)
        between(c, skip=(50,))
        c.text(GX(50), BY + 22, "50", size=12, color=MUL, weight="bold")
        hop(c, GX(1), GX(2), BY, "log 2", color=MUL, height=30, size=13)
        hop(c, GX(2), GX(100), BY, "+ log 50", color=MUL, height=56, size=13)
        c.circle(GX(100), BY, 11, color=MUL, width=2.5)
        tag(c, 560, BY - 110, "2 \\times 50 = 100", MUL, size=16)

    return wt


# ---------------------------------------------------------------------------
# Periodic functions
# ---------------------------------------------------------------------------


@diagram("periodic-functions", "Periodic Functions", CAT)
def build_periodic() -> Walkthrough:
    wt = Walkthrough(
        "periodic-functions", "Periodic Functions: Sawtooth and Square Waves", CAT,
        concept="f(x + T) = f(x):  period T = 2,  amplitude 1",
        summary="A periodic function repeats one cycle forever. The period is the length of one cycle, and the "
                "amplitude is half the distance from the lowest value to the highest.",
        width=720, height=450, level="201",
    )
    T = 2
    ONE, REP, PER, AMP = theme.ORANGE, theme.BLUE, theme.GREEN, theme.PURPLE
    starts = [-2, 0, 2, 4, 6]

    @wt.setup
    def _(c):
        p = Plane(c, box=(56, 34, 600, 170), x=(-2.6, 8.6), y=(-1.6, 1.6))
        p.grid(step=1, ystep=1)
        p.axes(step=1, ystep=1, ylabel="")
        c.text(16, 20, "sawtooth", size=13, color=theme.SOFT_INK, anchor="start", weight="bold")
        q = Plane(c, box=(56, 254, 600, 170), x=(-2.6, 8.6), y=(-1.6, 1.6))
        q.grid(step=1, ystep=1)
        q.axes(step=1, ystep=1, ylabel="")
        c.text(16, 240, "square wave", size=13, color=theme.SOFT_INK, anchor="start", weight="bold")
        return p, q

    def tooth(p, a, col, width=3):
        p.segment(a, -1, a + T, 1, color=col, width=width)
        p.point(a, -1, color=col, r=4.5)
        p.point(a + T, 1, color=col, r=4.5, hollow=True)

    def square(p, a, col, width=3):
        p.segment(a, 1, a + 1, 1, color=col, width=width)
        p.segment(a + 1, -1, a + T, -1, color=col, width=width)
        p.point(a, 1, color=col, r=4.5)
        p.point(a + 1, 1, color=col, r=4.5, hollow=True)
        p.point(a + 1, -1, color=col, r=4.5)
        p.point(a + T, -1, color=col, r=4.5, hollow=True)

    @wt.step("Draw one cycle", "Draw one ramp from (0, −1) up to (2, 1). The left end is solid and the "
             "right end is hollow, because the next cycle owns that spot.",
             math="f(x) = x - 1 on 0 \\leq x < 2")
    def _(c, pq):
        p, _ = pq
        tooth(p, 0, ONE, width=3.5)
        p.label(1.0, 1.3, "one cycle", color=ONE, size=14, math=False)

    @wt.step("Copy it forever", "Paste the same ramp every 2 units, left and right. Shifting the graph by "
             "2 lands it on itself, so f(x + 2) = f(x).", math="f(x + 2) = f(x)")
    def _(c, pq):
        p, _ = pq
        for a in starts:
            if a != 0:
                tooth(p, a, REP, width=2.5)
            if a > -2:
                p.vline(a, color=theme.MUTED, width=1, dash="2 4", y0=-1, y1=1)
        p.label(5.0, 1.3, "same shape, again and again", color=REP, size=13, math=False)

    def period_mark(c, p, y):
        a, b = p.px(2, y), p.px(4, y)
        c.arrow(a[0], a[1], b[0], b[1], color=PER, width=2, both=True)
        c.text((a[0] + b[0]) / 2, a[1] - 11, "period 2", size=13, color=PER, weight="bold", halo=True)

    def amp_mark(c, p):
        p.hline(0, color=AMP, width=1.5, dash="6 4", x0=-2.6, x1=8.6)
        X = p.X(-1.5)
        c.arrow(X, p.Y(0), X, p.Y(1), color=AMP, width=2.2)
        c.text(X, p.Y(1.33), "amplitude 1", size=13, color=AMP, weight="bold", halo=True)
        c.text(p.X(-2.55), p.Y(0.22), "midline", size=11, color=AMP, anchor="start", halo=True)

    @wt.step("Read the period", "Measure from the start of one cycle to the start of the next: 2 units. "
             "That length is the period.", math="period T = 2")
    def _(c, pq):
        p, _ = pq
        period_mark(c, p, -1.35)

    @wt.step("Read the amplitude", "The ramp runs from −1 to 1. The midline sits halfway at 0, and the "
             "amplitude is the distance from the midline to the top: 1.",
             math="amplitude = (max - min)/2 = (1 - (-1))/2 = 1")
    def _(c, pq):
        p, _ = pq
        amp_mark(c, p)

    @wt.step("Build a square wave", "Same recipe, new cycle: stay at 1 for one unit, then drop to −1 for "
             "one unit. Copy every 2 units. It switches like a light that someone keeps flicking.",
             math="g(x) = 1 on [0, 1),  -1 on [1, 2),  g(x + 2) = g(x)")
    def _(c, pq):
        _, q = pq
        for a in starts:
            square(q, a, ONE if a == 0 else REP, width=3.5 if a == 0 else 2.5)
            for x in (a, a + 1):
                if x > -2.6:
                    q.vline(x, color=theme.MUTED, width=1, dash="2 4", y0=-1, y1=1)

    @wt.step("Read it the same way", "One cycle is still 2 units long, and the wave still swings 1 above "
             "and below the midline. Two different shapes, same period, same amplitude.",
             math="square wave: period 2, amplitude 1")
    def _(c, pq):
        _, q = pq
        period_mark(c, q, -1.35)
        amp_mark(c, q)

    return wt
