"""Probability diagrams: trees, Bayes with counts, dice grids, Venn diagrams, binomial counts, long-run frequency."""

from __future__ import annotations

import math
import random
from fractions import Fraction
from itertools import product

from .. import theme
from ..annotate import brace, segment_label
from ..plane import Plane
from ..registry import diagram
from ..svg import text_width
from ..walkthrough import Walkthrough


def frac(n, d) -> str:
    return f"{n}/{d}"


def mono_word(c, x, y, word, colors, size=14, weight="bold"):
    """Writes a word letter by letter in a monospace font, each letter in its own color."""
    adv = 0.6 * size
    for i, ch in enumerate(word):
        c.text(x + i * adv, y, ch, size=size, font="mono", anchor="start", color=colors[ch], weight=weight)
    return len(word) * adv


# ---------------------------------------------------------------------------
# Probability tree
# ---------------------------------------------------------------------------

BALL = {"R": theme.RED, "B": theme.BLUE}
BALL_NAME = {"R": "red", "B": "blue"}


def marble(c, x, y, r, key):
    c.circle(x, y, r, color=theme.INK, fill=BALL[key], width=1.2)


@diagram("probability-tree", "Probability Trees", "Probability")
def probability_tree() -> Walkthrough:
    wt = Walkthrough(
        "probability-tree", "Probability Trees", "Probability",
        concept="P(A and B) = P(A) \\cdot P(B | A)",
        summary="Draw one branch for each way a draw can go and write its chance on it. Multiply along a path "
                "to get the chance of that whole path, and add paths that answer the same question.",
        width=700, height=410, level="301",
    )
    bag = {"R": 3, "B": 2}
    total = sum(bag.values())
    root = (180, 200)
    L1 = {"R": (330, 105), "B": (330, 295)}
    L2 = {("R", "R"): (470, 50), ("R", "B"): (470, 155), ("B", "R"): (470, 245), ("B", "B"): (470, 350)}
    NR = 14

    def first(k):
        return bag[k], total

    def second(k1, k2):
        left = dict(bag)
        left[k1] -= 1
        return left[k2], total - 1

    def path_p(k1, k2):
        a, b = first(k1)
        c2, d = second(k1, k2)
        return Fraction(a, b) * Fraction(c2, d), a * c2, b * d

    def edge(c, p0, p1, key, num, den, side, r0=0):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        a = (p0[0] + ux * r0, p0[1] + uy * r0)
        b = (p1[0] - ux * NR, p1[1] - uy * NR)
        c.line(*a, *b, color=BALL[key], width=2.5)
        segment_label(c, a, b, frac(num, den), color=BALL[key], side=side, offset=12, size=16)

    def node(c, p, key):
        c.circle(p[0], p[1], NR, color="none", fill=BALL[key])
        c.text(p[0], p[1], key, size=14, weight="bold", color=theme.PAPER)

    def mini_left(c, xr, y, counts):
        c.text(xr - 4 * 13 - 6, y, "left:", size=12, color=theme.SOFT_INK, anchor="end")
        keys = ["R"] * counts["R"] + ["B"] * counts["B"]
        for i, k in enumerate(keys):
            marble(c, xr - (len(keys) - 1 - i) * 13, y, 5, k)

    @wt.step("Look in the bag", "The bag holds 3 red marbles and 2 blue ones. Draw one, keep it out, then "
             "draw again. Since the first marble stays out, the second draw sees a smaller bag.",
             math=f"P(R) = {frac(bag['R'], total)},  P(B) = {frac(bag['B'], total)}")
    def _(c):
        c.rect(32, 132, 104, 140, color=theme.SOFT_INK, fill=theme.PANEL, rx=26, width=2)
        c.path("M58,134 Q84,112 110,134", color=theme.SOFT_INK, width=2)
        pos = [(58, 172), (84, 172), (110, 172), (71, 214), (97, 214)]
        for (x, y), k in zip(pos, ["R", "R", "R", "B", "B"]):
            marble(c, x, y, 12, k)
        c.text(84, 250, f"{total} marbles", size=13, color=theme.SOFT_INK)
        c.text(84, 296, f"{bag['R']} red: {frac(bag['R'], total)}", size=14, color=theme.RED, weight="bold")
        c.text(84, 316, f"{bag['B']} blue: {frac(bag['B'], total)}", size=14, color=theme.BLUE, weight="bold")

    @wt.step("Branch for the first draw", "One branch per color, labeled with its chance. The two chances "
             "add to 1 because the first marble is surely red or blue.",
             math=f"{frac(bag['R'], total)} + {frac(bag['B'], total)} = 1")
    def _(c):
        c.dot(*root, r=6)
        c.text(root[0], root[1] + 22, "start", size=12, color=theme.SOFT_INK)
        c.text(330, 22, "1st draw", size=13, color=theme.SOFT_INK, weight="bold")
        for k, side in (("R", 1), ("B", -1)):
            edge(c, root, L1[k], k, *first(k), side=side, r0=6)
            node(c, L1[k], k)

    @wt.step("Branch again from what is left", "After a red, the bag has 2 red and 2 blue. After a blue, it "
             "has 3 red and 1 blue. Each set of second-draw chances depends on the first draw.",
             math="P(R second | R first) = 2/4;  P(R second | B first) = 3/4")
    def _(c):
        c.text(470, 22, "2nd draw", size=13, color=theme.SOFT_INK, weight="bold")
        for k1 in "RB":
            left = dict(bag)
            left[k1] -= 1
            y = L1[k1][1] + (-30 if k1 == "R" else 30)
            mini_left(c, 318, y, left)
            for k2 in "RB":
                end = L2[(k1, k2)]
                side = 1 if k2 == "R" else -1
                edge(c, L1[k1], end, k2, *second(k1, k2), side=side, r0=NR)
                node(c, end, k2)

    @wt.step("Multiply along each path", "Follow a path from start to end and multiply its chances. "
             "Over 20 equally likely ordered draws, each path claims its share.",
             math="P(RR) = 3/5 \\times 2/4 = 6/20")
    def _(c):
        for (k1, k2), (x, y) in L2.items():
            a, b = first(k1)
            c2, d = second(k1, k2)
            _p, num, den = path_p(k1, k2)
            xx = x + 26
            w = mono_word(c, xx, y, k1 + k2, BALL, size=16)
            c.math(xx + w + 8, y, f"{frac(a, b)} \\times {frac(c2, d)} = {frac(num, den)}", size=16,
                   anchor="start")

    rb = path_p("R", "B")[0] + path_p("B", "R")[0]
    tot = sum(path_p(a, b)[0] for a, b in L2)

    @wt.step("Add the paths you want", "One of each color happens on two paths, RB and BR. Add them. "
             "All four paths together add to 1, a good check that no marble went missing.",
             math=f"P(one of each) = 6/20 + 6/20 = 12/20 = {rb}")
    def _(c):
        for key in (("R", "B"), ("B", "R")):
            x, y = L2[key]
            c.rect(x + 20, y - 15, 200, 30, color=theme.GREEN, fill="none", width=2.2, rx=6)
        c.text(590, 200, "one of each", size=13, color=theme.GREEN, weight="bold", halo=True)
        c.text(595, 392, f"all four paths: 20/20 = {tot}", size=13, color=theme.SOFT_INK)

    return wt


