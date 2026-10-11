"""Greatest common divisor and least common multiple: Venn diagrams, lists, and the Euclidean algorithm."""

from __future__ import annotations

import math
from collections import Counter

from .. import theme
from ..annotate import number_line
from ..registry import diagram
from ..svg import fmt
from ..walkthrough import Walkthrough
from .factors import node, prime_factors, split

A_COL, B_COL = theme.BLUE, theme.ORANGE
GCD_COL, LCM_COL = theme.GREEN, theme.PURPLE


def times(xs) -> str:
    return " \\times ".join(str(x) for x in xs)


@diagram("gcd-lcm-venn", "GCD and LCM with a Venn Diagram", "Number Theory")
def build_venn() -> Walkthrough:
    A, B = 12, 18
    fa, fb = Counter(prime_factors(A)), Counter(prime_factors(B))
    shared = sorted((fa & fb).elements())
    only_a = sorted((fa - fb).elements())
    only_b = sorted((fb - fa).elements())
    g = math.prod(shared)
    l = math.prod(shared + only_a + only_b)
    assert g == math.gcd(A, B) and l == A * B // g

    wt = Walkthrough(
        "gcd-lcm-venn", "GCD and LCM with a Venn Diagram", "Number Theory",
        concept=f"gcd({A}, {B}) = {g},  lcm({A}, {B}) = {l},  {g} \\times {l} = {A} \\times {B}",
        summary="Put the prime factors of two numbers in a Venn diagram. The overlap multiplies to the GCD, "
                "and everything together multiplies to the LCM.",
        width=700, height=420, level="101",
    )
    CY, R = 226, 120
    CXA, CXB = 185, 315
    d = CXB - CXA
    h = math.sqrt(R * R - (d / 2) ** 2)
    mx = (CXA + CXB) / 2
    top, bot = (mx, CY - h), (mx, CY + h)
    PX = 575  # right panel center

    def token(c, x, y, p, ring=None):
        c.circle(x, y, 19, color=ring or theme.INK, fill=theme.PAPER, width=2)
        c.text(x, y, str(p), size=18, weight="bold")

    def spots(xc, n, gap=62):
        return [(xc, CY + (i - (n - 1) / 2) * gap) for i in range(n)]

    def box(c, y, lines, col):
        c.rect(PX - 105, y, 210, 24 * len(lines) + 14, color=col, fill=theme.fill(col, "18"), width=1.8, rx=8)
        for i, (s, sz) in enumerate(lines):
            c.text(PX, y + 19 + 24 * i, s, size=sz, color=col, weight="bold" if i == 0 else None, math=i > 0)

    @wt.step("Factor both numbers", "Break each number into primes. Both lists contain a 2 and a 3, which "
             "is where the two numbers overlap.", math=f"{A} = {times(prime_factors(A))},  {B} = {times(prime_factors(B))}")
    def _(c):
        c.math(CXA - 40, 34, f"{A} = {times(prime_factors(A))}", color=A_COL, size=20)
        c.math(CXB + 40, 34, f"{B} = {times(prime_factors(B))}", color=B_COL, size=20)
        if c.is_new:
            for pos in (
                {"r": (CXA - 40, 100, A), "a": (CXA - 90, 175, 2), "b": (CXA + 10, 175, 6),
                 "c": (CXA - 30, 250, 2), "d": (CXA + 50, 250, 3)},
                {"r": (CXB + 40, 100, B), "a": (CXB - 10, 175, 2), "b": (CXB + 90, 175, 9),
                 "c": (CXB + 50, 250, 3), "d": (CXB + 130, 250, 3)},
            ):
                node(c, *pos["r"])
                split(c, pos, "r", ["a", "b"])
                split(c, pos, "b", ["c", "d"])
            c.text(CXA + 65, 310, "colored = prime", size=13, color=theme.SOFT_INK)

    @wt.step("Put shared primes in the overlap", "Draw a circle for each number. One 2 and one 3 belong to "
             "both, so they sit where the circles overlap.", math=f"shared: {times(shared)}")
    def _(c):
        c.circle(CXA, CY, R, color=A_COL, fill=theme.fill(A_COL, "14"), width=2.5)
        c.circle(CXB, CY, R, color=B_COL, fill=theme.fill(B_COL, "14"), width=2.5)
        c.text(CXA - 50, CY - R - 30, f"primes of {A}", size=15, color=A_COL, weight="bold")
        c.text(CXB + 50, CY - R - 30, f"primes of {B}", size=15, color=B_COL, weight="bold")
        for (x, y), p in zip(spots(mx, len(shared)), shared):
            token(c, x, y, p)

    @wt.step("Put the leftovers outside the overlap", f"{A} has one more 2, and {B} has one more 3. Each goes "
             "in its own circle only.", math=f"{A} = {times(shared)} \\times {times(only_a)},  "
                                             f"{B} = {times(shared)} \\times {times(only_b)}")
    def _(c):
        for (x, y), p in zip(spots(CXA - 60, len(only_a)), only_a):
            token(c, x, y, p, ring=A_COL)
        for (x, y), p in zip(spots(CXB + 60, len(only_b)), only_b):
            token(c, x, y, p, ring=B_COL)

    @wt.step("The overlap is the GCD", "Multiply the primes in the overlap. That is the biggest number that "
             "divides both, so it is the greatest common divisor.", math=f"gcd({A}, {B}) = {times(shared)} = {g}")
    def _(c):
        lens = (f"M{fmt(top[0])},{fmt(top[1])} A{R},{R} 0 0 0 {fmt(bot[0])},{fmt(bot[1])} "
                f"A{R},{R} 0 0 0 {fmt(top[0])},{fmt(top[1])} Z")
        c.path(lens, color=GCD_COL, fill=theme.fill(GCD_COL, "40"), width=3)
        for (x, y), p in zip(spots(mx, len(shared)), shared):
            token(c, x, y, p, ring=GCD_COL)
        box(c, 70, [("GCD: the overlap", 15), (f"{times(shared)} = {g}", 18)], GCD_COL)

    @wt.step("Everything together is the LCM", "Multiply every prime in the picture, each one once. The "
             "result is the smallest number both divide into, the least common multiple.",
             math=f"lcm({A}, {B}) = {times(only_a + shared + only_b)} = {l}")
    def _(c):
        R2 = R + 8
        h2 = math.sqrt(R2 * R2 - (d / 2) ** 2)
        t2, b2 = (mx, CY - h2), (mx, CY + h2)
        union = (f"M{fmt(t2[0])},{fmt(t2[1])} A{R2},{R2} 0 1 0 {fmt(b2[0])},{fmt(b2[1])} "
                 f"A{R2},{R2} 0 1 0 {fmt(t2[0])},{fmt(t2[1])} Z")
        c.path(union, color=LCM_COL, width=3, dash="8 5")
        c.text(mx, CY + R + 28, f"LCM = {l}", size=16, color=LCM_COL, weight="bold", halo=True)
        box(c, 170, [("LCM: the whole picture", 15), (f"{times(only_a + shared + only_b)} = {l}", 18)], LCM_COL)

    @wt.step("Check the shortcut", "The GCD holds the shared primes, and the LCM holds every prime once. "
             "Together they hold the shared primes twice and the rest once, just like 12 × 18. A free check.",
             math=f"{g} \\times {l} = {g * l} = {A} \\times {B}")
    def _(c):
        box(c, 270, [("check", 15), (f"{g} \\times {l} = {g * l}", 18), (f"{A} \\times {B} = {A * B}", 18)],
            theme.INK)

    return wt


