"""Exponents: the rules as repeated multiplication, and linear versus exponential growth."""

from __future__ import annotations

from .. import theme
from ..annotate import brace
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._algebra_helpers import tile

BOX, GAP = 44, 8


def _boxes(c, x, y, count, color, label="x", dashed=False):
    """Draws a row of factor boxes and returns the right edge."""
    for i in range(count):
        tile(c, x + i * (BOX + GAP), y, BOX, BOX, color, label, size=20, dashed=dashed)
    return x + count * (BOX + GAP) - GAP


@diagram("exponent-rules", "Exponent Rules as Repeated Multiplication", "Algebra")
def build_rules() -> Walkthrough:
    wt = Walkthrough(
        "exponent-rules", "Exponent Rules as Repeated Multiplication", "Algebra",
        concept="x^m \\cdot x^n = x^{m+n},   (x^m)^n = x^{mn}",
        summary="An exponent counts how many x's are multiplied together. Multiplying powers puts the rows "
                "side by side, so the counts add; a power of a power repeats a group, so the counts multiply.",
        width=680, height=420, level="201",
    )
    m, n = 3, 2
    p_, q_ = 2, 3
    A, B, S = theme.BLUE, theme.ORANGE, theme.GREEN
    Y1, Y2 = 90, 280
    X0 = 50
    RX = 450  # right column for the number check

    @wt.setup
    def _(c):
        return None

    @wt.step("Write x³ as three x's", f"x³ means x times x times x. Draw one box per factor: {m} boxes.",
             math="x^3 = x \\cdot x \\cdot x")
    def _(c):
        r = _boxes(c, X0, Y1, m, A)
        brace(c, r, Y1 + BOX + 6, X0, Y1 + BOX + 6, "x^3", color=A, size=18)

    @wt.step("Multiply by x²", f"x² adds a row of {n} more boxes. Multiplying just lines the factors up.",
             math="x^3 \\cdot x^2 = (x \\cdot x \\cdot x)(x \\cdot x)")
    def _(c):
        x2 = X0 + m * (BOX + GAP) + 24
        c.text(x2 - 14, Y1 + BOX / 2, "·", size=30, color=theme.INK, weight="bold")
        r = _boxes(c, x2, Y1, n, B)
        brace(c, r, Y1 + BOX + 6, x2, Y1 + BOX + 6, "x^2", color=B, size=18)

    @wt.step("Count all the factors", f"There are {m} + {n} = {m + n} boxes. The exponents add.",
             math=f"x^3 \\cdot x^2 = x^{{3+2}} = x^{m + n}")
    def _(c):
        right = X0 + (m + n) * (BOX + GAP) + 24 - GAP
        brace(c, X0, Y1 - 8, right, Y1 - 8, f"x^{m + n}: {m + n} factors", color=S, size=18)
        xs = [X0 + i * (BOX + GAP) for i in range(m)] + [X0 + m * (BOX + GAP) + 24 + i * (BOX + GAP) for i in range(n)]
        for i, bx in enumerate(xs):
            c.text(bx + BOX - 7, Y1 + BOX - 9, str(i + 1), size=11, color=S, weight="bold")

    @wt.step("Raise x² to the third power", f"(x²)³ means three copies of the group x · x. Each group is "
             f"one x², framed in purple.", math="(x^2)^3 = x^2 \\cdot x^2 \\cdot x^2")
    def _(c):
        gw = p_ * (BOX + GAP) - GAP
        for g in range(q_):
            gx = X0 + g * (gw + 30)
            _boxes(c, gx, Y2, p_, A)
            c.rect(gx - 5, Y2 - 5, gw + 10, BOX + 10, color=theme.PURPLE, width=2, dash="6 4", rx=6)
            brace(c, gx + gw, Y2 + BOX + 10, gx, Y2 + BOX + 10, "x^2", color=theme.PURPLE, size=17)
            if g < q_ - 1:
                c.text(gx + gw + 15, Y2 + BOX / 2, "·", size=30, color=theme.INK, weight="bold")

    @wt.step("Count again", f"{q_} groups of {p_} boxes make {p_ * q_} boxes. The exponents multiply.",
             math=f"(x^2)^3 = x^{{2 \\cdot 3}} = x^{p_ * q_}")
    def _(c):
        gw = p_ * (BOX + GAP) - GAP
        right = X0 + q_ * (gw + 30) - 30
        brace(c, X0 - 5, Y2 - 12, right + 5, Y2 - 12, f"x^{p_ * q_}: {q_} \\times {p_} = {p_ * q_} factors",
              color=S, size=18)
        k = 0
        for g in range(q_):
            for i in range(p_):
                k += 1
                bx = X0 + g * (gw + 30) + i * (BOX + GAP)
                c.text(bx + BOX - 7, Y2 + BOX - 9, str(k), size=11, color=S, weight="bold")

    @wt.step("Check with x = 2", "Numbers keep the rules honest. Put 2 in for x and both sides agree.",
             math=f"2^3 \\cdot 2^2 = 8 \\cdot 4 = 32 = 2^5,   (2^2)^3 = 4^3 = 64 = 2^6")
    def _(c):
        c.label_box(RX + 100, Y1 + BOX / 2, f"2^3 \\cdot 2^2 = 8 \\cdot 4 = {2 ** 3 * 2 ** 2} = 2^5", size=18,
                    color=S, border=S, math=True, pad=12)
        c.label_box(RX + 100, Y2 + BOX / 2, f"(2^2)^3 = 4^3 = {(2 ** 2) ** 3} = 2^6", size=18,
                    color=S, border=S, math=True, pad=12)

    return wt


