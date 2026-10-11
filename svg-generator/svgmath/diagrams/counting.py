"""Counting: Pascal's triangle, grid paths, permutations and combinations, the pigeonhole principle,
and counting trees."""

from __future__ import annotations

import math
from itertools import combinations, permutations

from .. import theme
from ..annotate import brace
from ..registry import diagram
from ..walkthrough import Walkthrough


def pascal_rows(n: int) -> list:
    rows = [[1]]
    for _ in range(n):
        prev = rows[-1]
        rows.append([1] + [prev[i] + prev[i + 1] for i in range(len(prev) - 1)] + [1])
    return rows


@diagram("pascals-triangle", "Pascal's Triangle", "Discrete Math")
def build_pascal() -> Walkthrough:
    NR = 6
    rows = pascal_rows(NR)
    for n, r in enumerate(rows):
        assert r == [math.comb(n, k) for k in range(n + 1)]
    wt = Walkthrough(
        "pascals-triangle", "Pascal's Triangle", "Discrete Math",
        concept="C(n, k) = C(n-1, k-1) + C(n-1, k),  row n sums to 2^n",
        summary="Each entry is the sum of the two entries above it. Row n adds up to 2^n, and entry k in row n "
                "counts the ways to choose k things from n.",
        width=700, height=420, level="301",
    )
    CX, Y0, DY, DX, R = 300, 34, 48, 58, 18
    SUM_X = 600
    EDGE, INNER = theme.BLUE, theme.INK
    EX_N, EX_K = 5, 2  # worked example entry
    SUM_COL, C_COL, EX_COL = theme.ORANGE, theme.PURPLE, theme.GREEN

    def pos(n, k):
        return CX + (k - n / 2) * DX, Y0 + n * DY

    def entry(c, n, k, color=None, ring=None):
        x, y = pos(n, k)
        v = rows[n][k]
        col = color or (EDGE if k in (0, n) else INNER)
        c.circle(x, y, R, color=ring or theme.MUTED, fill=theme.PAPER, width=2.5 if ring else 1.2)
        c.text(x, y, str(v), size=16, color=col, weight="bold" if k in (0, n) or color else None)

    def row_label(c, n):
        c.text(40, Y0 + n * DY, f"row {n}", size=13, color=theme.SOFT_INK, anchor="start")

    def adds(c, n, k, color=theme.SOFT_INK, width=1.5):
        """Arrows from the two parents of (n, k) into it."""
        x, y = pos(n, k)
        for kk in (k - 1, k):
            px, py = pos(n - 1, kk)
            dx, dy = x - px, y - py
            L = math.hypot(dx, dy)
            c.arrow(px + dx / L * R, py + dy / L * R, x - dx / L * (R + 2), y - dy / L * (R + 2), color=color,
                    width=width)

    @wt.step("Start with ones", "Row 0 is a single 1. Every row starts and ends with 1, so the edges of the "
             "triangle are all ones.", math="row 0: 1,  row 1: 1  1")
    def _(c):
        for n in range(2):
            row_label(c, n)
            for k in range(n + 1):
                entry(c, n, k)

    @wt.step("Add the two numbers above", "Each inside entry is the sum of the two entries just above it. "
             "Row 2 gets 1 + 1 = 2 in the middle.", math="1 + 1 = 2")
    def _(c):
        row_label(c, 2)
        for k in range(3):
            entry(c, 2, k)
        adds(c, 2, 1, color=EX_COL, width=2)

    @wt.step("Keep building rows", f"Rows 3 to {NR} follow the same rule. For example, "
             f"{rows[EX_N - 1][EX_K - 1]} + {rows[EX_N - 1][EX_K]} = {rows[EX_N][EX_K]} in row {EX_N}. "
             "Two rules, endless rows.",
             math=f"{rows[EX_N - 1][EX_K - 1]} + {rows[EX_N - 1][EX_K]} = {rows[EX_N][EX_K]}")
    def _(c):
        for n in range(3, NR + 1):
            row_label(c, n)
            for k in range(n + 1):
                entry(c, n, k, color=EX_COL if (n, k) == (EX_N, EX_K) else None,
                      ring=EX_COL if (n, k) == (EX_N, EX_K) else None)
        adds(c, EX_N, EX_K, color=EX_COL, width=2)

    @wt.step("Each row sums to a power of 2", "Add up each row: 1, 2, 4, 8, 16, 32, 64. Every entry is "
             "used twice to build the next row, so each row sum doubles.",
             math=f"row n sum = 2^n,  row {NR}: {' + '.join(map(str, rows[NR]))} = {2 ** NR}")
    def _(c):
        c.text(SUM_X, Y0 - 22, "row sum", size=13, color=SUM_COL, weight="bold")
        for n in range(NR + 1):
            s = sum(rows[n])
            assert s == 2 ** n
            c.math(SUM_X, Y0 + n * DY, f"{s} = 2^{n}", size=17, color=SUM_COL)

    @wt.step("Entries count choices", f"Entry k in row n is C(n, k), the number of ways to choose k things from n. "
             f"The circled {rows[EX_N][EX_K]} says there are {rows[EX_N][EX_K]} ways to pick {EX_K} toppings from "
             f"{EX_N}. Count k from 0 at the left edge.",
             math=f"C({EX_N}, {EX_K}) = {EX_N}!/({EX_K}! \\cdot {EX_N - EX_K}!) = {rows[EX_N][EX_K]}")
    def _(c):
        for k in range(EX_N + 1):
            x, y = pos(EX_N, k)
            c.text(x, y + R + 9, f"k={k}", size=10, color=C_COL, halo=True)
        x, y = pos(EX_N, EX_K)
        c.rect(400, Y0 - 16, 150, 64, color=C_COL, fill=theme.fill(C_COL, "14"), width=1.5, rx=8)
        c.text(475, Y0 + 2, f"circled {rows[EX_N][EX_K]} in row {EX_N}:", size=13, color=C_COL)
        c.math(475, Y0 + 28, f"C({EX_N}, {EX_K}) = {rows[EX_N][EX_K]}", size=18, color=C_COL)
        bottom = Y0 + NR * DY + 40
        c.text(CX, bottom, f"row {EX_N}: " + ",  ".join(f"C({EX_N},{k})" for k in range(EX_N + 1))
               + " = " + ", ".join(map(str, rows[EX_N])), size=14, color=C_COL)

    return wt


