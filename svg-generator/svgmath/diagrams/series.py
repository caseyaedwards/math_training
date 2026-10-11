"""Series diagrams: the geometric series 1/2 + 1/4 + ..., Gauss's sum, and the harmonic series."""

from __future__ import annotations

import math
from fractions import Fraction

from .. import theme
from ..annotate import brace, hop, number_line
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough

COLORS = [theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE, theme.SKY, theme.RED]
GAP_C = theme.INK  # the unshaded remainder


def _stage(scene, stage):
    def draw(c, ctx):
        scene(c, stage)
    return draw


def frac(f: Fraction) -> str:
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


# ---------------------------------------------------------------------------
# Geometric series by square subdivision
# ---------------------------------------------------------------------------


def halving_pieces(n: int):
    """Returns n rectangles (x0, y0, x1, y1) in the unit square, each half of what remains, and the remainder."""
    x0, y0, x1, y1 = 0.0, 0.0, 1.0, 1.0
    out = []
    for i in range(n):
        if i % 2 == 0:  # cut off the left half
            xm = (x0 + x1) / 2
            out.append((x0, y0, xm, y1))
            x0 = xm
        else:  # cut off the top half
            ym = (y0 + y1) / 2
            out.append((x0, ym, x1, y1))
            y1 = ym
    return out, (x0, y0, x1, y1)