# ---------------------------------------------------------------------------
# Bayes with natural frequencies
# ---------------------------------------------------------------------------

def _bayes_numbers():
    pop = 1000
    sick = pop * 1 // 100
    tp = sick * 90 // 100
    fn = sick - tp
    healthy = pop - sick
    fp_exact = healthy * 9 / 100
    fp = round(fp_exact)
    tn = healthy - fp
    return dict(pop=pop, sick=sick, tp=tp, fn=fn, healthy=healthy, fp=fp, fp_exact=fp_exact, tn=tn)


@diagram("bayes-natural-frequencies", "Bayes' Theorem with Counts", "Probability")
def bayes_counts() -> Walkthrough:
    N = _bayes_numbers()
    pos = N["tp"] + N["fp"]
    ans = N["tp"] / pos
    wt = Walkthrough(
        "bayes-natural-frequencies", "Bayes' Theorem with Counts", "Probability",
        concept="P(sick | +) = 9/(9 + 89) \\approx 9.2%",
        summary="Turn percentages into people. Out of 1000 people, a test with 90% sensitivity and a 9% "
                "false positive rate flags 98 people, and only 9 of them are sick.",
        width=720, height=450, level="301",
    )
    COLS, ROWS, CELL = 40, 25, 9
    GX, GY = 20, 48
    C_TP, C_FP = theme.RED, theme.PURPLE
    C_FN = theme.fill(theme.RED, "55")
    C_TN = theme.fill(theme.MUTED, "66")

    def kind(i):
        if i < N["tp"]:
            return "tp"
        if i < N["sick"]:
            return "fn"
        if i < N["sick"] + N["fp"]:
            return "fp"
        return "tn"

    def cell(c, i, fill, border=None):
        r, col = divmod(i, COLS)
        c.rect(GX + col * CELL, GY + r * CELL, CELL - 1.5, CELL - 1.5, color=border or "none", fill=fill,
               width=1)

    def tnode(c, x, y, num, word, color, swatch=None, swatch_border=None):
        c.text(x, y - 7, num, size=16, weight="bold", color=color)
        c.text(x, y + 10, word, size=11, color=color)
        if swatch:
            w = text_width(num, 16) / 2
            c.rect(x - w - 16, y - 13, 10, 10, color=swatch_border or "none", fill=swatch, width=1)

    def tedge(c, a, b, label, side):
        c.line(*a, *b, color=theme.MUTED, width=1.6)
        segment_label(c, a, b, label, color=theme.SOFT_INK, size=12, offset=8, side=side, math_label=False)

    ROOT, SICK, HEAL = (432, 160), (548, 85), (548, 235)
    LEAF = {"tp": (664, 45), "fn": (664, 125), "fp": (664, 195), "tn": (664, 275)}

    @wt.step("Start with 1000 people", "Percentages are slippery, so count people instead. Each square is "
             "one person.", math="1000 people")
    def _(c):
        c.text(GX + COLS * CELL / 2, 26, "1000 people, one square each", size=13, color=theme.SOFT_INK)
        for i in range(N["pop"]):
            cell(c, i, C_TN)
        tnode(c, *ROOT, str(N["pop"]), "people", theme.INK)

    @wt.step("Mark the 1% who are sick", f"One percent of 1000 is {N['sick']}. The other {N['healthy']} "
             "are healthy.", math=f"1% \\times 1000 = {N['sick']}")
    def _(c):
        for i in range(N["sick"]):
            cell(c, i, C_TP)
        tedge(c, (ROOT[0] + 26, ROOT[1] - 16), (SICK[0] - 18, SICK[1] + 4), "1%", 1)
        tedge(c, (ROOT[0] + 26, ROOT[1] + 20), (HEAL[0] - 22, HEAL[1] - 4), "99%", -1)
        tnode(c, *SICK, str(N["sick"]), "sick", theme.RED)
        tnode(c, *HEAL, str(N["healthy"]), "healthy", theme.SOFT_INK)

    @wt.step("Test the sick", f"The test catches 90% of sick people: {N['tp']} test positive and "
             f"{N['fn']} slips through as negative.", math=f"90% \\times {N['sick']} = {N['tp']}")
    def _(c):
        for i in range(N["sick"]):
            if kind(i) == "fn":
                cell(c, i, theme.PAPER)
                cell(c, i, C_FN, border=theme.RED)
        tedge(c, (SICK[0] + 18, SICK[1] - 10), (LEAF["tp"][0] - 30, LEAF["tp"][1] + 2), "90%", 1)
        tedge(c, (SICK[0] + 18, SICK[1] + 8), (LEAF["fn"][0] - 30, LEAF["fn"][1] - 4), "10%", -1)
        tnode(c, *LEAF["tp"], str(N["tp"]), "test +", C_TP, swatch=C_TP)
        tnode(c, *LEAF["fn"], str(N["fn"]), "test −", theme.RED, swatch=C_FN, swatch_border=theme.RED)

    @wt.step("Test the healthy", f"The test also flags 9% of healthy people by mistake. Nine percent of "
             f"{N['healthy']} is {N['fp_exact']:g}, so about {N['fp']} false alarms.",
             math=f"9% \\times {N['healthy']} = {N['fp_exact']:g} \\approx {N['fp']}")
    def _(c):
        for i in range(N["sick"], N["sick"] + N["fp"]):
            cell(c, i, C_FP)
        tedge(c, (HEAL[0] + 26, HEAL[1] - 10), (LEAF["fp"][0] - 34, LEAF["fp"][1] + 2), "9%", 1)
        tedge(c, (HEAL[0] + 26, HEAL[1] + 8), (LEAF["tn"][0] - 34, LEAF["tn"][1] - 4), "91%", -1)
        tnode(c, *LEAF["fp"], str(N["fp"]), "test +", C_FP, swatch=C_FP)
        tnode(c, *LEAF["tn"], str(N["tn"]), "test −", theme.SOFT_INK, swatch=C_TN)

    BX, BY, BW = 27, 340, 6.8

    @wt.step("Line up everyone who tests positive", f"Pull out the positives: {N['tp']} sick people and "
             f"{N['fp']} healthy ones. The healthy crowd is much bigger, so it makes most of the "
             "positive results.", math=f"{N['tp']} + {N['fp']} = {pos} positive tests")
    def _(c):
        c.text(360, 318, f"the {pos} people who test positive", size=13, color=theme.INK, weight="bold")
        for i in range(pos):
            col = C_TP if i < N["tp"] else C_FP
            c.rect(BX + i * BW, BY, BW - 1.2, 14, color="none", fill=col)
        brace(c, BX + N["tp"] * BW - 1.2, BY + 20, BX, BY + 20, label=f"{N['tp']} sick", color=theme.RED,
              size=13, math_label=False)
        brace(c, BX + pos * BW - 1.2, BY + 20, BX + N["tp"] * BW, BY + 20, label=f"{N['fp']} healthy",
              color=theme.PURPLE, size=13, math_label=False)

    @wt.step("Read the answer", f"A positive test means about a {ans:.0%} chance of being sick, not 90%. "
             "The rare disease loses the numbers game to the big healthy group.",
             math=f"P(sick | +) = {N['tp']}/{pos} \\approx {ans * 100:.1f}%")
    def _(c):
        c.label_box(360, 420, f"P(sick | +) = {N['tp']}/{pos} ≈ {ans * 100:.1f}%", color=theme.RED,
                    border=theme.RED, size=16)
        c.rect(BX - 3, BY - 3, N["tp"] * BW + 4.8, 20, color=theme.RED, width=2, rx=3)

    return wt


