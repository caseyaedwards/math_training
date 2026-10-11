"""Fractions: strips, circles, number lines, and area models."""

from __future__ import annotations

import math
from fractions import Fraction as F

from .. import theme
from ..annotate import brace, hop, number_line
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._kit import frac, rich, tag

CAT = "Fractions and Ratios"


# ---------------------------------------------------------------------------
# Adding fractions with strips
# ---------------------------------------------------------------------------

@diagram("fraction-strips-addition", "Adding Fractions with Strips", CAT)
def build_strips() -> Walkthrough:
    a, b = F(1, 2), F(1, 3)
    den = a.denominator * b.denominator // math.gcd(a.denominator, b.denominator)  # 6
    na, nb = a.numerator * den // a.denominator, b.numerator * den // b.denominator  # 3, 2
    s = a + b
    assert s == F(na + nb, den)

    wt = Walkthrough(
        "fraction-strips-addition", "Adding Fractions with Strips", CAT,
        concept="1/2 + 1/3 = 3/6 + 2/6 = 5/6",
        summary="Halves and thirds are different sizes, so they cannot be counted together. Cut both into "
                "sixths, a size that fits each one exactly, then count sixths.",
        width=700, height=410, level="101",
    )
    BL, BR, BH = 150, 630, 40
    W = BR - BL
    ROW = {"one": 46, "half": 104, "third": 162, "sixth": 220, "sum": 320}
    BLUE, ORANGE, GREEN = theme.BLUE, theme.ORANGE, theme.GREEN

    def X(v):
        return BL + float(v) * W

    def strip(c, row, n, color, shaded, label=True, size=15):
        y = ROW[row] - BH / 2
        for i in range(n):
            x0, x1 = X(F(i, n)), X(F(i + 1, n))
            on = i < shaded
            c.rect(x0, y, x1 - x0, BH, color=color if on else theme.MUTED,
                   fill=theme.fill(color, "45") if on else theme.PAPER, width=2 if on else 1.4)
            if label:
                lx = (x0 + x1) / 2 if n == den else x0 + 24  # keep clear of the later sixth cuts
                frac(c, lx, ROW[row], "1", str(n), size=size,
                     color=color if on else theme.MUTED, halo=on)

    def row_label(c, row, num, den, color):
        frac(c, BL - 30, ROW[row], num, den, size=18, color=color)

    @wt.step("Show one half and one third", "The top strip is one whole. One half of it is blue, "
             "and one third of it is orange.", math="1/2 + 1/3 = ?")
    def _(c):
        c.rect(BL, ROW["one"] - BH / 2, W, BH, color=theme.INK, fill=theme.PANEL, width=2)
        c.text((BL + BR) / 2, ROW["one"], "1 whole", size=16, weight="bold")
        c.text(BL - 30, ROW["one"], "1", size=20, font="serif")
        strip(c, "half", 2, BLUE, 1)
        strip(c, "third", 3, ORANGE, 1)
        row_label(c, "half", "1", "2", BLUE)
        row_label(c, "third", "1", "3", ORANGE)

    @wt.step("Put the pieces end to end", "Slide the two pieces together. The total is clearly less "
             "than one, but a half plus a third is not two of anything: the pieces have different sizes.",
             math="1/2 + 1/3 \\neq 2/5")
    def _(c):
        y = ROW["sum"] - BH / 2
        c.rect(BL, y, W, BH, color=theme.MUTED, width=1.4, dash="5 4")
        c.rect(X(0), y, X(a) - X(0), BH, color=BLUE, fill=theme.fill(BLUE, "45"), width=2)
        c.rect(X(a), y, X(s) - X(a), BH, color=ORANGE, fill=theme.fill(ORANGE, "45"), width=2)
        c.text(BL - 30, ROW["sum"], "sum", size=15, weight="bold")
        if c.is_new:
            frac(c, (X(0) + X(a)) / 2, ROW["sum"], "1", "2", size=15, color=BLUE, halo=True)
            frac(c, (X(a) + X(s)) / 2, ROW["sum"], "1", "3", size=15, color=ORANGE, halo=True)
            c.text((X(s) + BR) / 2, ROW["sum"], "?", size=24, color=theme.RED, weight="bold")
            c.text((BL + BR) / 2, ROW["sum"] + 44, "a half plus a third is not two halves, "
                   "not two thirds, and not 2/5", size=13, color=theme.RED)

    @wt.step("Cut everything into sixths", "Six is the smallest number both 2 and 3 divide. "
             "Each half splits into three sixths and each third into two sixths.",
             math=f"1/2 = {na}/{den},  1/3 = {nb}/{den}")
    def _(c):
        strip(c, "sixth", den, GREEN, den, size=14)
        row_label(c, "sixth", "1", str(den), GREEN)
        for row, color in (("half", BLUE), ("third", ORANGE)):
            y = ROW[row] - BH / 2
            for k in range(1, den):
                v = F(k, den)
                c.line(X(v), y + 3, X(v), y + BH - 3, color=color, width=1.5, dash="4 3")
        y = ROW["sum"] - BH / 2
        for k in range(1, na + nb):
            v = F(k, den)
            c.line(X(v), y + 3, X(v), y + BH - 3, color=BLUE if v < a else ORANGE, width=1.5, dash="4 3")
        yb = ROW["sum"] + BH / 2 + 4
        brace(c, X(a), yb, X(0), yb, label=f"{na}/{den}", color=BLUE, size=16)
        brace(c, X(s), yb, X(a), yb, label=f"{nb}/{den}", color=ORANGE, size=16)
        c.text(X(a) - 4, ROW["half"] + BH / 2 + 9, f"1/2 = {na} sixths", size=12, color=BLUE, anchor="end")
        c.text(X(F(1, 3)) - 4, ROW["third"] + BH / 2 + 9, f"1/3 = {nb} sixths", size=12, color=ORANGE,
               anchor="end")

    @wt.step("Count the sixths", "Now every piece is a sixth, so counting works. Three sixths plus "
             "two sixths is five sixths, one sixth short of a whole.",
             math=f"{na}/{den} + {nb}/{den} = {s.numerator}/{s.denominator}")
    def _(c):
        y = ROW["sum"] - BH / 2
        for k in range(na + nb):
            c.text(X(F(k, den)) + W / den / 2, ROW["sum"], str(k + 1), size=16, weight="bold",
                   color=BLUE if k < na else ORANGE, halo=True)
        brace(c, X(0), y - 4, X(s), y - 4, label=f"{s.numerator}/{s.denominator}", color=GREEN, size=19)
        c.text((X(s) + BR) / 2, ROW["sum"], f"1/{den} left", size=12, color=theme.SOFT_INK)

    return wt