@diagram("geometric-series-square", "Geometric Series in a Square", "Sequences and Series")
def build_geometric_square() -> Walkthrough:
    wt = Walkthrough(
        "geometric-series-square", "Geometric Series: Halving a Square", "Sequences and Series",
        concept="1/2 + 1/4 + 1/8 + \\ldots = 1",
        summary="Shade half of a square, then half of what is left, and keep going. The shaded pieces fill the "
                "whole square, so the infinite sum 1/2 + 1/4 + 1/8 + ... equals 1.",
        width=680, height=400, level="201",
    )
    SX, SY, SW = 30, 40, 320
    NMAX = 10
    stages = {1: 0, 2: 1, 3: 2, 4: 4, 5: NMAX}

    def scene(c, stage):
        n = stages[stage]
        pieces, rem = halving_pieces(n)

        def px(x, y):
            return SX + x * SW, SY + (1 - y) * SW

        for i, (x0, y0, x1, y1) in enumerate(pieces):
            col = COLORS[i % len(COLORS)]
            X0, Y1 = px(x0, y1)
            X1, Y0 = px(x1, y0)
            c.rect(X0, Y1, X1 - X0, Y0 - Y1, color=theme.PAPER, fill=theme.fill(col, "99"), width=1.5)
            if i < 5:
                lab = frac(Fraction(1, 2 ** (i + 1)))
                c.text((X0 + X1) / 2, (Y0 + Y1) / 2, lab, size=[22, 19, 16, 14, 11][i], weight="bold",
                       color=theme.INK, halo=True)
        c.rect(SX, SY, SW, SW, color=theme.INK, width=2.5)
        c.text(SX + SW / 2, SY - 16, "area 1", size=14, color=theme.SOFT_INK)
        # the leftover piece
        rx0, ry0, rx1, ry1 = rem
        left = Fraction(1, 2 ** n)
        X0, Y1 = px(rx0, ry1)
        X1, Y0 = px(rx1, ry0)
        if n:
            c.rect(X0, Y1, X1 - X0, Y0 - Y1, color=GAP_C, width=2, dash="5 3")
        if n <= 2:
            c.text((X0 + X1) / 2, (Y0 + Y1) / 2, "left: " + frac(left) if n else "", size=15, color=GAP_C,
                   halo=True)
        else:
            tx, ty = X1 - 2, Y0 + 2
            c.line(tx, ty, SX + SW + 20, SY + SW - 10, color=GAP_C, width=1.4)
            c.text(SX + SW + 24, SY + SW - 10, "left: " + frac(left), size=14, color=GAP_C, anchor="start")
        # running table
        tx = 420
        cols = [tx, tx + 50, tx + 130, tx + 210]
        heads = ["n", "term", "sum", "left"]
        for x, h in zip(cols, heads):
            c.text(x, 40, h, size=14, weight="bold", color=theme.SOFT_INK, math=(h == "n"))
        c.line(tx - 20, 54, 680 - 10, 54, color=theme.GRID, width=1.5)
        total = Fraction(0)
        rows = list(range(1, n + 1))
        if n > 6:
            rows = [1, 2, 3, 4, None, n]
        k_total = {}
        for k in range(1, n + 1):
            total += Fraction(1, 2 ** k)
            k_total[k] = total
        for r, k in enumerate(rows):
            y = 76 + r * 28
            if k is None:
                c.text(cols[0], y, "⋮", size=16, color=theme.SOFT_INK)
                c.text(cols[2], y, "⋮", size=16, color=theme.SOFT_INK)
                continue
            col = COLORS[(k - 1) % len(COLORS)]
            c.text(cols[0], y, str(k), size=14)
            c.text(cols[1], y, frac(Fraction(1, 2 ** k)), size=14, color=col, weight="bold")
            c.text(cols[2], y, frac(k_total[k]), size=14)
            c.text(cols[3], y, frac(1 - k_total[k]), size=14, color=GAP_C)
        if 2 <= stage <= 4:
            y = 76 + len(rows) * 28 + 20
            c.text(tx - 20, y, "The white gap always equals", size=14, anchor="start", color=theme.SOFT_INK)
            c.text(tx - 20, y + 20, "the last piece shaded.", size=14, anchor="start", color=theme.SOFT_INK)
            c.text(tx - 20, y + 50, "sum + left = 1 in every row", size=14, anchor="start", color=theme.INK,
                   weight="bold")
        if stage == 5:
            y = 76 + len(rows) * 28 + 20
            c.text(tx - 20, y, f"after {n} halvings the gap is", size=14, anchor="start", color=theme.SOFT_INK)
            c.text(tx - 20, y + 22, f"{frac(left)} ≈ {float(left):.4f}: too thin to see", size=14,
                   anchor="start", color=GAP_C)
            c.label_box(545, y + 66, "sum → 1", size=18, color=theme.GREEN, border=theme.GREEN)

    wt.step("Start with a square of area 1",
            "The whole square has area 1. Every piece cut from it has an area that is a fraction of 1.",
            math="area = 1", fresh=True)(_stage(scene, 1))
    wt.step("Shade half",
            "Shade the left half. The first term is 1/2, and the other half is still white.",
            math="S_1 = 1/2,  left = 1/2", fresh=True)(_stage(scene, 2))
    wt.step("Shade half of what is left",
            "Cut the white half in two and shade one part. The new piece is 1/4, so the total is 3/4.",
            math="S_2 = 1/2 + 1/4 = 3/4", fresh=True)(_stage(scene, 3))
    wt.step("Keep halving the gap",
            "Two more cuts add 1/8 and 1/16. The shaded total is 15/16, and the white gap is exactly the "
            "last piece added.", math="S_4 = 15/16 = 1 - 1/16", fresh=True)(_stage(scene, 4))
    wt.step("Let the gap vanish",
            f"After n terms the gap is 1/2ⁿ. It shrinks toward zero but never goes negative, so the "
            "shaded area closes in on the whole square.",
            math="S_n = 1 - 1/2^n \\to 1", fresh=True)(_stage(scene, 5))
    return wt