@diagram("bayes-area-square", "Bayes' Theorem as Areas", "Probability")
def bayes_square() -> Walkthrough:
    """Alternate view: the unit square split by disease, then by test result."""
    p_d, sens, fpr = 0.01, 0.90, 0.09
    tp, fp = p_d * sens, (1 - p_d) * fpr
    ans = tp / (tp + fp)
    wt = Walkthrough(
        "bayes-area-square", "Bayes' Theorem as Areas", "Probability",
        concept="P(D | +) = P(D)P(+ | D) / (P(D)P(+ | D) + P(H)P(+ | H))",
        summary="Draw all possibilities as a square of area 1. Split it into sick and healthy, then split "
                "each part by test result. The answer is one slice of positive area over all of it.",
        width=700, height=420, level="301",
    )
    X0, Y0, S = 60, 40, 330
    # stretch the sick strip so a 1% width stays visible: draw widths with a broken scale
    SICK_W = 40  # px standing for 1%

    def xs(frac_healthy):
        return X0 + SICK_W + frac_healthy * (S - SICK_W)

    @wt.step("Draw everyone as a square", "The whole square has area 1: every person, every outcome.",
             math="total area = 1")
    def _(c):
        c.rect(X0, Y0, S, S, color=theme.INK, fill=theme.PAPER, width=2)
        c.text(X0 + S / 2, Y0 - 16, "everyone", size=13, color=theme.SOFT_INK)

    @wt.step("Split by disease", "A thin strip on the left stands for the 1% who are sick. It is drawn "
             "wider than true scale so you can see it at all.",
             math="P(D) = 0.01;  P(H) = 0.99")
    def _(c):
        c.rect(X0, Y0, SICK_W, S, color=theme.RED, fill=theme.fill(theme.RED, "22"), width=2)
        c.text(X0 + SICK_W / 2, Y0 + S + 18, "sick 1%", size=12, color=theme.RED, weight="bold")
        c.text(X0 + SICK_W + (S - SICK_W) / 2, Y0 + S + 18, "healthy 99%", size=12, color=theme.SOFT_INK,
               weight="bold")
        c.text(X0 + SICK_W / 2, Y0 + S + 34, "(not to scale)", size=10, color=theme.SOFT_INK)

    @wt.step("Split each part by the test", "In the sick strip, 90% of the height tests positive. In the "
             "healthy part, only 9% does. Positive area is shaded.",
             math="P(+ | D) = 0.90;  P(+ | H) = 0.09")
    def _(c):
        h1 = S * sens
        c.rect(X0, Y0, SICK_W, h1, color="none", fill=theme.RED)
        c.text(X0 + SICK_W / 2, Y0 + h1 / 2, "90%", size=12, color=theme.PAPER, weight="bold")
        h2 = S * fpr
        c.rect(X0 + SICK_W, Y0, S - SICK_W, h2, color="none", fill=theme.PURPLE)
        c.text(X0 + SICK_W + (S - SICK_W) / 2, Y0 + h2 / 2, "9% false alarms", size=12, color=theme.PAPER,
               weight="bold")
        c.text(X0 + SICK_W + (S - SICK_W) / 2, Y0 + S * 0.55, "healthy, test −: 91%", size=13,
               color=theme.SOFT_INK)
        c.line(X0 + SICK_W, Y0 + h2, X0 + S, Y0 + h2, color=theme.INK, width=1)
        c.line(X0, Y0 + h1, X0 + SICK_W, Y0 + h1, color=theme.INK, width=1)
        c.text(X0 + SICK_W / 2, Y0 + (h1 + S) / 2, "10%", size=11, color=theme.RED, weight="bold")

    RX = 440

    @wt.step("Compute the two positive areas", "Each area is a width times a height. The purple area is "
             "about ten times the red one, even though it looks thin.",
             math=f"0.01 \\times 0.90 = {tp:.4f},   0.99 \\times 0.09 = {fp:.4f}")
    def _(c):
        c.rect(RX, 80, 22, 22, color="none", fill=theme.RED)
        c.math(RX + 32, 91, f"0.01 \\times 0.90 = {tp:.4f}", size=17, anchor="start", color=theme.RED)
        c.rect(RX, 130, 22, 22, color="none", fill=theme.PURPLE)
        c.math(RX + 32, 141, f"0.99 \\times 0.09 = {fp:.4f}", size=17, anchor="start", color=theme.PURPLE)
        c.text(RX, 60, "positive areas", size=13, color=theme.SOFT_INK, anchor="start", weight="bold")

    @wt.step("Take the sick share of the positive area", "Given a positive test, you are somewhere in "
             "the shaded area. The red part is your chance of being sick.",
             math=f"{tp:.4f} / ({tp:.4f} + {fp:.4f}) \\approx {ans:.3f}")
    def _(c):
        y = 220
        c.text(RX + 110, y - 28, "red share of all positive area", size=13, color=theme.SOFT_INK)
        W = 220
        wr = W * ans
        c.rect(RX, y, wr, 26, color="none", fill=theme.RED)
        c.rect(RX + wr, y, W - wr, 26, color="none", fill=theme.PURPLE)
        c.rect(RX, y, W, 26, color=theme.INK, width=1.2)
        c.label_box(RX + 110, y + 70, f"P(sick | +) ≈ {ans:.1%}", color=theme.RED, border=theme.RED, size=17)

    return wt