@diagram("fraction-addition-number-line", "Adding Fractions on a Number Line", CAT)
def build_add_line() -> Walkthrough:
    a, b = F(1, 2), F(1, 3)
    s = a + b
    den = s.denominator

    wt = Walkthrough(
        "fraction-addition-number-line", "Adding Fractions on a Number Line", CAT,
        concept="1/2 + 1/3 = 5/6",
        summary="Add fractions as two hops on a number line. The landing spot falls between the half and "
                "third marks, and sixth marks name it exactly.",
        width=700, height=300, level="101",
    )
    L, R, Y = 70, 630, 170
    BLUE, ORANGE, GREEN = theme.BLUE, theme.ORANGE, theme.GREEN

    def X(v):
        return L + float(v) * (R - L)

    @wt.setup
    def _(c):
        c.arrow(L - 20, Y, R + 24, Y, color=theme.INK, width=2, both=True)
        for v, s_ in ((0, "0"), (1, "1")):
            c.line(X(v), Y - 10, X(v), Y + 10, color=theme.INK, width=2.4)
            c.text(X(v), Y + 30, s_, size=18, font="serif", weight="bold")
        return None

    @wt.step("Hop one half from zero", "Start at 0 and jump one half. The halfway tick is the "
             "landing spot.", math="0 + 1/2 = 1/2")
    def _(c):
        c.line(X(a), Y - 8, X(a), Y + 8, color=BLUE, width=2)
        frac(c, X(a), Y + 34, "1", "2", size=15, color=BLUE)
        hop(c, X(0), X(a), Y, "+1/2", color=BLUE, height=60, size=17)
        c.dot(X(a), Y, r=6, color=BLUE)

    @wt.step("Hop one third more", "From one half, jump one third. The hop is the same length "
             "as the gap from 0 to the first third mark.", math="1/2 + 1/3 = ?")
    def _(c):
        for k in (1, 2):
            c.line(X(F(k, 3)), Y - 6, X(F(k, 3)), Y + 6, color=ORANGE, width=1.8)
        if c.is_new:
            frac(c, X(F(1, 3)), Y + 34, "1", "3", size=15, color=ORANGE)
            frac(c, X(F(2, 3)), Y + 34, "2", "3", size=15, color=ORANGE)
        y2 = Y + 64
        c.line(X(0), y2, X(b), y2, color=ORANGE, width=4)
        c.text(X(b) + 8, y2, "a one-third ruler", size=12, color=ORANGE, anchor="start")
        hop(c, X(a), X(s), Y, "+1/3", color=ORANGE, height=36, size=17)
        c.dot(X(s), Y, r=6, color=ORANGE)
        if c.is_new:
            c.text(X(s), Y - 66, "lands between ticks", size=13, color=theme.RED)

    @wt.step("Add sixth marks to name the spot", "Sixths include every half mark and every third "
             "mark. The landing spot sits on the fifth sixth mark.", math="1/2 = 3/6, 1/3 = 2/6")
    def _(c):
        for k in range(1, den):
            v = F(k, den)
            c.line(X(v), Y - 6, X(v), Y + 6, color=GREEN, width=1.6)
            c.text(X(v), Y + 84, f"{k}/{den}", size=13, color=GREEN)
        c.text(X(0), Y + 84, f"0/{den}", size=13, color=GREEN)

    @wt.step("Read the answer", "Count the sixths from 0: three for the half plus two for the third "
             "lands on five sixths.", math="1/2 + 1/3 = 3/6 + 2/6 = 5/6")
    def _(c):
        c.circle(X(s), Y, 13, color=GREEN, width=3)
        tag(c, X(s), Y - 82, "5/6", GREEN, size=19)

    return wt