@diagram("geometric-series-number-line", "Geometric Series on a Number Line", "Sequences and Series")
def build_geometric_line() -> Walkthrough:
    wt = Walkthrough(
        "geometric-series-number-line", "Geometric Series: Halfway Hops", "Sequences and Series",
        concept="1/2 + 1/4 + 1/8 + \\ldots = 1",
        summary="A frog hops half the remaining distance to 1 on each jump. It never lands on 1 in finitely "
                "many hops, but the total distance closes in on 1, so the infinite sum equals 1.",
        width=680, height=330, level="201",
    )
    Y = 200
    L, Rr = 60, 620
    MAG_Y = 290

    def X(v):
        return L + float(v) * (Rr - L)

    def scene(c, stage):
        number_line(c, L, Y, Rr, 0, 1, step=0.25, fmt_label=lambda v: {0: "0", 0.25: "1/4", 0.5: "1/2",
                                                                        0.75: "3/4", 1: "1"}[v])
        c.dot(X(1), Y, r=7, color=theme.GREEN)
        c.text(X(1) + 12, Y - 16, "goal", size=13, color=theme.GREEN, weight="bold", anchor="start")
        n = {1: 1, 2: 2, 3: 4, 4: 8}[stage]
        pos = Fraction(0)
        heights = [110, 80, 58, 44, 36, 30, 26, 22]
        for k in range(n):
            step = Fraction(1, 2 ** (k + 1))
            col = COLORS[k % len(COLORS)]
            lab = frac(step) if k < 4 else None
            hop(c, X(pos), X(pos + step), Y, lab, color=col, height=heights[k], size=14)
            pos += step
        c.dot(X(pos), Y, r=6, color=theme.INK)
        c.text(30, 40, f"after {n} hop{'s' if n > 1 else ''}:", size=15, anchor="start", color=theme.SOFT_INK)
        c.math(160, 40, f"S_{n} = {frac(pos)}", size=18, anchor="start")
        c.text(330, 40, f"distance to 1: {frac(1 - pos)}", size=15, anchor="start", color=GAP_C, weight="bold")
        if stage >= 3:
            # magnify the last quarter of the line
            a = 0.75
            c.line(X(a), Y + 34, 60, MAG_Y - 16, color=theme.MUTED, width=1, dash="4 3")
            c.line(X(1), Y + 34, 620, MAG_Y - 16, color=theme.MUTED, width=1, dash="4 3")
            c.line(60, MAG_Y, 620, MAG_Y, color=theme.INK, width=1.5)

            def M(v):
                return 60 + (float(v) - a) / (1 - a) * 560

            for v, lab in ((0.75, "3/4"), (0.875, "7/8"), (0.9375, "15/16"), (1, "1")):
                c.line(M(v), MAG_Y - 6, M(v), MAG_Y + 6, color=theme.INK, width=1.5)
                c.text(M(v), MAG_Y + 20, lab, size=12, color=theme.SOFT_INK)
            p2 = Fraction(3, 4)
            for k in range(2, n):
                stp = Fraction(1, 2 ** (k + 1))
                col = COLORS[k % len(COLORS)]
                c.line(M(p2), MAG_Y, M(p2 + stp), MAG_Y, color=col, width=5)
                p2 += stp
            c.text(340, MAG_Y - 22, "zoom on the last quarter", size=12, color=theme.SOFT_INK, halo=True)
        if stage == 4:
            c.text(330, 66, "each gap is half the one before; the frog never quite arrives",
                   size=13, anchor="start", color=theme.SOFT_INK)

    wt.step("Hop halfway",
            "Start at 0 and hop half of the distance to 1. The frog lands on 1/2.",
            math="S_1 = 1/2", fresh=True)(_stage(scene, 1))
    wt.step("Hop half of what remains",
            "The distance left is 1/2, so the next hop is 1/4. The frog lands on 3/4.",
            math="S_2 = 1/2 + 1/4 = 3/4", fresh=True)(_stage(scene, 2))
    wt.step("Watch the hops shrink",
            "Hops of 1/8 and 1/16 follow. Each hop halves the distance left, so the gap is always the size of "
            "the last hop.", math="S_4 = 15/16", fresh=True)(_stage(scene, 3))
    wt.step("Add infinitely many hops",
            "After eight hops the frog is 1/256 short. The partial sums never pass 1 and get as close as you "
            "like, so the infinite sum is exactly 1.", math="1/2 + 1/4 + 1/8 + \\ldots = 1",
            fresh=True)(_stage(scene, 4))
    return wt


# ---------------------------------------------------------------------------
# Gauss's sum
# ---------------------------------------------------------------------------