@diagram("gcd-lcm-lists", "GCD and LCM by Listing", "Number Theory")
def build_lists() -> Walkthrough:
    A, B = 12, 18
    g, l = math.gcd(A, B), A * B // math.gcd(A, B)
    fa = [d for d in range(1, A + 1) if A % d == 0]
    fb = [d for d in range(1, B + 1) if B % d == 0]
    common = [d for d in fa if d in fb]
    HI = 72
    wt = Walkthrough(
        "gcd-lcm-lists", "GCD and LCM by Listing", "Number Theory",
        concept=f"gcd({A}, {B}) = {g},  lcm({A}, {B}) = {l}",
        summary="List the factors of both numbers and take the biggest one they share. Hop along the "
                "multiples of both numbers and take the first place they meet.",
        width=700, height=420, level="101",
    )
    X0, X1 = 50, 660

    def chips(c, y, xs, col, hl=(), hl_col=None, label=""):
        c.text(X0, y, label, size=15, color=col, anchor="start", weight="bold")
        for i, v in enumerate(xs):
            x = 200 + i * 48
            on = v in hl
            cc = hl_col if on else col
            c.rect(x - 18, y - 15, 36, 30, color=cc, fill=theme.fill(cc, "40" if on else "14"), width=2 if on else 1.2,
                   rx=6)
            c.text(x, y, str(v), size=15, color=cc, weight="bold" if on else None)

    def chip_x(xs, v):
        return 200 + xs.index(v) * 48

    @wt.step("List the factors of each number", f"{A} has {len(fa)} factors and {B} has {len(fb)}. "
             "Write them in order, small to big.",
             math=f"{A}: {', '.join(map(str, fa))};  {B}: {', '.join(map(str, fb))}")
    def _(c):
        chips(c, 50, fa, A_COL, label=f"factors of {A}")
        chips(c, 100, fb, B_COL, label=f"factors of {B}")
        pairs = lambda n: ", ".join(f"{d}×{n // d}" for d in range(1, n + 1) if n % d == 0 and d * d <= n)
        c.text(500, 50, f"pairs: {pairs(A)}", size=12, color=A_COL, anchor="start")
        c.text(500, 100, f"pairs: {pairs(B)}", size=12, color=B_COL, anchor="start")

    @wt.step("Find the shared factors, take the biggest", "Both lists contain 1, 2, 3, and 6. The biggest "
             f"shared factor is {g}, the GCD.", math=f"common: {', '.join(map(str, common))}  \\implies  gcd = {g}")
    def _(c):
        chips(c, 50, fa, A_COL, hl=common, hl_col=GCD_COL, label=f"factors of {A}")
        chips(c, 100, fb, B_COL, hl=common, hl_col=GCD_COL, label=f"factors of {B}")
        for v in common:
            c.line(chip_x(fa, v), 66, chip_x(fb, v), 84, color=GCD_COL, width=1.5)
        x = chip_x(fb, g) + 60
        c.label_box(560, 75, f"GCD = {g}", color=GCD_COL, border=GCD_COL, size=16)

    Y_A, Y_B = 220, 330

    @wt.step(f"Hop by {A} and by {B}", f"Now look at multiples. One frog hops {A} at a time, another hops {B} "
             "at a time, both starting at 0.",
             math=f"{A}, {2 * A}, {3 * A}, {4 * A}, {5 * A}, {6 * A};  {B}, {2 * B}, {3 * B}, {4 * B}")
    def _(c):
        for y, step, col in ((Y_A, A, A_COL), (Y_B, B, B_COL)):
            X = number_line(c, X0 + 50, y, X1 - 20, 0, HI, step=6, label_every=1, size=11, color=theme.SOFT_INK)
            c.text(X0 - 6, y - 40, f"multiples of {step}", size=14, color=col, anchor="start", weight="bold")
            k = 0
            while (k + 1) * step <= HI:
                a, b = X(k * step), X((k + 1) * step)
                h = 30
                d = f"M{fmt(a)},{fmt(y)} C{fmt(a)},{fmt(y - h * 1.3)} {fmt(b)},{fmt(y - h * 1.3)} {fmt(b)},{fmt(y - 2)}"
                c.path(d, color=col, width=2.2, marker_end=c.marker(col))
                c.dot(b, y, r=5, color=col)
                k += 1

    @wt.step("The first meeting point is the LCM", f"Both frogs land on {l} first. That is the smallest "
             f"common multiple. They meet again at {2 * l}, and every {l} after that.",
             math=f"lcm({A}, {B}) = {l}")
    def _(c):
        X = lambda v: X0 + 50 + v / HI * (X1 - 20 - X0 - 50)
        c.line(X(l), Y_A - 50, X(l), Y_B + 30, color=LCM_COL, width=2.5, dash="6 4")
        c.label_box(X(l), Y_B + 52, f"LCM = {l}", color=LCM_COL, border=LCM_COL, size=16)
        c.line(X(2 * l), Y_A - 50, X(2 * l), Y_B + 30, color=LCM_COL, width=1.5, dash="3 4")
        c.text(X(2 * l), Y_B + 52, f"{2 * l} = 2 × {l}", size=13, color=LCM_COL, halo=True)

    return wt