# ---------------------------------------------------------------------------
# Equivalent fractions
# ---------------------------------------------------------------------------

def pie(c, cx, cy, r, n, shaded, color, base=None):
    """Draws a circle cut into n slices, shading the first `shaded` clockwise from the top.

    base=4 draws the fourth cuts thick so the finer cuts read as splits of fourths.
    """
    for i in range(n):
        a0 = 90 - i * 360 / n
        a1 = 90 - (i + 1) * 360 / n
        on = i < shaded
        c.arc(cx, cy, r, a0, a1, sector=True, color=color if on else theme.MUTED,
              fill=theme.fill(color, "55") if on else theme.PAPER, width=1.2)
    if base:
        for i in range(base):
            ang = math.radians(90 - i * 360 / base)
            c.line(cx, cy, cx + r * math.cos(ang), cy - r * math.sin(ang), color=theme.INK, width=2.4)
    c.circle(cx, cy, r, color=theme.INK, width=2.4)


@diagram("equivalent-fractions-circles", "Equivalent Fractions with Circles", CAT)
def build_circles() -> Walkthrough:
    base = F(3, 4)
    ks = [1, 2, 3]
    fr = [(base.numerator * k, base.denominator * k) for k in ks]
    assert all(F(n, d) == base for n, d in fr)

    wt = Walkthrough(
        "equivalent-fractions-circles", "Equivalent Fractions with Circles", CAT,
        concept="3/4 = 6/8 = 9/12",
        summary="Cutting every slice into equal smaller slices changes the names but not the amount. "
                "Multiply the top and bottom by the same number and the fraction stays put.",
        width=700, height=380, level="101",
    )
    CX = [115, 350, 585]
    CY, RAD = 146, 86
    COLORS = [theme.BLUE, theme.ORANGE, theme.GREEN]

    def label(c, i):
        n, d = fr[i]
        k = ks[i]
        color = COLORS[i]
        if k == 1:
            frac(c, CX[i], 292, str(n), str(d), size=24, color=color)
            c.text(CX[i], 336, f"{n} of {d} slices", size=13, color=theme.SOFT_INK)
            return
        frac(c, CX[i] - 44, 292, [("3", theme.INK), (f" × {k}", theme.PURPLE)],
             [("4", theme.INK), (f" × {k}", theme.PURPLE)], size=19)
        c.text(CX[i] + 6, 292, "=", size=22, font="serif")
        frac(c, CX[i] + 40, 292, str(n), str(d), size=24, color=color)
        c.text(CX[i], 336, f"{n} of {d} slices", size=13, color=theme.SOFT_INK)
        c.text(CX[i], 354, f"(each fourth cut into {k})", size=12, color=theme.PURPLE)

    @wt.step("Shade three fourths", "Cut a circle into 4 equal slices and shade 3 of them. "
             "That is three fourths of a pizza.", math="3/4")
    def _(c):
        pie(c, CX[0], CY, RAD, 4, 3, COLORS[0])
        label(c, 0)

    @wt.step("Cut each fourth in half", "Slice every fourth into 2 pieces. There are now 8 slices and "
             "6 are shaded, but the shaded area has not changed.", math="3/4 = (3 \\times 2)/(4 \\times 2) = 6/8")
    def _(c):
        pie(c, CX[1], CY, RAD, 8, 6, COLORS[1], base=4)
        label(c, 1)

    @wt.step("Cut each fourth into thirds", "Slice every fourth into 3 pieces. Now 9 of 12 slices are "
             "shaded. More slices, smaller slices, same amount of pizza.",
             math="3/4 = (3 \\times 3)/(4 \\times 3) = 9/12")
    def _(c):
        pie(c, CX[2], CY, RAD, 12, 9, COLORS[2], base=4)
        label(c, 2)

    @wt.step("Compare the shaded areas", "Trace the edge of the shaded part. The same outline fits all "
             "three circles, so the three fractions name one amount.", math="3/4 = 6/8 = 9/12")
    def _(c):
        for cx in CX:
            c.arc(cx, CY, RAD, 90, -180, sector=True, color=theme.RED, width=4)
        for i in range(2):
            c.text((CX[i] + CX[i + 1]) / 2, CY, "=", size=36, color=theme.RED, weight="bold")

    return wt