# ---------------------------------------------------------------------------
# Two dice
# ---------------------------------------------------------------------------

@diagram("dice-sum-grid", "Sums of Two Dice", "Probability")
def dice_grid() -> Walkthrough:
    counts = {s: 0 for s in range(2, 13)}
    for a, b in product(range(1, 7), repeat=2):
        counts[a + b] += 1
    n10 = sum(counts[s] for s in (10, 11, 12))
    wt = Walkthrough(
        "dice-sum-grid", "Sums of Two Dice", "Probability",
        concept="P(sum = 7) = 6/36 = 1/6",
        summary="Two dice give 36 equally likely outcomes. Sums run along diagonals of the grid, so 7 has "
                "the most ways and 2 and 12 have only one each.",
        width=700, height=430, level="301",
    )
    GX, GY, CS = 72, 74, 46

    def cx(b):
        return GX + (b - 0.5) * CS

    def cy(a):
        return GY + (a - 0.5) * CS

    BX0, BY0, BW, BH = 440, 60, 240, 290
    p = Plane(None, box=(BX0, BY0, BW, BH), x=(1.4, 12.6), y=(0, 6.6))

    def chart_axes(c):
        p.c = c
        for k in range(1, 7):
            c.line(BX0, p.Y(k), BX0 + BW, p.Y(k), color=theme.GRID, width=1)
            c.text(BX0 - 8, p.Y(k), str(k), size=12, color=theme.SOFT_INK, anchor="end")
        for s in counts:
            c.text(p.X(s), BY0 + BH + 14, str(s), size=12, color=theme.INK)
        c.line(BX0, BY0 + BH, BX0 + BW, BY0 + BH, color=theme.INK, width=1.6)
        c.text(BX0 + BW / 2, BY0 + BH + 36, "sum", size=13, color=theme.SOFT_INK)
        c.text(BX0 + BW / 2, BY0 - 30, "ways to roll each sum", size=13, color=theme.SOFT_INK, weight="bold")

    @wt.setup
    def _(c):
        c.text(GX + 3 * CS, 22, "second die", size=13, color=theme.ORANGE, weight="bold")
        c.text(26, GY + 3 * CS, "first die", size=13, color=theme.BLUE, weight="bold",
               transform=f"rotate(-90 26 {GY + 3 * CS})")
        for k in range(1, 7):
            c.text(cx(k), GY - 16, str(k), size=15, color=theme.ORANGE, weight="bold")
            c.text(GX - 16, cy(k), str(k), size=15, color=theme.BLUE, weight="bold")
        for k in range(7):
            c.line(GX + k * CS, GY, GX + k * CS, GY + 6 * CS, color=theme.MUTED, width=1)
            c.line(GX, GY + k * CS, GX + 6 * CS, GY + k * CS, color=theme.MUTED, width=1)
        chart_axes(c)
        return None

    @wt.step("List every outcome", "Each row is the first die and each column is the second. Every "
             "cell is one outcome, and all 36 are equally likely, assuming nobody loaded the dice.",
             math="6 \\times 6 = 36 outcomes")
    def _(c):
        for a, b in product(range(1, 7), repeat=2):
            c.text(cx(b) - 7, cy(a), str(a), size=14, color=theme.BLUE, anchor="end")
            c.text(cx(b), cy(a), ",", size=14, color=theme.SOFT_INK)
            c.text(cx(b) + 6, cy(a), str(b), size=14, color=theme.ORANGE, anchor="start")

    def sums(c):
        for a, b in product(range(1, 7), repeat=2):
            c.text(cx(b), cy(a), str(a + b), size=16, color=theme.INK)

    @wt.step("Write the sum in each cell", "Replace each pair with its total. The same sum repeats along "
             "each diagonal that runs from lower left to upper right.", math="sum = first + second",
             fresh=True)
    def _(c):
        sums(c)

    @wt.step("Find every 7", "Six cells hold a 7, one in every row. No other sum fills a whole diagonal "
             "corner to corner.", math=f"P(7) = {counts[7]}/36 = {Fraction(counts[7], 36)}", fresh=True)
    def _(c):
        for a, b in product(range(1, 7), repeat=2):
            if a + b == 7:
                c.rect(GX + (b - 1) * CS + 2, GY + (a - 1) * CS + 2, CS - 4, CS - 4, color="none",
                       fill=theme.fill(theme.GREEN, "55"), rx=4)
        sums(c)
        bars(c, only=7)

    def bars(c, hi=None, only=None):
        p.c = c
        for s, n in counts.items():
            if only and s != only:
                continue
            col = theme.GREEN if s == 7 else theme.BLUE
            if hi and s in hi:
                col = theme.RED
            p.rect(s - 0.4, 0, s + 0.4, n, color=col, fill=theme.fill(col, "66"), width=1.5)
            c.text(p.X(s), p.Y(n) - 10, str(n), size=12, color=col, weight="bold")

    @wt.step("Count the ways for each sum", "Each diagonal becomes one bar. The bars climb by one from 2 "
             "up to 7 and step down again to 12, a tidy tent.",
             math="ways(s) = 6 - |s - 7|")
    def _(c):
        bars(c)

    @wt.step("Add ways for a bigger event", "Rolling 10 or more covers three diagonals in the corner. "
             "Add their counts, then divide by 36.",
             math=f"P(sum \\geq 10) = (3 + 2 + 1)/36 = {n10}/36 = {Fraction(n10, 36)}", fresh=True)
    def _(c):
        for a, b in product(range(1, 7), repeat=2):
            if a + b >= 10:
                c.rect(GX + (b - 1) * CS + 2, GY + (a - 1) * CS + 2, CS - 4, CS - 4, color="none",
                       fill=theme.fill(theme.RED, "44"), rx=4)
            elif a + b == 7:
                c.rect(GX + (b - 1) * CS + 2, GY + (a - 1) * CS + 2, CS - 4, CS - 4, color="none",
                       fill=theme.fill(theme.GREEN, "33"), rx=4)
        sums(c)
        bars(c, hi=(10, 11, 12))

    return wt