@diagram("euclidean-algorithm", "Euclidean Algorithm with Squares", "Number Theory")
def build_euclid() -> Walkthrough:
    W0, H0 = 48, 18
    # Run the algorithm on a rectangle: cut the biggest squares, then repeat on the leftover strip.
    stages = []  # (side, count, list of square origins in units, leftover rect)
    x, y, w, h = 0, 0, W0, H0
    while w and h:
        s = min(w, h)
        n = max(w, h) // s
        squares = []
        for i in range(n):
            squares.append((x + i * s, y) if w >= h else (x, y + i * s))
        if w >= h:
            x, w = x + n * s, w - n * s
        else:
            y, h = y + n * s, h - n * s
        stages.append((s, n, squares, (x, y, w, h)))
    g = stages[-1][0]
    assert g == math.gcd(W0, H0)
    eqs = []
    a, b = W0, H0
    while b:
        eqs.append((a, a // b, b, a % b))
        a, b = b, a % b

    COLS = [theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE]
    wt = Walkthrough(
        "euclidean-algorithm", "Euclidean Algorithm with Squares", "Number Theory",
        concept=f"gcd({W0}, {H0}) = gcd({H0}, {W0 % H0}) = \\ldots = {g}",
        summary="Cut the biggest possible squares off a rectangle, then repeat on the leftover strip. "
                "The last square size that fits exactly is the GCD of the two sides.",
        width=680, height=420, level="101",
    )
    U = 12  # px per unit
    LX, TY = 52, 52

    def R(ux, uy, uw, uh):
        return LX + ux * U, TY + uy * U, uw * U, uh * U

    @wt.setup
    def _(c):
        c.rect(*R(0, 0, W0, H0), color=theme.INK, width=2.5)
        c.text(LX + W0 * U / 2, TY - 18, str(W0), size=16, weight="bold")
        c.text(LX - 16, TY + H0 * U / 2, str(H0), size=16, weight="bold")
        return None

    def eq_line(c, i):
        a, q, b, r = eqs[i]
        col = COLS[i]
        y = TY + H0 * U + 50 + i * 34
        c.math(LX, y, f"{a} = {q} \\times {b} + {r}", anchor="start", color=col, size=19)
        note = f"{q} square{'s' if q > 1 else ''} of side {b}, " + (f"{r} left over" if r else "nothing left over")
        c.text(LX + 210, y, note, size=14, anchor="start", color=theme.SOFT_INK)

    def draw_stage(c, i):
        s, n, squares, rest = stages[i]
        col = COLS[i]
        for (ux, uy) in squares:
            c.rect(*R(ux, uy, s, s), color=col, fill=theme.fill(col, "33"), width=2.5)
            cx, cy = LX + (ux + s / 2) * U, TY + (uy + s / 2) * U
            c.text(cx, cy, f"{s} × {s}" if s * U >= 60 else str(s), size=15 if s * U >= 60 else 13, color=col,
                   weight="bold", halo=True)
        rx, ry, rw, rh = rest
        if rw and rh and c.is_new:
            c.rect(*R(rx, ry, rw, rh), color=theme.RED, fill=theme.fill(theme.RED, "14"), width=2, dash="6 4")
            mx, my = LX + (rx + rw / 2) * U, TY + (ry + rh / 2) * U
            c.text(mx, my - 9, f"{rw} × {rh}", size=14, color=theme.RED, weight="bold", halo=True)
            c.text(mx, my + 9, "leftover", size=12, color=theme.RED, halo=True)
        eq_line(c, i)

    @wt.step("The puzzle", f"Find the biggest square tile that covers a {W0} × {H0} rectangle with no gaps "
             "and no cutting. Its side must divide both 48 and 18.", math=f"gcd({W0}, {H0}) = ?")
    def _(c):
        if c.is_new:
            c.text(LX + W0 * U / 2, TY + H0 * U / 2, "?", size=48, color=theme.MUTED)
            y = TY + H0 * U + 50
            c.text(LX, y, f"area: {W0} × {H0} = {W0 * H0} square units", size=15, anchor="start")
            c.text(LX, y + 30, f"1 × 1 tiles work ({W0 * H0} of them), but that is a lot of grout. Go bigger.",
                   size=14, anchor="start", color=theme.SOFT_INK)

    titles = [
        "Cut the biggest squares",
        "Repeat on the leftover strip",
        "Stop when nothing is left",
    ]
    texts = [
        f"Squares of side {H0} are the biggest that fit. Two fit, and a {stages[0][3][2]} × {stages[0][3][3]} "
        "strip is left over. Any tile that covers the rectangle also covers that strip.",
        f"The strip is {stages[0][3][2]} wide, so cut squares of side {stages[1][0]}. One fits and a "
        f"{stages[1][3][2]} × {stages[1][3][3]} strip is left over.",
        f"Two squares of side {g} fill the last strip exactly. No leftover, so the algorithm stops.",
    ]
    for i in range(len(stages)):
        a, q, b, r = eqs[i]
        wt.step(titles[i], texts[i], math=f"{a} = {q} \\times {b} + {r}")(
            (lambda i: lambda c: draw_stage(c, i))(i))

    @wt.step(f"Squares of side {g} tile everything", f"Every square in the picture is a whole number of "
             f"{g} × {g} tiles, so {g} × {g} tiles cover the whole rectangle: {W0 // g} across and {H0 // g} down. "
             f"No bigger tile works, so the GCD is {g}.",
             math=f"gcd({W0}, {H0}) = {g},  {W0 // g} \\times {H0 // g} = {(W0 // g) * (H0 // g)} tiles")
    def _(c):
        col = COLS[len(stages) - 1]
        for k in range(1, W0 // g):
            c.line(LX + k * g * U, TY, LX + k * g * U, TY + H0 * U, color=col, width=1, dash="3 3")
        for k in range(1, H0 // g):
            c.line(LX, TY + k * g * U, LX + W0 * U, TY + k * g * U, color=col, width=1, dash="3 3")
        for i, (s, n, squares, rest) in enumerate(stages):
            for (ux, uy) in squares:
                c.text(LX + (ux + s / 2) * U, TY + (uy + s / 2) * U, f"{s} × {s}", size=15,
                       color=COLS[i], weight="bold", halo=True)
        c.label_box(LX + W0 * U - 50, TY + H0 * U + 118, f"GCD = {g}", color=col, border=col, size=18)

    return wt
