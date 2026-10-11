"""Proof diagrams: induction as dominoes, a flowchart proof, and proof by contradiction."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import angle_mark
from ..registry import diagram
from ..svg import text_width
from ..walkthrough import Walkthrough


def _stage(scene, stage):
    def draw(c, ctx):
        scene(c, stage)
    return draw


# ---------------------------------------------------------------------------
# Proof by induction
# ---------------------------------------------------------------------------


def _domino(c, x, base, w, h, angle_deg, color, fill, label=None):
    """Draws a domino whose bottom-right corner is at (x + w, base), tipped right by angle_deg."""
    a = math.radians(angle_deg)
    px, py = x + w, base
    corners = [(x, base), (x + w, base), (x + w, base - h), (x, base - h)]
    pts = []
    for cx, cy in corners:
        dx, dy = cx - px, cy - py
        # clockwise rotation on screen (y down) tips the top to the right
        pts.append((px + dx * math.cos(a) - dy * math.sin(a), py + dx * math.sin(a) + dy * math.cos(a)))
    c.polygon(pts, color=color, fill=fill, width=2)
    if label:
        mx = sum(p[0] for p in pts) / 4
        my = sum(p[1] for p in pts) / 4
        c.circle(mx, my - 14 * math.cos(a), 3, color="none", fill=color)
        c.circle(mx, my + 14 * math.cos(a), 3, color="none", fill=color)


def tri(n: int) -> int:
    return n * (n + 1) // 2


@diagram("proof-by-induction", "Proof by Induction", "Logic and Proof")
def build_induction() -> Walkthrough:
    wt = Walkthrough(
        "proof-by-induction", "Proof by Induction: Falling Dominoes", "Logic and Proof",
        concept="1 + 2 + \\ldots + n = n(n + 1)/2  for every n \\geq 1",
        summary="Induction proves a statement for every whole number in two moves: knock over the first domino "
                "(the base case), and show each domino knocks over the next (the inductive step).",
        width=700, height=420, level="201",
    )
    N = 8
    W, H, GAP, X0, BASE = 18, 86, 76, 54, 160
    lean = math.degrees(math.asin((GAP - W) / H))
    K = 4  # the sample k for the inductive step picture

    def xs(i):
        return X0 + i * GAP

    def scene(c, stage):
        fallen = 0
        if stage >= 2:
            fallen = 1
        if stage >= 5:
            fallen = N
        c.line(20, BASE, 680, BASE, color=theme.MUTED, width=2)
        for i in range(N):
            if i < fallen:
                col = theme.GREEN if i == 0 else theme.BLUE
                ang = lean if i < N - 1 else 90
                _domino(c, xs(i), BASE, W, H, ang, col, theme.fill(col, "40"), label=True)
            else:
                _domino(c, xs(i), BASE, W, H, 0, theme.INK, theme.PANEL, label=True)
            c.math(xs(i) + W / 2, BASE + 20, f"P({i + 1})", size=15,
                   color=theme.GREEN if (i == 0 and stage >= 2) else theme.INK)
        if stage < 5:
            c.text(xs(N - 1) + 50, BASE - 40, "…", size=22, color=theme.SOFT_INK)
        if stage >= 2:
            c.text(xs(0) + 4, 38, "base case", size=14, color=theme.GREEN, weight="bold")
            c.math(xs(0) + 4, 58, "1 = 1\\cdot2/2", size=14, color=theme.GREEN)
        if stage >= 3 and stage < 5:
            i = K - 1
            x1, x2 = xs(i) + W / 2, xs(i + 1) + W / 2
            c.curved_arrow(x1, BASE - H - 6, x2, BASE - H - 6, bend=0.3, color=theme.ORANGE, width=2.6)
            c.math((x1 + x2) / 2, 18, "P(k) \\implies P(k + 1)", size=16, color=theme.ORANGE, halo=True)
            c.text((x1 + x2) / 2, 38, "each one tips the next", size=13, color=theme.ORANGE)
        if stage >= 5:
            c.text(420, 40, "every domino falls:", size=15, color=theme.BLUE, weight="bold", anchor="start")
            c.math(420, 62, "P(n) true for all n", size=16, color=theme.BLUE, anchor="start")
        if stage >= 4:
            s, bx, by = 18, 70, 392
            c.text(bx, 262, f"why the step works, for k = {K}:", size=14, color=theme.SOFT_INK, anchor="start")
            for col in range(1, K + 1):
                for r in range(col):
                    c.rect(bx + (col - 1) * s, by - (r + 1) * s, s, s, color=theme.PAPER,
                           fill=theme.BLUE, width=1.5)
            for r in range(K + 1):
                c.rect(bx + K * s, by - (r + 1) * s, s, s, color=theme.PAPER, fill=theme.ORANGE, width=1.5)
            tx = bx + (K + 1) * s + 30
            c.math(tx, 290, f"1 + 2 + 3 + 4 = {tri(K)} = {K}\\cdot{K + 1}/2", size=17, color=theme.BLUE,
                   anchor="start")
            c.math(tx, 324, f"+ {K + 1}  (one new column)", size=17, color=theme.ORANGE, anchor="start")
            c.math(tx, 364, f"= {tri(K) + K + 1} = {K + 1}\\cdot{K + 2}/2", size=17, color=theme.INK,
                   anchor="start", weight="bold")
            assert tri(K) + K + 1 == tri(K + 1)
            gx = 470
            c.text(gx, 262, "same move for any k:", size=14, color=theme.SOFT_INK, anchor="start")
            c.math(gx, 296, "k(k + 1)/2 + (k + 1)", size=17, color=theme.BLUE, anchor="start")
            c.math(gx, 330, "= (k + 1)(k/2 + 1)", size=17, anchor="start")
            c.math(gx, 364, "= (k + 1)(k + 2)/2", size=17, anchor="start", weight="bold")
            c.line(gx - 20, 250, gx - 20, 385, color=theme.GRID, width=1.5)

    wt.step("Line up the statements",
            "Each domino is one statement P(n): the sum 1 + 2 + … + n equals n(n + 1)/2. Infinitely many "
            "dominoes, infinitely many claims, and no time to check them one by one.",
            math="P(n):  1 + 2 + \\ldots + n = n(n + 1)/2", fresh=True)(_stage(scene, 1))
    wt.step("Prove the base case",
            "Check P(1) by hand. The sum of the first one number is 1, and 1·2/2 is also 1, so the first "
            "domino falls.", math="P(1):  1 = 1\\cdot2/2", fresh=True)(_stage(scene, 2))
    wt.step("Prove the inductive step",
            "Assume P(k) is true for some k. Add the next number k + 1 to both sides and simplify. The result "
            "is P(k + 1), so each falling domino knocks over the next.",
            math="k(k + 1)/2 + (k + 1) = (k + 1)(k + 2)/2", fresh=True)(_stage(scene, 3))
    wt.step("See the inductive step",
            f"The sum up to {K} is a staircase of {tri(K)} blue squares. Adding a column of {K + 1} orange "
            f"squares gives the staircase for {K + 1}, which matches the formula.",
            math=f"{tri(K)} + {K + 1} = {tri(K + 1)} = {K + 1}\\cdot{K + 2}/2", fresh=True)(_stage(scene, 4))
    wt.step("Every domino falls",
            "The first domino falls, and each one knocks over the next. Together these two facts topple the "
            "whole infinite row, so P(n) holds for every n.",
            math="1 + 2 + \\ldots + n = n(n + 1)/2", fresh=True)(_stage(scene, 5))
    return wt


# ---------------------------------------------------------------------------
# Flowchart proof
# ---------------------------------------------------------------------------


def _flow_box(c, x, y, stmt, reason, new=False, border=theme.INK):
    w = max(text_width(stmt, 16, "serif"), text_width(reason, 12)) + 30
    h = 54
    c.rect(x - w / 2, y - h / 2, w, h, color=border, fill=theme.HIGHLIGHT if new else theme.PAPER,
           width=2.4 if new else 1.6, rx=8)
    c.math(x, y - 8, stmt, size=16)
    c.text(x, y + 14, reason, size=12, italic=True, color=theme.SOFT_INK)
    return w, h


@diagram("proof-flowchart", "Flowchart Proof", "Logic and Proof")
def build_flowchart() -> Walkthrough:
    wt = Walkthrough(
        "proof-flowchart", "Flowchart Proof: Vertical Angles Are Equal", "Logic and Proof",
        concept="m\\angle1 = m\\angle3",
        summary="A flowchart proof writes each statement in a box with its reason underneath, and arrows show "
                "which facts lead to which. Here two linear pairs prove that vertical angles are equal.",
        width=720, height=430, level="201",
    )
    T = 50  # angle between the lines, degrees
    a1, a2, a3 = T, 180 - T, T
    assert a1 + a2 == 180 and a3 + a2 == 180
    CX, CY, L = 140, 200, 115
    COL1, COL2, COL3 = theme.BLUE, theme.ORANGE, theme.GREEN

    def pt(deg, r=L):
        return (CX + r * math.cos(math.radians(deg)), CY - r * math.sin(math.radians(deg)))

    boxes = {
        "G": (505, 40, "lines ℓ and m intersect", "given"),
        "S1": (400, 140, "m\\angle1 + m\\angle2 = 180\\deg", "linear pair"),
        "S2": (612, 140, "m\\angle3 + m\\angle2 = 180\\deg", "linear pair"),
        "S3": (505, 250, "m\\angle1 + m\\angle2 = m\\angle3 + m\\angle2", "both equal 180\\deg"),
        "S4": (505, 360, "m\\angle1 = m\\angle3", "subtract m∠2 from both sides"),
    }
    order = ["G", "S1", "S2", "S3", "S4"]
    reveal = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
    edges = [("G", "S1"), ("G", "S2"), ("S1", "S3"), ("S2", "S3"), ("S3", "S4")]

    def scene(c, stage):
        # figure
        hi = {1: (), 2: (1, 2), 3: (3, 2), 4: (1, 2, 3), 5: (1, 3)}[stage]
        marks = [(1, 0, T, COL1, 34), (2, T, 180, COL2, 26), (3, 180, 180 + T, COL3, 34)]
        for k, d0, d1, col, r in marks:
            if stage >= 2 or k == 1 or True:
                faded = k not in hi and stage >= 2
                angle_mark(c, (CX, CY), pt(d0), pt(d1), r=r, color=theme.MUTED if faded else col,
                           label=str(k), label_r=r + 14)
        c.line(*pt(180), *pt(0), color=theme.INK, width=2.4)
        c.line(*pt(180 + T), *pt(T), color=theme.INK, width=2.4)
        c.dot(CX, CY, r=4)
        c.text(pt(0)[0] + 4, CY - 14, "ℓ", size=20, italic=True, anchor="end", font="serif")
        c.math(pt(T)[0] + 10, pt(T)[1], "m", size=20, anchor="start")
        if stage == 2:
            c.text(CX, 300, "∠1 and ∠2 make a straight line", size=13, color=theme.SOFT_INK)
        if stage == 3:
            c.text(CX, 300, "∠3 and ∠2 make a straight line", size=13, color=theme.SOFT_INK)
        if stage >= 5:
            ys = 320
            for i, (k, v, col) in enumerate(((1, a1, COL1), (2, a2, COL2), (3, a3, COL3))):
                c.math(40, ys + i * 28, f"m\\angle{k} = {v}\\deg", size=17, color=col, anchor="start")
            c.text(150, ys + 56, "\u2190 same as \u22201", size=13, color=COL3, anchor="start")
        # flowchart
        shown = order[:reveal[stage]]
        for a, b in edges:
            if a in shown and b in shown:
                ax, ay = boxes[a][0], boxes[a][1] + 27
                bx, by = boxes[b][0], boxes[b][1] - 29
                c.arrow(ax, ay, bx, by, color=theme.SOFT_INK, width=1.8)
        for key in shown:
            x, y, s, r = boxes[key]
            new = key == shown[-1]
            border = theme.GREEN if (key == "S4" and stage == 5) else theme.INK
            _flow_box(c, x, y, s, r.replace("\\deg", "°"), new=new, border=border)

    wt.step("Start from the given",
            "Two lines cross and make four angles. Angles 1 and 3 sit across from each other, so they are "
            "vertical angles. Claim: they are equal.", math="prove: m\\angle1 = m\\angle3",
            fresh=True)(_stage(scene, 1))
    wt.step("Use the first linear pair",
            "Angles 1 and 2 sit side by side on line ℓ and make a straight angle. Linear pairs add to 180°.",
            math="m\\angle1 + m\\angle2 = 180\\deg", fresh=True)(_stage(scene, 2))
    wt.step("Use the second linear pair",
            "Angles 3 and 2 also make a straight angle, this time along line m. The same reason applies.",
            math="m\\angle3 + m\\angle2 = 180\\deg", fresh=True)(_stage(scene, 3))
    wt.step("Join the two equations",
            "Both sums equal 180°, so they equal each other. Arrows from both boxes feed this one.",
            math="m\\angle1 + m\\angle2 = m\\angle3 + m\\angle2", fresh=True)(_stage(scene, 4))
    wt.step("Subtract the shared angle",
            f"Take m∠2 away from both sides. What remains is the claim. With a {T}° crossing, both vertical "
            f"angles measure {a1}° and the other pair measures {a2}°.",
            math=f"m\\angle1 = m\\angle3 = {a1}\\deg", fresh=True)(_stage(scene, 5))
    return wt


# ---------------------------------------------------------------------------
# Proof by contradiction
# ---------------------------------------------------------------------------


def _smallest_factor(n: int) -> int:
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return n


def _factor(n: int):
    out = []
    while n > 1:
        d = _smallest_factor(n)
        out.append(d)
        n //= d
    return out


@diagram("proof-by-contradiction", "Proof by Contradiction", "Logic and Proof")
def build_contradiction() -> Walkthrough:
    wt = Walkthrough(
        "proof-by-contradiction", "Proof by Contradiction: Infinitely Many Primes", "Logic and Proof",
        concept="N = p_1\\cdot p_2\\cdot \\ldots \\cdot p_k + 1  has a prime factor missing from the list",
        summary="Assume the opposite of the claim and follow it to something impossible. If the primes were a "
                "finite list, multiplying them and adding 1 builds a number no prime on the list divides.",
        width=700, height=430, level="201",
    )
    primes = [2, 3, 5, 7]
    P = 1
    for p in primes:
        P *= p
    Nn = P + 1
    lo, hi = Nn - 13, Nn + 1
    vals = list(range(lo, hi + 1))
    X0, DX = 120, 30

    def X(v):
        return X0 + (v - lo) * DX

    rows_y = {p: 150 + i * 42 for i, p in enumerate(primes)}
    big = [2, 3, 5, 7, 11, 13]
    PB = 1
    for p in big:
        PB *= p
    NB = PB + 1
    fb = _factor(NB)

    def scene(c, stage):
        # the assumed list
        c.text(30, 34, "Assume these are all the primes:", size=15, anchor="start",
               color=theme.RED if stage >= 4 else theme.INK)
        bx = 290
        for i, p in enumerate(primes):
            c.label_box(bx + i * 46, 34, str(p), size=17, border=theme.BLUE, color=theme.BLUE)
        c.text(bx + 4 * 46 - 6, 34, "and no others", size=13, color=theme.SOFT_INK, anchor="start")
        if stage >= 4:
            c.line(26, 35, 252, 35, color=theme.RED, width=2.5)
            c.text(bx + 4 * 46 - 6, 54, "(oops)", size=13, color=theme.RED, anchor="start", weight="bold")
        if stage == 1:
            c.text(30, 110, "Claim: there are infinitely many primes.", size=16, anchor="start", weight="bold")
            c.text(30, 145, "Plan: assume the claim is false, follow the logic, and hit something impossible.",
                   size=15, anchor="start")
            c.text(30, 172, "If the assumption leads to nonsense, the assumption was wrong.", size=15,
                   anchor="start", color=theme.SOFT_INK)
            c.text(30, 230, "A finite list of primes would look like this:", size=15, anchor="start")
            c.math(30, 262, "p_1, p_2, p_3, \\ldots, p_k", size=20, anchor="start", color=theme.BLUE)
            c.text(30, 300, "For the small picture, k = 4 and the list is 2, 3, 5, 7.", size=15, anchor="start",
                   color=theme.BLUE)
        if stage >= 2:
            c.math(30, 78, f"N = 2\\cdot3\\cdot5\\cdot7 + 1 = {P} + 1 = {Nn}", size=18, anchor="start",
                   color=theme.PURPLE)
            # number strip
            ty = 120
            c.rect(X(Nn) - DX / 2, ty - 14, DX, rows_y[primes[-1]] - ty + 30, color="none",
                   fill=theme.fill(theme.PURPLE, "26"))
            for v in vals:
                c.text(X(v), ty, str(v), size=11 if v != Nn else 13,
                       color=theme.PURPLE if v == Nn else theme.SOFT_INK,
                       weight="bold" if v in (Nn, P) else None)
        if stage >= 3:
            for p in primes:
                y = rows_y[p]
                c.line(X(lo) - 12, y, X(hi) + 12, y, color=theme.GRID, width=1.5)
                c.text(X(lo) - 22, y, f"÷ {p}", size=14, anchor="end", color=theme.BLUE)
                for v in vals:
                    if v % p == 0:
                        c.dot(X(v), y, r=6 if v == P else 4.5, color=theme.BLUE)
                c.circle(X(Nn), y, 6, color=theme.RED, width=2, fill=theme.PAPER)
                q, r = divmod(Nn, p)
                c.math(X(hi) + 30, y, f"{Nn} = {p}\\cdot{q} + {r}", size=15, anchor="start", color=theme.INK)
            c.text(X(P) + 16, rows_y[primes[-1]] + 30, f"{P}: every prime divides it", size=12, color=theme.BLUE,
                   anchor="end")
            c.text(690, rows_y[primes[-1]] + 30, "remainder 1 every time", size=13, color=theme.RED,
                   anchor="end", weight="bold")
        if stage >= 4:
            f = _smallest_factor(Nn)
            msg = (f"{Nn} is prime itself, and it is not on the list" if f == Nn
                   else f"{Nn} has prime factor {f}, which is not on the list")
            c.label_box(350, 352, msg, size=15, border=theme.RED, color=theme.RED)
            c.text(350, 380, "contradiction: the list was not complete", size=14, color=theme.RED,
                   weight="bold")
        if stage >= 5:
            fs = "\\cdot".join(str(d) for d in fb)
            c.math(350, 414, f"Bigger list: 2\\cdot3\\cdot5\\cdot7\\cdot11\\cdot13 + 1 = {NB} = {fs}",
                   size=16, color=theme.GREEN)

    f0 = _smallest_factor(Nn)
    wt.step("Assume the opposite",
            "To prove there are infinitely many primes, suppose there are only finitely many. For a small "
            "picture, pretend the whole list is 2, 3, 5, and 7.",
            math="primes = {p_1, p_2, \\ldots, p_k}", fresh=True)(_stage(scene, 1))
    wt.step("Build a new number",
            f"Multiply every prime on the list and add 1. Here the product is {P}, so N is {Nn}.",
            math="N = p_1\\cdot p_2\\cdot \\ldots \\cdot p_k + 1", fresh=True)(_stage(scene, 2))
    wt.step("Divide by each listed prime",
            f"Each prime divides the product {P}, shown as a blue dot. N sits one step past it, so every "
            "division leaves remainder 1. No prime on the list divides N.",
            math=f"{Nn} \\div p  leaves remainder 1", fresh=True)(_stage(scene, 3))
    wt.step("Reach the contradiction",
            "Every whole number above 1 has a prime factor. N has one, but it cannot be on the list. "
            "So the list was missing a prime, which breaks the assumption.",
            math=(f"{Nn} is prime, and {Nn} \\notin {{2, 3, 5, 7}}" if f0 == Nn
                  else f"{f0} divides {Nn}, and {f0} \\notin {{2, 3, 5, 7}}"), fresh=True)(_stage(scene, 4))
    wt.step("Conclude for every list",
            f"The same move defeats any finite list. With six primes, N = {NB} splits into primes "
            f"{' and '.join(str(d) for d in fb)}, again missing from the list. The primes never run out.",
            math="no finite list holds every prime", fresh=True)(_stage(scene, 5))
    return wt