@diagram("gauss-sum", "Gauss's Sum", "Sequences and Series")
def build_gauss() -> Walkthrough:
    wt = Walkthrough(
        "gauss-sum", "Gauss's Trick: Two Staircases Make a Rectangle", "Sequences and Series",
        concept="1 + 2 + \\ldots + n = n(n + 1)/2",
        summary="Stack 1 + 2 + ... + 10 as a staircase of squares. A second, flipped staircase fills the gaps "
                "and makes a 10 by 11 rectangle, so one staircase holds half of 110, which is 55.",
        width=680, height=360, level="101",
    )
    n = 10
    S = 22
    X0, BASE = 110, 316
    TOP = BASE - (n + 1) * S
    total = sum(range(1, n + 1))
    assert total == n * (n + 1) // 2

    def scene(c, stage):
        for i in range(1, n + 1):
            x = X0 + (i - 1) * S
            for r in range(i):
                c.rect(x, BASE - (r + 1) * S, S, S, color=theme.PAPER, fill=theme.BLUE, width=1.5)
            if stage >= 2:
                for r in range(i, n + 1):
                    c.rect(x, BASE - (r + 1) * S, S, S, color=theme.PAPER, fill=theme.ORANGE, width=1.5)
            if stage < 4:
                c.text(x + S / 2, BASE + 14, str(i), size=12, color=theme.BLUE, weight="bold")
            if stage == 3:
                c.text(x + S / 2, TOP - 12, str(n + 1), size=12, color=theme.GREEN, weight="bold")
        if stage >= 2:
            c.rect(X0, TOP, n * S, (n + 1) * S, color=theme.INK if stage >= 4 else "none", width=2)
        if stage >= 4:
            brace(c, X0 + n * S, BASE + 6, X0, BASE + 6, label="n = 10" if stage == 5 else "10",
                  color=theme.INK, size=15)
            brace(c, X0 - 6, BASE, X0 - 6, TOP, label="n + 1 = 11" if stage == 5 else "11",
                  color=theme.INK, size=15)
        if stage == 3:
            c.text(X0 + n * S / 2, TOP - 30, "every column holds 11", size=13, color=theme.GREEN)
        # right panel
        tx = 372
        if stage == 1:
            c.math(tx, 60, "1 + 2 + 3 + \\ldots + 10 = ?", size=20, anchor="start", color=theme.BLUE)
            c.text(tx, 100, "Column i holds i blue squares.", size=15, anchor="start")
            c.text(tx, 126, "Counting them one by one works,", size=15, anchor="start")
            c.text(tx, 150, "but it is slow and easy to botch.", size=15, anchor="start", color=theme.SOFT_INK)
        if stage == 2:
            c.text(tx, 60, "Columns, left to right:", size=15, anchor="start")
            c.text(tx, 92, "blue:    " + ", ".join(str(i) for i in range(1, n + 1)), size=15, anchor="start",
                   color=theme.BLUE)
            c.text(tx, 120, "orange: " + ", ".join(str(n + 1 - i) for i in range(1, n + 1)), size=15,
                   anchor="start", color=theme.ORANGE)
            c.text(tx, 160, "The orange copy is the same staircase,", size=14, anchor="start",
                   color=theme.SOFT_INK)
            c.text(tx, 180, "turned upside down.", size=14, anchor="start", color=theme.SOFT_INK)
        if stage == 3:
            for i in range(1, n + 1):
                y = 46 + (i - 1) * 25
                c.math(tx + 20, y, f"{i}", size=17, anchor="end", color=theme.BLUE)
                c.math(tx + 30, y, "+", size=17, anchor="start")
                c.math(tx + 70, y, f"{n + 1 - i}", size=17, anchor="end", color=theme.ORANGE)
                c.math(tx + 80, y, f"= {n + 1}", size=17, anchor="start", color=theme.GREEN)
            c.text(tx + 160, 160, f"{n} pairs,", size=15, anchor="start")
            c.text(tx + 160, 184, f"each worth {n + 1}", size=15, anchor="start", color=theme.GREEN)
        if stage == 4:
            c.math(tx, 70, f"two staircases = {n} \\times {n + 1} = {n * (n + 1)}", size=19, anchor="start")
            c.math(tx, 120, f"one staircase = {n * (n + 1)} \\div 2 = {total}", size=19, anchor="start",
                   color=theme.BLUE, weight="bold")
            c.text(tx, 170, "Young Gauss reportedly did this in his head", size=13, anchor="start",
                   color=theme.SOFT_INK)
            c.text(tx, 190, "while his classmates were still adding.", size=13, anchor="start",
                   color=theme.SOFT_INK)
        if stage == 5:
            c.math(tx, 70, "1 + 2 + \\ldots + n = n(n + 1)/2", size=20, anchor="start", weight="bold")
            for i, m in enumerate((10, 100, 1000)):
                c.math(tx, 120 + i * 32, f"n = {m}:  {m * (m + 1) // 2}", size=17, anchor="start",
                       color=theme.BLUE)
            c.text(tx, 232, "Same picture, any n: an n by (n + 1)", size=14, anchor="start", color=theme.SOFT_INK)
            c.text(tx, 252, "rectangle cut along its staircase.", size=14, anchor="start", color=theme.SOFT_INK)

    wt.step("Build the staircase",
            "Draw the sum 1 + 2 + … + 10 as columns of squares. Column 1 has one square, column 10 has ten.",
            math="1 + 2 + \\ldots + 10 = ?", fresh=True)(_stage(scene, 1))
    wt.step("Add a flipped copy",
            "Turn a second copy of the staircase upside down and set it on top. Its columns run 10, 9, …, 1.",
            math="(1 + \\ldots + 10) + (10 + \\ldots + 1)", fresh=True)(_stage(scene, 2))
    wt.step("Every column holds 11",
            "Each column pairs a blue count with an orange count that add to 11: 1 + 10, 2 + 9, and so on.",
            math="i + (11 - i) = 11", fresh=True)(_stage(scene, 3))
    wt.step("Count the rectangle and halve it",
            f"The two staircases fill a 10 by 11 rectangle of {n * (n + 1)} squares. One staircase is half "
            f"of that.", math=f"1 + 2 + \\ldots + 10 = {n}\\cdot{n + 1}/2 = {total}", fresh=True)(_stage(scene, 4))
    wt.step("Use it for any n",
            "Nothing in the picture depends on 10. For any n the two staircases make an n by n + 1 rectangle.",
            math="1 + 2 + \\ldots + n = n(n + 1)/2", fresh=True)(_stage(scene, 5))
    return wt