# ---------------------------------------------------------------------------
# Addition rule with a Venn diagram
# ---------------------------------------------------------------------------

def spread_points(inside, n, box, step, seed_xy):
    """Picks n well spread points from a grid of candidates, by farthest point sampling."""
    x0, y0, x1, y1 = box
    cands = []
    y = y0
    row = 0
    while y <= y1:
        x = x0 + (step / 2 if row % 2 else 0)
        while x <= x1:
            if inside(x, y):
                cands.append((x, y))
            x += step
        y += step * 0.87
        row += 1
    if len(cands) < n:
        raise ValueError(f"only {len(cands)} candidate points for {n}")
    start = min(cands, key=lambda q: (q[0] - seed_xy[0]) ** 2 + (q[1] - seed_xy[1]) ** 2)
    chosen = [start]
    d = [math.hypot(q[0] - start[0], q[1] - start[1]) for q in cands]
    while len(chosen) < n:
        i = max(range(len(cands)), key=lambda k: d[k])
        q = cands[i]
        chosen.append(q)
        d = [min(d[k], math.hypot(cands[k][0] - q[0], cands[k][1] - q[1])) for k in range(len(cands))]
    return sorted(chosen, key=lambda q: (q[1], q[0]))


@diagram("addition-rule-venn", "The Addition Rule", "Probability")
def addition_rule() -> Walkthrough:
    deck, hearts, faces, both = 52, 13, 12, 3
    union = hearts + faces - both
    wt = Walkthrough(
        "addition-rule-venn", "The Addition Rule", "Probability",
        concept="P(A \\cup B) = P(A) + P(B) - P(A \\cap B)",
        summary="To find the chance of A or B, add their chances and subtract the overlap once, because "
                "the overlap got counted in both.",
        width=700, height=410, level="301",
    )
    RX0, RY0, RX1, RY1 = 30, 52, 670, 392
    A, B, R = (275, 222), (425, 222), 125

    def din(p, q, r):
        return math.hypot(p[0] - q[0], p[1] - q[1]) < r

    def outside(x, y):
        if not (RX0 + 16 < x < RX1 - 16 and RY0 + 16 < y < RY1 - 14):
            return False
        if y < 100 and 120 < x < 580:
            return False
        if 225 < x < 475 and y > 334:
            return False
        return not din((x, y), A, R + 14) and not din((x, y), B, R + 14)

    pts_both = [(350, 192), (350, 222), (350, 252)]
    pts_a = spread_points(lambda x, y: din((x, y), A, R - 18) and not din((x, y), B, R + 16), hearts - both,
                          (150, 97, 330, 347), 14, (200, 222))
    pts_b = spread_points(lambda x, y: din((x, y), B, R - 18) and not din((x, y), A, R + 16), faces - both,
                          (370, 97, 550, 347), 14, (500, 222))
    pts_o = spread_points(outside, deck - union, (RX0, RY0, RX1, RY1), 12, (45, 70))

    @wt.setup
    def _(c):
        c.rect(RX0, RY0, RX1 - RX0, RY1 - RY0, color=theme.INK, width=1.6, rx=8)
        c.text(RX0, 30, f"one card from a {deck}-card deck", size=13, color=theme.SOFT_INK, anchor="start",
               weight="bold")
        return None

    def dots(c, pts, color=theme.INK):
        for x, y in pts:
            c.dot(x, y, r=4.5, color=color)

    @wt.step("Draw the sample space", f"Each dot is one card, and each card is equally likely. "
             f"There are {deck} dots.", math=f"{deck} equally likely cards")
    def _(c):
        dots(c, pts_o + pts_a + pts_b + pts_both)

    @wt.step("Circle the hearts", f"Event A is drawing a heart. It holds {hearts} cards.",
             math=f"P(A) = {hearts}/{deck}")
    def _(c):
        c.circle(*A, R, color=theme.BLUE, fill=theme.fill(theme.BLUE, "26"), width=2.5)
        c.text(A[0] - 70, 78, f"A: hearts ({hearts})", size=15, color=theme.BLUE, weight="bold")
        dots(c, pts_a + pts_both)

    @wt.step("Circle the face cards", f"Event B is drawing a jack, queen, or king. It holds {faces} cards, "
             f"and {both} of them are hearts too.", math=f"P(B) = {faces}/{deck}")
    def _(c):
        c.circle(*B, R, color=theme.ORANGE, fill=theme.fill(theme.ORANGE, "26"), width=2.5)
        c.text(B[0] + 70, 78, f"B: face cards ({faces})", size=15, color=theme.ORANGE, weight="bold")
        dots(c, pts_b + pts_both)

    @wt.step("Notice the double count", f"Adding {hearts} and {faces} gives {hearts + faces}, but the "
             f"{both} heart face cards sit in both circles and got counted twice.",
             math=f"{hearts} + {faces} = {hearts + faces} \\neq {union}")
    def _(c):
        for x, y in pts_both:
            c.circle(x, y, 9, color=theme.PURPLE, width=2.5)
        c.arrow(350, 352, 350, 268, color=theme.PURPLE, width=2)
        c.text(350, 370, f"J, Q, K of hearts: counted twice", size=13, color=theme.PURPLE, weight="bold",
               halo=True)

    @wt.step("Subtract the overlap once", f"Take the {both} extra counts back out. The union, A or B, "
             f"holds {union} cards.",
             math=f"P(A \\cup B) = {hearts}/{deck} + {faces}/{deck} - {both}/{deck} = {union}/{deck} = "
                  f"{Fraction(union, deck)}")
    def _(c):
        top, bot = (350, A[1] - 100), (350, A[1] + 100)
        c.path(f"M{top[0]},{top[1]} A{R},{R} 0 1 0 {bot[0]},{bot[1]} A{R},{R} 0 1 0 {top[0]},{top[1]}",
               color=theme.GREEN, width=4)
        c.label_box(670, 30, f"A ∪ B: {union} cards inside the green outline", color=theme.GREEN, border=theme.GREEN,
                    size=13, anchor="end")

    return wt