@diagram("pascals-grid-paths", "Pascal's Triangle as Grid Paths", "Discrete Math")
def build_paths() -> Walkthrough:
    RIGHT, DOWN = 3, 2
    total = math.comb(RIGHT + DOWN, DOWN)
    wt = Walkthrough(
        "pascals-grid-paths", "Pascal's Triangle as Grid Paths", "Discrete Math",
        concept=f"paths to a corner = paths from the left + paths from above;  C({RIGHT + DOWN}, {DOWN}) = {total}",
        summary="Count the shortest paths across a grid that only move right or down. The count at each corner is "
                "the sum of the counts from the left and from above, which builds Pascal's triangle.",
        width=680, height=400, level="301",
    )
    S, X0, Y0 = 118, 70, 80
    PATH_COLS = [theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE, theme.RED, theme.SKY,
                 theme.SOFT_INK, theme.BLUE, theme.ORANGE, theme.GREEN]

    counts = [[0] * (RIGHT + 1) for _ in range(DOWN + 1)]
    for r in range(DOWN + 1):
        for k in range(RIGHT + 1):
            counts[r][k] = 1 if r == 0 or k == 0 else counts[r - 1][k] + counts[r][k - 1]
    assert counts[DOWN][RIGHT] == total

    def P(k, r):
        return X0 + k * S, Y0 + r * S

    @wt.setup
    def _(c):
        for r in range(DOWN + 1):
            c.line(*P(0, r), *P(RIGHT, r), color=theme.MUTED, width=2)
        for k in range(RIGHT + 1):
            c.line(*P(k, 0), *P(k, DOWN), color=theme.MUTED, width=2)
        c.text(*(lambda p: (p[0] - 10, p[1] - 22))(P(0, 0)), "start", size=13, color=theme.SOFT_INK, anchor="end")
        c.text(P(RIGHT, DOWN)[0] + 14, P(RIGHT, DOWN)[1] + 24, "end", size=13, color=theme.SOFT_INK, anchor="start")
        return None

    def badge(c, k, r, color=theme.INK):
        x, y = P(k, r)
        c.circle(x, y, 16, color=color, fill=theme.PAPER, width=2)
        c.text(x, y, str(counts[r][k]), size=15, weight="bold", color=color)

    @wt.step("Move only right or down", f"Walk from the top-left corner to the bottom-right corner, one block at "
             f"a time, only right or down. Every such path takes {RIGHT} rights and {DOWN} downs.",
             math=f"path = {RIGHT} R and {DOWN} D in some order")
    def _(c):
        pts = [P(0, 0), P(1, 0), P(1, 1), P(2, 1), P(3, 1), P(3, 2)]
        c.polyline(pts, color=theme.BLUE, width=5, opacity=0.8)
        if c.is_new:
            for i, ((xa, ya), (xb, yb)) in enumerate(zip(pts, pts[1:])):
                horiz = ya == yb
                c.text((xa + xb) / 2 + (0 if horiz else 10), (ya + yb) / 2 + (-16 if horiz else 0),
                       f"{i + 1}: {'R' if horiz else 'D'}", size=14, color=theme.BLUE, weight="bold", halo=True,
                       anchor="middle" if horiz else "start")
        c.text(490, 60, "one path: R D R R D", size=15, color=theme.BLUE, anchor="start", weight="bold")
        c.dot(*P(0, 0), r=7, color=theme.INK)
        c.dot(*P(RIGHT, DOWN), r=7, color=theme.INK)

    @wt.step("Edges have exactly one path", "Corners on the top edge or the left edge can be reached one way only: "
             "straight along the edge. Write 1 at each.", math="top edge and left edge: 1")
    def _(c):
        for k in range(RIGHT + 1):
            badge(c, k, 0, theme.BLUE)
        for r in range(1, DOWN + 1):
            badge(c, 0, r, theme.BLUE)

    @wt.step("Add from the left and from above", "Any path into an inside corner arrives from the left or from "
             "above, never both. So add those two counts, the same rule as Pascal's triangle.",
             math=f"{counts[1][0]} + {counts[0][1]} = {counts[1][1]},  {counts[1][1]} + {counts[0][2]} = "
                  f"{counts[1][2]},  \\ldots")
    def _(c):
        for r in range(1, DOWN + 1):
            for k in range(1, RIGHT + 1):
                x, y = P(k, r)
                c.arrow(x - S + 18, y, x - 20, y, color=theme.ORANGE, width=1.6)
                c.arrow(x, y - S + 18, x, y - 20, color=theme.GREEN, width=1.6)
                badge(c, k, r, theme.INK if (k, r) != (RIGHT, DOWN) else theme.PURPLE)
        c.text(490, 100, "orange: from the left", size=13, color=theme.ORANGE, anchor="start")
        c.text(490, 122, "green: from above", size=13, color=theme.GREEN, anchor="start")

    @wt.step("Read the answer as C(n, k)", f"The far corner shows {total}. A path is {RIGHT + DOWN} moves, and "
             f"choosing which {DOWN} are downs fixes it, so the count is C({RIGHT + DOWN}, {DOWN}). Read the badges "
             "along each diagonal and you get pieces of the rows of Pascal's triangle.",
             math=f"C({RIGHT + DOWN}, {DOWN}) = {total}")
    def _(c):
        diags = [[counts[r][d - r] for r in range(DOWN + 1) if 0 <= d - r <= RIGHT] for d in range(RIGHT + DOWN + 1)]
        c.rect(480, 160, 180, 40 + 22 * len(diags), color=theme.PURPLE, fill=theme.fill(theme.PURPLE, "14"),
               width=1.5, rx=8)
        c.text(570, 180, "diagonals = Pascal rows", size=13, color=theme.PURPLE)
        for i, row in enumerate(diags):
            c.text(570, 206 + i * 22, " ".join(map(str, row)), size=15, color=theme.PURPLE, weight="bold")
        x, y = P(RIGHT, DOWN)
        c.circle(x, y, 24, color=theme.PURPLE, width=3)

    return wt