# ---------------------------------------------------------------------------
# Harmonic series
# ---------------------------------------------------------------------------


def H(n: int) -> float:
    return sum(1 / k for k in range(1, n + 1))


@diagram("harmonic-series", "Harmonic Series Diverges", "Sequences and Series")
def build_harmonic() -> Walkthrough:
    wt = Walkthrough(
        "harmonic-series", "The Harmonic Series Diverges", "Sequences and Series",
        concept="1 + 1/2 + 1/3 + 1/4 + \\ldots = \\infty",
        summary="Group the terms of 1 + 1/2 + 1/3 + ... into blocks of 1, 2, 4, 8, ... terms. Each block adds "
                "at least 1/2, and infinitely many halves add up to infinity.",
        width=700, height=420, level="301",
    )
    U = 300  # px per unit
    BX = 210
    HALF_X = BX + U / 2

    groups = [(1, 1), (2, 2), (3, 4), (5, 8), (9, 16)]
    rows_y = [44, 92, 150, 222, 294]

    def bar_row(c, y, terms, colors, h=18, dash=None, label_inside=True):
        x = BX
        for k, (t, col) in enumerate(zip(terms, colors)):
            w = t * U
            c.rect(x, y - h / 2, w, h, color=theme.PAPER, fill=col, width=1.2, dash=dash)
            x += w
        return x

    def scene(c, stage):
        c.line(BX, 22, BX, 340, color=theme.INK, width=1.5)
        c.line(HALF_X, 22, HALF_X, 340, color=theme.GREEN, width=1.5, dash="6 4")
        c.text(HALF_X, 352, "1/2", size=13, color=theme.GREEN, weight="bold")
        c.text(BX, 352, "0", size=13, color=theme.SOFT_INK)
        c.line(BX + U, 22, BX + U, 340, color=theme.GRID, width=1.5)
        c.text(BX + U, 352, "1", size=13, color=theme.SOFT_INK)
        shown = {1: 2, 2: 3, 3: 4, 4: 5, 5: 5}[stage]
        lower = 0.0
        for g in range(shown):
            a, b = groups[g]
            y = rows_y[g]
            terms = [1 / k for k in range(a, b + 1)]
            cols = [COLORS[g % len(COLORS)] if (k - a) % 2 == 0 else theme.fill(COLORS[g % len(COLORS)], "99")
                    for k in range(a, b + 1)]
            label = f"1/{a}" if a == b else f"1/{a} + … + 1/{b}" if b - a > 1 else f"1/{a} + 1/{b}"
            if a == 1:
                label = "1"
            c.text(BX - 12, y, label, size=14, anchor="end", color=COLORS[g % len(COLORS)], weight="bold")
            end = bar_row(c, y, terms, cols)
            c.text(end + 8, y, f"= {sum(terms):.3f}", size=13, anchor="start", color=theme.INK)
            if b - a >= 1:
                n = b - a + 1
                small = 1 / b
                ref = [small] * n
                yr = y + 24
                x = BX
                for _ in ref:
                    c.rect(x, yr - 7, small * U, 14, color=theme.PAPER, fill=theme.fill(theme.GREEN, "66"),
                           width=1.2)
                    x += small * U
                c.text(BX - 12, yr, f"≥ {n} × 1/{b}", size=13, anchor="end", color=theme.GREEN)
                c.text(x + 8, yr, "= 1/2", size=13, anchor="start", color=theme.GREEN, weight="bold")
            lower += 0.5 if g > 0 else 1
        if stage >= 4:
            c.text(560, 150, "Every block", size=14, anchor="start", color=theme.GREEN)
            c.text(560, 170, "passes the", size=14, anchor="start", color=theme.GREEN)
            c.text(560, 190, "dashed line.", size=14, anchor="start", color=theme.GREEN)
        if stage >= 5:
            m = 4
            c.label_box(350, 390, f"1 + 1/2 + … + 1/16 ≥ 1 + {m}·1/2 = {1 + m / 2:g}   "
                        f"(true value {H(16):.3f})", size=15, border=theme.BLUE, color=theme.BLUE)

    def growth(c, ctx):
        p = Plane(c, box=(70, 30, 560, 320), x=(0, 66), y=(0, 5.2))
        p.grid(step=8, ystep=1)
        p.axes(xlabel="n", ylabel="S_n", step=8, ystep=1)
        for k in range(1, 65):
            p.point(k, H(k), r=2.6, color=theme.BLUE)
        bound = [(2 ** m, 1 + m / 2) for m in range(0, 7)]
        for i in range(len(bound) - 1):
            (x0, y0), (x1, y1) = bound[i], bound[i + 1]
            p.segment(x0, y0, x1, y0, color=theme.GREEN, width=2, dash="5 4")
            p.segment(x1, y0, x1, y1, color=theme.GREEN, width=2, dash="5 4")
        for x, y in bound:
            p.point(x, y, r=5, color=theme.GREEN)
        p.label(64, H(64) + 0.3, f"S_64 ≈ {H(64):.2f}", color=theme.BLUE, size=15, anchor="end")
        p.label(63, 3.5 - 0.3, "floor at n = 64:  1 + 6/2 = 4", color=theme.GREEN, size=15, anchor="end")
        p.label(20, 4.6, "slow, but it never stops climbing", color=theme.SOFT_INK, size=14, math=False,
                anchor="start")

    wt.step("Write out the first terms",
            "Draw each term as a bar on a ruler from 0 to 1. The first two terms are 1 and 1/2. The green "
            "dashed line marks 1/2.", math="1 + 1/2 + 1/3 + 1/4 + \\ldots", fresh=True)(_stage(scene, 1))
    wt.step("Group two terms",
            "Take 1/3 + 1/4. Both terms are at least 1/4, so the pair is at least two quarters, which is 1/2.",
            math="1/3 + 1/4 \\geq 1/4 + 1/4 = 1/2", fresh=True)(_stage(scene, 2))
    wt.step("Group the next four",
            "The four terms from 1/5 to 1/8 are each at least 1/8. Four eighths make 1/2 again.",
            math="1/5 + \\ldots + 1/8 \\geq 4\\cdot1/8 = 1/2", fresh=True)(_stage(scene, 3))
    wt.step("Group the next eight",
            "Eight terms from 1/9 to 1/16 are each at least 1/16, so this block also beats 1/2. The pattern "
            "never runs out of blocks.", math="1/9 + \\ldots + 1/16 \\geq 8\\cdot1/16 = 1/2",
            fresh=True)(_stage(scene, 4))
    wt.step("Add up the blocks",
            "After the first term, every doubling of the number of terms adds at least another 1/2.",
            math="S_n \\geq 1 + m/2  when  n = 2^m", fresh=True)(_stage(scene, 5))
    wt.step("Watch the sum grow without bound",
            "The blue partial sums always stay above the green floor 1 + m/2, and that floor climbs forever. "
            "So the series diverges, even though its terms shrink to zero.",
            math="1 + 1/2 + 1/3 + \\ldots = \\infty", fresh=True)(growth)
    return wt