@diagram("exponent-division", "Dividing Powers: Zero and Negative Exponents", "Algebra")
def build_division() -> Walkthrough:
    wt = Walkthrough(
        "exponent-division", "Dividing Powers: Zero and Negative Exponents", "Algebra",
        concept="x^m / x^n = x^{m-n},   x^0 = 1,   x^{-n} = 1 / x^n",
        summary="Write the top and the bottom as rows of x's and cancel them in pairs. What survives gives the "
                "rule, and the leftover cases explain x⁰ = 1 and negative exponents.",
        width=680, height=440, level="201",
    )
    A, B, K, S = theme.BLUE, theme.ORANGE, theme.RED, theme.GREEN

    def fraction(c, x, y, top, bot, cancel, top_col=A, bot_col=B):
        """Draws top x's over bot x's with a bar. Returns (bar_y, width, cancelled top x positions)."""
        w = max(top, bot) * (BOX + GAP) - GAP
        _boxes(c, x, y, top, top_col)
        bar = y + BOX + 12
        c.line(x - 6, bar, x + w + 6, bar, color=theme.INK, width=2.2)
        _boxes(c, x, bar + 12, bot, bot_col)
        if cancel:
            for i in range(cancel):
                bx = x + i * (BOX + GAP)
                for by in (y, bar + 12):
                    c.line(bx + 4, by + BOX - 4, bx + BOX - 4, by + 4, color=K, width=3)
                c.text(bx + BOX / 2, bar, "1", size=13, color=K, weight="bold", halo=True)
        return bar, w

    TX, TY = 60, 62

    @wt.setup
    def _(c):
        return None

    @wt.step("Write the division as a fraction", "x⁵ over x² is five x's on top and two x's on the bottom.",
             math="x^5 / x^2 = (x \\cdot x \\cdot x \\cdot x \\cdot x) / (x \\cdot x)")
    def _(c):
        fraction(c, TX, TY, 5, 2, 0)
        c.math(TX + 290, TY + BOX / 2, "x^5", size=20, color=A, anchor="start")
        c.math(TX + 290, TY + BOX + 24 + BOX / 2, "x^2", size=20, color=B, anchor="start")

    @wt.step("Cancel matching pairs", "Each x on top meets an x on the bottom, and x / x = 1. "
             "Two pairs cancel.", math="x / x = 1")
    def _(c):
        fraction(c, TX, TY, 5, 2, 2)

    @wt.step("Count what survives", "Three x's remain on top. Subtract the exponents: 5 − 2 = 3.",
             math="x^5 / x^2 = x^{5-2} = x^3")
    def _(c):
        left = TX + 2 * (BOX + GAP)
        right = TX + 5 * (BOX + GAP) - GAP
        brace(c, left, TY - 6, right, TY - 6, "x^3 left", color=S, size=17)

    LY = 250

    @wt.step("Cancel everything: x⁰ = 1", "x² over x² cancels every pair and leaves 1. The rule says "
             "2 − 2 = 0, so x⁰ must equal 1.", math="x^2 / x^2 = x^{2-2} = x^0 = 1")
    def _(c):
        bar, w = fraction(c, TX, LY, 2, 2, 2)
        c.math(TX + w + 24, bar, "= 1 = x^0", size=22, color=S, anchor="start")

    @wt.step("Cancel too many: negative exponents", "x² over x⁵ leaves three x's on the bottom. "
             "The rule gives 2 − 5 = −3, so a negative exponent means one over.",
             math="x^2 / x^5 = 1 / x^3 = x^{-3}")
    def _(c):
        x0 = 330
        bar, w = fraction(c, x0, LY, 2, 5, 2, top_col=A, bot_col=B)
        c.math(x0 + w / 2, bar + BOX + 56, "= 1 / x^3 = x^{-3}", size=22, color=S)

    return wt