@diagram("permutations-combinations", "Permutations and Combinations", "Discrete Math")
def build_perm() -> Walkthrough:
    letters = "ABCDE"
    n, r = len(letters), 3
    nPr = math.perm(n, r)
    nCr = math.comb(n, r)
    pick = ["C", "A", "E"]
    group = sorted(pick)
    orders = ["".join(p) for p in permutations(group)]
    combos = ["".join(cmb) for cmb in combinations(letters, r)]
    assert len(orders) == math.factorial(r) and len(combos) == nCr == nPr // math.factorial(r)
    wt = Walkthrough(
        "permutations-combinations", "Permutations and Combinations", "Discrete Math",
        concept=f"P({n}, {r}) = {n} \\times {n - 1} \\times {n - 2} = {nPr},  C({n}, {r}) = {nPr}/{r}! = {nCr}",
        summary="Filling ordered slots multiplies the choices left at each slot. When order does not matter, divide "
                "by the number of ways to arrange the chosen items.",
        width=700, height=440, level="301",
    )
    TOK_Y, SLOT_Y = 46, 150
    SLOT_X = [200, 320, 440]
    COLS = [theme.BLUE, theme.ORANGE, theme.GREEN]
    ORD_COL, GRP_COL = theme.RED, theme.PURPLE

    def tok_x(i):
        return 170 + i * 70

    @wt.setup
    def _(c):
        c.text(40, TOK_Y, "pool", size=13, color=theme.SOFT_INK, anchor="start")
        for i, L in enumerate(letters):
            c.circle(tok_x(i), TOK_Y, 20, color=theme.INK, fill=theme.PAPER, width=2)
            c.text(tok_x(i), TOK_Y, L, size=18, weight="bold")
        for j, x in enumerate(SLOT_X):
            c.text(x, SLOT_Y - 42, ["1st", "2nd", "3rd"][j], size=13, color=theme.SOFT_INK)
            c.rect(x - 32, SLOT_Y - 28, 64, 56, color=theme.INK, fill=theme.PAPER, width=2, rx=6)
        return None

    def use(c, j):
        L = pick[j]
        i = letters.index(L)
        col = COLS[j]
        c.circle(tok_x(i), TOK_Y, 20, color=theme.MUTED, fill=theme.PANEL, width=2, dash="4 3")
        c.text(tok_x(i), TOK_Y, L, size=18, color=theme.MUTED)
        c.text(SLOT_X[j], SLOT_Y, L, size=26, weight="bold", color=col)
        c.text(SLOT_X[j], SLOT_Y + 46, f"{n - j} choices", size=15, color=col, weight="bold")
        if j:
            c.text((SLOT_X[j - 1] + SLOT_X[j]) / 2, SLOT_Y + 46, "×", size=18, color=theme.SOFT_INK)

    @wt.step("Five letters, three ordered slots", "Pick 3 of the letters A to E and line them up in slots. "
             "Here ABC and CAB count as different, like a podium.", math=f"{n} letters, {r} slots, order matters")
    def _(c):
        c.text(560, SLOT_Y, "gold, silver, bronze", size=13, color=theme.SOFT_INK)

    @wt.step("The first slot has 5 choices", "Any of the five letters can go first. Say C goes first, so it leaves "
             "the pool.", math=f"slot 1: {n} choices")
    def _(c):
        use(c, 0)

    @wt.step("Each slot has one fewer choice", f"Four letters remain for slot 2 and three for slot 3. Multiply: "
             f"{n} × {n - 1} × {n - 2} = {nPr} ordered lineups.",
             math=f"P({n}, {r}) = {n} \\times {n - 1} \\times {n - 2} = {nPr}")
    def _(c):
        use(c, 1)
        use(c, 2)
        c.text(SLOT_X[2] + 60, SLOT_Y + 46, f"= {nPr} lineups", size=16, color=ORD_COL, weight="bold",
               anchor="start")

    LOW = 300

    @wt.step("One group hides 3! lineups", f"The group {{A, C, E}} shows up in {len(orders)} of those lineups, "
             f"one for each way to order three letters: 3 × 2 × 1 = {len(orders)}.",
             math=f"{r}! = {math.factorial(r)} orders of A, C, E")
    def _(c):
        c.line(20, LOW - 40, 680, LOW - 40, color=theme.GRID, width=1.5)
        c.text(40, LOW - 18, "lineups of one group", size=13, color=ORD_COL, anchor="start", weight="bold")
        for i, w in enumerate(orders):
            x = 70 + (i % 3) * 82
            y = LOW + 14 + (i // 3) * 44
            c.rect(x - 32, y - 16, 64, 32, color=ORD_COL, fill=theme.fill(ORD_COL, "18"), width=1.5, rx=6)
            c.text(x, y, w, size=16, color=ORD_COL, weight="bold")
        brace(c, 70 + 2 * 82 + 32, LOW + 80, 70 - 32, LOW + 80, f"{len(orders)} lineups = 1 group",
              color=GRP_COL, math_label=False, size=14)

    @wt.step("Divide to count groups", f"Each group got counted {len(orders)} times, so divide: {nPr} ÷ "
             f"{len(orders)} = {nCr} groups. Listing them all proves it, if you trust nobody.",
             math=f"C({n}, {r}) = P({n}, {r}) / {r}! = {nPr}/{math.factorial(r)} = {nCr}")
    def _(c):
        c.text(370, LOW - 18, f"all {nCr} groups (order ignored)", size=13, color=GRP_COL, anchor="start",
               weight="bold")
        for i, w in enumerate(combos):
            x = 400 + (i % 5) * 58
            y = LOW + 14 + (i // 5) * 44
            on = w == "".join(group)
            c.rect(x - 25, y - 16, 50, 32, color=GRP_COL, fill=theme.fill(GRP_COL, "40" if on else "14"),
                   width=2.5 if on else 1.2, rx=6)
            c.text(x, y, w, size=15, color=GRP_COL, weight="bold" if on else None)
        c.arrow(300, LOW + 36, 362, LOW + 36, color=GRP_COL, width=2)
        c.text(331, LOW + 18, f"÷ {len(orders)}", size=14, color=GRP_COL, weight="bold")

    return wt


@diagram("pigeonhole", "Pigeonhole Principle", "Discrete Math")
def build_pigeon() -> Walkthrough:
    HOLES, BIRDS = 9, 10
    wt = Walkthrough(
        "pigeonhole", "Pigeonhole Principle", "Discrete Math",
        concept="n + 1 items in n boxes  \\implies  some box holds at least 2",
        summary="If there are more items than boxes, some box must hold two or more. "
                "With N items in k boxes, some box holds at least ⌈N/k⌉.",
        width=680, height=360, level="301",
    )
    BW, GAP, X0, BY, BH = 58, 12, 25, 170, 96
    DOT_R = 13
    BIRD, EXTRA = theme.BLUE, theme.RED
    DOUBLE = 3  # the hole that gets the extra pigeon (0-based)

    def hole_x(i, w=BW, gap=GAP, x0=X0):
        return x0 + i * (w + gap)

    def holes(c, n, w, gap, x0, labels):
        for i in range(n):
            x = hole_x(i, w, gap, x0)
            c.path(f"M{x},{BY} L{x},{BY + BH} L{x + w},{BY + BH} L{x + w},{BY}", color=theme.INK, width=2.2)
            c.text(x + w / 2, BY + BH + 18, labels[i], size=13, color=theme.SOFT_INK)

    def bird(c, x, y, label, color):
        c.circle(x, y, DOT_R, color=color, fill=theme.fill(color, "40"), width=2)
        c.text(x, y, label, size=12, weight="bold", color=color)

    def in_hole(i, k, w=BW, gap=GAP, x0=X0):
        return hole_x(i, w, gap, x0) + w / 2, BY + BH - 18 - k * 28

    def counts_row(c, vals, w=BW, gap=GAP, x0=X0, hl=None):
        for i, v in enumerate(vals):
            col = EXTRA if i == hl else theme.SOFT_INK
            c.text(hole_x(i, w, gap, x0) + w / 2, BY - 22, str(v), size=15, color=col,
                   weight="bold" if i == hl else None)

    def wait_x(i):
        return 70 + i * 54

    @wt.step(f"{BIRDS} pigeons, {HOLES} holes", f"There are {BIRDS} pigeons and only {HOLES} holes. Every pigeon "
             "needs a hole. No pigeon gets a vote.", math=f"{BIRDS} > {HOLES}")
    def _(c):
        holes(c, HOLES, BW, GAP, X0, [str(i + 1) for i in range(HOLES)])
        for i in range(BIRDS):
            bird(c, wait_x(i), 60, str(i + 1), BIRD)
        c.text(wait_x(0) - 22, 30, "waiting", size=13, color=theme.SOFT_INK, anchor="start")

    @wt.step("Spread them out", f"Give each hole one pigeon, the fairest way. That uses {HOLES} pigeons, and "
             "every hole is now full of exactly one.", math=f"{HOLES} pigeons placed, 1 per hole")
    def _(c):
        for i in range(HOLES):
            c.circle(wait_x(i), 60, DOT_R, color=theme.MUTED, fill=theme.PAPER, width=1.5, dash="3 3")
            bird(c, *in_hole(i, 0), str(i + 1), BIRD)
        if c.is_new:
            counts_row(c, [1] * HOLES)

    @wt.step("The last pigeon has to double up", f"Pigeon {BIRDS} still needs a hole, and every hole is taken. "
             "Wherever it goes, that hole holds 2. No clever plan avoids it.",
             math=f"{BIRDS} pigeons in {HOLES} holes  \\implies  some hole has \\geq 2")
    def _(c):
        c.circle(wait_x(BIRDS - 1), 60, DOT_R, color=theme.MUTED, fill=theme.PAPER, width=1.5, dash="3 3")
        x, y = in_hole(DOUBLE, 1)
        bird(c, x, y, str(BIRDS), EXTRA)
        c.curved_arrow(wait_x(BIRDS - 1) - 8, 78, x + 18, y - 14, bend=-0.2, color=EXTRA, width=2)
        hx = hole_x(DOUBLE)
        c.rect(hx - 4, BY - 6, BW + 8, BH + 10, color=EXTRA, width=2.5, dash="6 4", rx=6)
        c.text(hx + BW / 2, BY + BH + 40, "2 here!", size=15, color=EXTRA, weight="bold")
        counts_row(c, [2 if i == DOUBLE else 1 for i in range(HOLES)], hl=DOUBLE)

    MW, MG, MX0 = 46, 8, 20
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    @wt.step("Birthdays: 13 people, 12 months", "Months are holes and people are pigeons. With 13 people, at "
             "least two share a birth month, no matter who shows up.",
             math="13 people > 12 months  \\implies  shared month", fresh=True)
    def _(c):
        holes(c, 12, MW, MG, MX0, months)
        for i in range(12):
            bird(c, *in_hole(i, 0, MW, MG, MX0), "", theme.BLUE)
        x, y = in_hole(2, 1, MW, MG, MX0)
        bird(c, x, y, "13", EXTRA)
        c.text(340, 60, "12 people fill 12 months; person 13 must share", size=15, color=theme.INK)
        counts_row(c, [2 if i == 2 else 1 for i in range(12)], MW, MG, MX0, hl=2)
        c.text(340, BY - 50, "people per month", size=13, color=theme.SOFT_INK)

    N2 = 25
    need = -(-N2 // 12)

    @wt.step("More pigeons, bigger piles", f"With {N2} people and 12 months, fill each month with 2 first. That "
             f"is only 24, so person {N2} makes a 3. Some month always has at least ⌈{N2}/12⌉ = {need}.",
             math=f"\\lceil {N2}/12 \\rceil = {need}".replace("\\lceil ", "⌈").replace(" \\rceil", "⌉"),
             fresh=True)
    def _(c):
        holes(c, 12, MW, MG, MX0, months)
        for i in range(12):
            for k in range(2):
                bird(c, *in_hole(i, k, MW, MG, MX0), "", theme.BLUE)
        x, y = in_hole(6, 2, MW, MG, MX0)
        bird(c, x, y, str(N2), EXTRA)
        c.text(340, 60, f"{N2} people: 2 per month uses 24, one left over", size=15, color=theme.INK)
        counts_row(c, [3 if i == 6 else 2 for i in range(12)], MW, MG, MX0, hl=6)
        c.text(340, BY - 50, "people per month", size=13, color=theme.SOFT_INK)

    return wt


@diagram("counting-tree", "Counting Tree", "Discrete Math")
def build_tree() -> Walkthrough:
    shirts = [("red", theme.RED), ("blue", theme.BLUE), ("green", theme.GREEN)]
    pants = ["jeans", "khakis"]
    shoes = ["sneakers", "boots"]
    total = len(shirts) * len(pants) * len(shoes)
    wt = Walkthrough(
        "counting-tree", "Counting Tree", "Discrete Math",
        concept=f"{len(shirts)} \\times {len(pants)} \\times {len(shoes)} = {total} outfits",
        summary="Draw one branch for each choice at each stage. The number of leaves is the product of the "
                "number of choices, which is the multiplication principle.",
        width=700, height=450, level="101",
    )
    X_ROOT, X_SHIRT, X_PANTS, X_SHOES, X_NUM = 50, 170, 320, 470, 560
    TOP, LEAF_DY = 64, 31.5
    HEAD_Y = 22
    FOOT_Y = 436

    def leaf_y(i):
        return TOP + i * LEAF_DY

    def mid(i0, n):
        return (leaf_y(i0) + leaf_y(i0 + n - 1)) / 2

    ROOT_Y = mid(0, total)
    per_shirt = len(pants) * len(shoes)

    def pill(c, x, y, text, color, filled=False, w=None):
        w = w or (len(text) * 8 + 18)
        c.rect(x - w / 2, y - 12, w, 24, color=color, fill=theme.fill(color, "40") if filled else theme.PAPER,
               width=1.8, rx=12)
        c.text(x, y, text, size=13, color=color if not filled else theme.INK, weight="bold")
        return w

    def branch(c, x1, y1, x2, y2, color, w1=0, w2=0):
        c.line(x1 + w1 / 2, y1, x2 - w2 / 2 - 2, y2, color=color, width=2)

    @wt.setup
    def _(c):
        c.circle(X_ROOT, ROOT_Y, 8, color=theme.INK, fill=theme.INK)
        c.text(X_ROOT, ROOT_Y + 22, "start", size=12, color=theme.SOFT_INK)
        return None

    @wt.step(f"Pick a shirt: {len(shirts)} branches", "Each shirt is one branch out of the start. Shirt color "
             "also colors every branch that follows it, so you can trace any outfit back.",
             math=f"{len(shirts)} shirts")
    def _(c):
        c.text(X_SHIRT, HEAD_Y, f"shirt ({len(shirts)})", size=14, weight="bold")
        c.text(X_SHIRT, FOOT_Y, f"{len(shirts)} branches", size=13, color=theme.SOFT_INK)
        for s, (name, col) in enumerate(shirts):
            y = mid(s * per_shirt, per_shirt)
            branch(c, X_ROOT + 8, ROOT_Y, X_SHIRT, y, col, w2=60)
            pill(c, X_SHIRT, y, name, col, filled=True, w=60)

    @wt.step(f"Each shirt splits {len(pants)} ways", f"Every shirt pairs with either pair of pants, so each "
             f"shirt branch grows {len(pants)} new branches.",
             math=f"{len(shirts)} \\times {len(pants)} = {len(shirts) * len(pants)} pairs of shirt and pants")
    def _(c):
        c.text(X_PANTS, HEAD_Y, f"pants ({len(pants)})", size=14, weight="bold")
        c.text(X_PANTS, FOOT_Y, f"{len(shirts)} × {len(pants)} = {len(shirts) * len(pants)}", size=13,
               color=theme.SOFT_INK)
        for s, (_, col) in enumerate(shirts):
            ys = mid(s * per_shirt, per_shirt)
            for p, pname in enumerate(pants):
                y = mid(s * per_shirt + p * len(shoes), len(shoes))
                branch(c, X_SHIRT, ys, X_PANTS, y, col, w1=60, w2=64)
                pill(c, X_PANTS, y, pname, col, w=64)

    @wt.step(f"Each pair splits {len(shoes)} ways", f"Add shoes. Every shirt-pants pair grows {len(shoes)} more "
             f"branches, so the tree ends in {total} leaves.",
             math=f"{len(shirts)} \\times {len(pants)} \\times {len(shoes)} = {total}")
    def _(c):
        c.text(X_SHOES, HEAD_Y, f"shoes ({len(shoes)})", size=14, weight="bold")
        c.text(X_SHOES, FOOT_Y, f"{len(shirts) * len(pants)} × {len(shoes)} = {total}", size=13,
               color=theme.SOFT_INK)
        for s, (_, col) in enumerate(shirts):
            for p in range(len(pants)):
                yp = mid(s * per_shirt + p * len(shoes), len(shoes))
                for h, hname in enumerate(shoes):
                    y = leaf_y(s * per_shirt + p * len(shoes) + h)
                    branch(c, X_PANTS, yp, X_SHOES, y, col, w1=64, w2=76)
                    pill(c, X_SHOES, y, hname, col, w=76)

    @wt.step("Count the leaves", f"Each leaf is one full outfit, read from left to right. There are {total} "
             "leaves, and multiplying gets there without drawing a single branch.",
             math=f"{len(shirts)} \\times {len(pants)} \\times {len(shoes)} = {total} outfits")
    def _(c):
        for i in range(total):
            s = i // per_shirt
            c.text(X_NUM, leaf_y(i), f"#{i + 1}", size=13, color=shirts[s][1], anchor="start", weight="bold")
        y0, y1 = leaf_y(0) - 10, leaf_y(total - 1) + 10
        brace(c, X_NUM + 40, y0, X_NUM + 40, y1, None, color=theme.INK)
        c.text(X_NUM + 70, (y0 + y1) / 2 - 12, f"{total}", size=26, weight="bold", anchor="start")
        c.text(X_NUM + 70, (y0 + y1) / 2 + 14, "outfits", size=14, anchor="start")

    return wt