@diagram("harmonic-series-area", "Harmonic Series as Area", "Sequences and Series")
def build_harmonic_area() -> Walkthrough:
    wt = Walkthrough(
        "harmonic-series-area", "The Harmonic Series as Area", "Sequences and Series",
        concept="1 + 1/2 + \\ldots + 1/n > \\int_1^{n+1} 1/x dx = ln(n + 1)",
        summary="Draw each term 1/k as a bar of width 1. The bars cover the area under y = 1/x, and that area "
                "grows like ln n without limit, so the harmonic series diverges.",
        width=680, height=380, level="301",
    )
    NB = 8

    @wt.setup
    def _(c):
        p = Plane(c, box=(60, 30, 560, 300), x=(0, 9.6), y=(0, 1.2))
        p.grid(step=1, ystep=0.25)
        p.axes(step=1, ystep=0.25, xlabel="x", ylabel="y")
        return p

    def bars(p, n, labels=True):
        for k in range(1, n + 1):
            col = COLORS[(k - 1) % len(COLORS)]
            p.rect(k, 0, k + 1, 1 / k, color=col, fill=theme.fill(col, "40"), width=1.5)
            if labels and k <= 6:
                X, Y = p.px(k + 0.5, 1 / k)
                p.c.text(X, Y - 12, "1" if k == 1 else f"1/{k}", size=13, color=col, weight="bold", halo=True)

    @wt.step("Draw each term as a bar",
             "Bar k sits on [k, k + 1] with height 1/k, so its area equals the term 1/k.",
             math="area of bar k = 1\\cdot1/k = 1/k")
    def _(c, p):
        bars(p, NB)
        c.math(470, 60, f"total bar area = H_{NB}", size=16, color=theme.BLUE, anchor="start")

    @wt.step("Slide the curve under the bars",
             "The curve y = 1/x starts at the top-left corner of each bar and then drops below it. So the bars "
             "hold more area than the region under the curve.", math="1/k \\geq 1/x  for  k \\leq x \\leq k + 1")
    def _(c, p):
        p.shade_under(lambda x: 1 / x, 1, NB + 1, color=theme.INK, opacity=0.12)
        p.plot(lambda x: 1 / x, 0.85, 9.6, color=theme.INK)
        p.label(3.5, 0.6, "y = 1/x", color=theme.INK, size=17)

    @wt.step("Compare the sum with a logarithm",
             f"The area under 1/x from 1 to {NB + 1} is ln {NB + 1}. The bars hold a little more than that.",
             math=f"H_{NB} = {H(NB):.3f} > ln {NB + 1} = {math.log(NB + 1):.3f}")
    def _(c, p):
        c.label_box(520, 110, f"H_{NB} = {H(NB):.3f}", size=15, border=theme.BLUE, color=theme.BLUE, math=True)
        c.label_box(520, 146, f"ln {NB + 1} = {math.log(NB + 1):.3f}", size=15, border=theme.INK, math=True)

    @wt.step("Let the logarithm run away",
             "The logarithm grows slowly but without any ceiling, and the sum stays above it. So the harmonic "
             "series diverges, just very lazily.",
             math=f"H_{{1000}} \\approx {H(1000):.2f},   H_{{1000000}} \\approx {math.log(10 ** 6) + 0.5772:.2f}")
    def _(c, p):
        c.text(520, 190, "ln n → ∞", size=17, color=theme.RED, weight="bold", math=True)
        c.text(520, 214, f"1000 terms: {H(1000):.2f}", size=13, color=theme.SOFT_INK)
        c.text(520, 234, f"a million terms: ≈ {math.log(10 ** 6) + 0.5772:.1f}", size=13, color=theme.SOFT_INK)

    return wt