@diagram("addition-rule-table", "The Addition Rule in a Table", "Probability")
def addition_table() -> Walkthrough:
    """Alternate view: the same deck as a two-way table of counts."""
    deck, hearts, faces, both = 52, 13, 12, 3
    union = hearts + faces - both
    cells = {(0, 0): both, (0, 1): hearts - both, (1, 0): faces - both, (1, 1): deck - union}
    wt = Walkthrough(
        "addition-rule-table", "The Addition Rule in a Table", "Probability",
        concept="P(A \\cup B) = P(A) + P(B) - P(A \\cap B)",
        summary="A two-way table splits the deck by two yes or no questions. The row total and the column "
                "total share one cell, so adding both totals counts that cell twice.",
        width=640, height=320, level="301",
    )
    X0, Y0, CW, RH, HW = 170, 60, 130, 56, 130
    rows = ["heart", "not heart"]
    cols = ["face card", "not face"]

    def cell_xy(r, k):
        return X0 + k * CW, Y0 + r * RH

    @wt.setup
    def _(c):
        for k, name in enumerate(cols + ["total"]):
            c.text(X0 + k * CW + CW / 2, Y0 - 18, name, size=14, weight="bold",
                   color=theme.ORANGE if k == 0 else theme.SOFT_INK)
        for r, name in enumerate(rows + ["total"]):
            c.text(X0 - 14, Y0 + r * RH + RH / 2, name, size=14, weight="bold", anchor="end",
                   color=theme.BLUE if r == 0 else theme.SOFT_INK)
        for r in range(3):
            for k in range(3):
                x, y = cell_xy(r, k)
                c.rect(x, y, CW, RH, color=theme.MUTED, width=1,
                       fill=theme.PANEL if (r == 2 or k == 2) else "none")
        return None

    def num(c, r, k, v, color=theme.INK):
        x, y = cell_xy(r, k)
        c.text(x + CW / 2, y + RH / 2, str(v), size=20, color=color, weight="bold")

    @wt.step("Sort the deck two ways", "Each card lands in exactly one cell: heart or not, face card or "
             "not. The four cells add to 52.",
             math=f"{both} + {hearts - both} + {faces - both} + {deck - union} = {deck}")
    def _(c):
        for (r, k), v in cells.items():
            num(c, r, k, v)
        num(c, 1, 2, deck - hearts, theme.SOFT_INK)
        num(c, 2, 1, deck - faces, theme.SOFT_INK)
        num(c, 2, 2, deck)

    @wt.step("Total the heart row", f"The heart row adds to {hearts}.", math=f"P(A) = {hearts}/{deck}")
    def _(c):
        x, y = cell_xy(0, 0)
        c.rect(x + 3, y + 3, 3 * CW - 6, RH - 6, color=theme.BLUE, width=2.5, rx=6)
        num(c, 0, 2, hearts, theme.BLUE)

    @wt.step("Total the face card column", f"The face card column adds to {faces}. The top left cell "
             "now sits inside both outlines.", math=f"P(B) = {faces}/{deck}")
    def _(c):
        x, y = cell_xy(0, 0)
        c.rect(x + 7, y + 7, CW - 14, 3 * RH - 14, color=theme.ORANGE, width=2.5, rx=6)
        num(c, 2, 0, faces, theme.ORANGE)

    @wt.step("Subtract the shared cell", f"Row plus column counts the {both} heart face cards twice, so "
             "take them away once. The three inner cells touched by either outline add to the same answer.",
             math=f"{hearts} + {faces} - {both} = {both} + {hearts - both} + {faces - both} = {union}")
    def _(c):
        x, y = cell_xy(0, 0)
        c.rect(x + 12, y + 12, CW - 24, RH - 24, color="none", fill=theme.fill(theme.PURPLE, "44"), rx=4)
        num(c, 0, 0, both, theme.PURPLE)
        c.label_box(320, 292, f"P(A ∪ B) = {union}/{deck} = {Fraction(union, deck)}", color=theme.GREEN,
                    border=theme.GREEN, size=16)

    return wt