@diagram("equivalent-fractions-number-lines", "Equivalent Fractions on Number Lines", CAT)
def build_eq_lines() -> Walkthrough:
    dens = [4, 8, 12]
    nums = [3 * d // 4 for d in dens]
    assert all(F(n, d) == F(3, 4) for n, d in zip(nums, dens))

    wt = Walkthrough(
        "equivalent-fractions-number-lines", "Equivalent Fractions on Number Lines", CAT,
        concept="3/4 = 6/8 = 9/12",
        summary="Stack number lines cut into fourths, eighths, and twelfths. The marks for 3/4, 6/8, and "
                "9/12 line up, so they are the same point.",
        width=700, height=360, level="101",
    )
    L, R = 90, 640
    YS = [70, 170, 270]
    COLORS = [theme.BLUE, theme.ORANGE, theme.GREEN]

    def X(v):
        return L + float(v) * (R - L)

    def line(c, i):
        d, n, y, color = dens[i], nums[i], YS[i], COLORS[i]
        c.line(L, y, R, y, color=theme.INK, width=2)
        c.line(X(0), y, X(F(n, d)), y, color=color, width=6)
        for k in range(d + 1):
            big = k in (0, d)
            c.line(X(F(k, d)), y - (10 if big else 7), X(F(k, d)), y + (10 if big else 7),
                   color=theme.INK if big else color, width=2 if big else 1.5)
            if 0 < k < d:
                c.text(X(F(k, d)), y + 22, f"{k}/{d}", size=12 if d == 12 else 13,
                       color=color, weight="bold" if k == n else None)
        c.text(L - 14, y, "0", size=15, anchor="end")
        c.text(R + 14, y, "1", size=15, anchor="start")
        c.text(L - 14, y - 26, {4: "fourths", 8: "eighths", 12: "twelfths"}[d], size=12, color=color, anchor="start")
        c.dot(X(F(n, d)), y, r=6.5, color=color)

    @wt.step("Mark three fourths", "Cut 0 to 1 into 4 equal steps and walk 3 of them.",
             math="3/4")
    def _(c):
        line(c, 0)

    @wt.step("Cut the steps in half", "Eighths are half as long as fourths, so it takes 6 of them "
             "to walk as far.", math="3/4 = 6/8")
    def _(c):
        line(c, 1)

    @wt.step("Cut the steps into thirds", "Twelfths are a third as long as fourths. Nine of them "
             "cover the same ground.", math="3/4 = 9/12")
    def _(c):
        line(c, 2)

    @wt.step("Line up the points", "A straight drop passes through all three dots. Different names, "
             "same address on the number line.", math="3/4 = 6/8 = 9/12 = 0.75")
    def _(c):
        x = X(F(3, 4))
        c.line(x, YS[0] - 30, x, YS[2] + 36, color=theme.RED, width=2.2, dash="6 4")
        for d, n, y, color in zip(dens, nums, YS, COLORS):
            c.text(x, y + 22, f"{n}/{d}", size=14, color=color, weight="bold", halo=True)
            c.dot(x, y, r=6.5, color=color)
        tag(c, x, YS[0] - 40, "same point: 0.75", theme.RED, size=14, math=False)

    return wt


# ---------------------------------------------------------------------------
# Multiplying and dividing
# ---------------------------------------------------------------------------

@diagram("fraction-multiplication-area", "Multiplying Fractions with Area", CAT)
def build_mult() -> Walkthrough:
    a, b = F(2, 3), F(3, 4)  # a of b
    p = a * b
    cells = a.denominator * b.denominator  # 12
    hit = a.numerator * b.numerator  # 6
    assert F(hit, cells) == p

    wt = Walkthrough(
        "fraction-multiplication-area", "Multiplying Fractions with Area", CAT,
        concept="2/3 \\times 3/4 = (2 \\times 3)/(3 \\times 4) = 6/12 = 1/2",
        summary="Shade 3/4 of a unit square one way and 2/3 the other way. The overlap is the product: "
                "multiply the tops to count overlap cells and the bottoms to count all cells.",
        width=700, height=400, level="101",
    )
    S, L, T = 300, 70, 56
    BLUE, ORANGE, GREEN = theme.BLUE, theme.ORANGE, theme.GREEN
    cw, ch = S / b.denominator, S / a.denominator
    PX = 540  # center of the right panel

    @wt.setup
    def _(c):
        return None

    @wt.step("Start with one whole square", "The square has side 1, so its area is 1. Every "
             "fraction in this example is a piece of it.", math="area = 1 \\times 1 = 1")
    def _(c):
        c.rect(L, T, S, S, color=theme.INK, fill=theme.PAPER, width=2.4)
        c.text(L + S / 2, T + S + 22, "1", size=18, font="serif")
        c.text(L - 18, T + S / 2, "1", size=18, font="serif")

    @wt.step("Shade 3/4 of the width", "Cut the square into 4 columns and shade 3 of them blue. "
             "The blue part is 3/4 of the square.", math="3/4")
    def _(c):
        for k in range(1, b.denominator):
            c.line(L + k * cw, T, L + k * cw, T + S, color=theme.INK, width=1.4)
        c.rect(L, T, b.numerator * cw, S, color=BLUE, fill=theme.fill(BLUE, "40"), width=2)
        brace(c, L, T - 4, L + b.numerator * cw, T - 4, label="3/4", color=BLUE, size=18)
        frac(c, PX, 110, "3", "4", size=26, color=BLUE)
        c.text(PX, 150, "blue part", size=13, color=BLUE)

    @wt.step("Take 2/3 of the blue part", "Cut the square into 3 rows and shade the bottom 2 orange. "
             "Times means of: 2/3 of 3/4 is where orange crosses blue.", math="2/3 \\times 3/4 = ?")
    def _(c):
        for k in range(1, a.denominator):
            c.line(L, T + k * ch, L + S, T + k * ch, color=theme.INK, width=1.4)
        c.rect(L, T + S - a.numerator * ch, S, a.numerator * ch, color=ORANGE, fill=theme.fill(ORANGE, "40"),
               width=2)
        brace(c, L + S + 4, T + S - a.numerator * ch, L + S + 4, T + S, label="2/3", color=ORANGE, size=18)
        frac(c, PX - 70, 110, "2", "3", size=26, color=ORANGE)
        c.text(PX - 35, 110, "×", size=24, font="serif")
        c.text(PX - 70, 150, "of", size=13, color=ORANGE)

    @wt.step("Count the overlap cells", "The cuts make 3 × 4 = 12 small cells. The overlap holds "
             "2 × 3 = 6 of them, so the product is 6/12.",
             math="2/3 \\times 3/4 = (2 \\times 3)/(3 \\times 4) = 6/12")
    def _(c):
        x0, y0 = L, T + S - a.numerator * ch
        c.rect(x0, y0, b.numerator * cw, a.numerator * ch, color=GREEN, fill=theme.fill(GREEN, "70"), width=3.4)
        k = 0
        for r in range(a.numerator):
            for col in range(b.numerator):
                k += 1
                c.text(x0 + (col + 0.5) * cw, y0 + (r + 0.5) * ch, str(k), size=20, weight="bold",
                       color=theme.INK, halo=True)
        c.text(PX + 35, 110, "=", size=24, font="serif")
        frac(c, PX + 82, 110, [("2", ORANGE), (" × ", theme.INK), ("3", BLUE)],
             [("3", ORANGE), (" × ", theme.INK), ("4", BLUE)], size=20)
        rich(c, PX - 10, 200, f"{hit} overlap cells", size=17, color=GREEN)
        rich(c, PX - 10, 228, f"out of {cells} cells", size=17, color=theme.INK)
        c.text(PX + 82, 214, "→", size=20, color=theme.SOFT_INK)
        frac(c, PX + 122, 214, str(hit), str(cells), size=22, color=GREEN)

    @wt.step("Simplify to one half", "Six of 12 cells is exactly half the square. Slide the six green "
             "cells together and they fill the left half.", math=f"6/12 = {p.numerator}/{p.denominator}")
    def _(c):
        s2, x2, y2 = 120, PX - 60, 262
        c.rect(x2, y2, s2 / 2, s2, color="none", fill=theme.fill(GREEN, "70"))
        for k in range(1, b.denominator):
            c.line(x2 + k * s2 / 4, y2, x2 + k * s2 / 4, y2 + s2, color=theme.INK, width=1)
        for k in range(1, a.denominator):
            c.line(x2, y2 + k * s2 / 3, x2 + s2, y2 + k * s2 / 3, color=theme.INK, width=1)
        c.rect(x2, y2, s2, s2, color=theme.INK, width=2)
        c.line(x2 + s2 / 2, y2 - 6, x2 + s2 / 2, y2 + s2 + 6, color=theme.RED, width=2.4, dash="5 3")
        tag(c, x2 + s2 + 48, y2 + s2 / 2, "= 1/2", GREEN, size=20)

    return wt


@diagram("fraction-division", "Dividing by a Fraction", CAT)
def build_div() -> Walkthrough:
    whole, piece = 2, F(1, 3)
    q = F(whole) / piece
    n = int(q)
    per = int(1 / piece)
    assert q == n == whole * per

    wt = Walkthrough(
        "fraction-division", "Dividing by a Fraction", CAT,
        concept="2 \\div 1/3 = 2 \\times 3 = 6",
        summary="Dividing by 1/3 asks how many thirds fit. Each whole holds 3 thirds, so 2 wholes hold 6.",
        width=700, height=330, level="101",
    )
    L, R = 60, 640
    TOP, BH = 120, 52
    LY = TOP + BH + 26  # number line
    BLUE, ORANGE, GREEN = theme.BLUE, theme.ORANGE, theme.GREEN

    def X(v):
        return L + float(v) / whole * (R - L)

    @wt.setup
    def _(c):
        return number_line(c, L, LY, R, 0, whole, step=1, size=15)

    @wt.step("Draw a bar 2 units long", "The bar is the amount to measure: 2 whole units. "
             "The question is how many pieces of size 1/3 fit in it.", math="2 \\div 1/3 = ?")
    def _(c, _X):
        c.rect(X(0), TOP, X(whole) - X(0), BH, color=BLUE, fill=theme.fill(BLUE, "30"), width=2.4)
        c.line(X(1), TOP, X(1), TOP + BH, color=BLUE, width=2.4)
        if c.is_new:
            c.text(X(F(1, 2)), TOP + BH / 2, "1 whole", size=15, color=BLUE, weight="bold")
            c.text(X(F(3, 2)), TOP + BH / 2, "1 whole", size=15, color=BLUE, weight="bold")
            c.rect(X(0), 50, X(piece) - X(0), 30, color=ORANGE, fill=theme.fill(ORANGE, "55"), width=2)
            c.text(X(piece) + 10, 65, "one piece = 1/3", size=14, color=ORANGE, anchor="start")

    def tile(c, k):
        x0, x1 = X(piece * k), X(piece * (k + 1))
        c.rect(x0 + 2, TOP + 4, x1 - x0 - 4, BH - 8, color=ORANGE, fill=theme.fill(ORANGE, "50"), width=2)
        c.text((x0 + x1) / 2, TOP + BH / 2, str(k + 1), size=20, weight="bold", color=theme.INK)
        hop(c, x0, x1, TOP - 4, None, color=ORANGE, height=22)

    @wt.step("Fit thirds into the first whole", "Lay 1/3 pieces end to end from 0. Three of "
             "them fill the first whole exactly.", math="1 \\div 1/3 = 3")
    def _(c, _X):
        for k in range(per):
            tile(c, k)
        for k in range(1, per * whole):
            if k % per:
                c.line(X(piece * k), LY - 5, X(piece * k), LY + 5, color=ORANGE, width=1.6)
                c.text(X(piece * k), LY + 22, f"{k}/{per}", size=12, color=ORANGE)

    @wt.step("Fit thirds into the second whole", "The second whole is the same size, so it holds "
             "another three. Same pattern, no surprises.", math="3 + 3 thirds")
    def _(c, _X):
        for k in range(per, per * whole):
            tile(c, k)

    @wt.step("Count the pieces", "Six pieces fit in 2 wholes. Dividing by 1/3 gives the same answer "
             "as multiplying by 3, which is why the flip rule works.",
             math="2 \\div 1/3 = 2 \\times 3 = 6")
    def _(c, _X):
        y = LY + 40
        brace(c, X(1), y, X(0), y, label="3 thirds", color=ORANGE, size=15)
        brace(c, X(2), y, X(1), y, label="3 thirds", color=ORANGE, size=15)
        tag(c, (L + R) / 2, 60, "6 pieces of 1/3 fit in 2", GREEN, size=18, math=False)

    return wt