@diagram("linear-vs-exponential", "Linear Versus Exponential Growth", "Algebra")
def build_growth() -> Walkthrough:
    wt = Walkthrough(
        "linear-vs-exponential", "Linear Versus Exponential Growth", "Algebra",
        concept="2n + 1  vs  2^n",
        summary="Linear growth adds the same amount each step; exponential growth multiplies by the same factor. "
                "The linear rule can lead early, but doubling always wins in the end.",
        width=720, height=460, level="201",
    )
    L, E = theme.BLUE, theme.ORANGE
    lin = lambda n: 2 * n + 1
    exp = lambda n: 2 ** n
    N = list(range(7))
    # crossover: solve 2x + 1 = 2^x for x > 1 by bisection
    lo, hi = 2.0, 3.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if 2 ** mid < 2 * mid + 1:
            lo = mid
        else:
            hi = mid
    cross = (lo + hi) / 2
    first_win = next(n for n in N if exp(n) > lin(n))

    CX = [50, 120, 250]  # column centers: n, 2n + 1, 2^n
    CW = [50, 80, 80]
    TOP, RH = 40, 34

    def cell_y(r):
        return TOP + RH * (r + 1) + RH / 2

    def table(c, hops_lin=False, hops_exp=False, highlight=None):
        heads = [("n", theme.INK), ("2n + 1", L), ("2^n", E)]
        for k, (h, col) in enumerate(heads):
            c.rect(CX[k] - CW[k] / 2, TOP, CW[k], RH, color=theme.MUTED, fill=theme.PANEL, width=1)
            c.math(CX[k], TOP + RH / 2, h, size=17, color=col)
        for r, n in enumerate(N):
            fill = theme.HIGHLIGHT if highlight == n else "none"
            for k, (v, col) in enumerate(((n, theme.INK), (lin(n), L), (exp(n), E))):
                c.rect(CX[k] - CW[k] / 2, cell_y(r) - RH / 2, CW[k], RH, color=theme.MUTED, fill=fill, width=1)
                c.text(CX[k], cell_y(r), str(v), size=16, color=col, weight="bold" if k else None)
        for flag, k, col, lab in ((hops_lin, 1, L, "+2"), (hops_exp, 2, E, "×2")):
            if not flag:
                continue
            x = CX[k] + CW[k] / 2 + 4
            for r in range(len(N) - 1):
                c.curved_arrow(x, cell_y(r) + 2, x, cell_y(r + 1) - 2, bend=0.5, color=col, width=1.6)
                c.text(x + 14, (cell_y(r) + cell_y(r + 1)) / 2, lab, size=13, color=col, weight="bold",
                       anchor="start")

    def notes(c, k):
        """Plain-language notes beside the table, before the graph takes that space."""
        if k >= 1:
            c.text(380, 130, "2n + 1: add 2 every row", size=15, color=L, weight="bold", anchor="start")
            c.text(380, 152, "steps: 2, 2, 2, 2, 2, 2", size=14, color=L, anchor="start")
        if k >= 2:
            c.text(380, 200, "2ⁿ: double every row", size=15, color=E, weight="bold", anchor="start")
            c.text(380, 222, "steps: 1, 2, 4, 8, 16, 32", size=14, color=E, anchor="start")
            c.text(380, 270, "Fixed steps versus growing steps.", size=14, color=theme.SOFT_INK, anchor="start")
            c.text(380, 290, "Place your bets.", size=14, color=theme.SOFT_INK, anchor="start")

    def graph(c, nmax, ymax, ystep, pts=True):
        p = Plane(c, box=(360, 40, 320, 360), x=(-0.3, nmax + 0.3), y=(-ystep * 0.4, ymax))
        p.grid(step=1, ystep=ystep)
        p.axes(step=1, ystep=ystep, xlabel="n", ylabel="")
        p.plot(lambda x: 2 * x + 1, 0, nmax + 0.3, color=L, width=2.5)
        p.plot(lambda x: 2 ** x, 0, nmax + 0.3, color=E, width=2.5)
        if pts:
            for n in range(nmax + 1):
                for fn, col in ((lin, L), (exp, E)):
                    if fn(n) <= ymax:
                        p.point(n, fn(n), None, color=col, r=4.5)
        return p

    @wt.setup
    def _(c):
        return None

    @wt.step("Fill in the table", "Both rules start at 1 when n = 0. After that they part ways.",
             math="2 \\cdot 0 + 1 = 1,   2^0 = 1")
    def _(c):
        table(c)
        if c.is_new:
            c.text(380, 130, "Two rules, same start.", size=15, color=theme.SOFT_INK, anchor="start")
            c.text(380, 152, "Which column is bigger at n = 6?", size=15, color=theme.SOFT_INK, anchor="start")

    @wt.step("Linear adds the same amount", "Each row of 2n + 1 is 2 more than the row above. Same step, "
             "every time, like climbing stairs.", math="+2, +2, +2, ...", fresh=True)
    def _(c):
        table(c, hops_lin=True)
        notes(c, 1)

    @wt.step("Exponential multiplies by the same factor", "Each row of 2ⁿ is double the row above. "
             "The steps themselves keep getting bigger: 1, 2, 4, 8, 16, 32.",
             math="\\times 2, \\times 2, \\times 2, ...", fresh=True)
    def _(c):
        table(c, hops_lin=True, hops_exp=True)
        notes(c, 2)

    @wt.step("Graph both near the start", "The blue line leads at n = 1 and n = 2. The orange curve starts "
             "slow, then bends upward.", math="n = 2:  5 > 4", fresh=True)
    def _(c):
        table(c, hops_lin=True, hops_exp=True)
        p = graph(c, 4, 18, 2)
        p.label(1.2, 7.2, "2n + 1", color=L, size=17)
        p.label(3.55, 15.5, "2^n", color=E, size=17, anchor="end")

    @wt.step("Find the crossover", f"The curves cross near n = {cross:.2f}. From n = {first_win} on, the "
             f"table shows 2ⁿ in front: {exp(first_win)} beats {lin(first_win)}.",
             math=f"2n + 1 = 2^n  at  n \\approx {cross:.2f}", fresh=True)
    def _(c):
        table(c, hops_lin=True, hops_exp=True, highlight=first_win)
        p = graph(c, 4, 18, 2)
        p.label(1.2, 7.2, "2n + 1", color=L, size=17)
        p.label(3.55, 15.5, "2^n", color=E, size=17, anchor="end")
        yc = 2 * cross + 1
        p.vline(cross, color=theme.GREEN, y0=0, y1=yc, width=2)
        p.point(cross, yc, f"n \\approx {cross:.2f}", color=theme.GREEN, r=6, offset=(12, 14), size=16)

    @wt.step("Zoom out", f"By n = 6 the score is {exp(6)} to {lin(6)}. Doubling turns a slow start into a "
             "runaway lead, which is why compound interest and viral videos feel sudden.",
             math=f"n = 6:  2^6 = {exp(6)},   2 \\cdot 6 + 1 = {lin(6)}", fresh=True)
    def _(c):
        table(c, hops_lin=True, hops_exp=True, highlight=6)
        p = graph(c, 6, 70, 10)
        p.label(5.2, 5, "2n + 1", color=L, size=17)
        p.label(4.6, 40, "2^n", color=E, size=17, anchor="end")
        p.point(6, exp(6), "64", color=E, r=5, offset=(-10, 0), anchor="end", size=15)
        p.point(6, lin(6), "13", color=L, r=5, offset=(-10, -14), anchor="end", size=15)

    return wt