# ---------------------------------------------------------------------------
# Binomial distribution
# ---------------------------------------------------------------------------

HT = {"H": theme.BLUE, "T": theme.ORANGE}


@diagram("binomial-distribution", "The Binomial Distribution", "Probability")
def binomial() -> Walkthrough:
    n = 4
    seqs = ["".join(s) for s in product("HT", repeat=n)]
    by_k = {k: [s for s in seqs if s.count("H") == k] for k in range(n + 1)}
    total = len(seqs)
    wt = Walkthrough(
        "binomial-distribution", "The Binomial Distribution", "Probability",
        concept="P(X = k) = C(4, k) / 2^4",
        summary="Four fair coin flips make 16 equally likely sequences. Grouping them by the number of heads "
                "gives the counts 1, 4, 6, 4, 1, and dividing by 16 gives the binomial probabilities.",
        width=700, height=420, level="301",
    )
    RX, LX, TOP, GAP = 26, 72, 34, 22.5

    def leaf_y(i):
        return TOP + i * GAP

    def node_y(prefix):
        idx = [i for i, s in enumerate(seqs) if s.startswith(prefix)]
        return (leaf_y(idx[0]) + leaf_y(idx[-1])) / 2

    BX, BASE, BW, BH = 452, 330, 44, 44

    def block_xy(k, j):
        return BX + k * (BW + 4), BASE - (j + 1) * (BH + 2)

    @wt.step("Branch on each flip", "Each flip splits every path in two: heads up, tails down. After four "
             "flips there are 16 paths, all equally likely.", math="2 \\times 2 \\times 2 \\times 2 = 16")
    def _(c):
        for lvl in range(1, n + 1):
            c.text(RX + lvl * LX, 14, f"flip {lvl}", size=12, color=theme.SOFT_INK, weight="bold")
        for lvl in range(n):
            for pre in set(s[:lvl] for s in seqs):
                x0, y0 = RX + lvl * LX, node_y(pre)
                for ch in "HT":
                    x1, y1 = RX + (lvl + 1) * LX, node_y(pre + ch)
                    c.line(x0, y0, x1, y1, color=HT[ch], width=1.8)
        c.dot(RX, node_y(""), r=5)
        for ch, dy in (("H", -12), ("T", 14)):
            x1, y1 = RX + LX, node_y(ch)
            c.text((RX + x1) / 2 - 6, (node_y("") + y1) / 2 + dy, ch, size=13, color=HT[ch], weight="bold",
                   halo=True)

    @wt.step("Count heads on each path", "Read each path as a sequence and count its heads. HHTT, HTHT, "
             "and four others all have exactly 2.", math="X = number of heads")
    def _(c):
        for i, s in enumerate(seqs):
            y = leaf_y(i)
            w = mono_word(c, RX + n * LX + 10, y, s, HT, size=14)
            c.text(RX + n * LX + 18 + w, y, f"→ {s.count('H')}", size=13, color=theme.INK, anchor="start")

    @wt.step("Stack the paths by heads", "Move each sequence into the column for its number of heads. "
             "The stacks hold 1, 4, 6, 4, and 1 sequences.",
             math="C(4, k): " + ", ".join(str(len(by_k[k])) for k in range(n + 1)))
    def _(c):
        for k in range(n + 1):
            for j, s in enumerate(by_k[k]):
                x, y = block_xy(k, j)
                c.rect(x, y, BW, BH, color=theme.MUTED, fill=theme.PANEL, width=1, rx=3)
                mono_word(c, x + (BW - 4 * 6.6) / 2, y + BH / 2, s, HT, size=11)
            c.text(BX + k * (BW + 4) + BW / 2, BASE + 16, str(k), size=14, weight="bold")
        c.line(BX - 4, BASE, BX + 5 * (BW + 4), BASE, color=theme.INK, width=1.6)
        c.text(BX + 2.5 * (BW + 4), BASE + 38, "number of heads k", size=13, color=theme.SOFT_INK)

    @wt.step("Divide by 16", "Each sequence has chance 1/16, so each stack's chance is its height over "
             "16. The middle stack wins because there are the most ways to split 2 and 2.",
             math="P(X = k) = C(4, k) / 16  ")
    def _(c):
        for k in range(n + 1):
            x, y = block_xy(k, len(by_k[k]) - 1)
            c.math(x + BW / 2, y - 14, f"{len(by_k[k])}/{total}", size=15)

    m = len(by_k[2])

    @wt.step("Read one probability", f"Exactly two heads happens on {m} of the 16 paths. Find them in the "
             "tree and in the tallest stack.", math=f"P(X = 2) = {m}/16 = {Fraction(m, 16)} = {m / 16}")
    def _(c):
        for i, s in enumerate(seqs):
            if s.count("H") == 2:
                y = leaf_y(i)
                c.rect(RX + n * LX + 4, y - 10, 92, 20, color=theme.GREEN, width=2, rx=4)
        x, y = block_xy(2, m - 1)
        c.rect(x - 4, y - 4, BW + 8, BASE - y + 8, color=theme.GREEN, width=2.5, rx=5)

    return wt


# ---------------------------------------------------------------------------
# Law of large numbers
# ---------------------------------------------------------------------------

LLN_SEED = 28


def _flips(n):
    rng = random.Random(LLN_SEED)
    return [rng.random() < 0.5 for _ in range(n)]


@diagram("law-of-large-numbers", "The Law of Large Numbers", "Probability")
def lln() -> Walkthrough:
    N = 2000
    flips = _flips(N)
    run = []
    h = 0
    for i, f in enumerate(flips, 1):
        h += f
        run.append(h / i)
    wt = Walkthrough(
        "law-of-large-numbers", "The Law of Large Numbers", "Probability",
        concept="heads / flips \\to 0.5  as  flips \\to \\infty",
        summary="The share of heads swings wildly over a few flips and settles near one half over many. "
                "The swings shrink like 1 over the square root of the number of flips.",
        width=700, height=400, level="301",
    )

    def plane(c, n):
        p = Plane(c, box=(70, 30, 590, 300), x=(0, n), y=(0, 1))
        step = n // 10
        for k in range(1, 10):
            p.c.line(p.X(0), p.Y(k / 10), p.X(n), p.Y(k / 10), color=theme.GRID, width=1)
        for v in range(0, n + 1, step):
            c.line(p.X(v), p.Y(0), p.X(v), p.Y(0) + 5, color=theme.INK, width=1.2)
            c.text(p.X(v), p.Y(0) + 17, str(v), size=12, color=theme.SOFT_INK)
        for k in (0, 0.25, 0.5, 0.75, 1):
            c.text(p.X(0) - 8, p.Y(k), f"{k:g}", size=12, color=theme.SOFT_INK, anchor="end")
        c.line(p.X(0), p.Y(0), p.X(n), p.Y(0), color=theme.INK, width=1.6)
        c.line(p.X(0), p.Y(0), p.X(0), p.Y(1), color=theme.INK, width=1.6)
        c.text(p.X(n / 2), p.Y(0) + 40, "number of flips", size=13, color=theme.SOFT_INK)
        c.text(22, p.Y(0.5), "share of heads", size=13, color=theme.SOFT_INK,
               transform=f"rotate(-90 22 {p.Y(0.5)})")
        p.hline(0.5, color=theme.GREEN, width=2, dash="7 5")
        c.text(p.X(n) + 6, p.Y(0.5), "0.5", size=13, color=theme.GREEN, anchor="start", weight="bold")
        return p

    def trace(p, n, dots=False):
        pts = [p.px(i, run[i - 1]) for i in range(1, n + 1)]
        p.c.polyline(pts, color=theme.BLUE, width=2.2 if n <= 200 else 1.6)
        if dots:
            for x, y in pts:
                p.c.dot(x, y, r=3.5, color=theme.BLUE)
        X, Y = pts[-1]
        p.c.text(X - 6, Y - 18, f"{run[n - 1]:.3f}", size=13, color=theme.BLUE, weight="bold", anchor="end",
                 halo=True)

    first = flips[:10]
    h10 = sum(first)

    @wt.step("Flip a coin ten times", f"Ten flips gave {h10} heads. The coin is fair; small samples just "
             "swing. One flip is a big deal in a small crowd, so the running share jumps every time.",
             math=f"{h10} heads / 10 flips = {h10 / 10}")
    def _(c):
        h = 0
        BASE, TALL = 360, 110
        for i, f in enumerate(first):
            x = 100 + i * 58
            h += f
            col = theme.BLUE if f else theme.ORANGE
            c.text(x, 30, f"#{i + 1}", size=12, color=theme.SOFT_INK)
            c.circle(x, 68, 21, color=col, fill=theme.fill(col, "33"), width=2.5)
            c.text(x, 68, "H" if f else "T", size=18, weight="bold", color=col)
            c.math(x, 118, f"{h}/{i + 1}", size=16)
            c.text(x, 146, f"{h / (i + 1):.2f}", size=13, color=theme.BLUE, weight="bold")
            top = BASE - TALL * h / (i + 1)
            c.rect(x - 16, top, 32, BASE - top, color=theme.BLUE, fill=theme.fill(theme.BLUE, "44"), width=1.5)
        c.text(18, 112, "heads", size=12, color=theme.SOFT_INK, anchor="start")
        c.text(18, 126, "so far", size=12, color=theme.SOFT_INK, anchor="start")
        c.text(18, 146, "share", size=12, color=theme.BLUE, anchor="start")
        c.line(70, BASE, 670, BASE, color=theme.INK, width=1.6)
        c.line(70, BASE - TALL, 670, BASE - TALL, color=theme.GRID, width=1)
        c.line(70, BASE - TALL / 2, 670, BASE - TALL / 2, color=theme.GREEN, width=2, dash="7 5")
        for v in (0, 0.5, 1):
            c.text(62, BASE - TALL * v, f"{v:g}", size=12, color=theme.GREEN if v == 0.5 else theme.SOFT_INK,
                   anchor="end")
        c.text(370, BASE - TALL - 22, "share of heads after each flip", size=13, color=theme.SOFT_INK)

    @wt.step("Plot the running share", "Plot the share after each of the first 20 flips. It wanders well "
             "away from one half.", math=f"share after 20 flips = {run[19]:.2f}", fresh=True)
    def _(c):
        p = plane(c, 20)
        trace(p, 20, dots=True)

    @wt.step("Keep flipping", "Over 200 flips the line still wobbles, but each new flip moves it less. "
             "One flip out of 200 barely nudges the average.", math=f"share after 200 flips = {run[199]:.3f}",
             fresh=True)
    def _(c):
        p = plane(c, 200)
        trace(p, 200)

    def zoom(c):
        p = plane(c, N)
        trace(p, N)
        return p

    @wt.step("Zoom out to 2000 flips", "Over 2000 flips the early swings squeeze against the left edge, "
             "and the line hugs one half.", math=f"share after 2000 flips = {run[N - 1]:.3f} \\approx 0.5",
             fresh=True)
    def _(c):
        zoom(c)

    @wt.step("See the swings shrink", "The shaded funnel is one half plus or minus 1/√n, where most runs "
             "stay. Four times the flips makes the funnel half as wide.",
             math="0.5 \\pm 1/sqrt(n)", fresh=True)
    def _(c):
        p = Plane(c, box=(70, 30, 590, 300), x=(0, N), y=(0, 1))
        p.shade_between(lambda x: min(1, 0.5 + 1 / math.sqrt(max(x, 1))),
                        lambda x: max(0, 0.5 - 1 / math.sqrt(max(x, 1))), 1, N, color=theme.GREEN,
                        opacity=0.16, n=400)
        zoom(c)
        for n in (100, 400, 1600):
            hw = 1 / math.sqrt(n)
            p.segment(n, 0.5 - hw, n, 0.5 + hw, color=theme.GREEN, width=1.5)
            c.text(p.X(n), p.Y(0.5 + hw) - 10, f"±{hw:.3f}", size=11, color=theme.GREEN, halo=True)

    return wt
