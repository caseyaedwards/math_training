"""Concept maps: the nested number systems and the prerequisite map of math branches."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import number_line
from ..registry import diagram
from ..svg import text_width
from ..walkthrough import Walkthrough


def _stage(scene, stage):
    def draw(c, ctx):
        scene(c, stage)
    return draw


# name, symbol, color, rect (x0, y0, x1, y1), new members [(x, y, text)], description
SYSTEMS = [
    ("natural", "\\mathbb{N}", theme.BLUE, (180, 214, 385, 344),
     [(232, 270, "1"), (282, 270, "2"), (332, 270, "3"), (282, 312, "42")], "count things"),
    ("integers", "\\mathbb{Z}", theme.ORANGE, (150, 166, 470, 360),
     [(420, 230, "0"), (420, 278, "-4"), (420, 326, "-17")], "add zero and negatives"),
    ("rationals", "\\mathbb{Q}", theme.GREEN, (110, 118, 560, 376),
     [(515, 186, "1/2"), (515, 236, "-0.75"), (515, 286, "0.333…"), (515, 336, "22/7")],
     "add fractions"),
    ("reals", "\\mathbb{R}", theme.PURPLE, (70, 70, 650, 392),
     [(605, 140, "sqrt(2)"), (605, 200, "\\pi"), (605, 260, "e"), (605, 320, "0.1010…")],
     "fill the gaps on the line"),
    ("complex", "\\mathbb{C}", theme.RED, (30, 22, 690, 408),
     [(330, 46, "i"), (420, 46, "3 + 2i"), (530, 46, "sqrt(-1) = i")], "step off the line"),
]


@diagram("number-systems-map", "Number Systems Map", "Concept Maps")
def build_number_systems() -> Walkthrough:
    wt = Walkthrough(
        "number-systems-map", "Number Systems: Sets Inside Sets", "Concept Maps",
        concept="\\mathbb{N} \\subset \\mathbb{Z} \\subset \\mathbb{Q} \\subset \\mathbb{R} \\subset \\mathbb{C}",
        summary="Each number system contains the one before it and adds new numbers to fix something the "
                "smaller system cannot do, from subtraction to square roots of negatives.",
        width=720, height=420, level="101",
    )

    def scene(c, stage):
        shown = SYSTEMS[:stage]
        # draw from the outside in so inner fills sit on top
        for i in range(len(shown) - 1, -1, -1):
            name, sym, col, (x0, y0, x1, y1), members, desc = shown[i]
            new = i == stage - 1
            c.rect(x0, y0, x1 - x0, y1 - y0, color="none", fill=theme.PAPER, rx=14)
            c.rect(x0, y0, x1 - x0, y1 - y0, color=col, fill=theme.fill(col, "1f"), width=3 if new else 2,
                   rx=14)
        for i, (name, sym, col, (x0, y0, x1, y1), members, desc) in enumerate(shown):
            new = i == stage - 1
            c.math(x0 + 14, y0 + 20, sym, size=22, color=col, anchor="start", weight="bold")
            c.text(x0 + 40, y0 + 20, name, size=14, color=col, anchor="start", weight="bold")
            dx = x0 + 44 + text_width(name, 14) + 6
            c.text(dx, y0 + 20, "– " + desc, size=12, color=theme.SOFT_INK, anchor="start")
            for x, y, s in members:
                c.math(x, y, s, size=18 if new else 16, color=col if new else theme.INK, halo=True)

    wt.step("Start with the counting numbers",
            "The natural numbers 1, 2, 3, … count things. Add two of them and you get another one. Subtract "
            "and you can get stuck: 2 − 5 has no answer here.", math="\\mathbb{N} = {1, 2, 3, \\ldots}",
            fresh=True)(_stage(scene, 1))
    wt.step("Add zero and the negatives",
            "The integers wrap around the naturals and add 0 and the negatives, so every subtraction works. "
            "Division still fails: 1 ÷ 2 is not an integer.",
            math="\\mathbb{N} \\subset \\mathbb{Z} = {\\ldots, -2, -1, 0, 1, 2, \\ldots}", fresh=True)(_stage(scene, 2))
    wt.step("Add the fractions",
            "The rationals are all fractions a/b with b not zero. Their decimals stop or repeat. Every integer "
            "is a fraction over 1, so ℤ sits inside ℚ.",
            math="\\mathbb{Z} \\subset \\mathbb{Q} = {a/b : b \\neq 0}", fresh=True)(_stage(scene, 3))
    wt.step("Fill the gaps with the reals",
            "Some lengths are not fractions: the diagonal of a unit square is √2. The reals add these "
            "irrational numbers and fill every gap on the number line.",
            math="\\mathbb{Q} \\subset \\mathbb{R},   sqrt(2), \\pi, e \\notin \\mathbb{Q}", fresh=True)(_stage(scene, 4))
    wt.step("Step off the line with the complex numbers",
            "No real number squares to −1. The complex numbers add i with i² = −1 and live on a plane, not a "
            "line. Every earlier number is a complex number with zero imaginary part.",
            math="\\mathbb{N} \\subset \\mathbb{Z} \\subset \\mathbb{Q} \\subset \\mathbb{R} \\subset \\mathbb{C}",
            fresh=True)(_stage(scene, 5))
    return wt


@diagram("number-systems-line", "Number Systems on a Number Line", "Concept Maps")
def build_number_systems_line() -> Walkthrough:
    wt = Walkthrough(
        "number-systems-line", "Number Systems: Tagging Points on the Line", "Concept Maps",
        concept="each number carries every tag from its own system outward",
        summary="Place sample numbers on a number line and tag each one with every system it belongs to. "
                "A natural number collects all four real tags, while π gets only one.",
        width=700, height=330, level="101",
    )
    Y = 120
    pts = [
        (-3, "-3", "Z"), (-0.75, "-0.75", "Q"), (0, "0", "Z"), (0.5, "1/2", "Q"), (1, "1", "N"),
        (math.sqrt(2), "sqrt(2)", "R"), (2, "2", "N"), (math.e, "e", "R"), (math.pi, "\\pi", "R"),
    ]
    order = ["N", "Z", "Q", "R"]
    cols = {"N": theme.BLUE, "Z": theme.ORANGE, "Q": theme.GREEN, "R": theme.PURPLE}
    syms = {"N": "\\mathbb{N}", "Z": "\\mathbb{Z}", "Q": "\\mathbb{Q}", "R": "\\mathbb{R}"}
    # stagger labels so close points do not collide
    lift = {"-0.75": 0, "1/2": 0, "sqrt(2)": 0, "e": 0, "\\pi": 1, "0": 1, "1": 1, "2": 1, "-3": 0}

    def scene(c, stage):
        X = number_line(c, 50, Y, 650, -4, 4, step=1)
        upto = order[:stage]
        for v, lab, home in pts:
            x = X(v)
            c.dot(x, Y, r=6, color=cols[home] if home in upto else theme.MUTED)
            c.math(x, Y - 26 - 22 * lift[lab], lab, size=16,
                   color=cols[home] if home in upto else theme.MUTED, halo=True)
            # tags: every system from home outward
            tags = [s for s in order[order.index(home):] if s in upto]
            for j, s in enumerate(tags):
                ty = Y + 48 + j * 24
                c.rect(x - 13, ty - 10, 26, 20, color=cols[s], fill=theme.fill(cols[s], "26"), width=1.4, rx=4)
                c.math(x, ty, syms[s], size=15, color=cols[s])
        c.text(30, 300, "tags:", size=13, color=theme.SOFT_INK, anchor="start")
        for j, s in enumerate(upto):
            name = {"N": "natural", "Z": "integer", "Q": "rational", "R": "real"}[s]
            c.text(80 + j * 120, 300, name, size=13, color=cols[s], anchor="start", weight="bold")

    wt.step("Tag the natural numbers",
            "Put sample numbers on the line. Only 1 and 2 are natural numbers, so only they get the ℕ tag.",
            math="1, 2 \\in \\mathbb{N}", fresh=True)(_stage(scene, 1))
    wt.step("Tag the integers",
            "Every natural number is also an integer, and so are 0 and −3. Their tag stacks grow.",
            math="-3, 0, 1, 2 \\in \\mathbb{Z}", fresh=True)(_stage(scene, 2))
    wt.step("Tag the rationals",
            "Fractions such as 1/2 and −0.75 join in, and every integer picks up a ℚ tag too.",
            math="-0.75, 1/2 \\in \\mathbb{Q}", fresh=True)(_stage(scene, 3))
    wt.step("Tag the reals",
            "Every point on the line is real. The irrationals √2, e, and π get only this one tag, while 1 and "
            "2 now wear four.", math="sqrt(2), e, \\pi \\in \\mathbb{R} but \\notin \\mathbb{Q}",
            fresh=True)(_stage(scene, 4))
    return wt


# ---------------------------------------------------------------------------
# Branches of mathematics
# ---------------------------------------------------------------------------

LAYER_Y = [44, 128, 212, 296, 380]
BOX_W, BOX_H = 150, 44
NODES = {
    "arith": ("Arithmetic", 0, 350, "+ − × ÷, fractions"),
    "alg": ("Algebra", 1, 230, "unknowns, equations"),
    "geo": ("Geometry", 1, 470, "shapes, proof"),
    "prob": ("Probability", 2, 110, "chance, counting"),
    "trig": ("Trigonometry", 2, 350, "angles, waves"),
    "lin": ("Linear Algebra", 2, 590, "vectors, matrices"),
    "stat": ("Statistics", 3, 110, "data, inference"),
    "calc": ("Calculus", 3, 350, "change, area"),
    "de": ("Differential Eq.", 4, 470, "laws of motion"),
}
EDGES = [("arith", "alg"), ("arith", "geo"), ("alg", "prob"), ("alg", "trig"), ("geo", "trig"),
         ("alg", "lin"), ("prob", "stat"), ("trig", "calc"), ("calc", "de"), ("lin", "de"), ("calc", "stat")]
LAYER_COL = [theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE, theme.RED]
PATH = ["arith", "alg", "trig", "calc", "de"]


@diagram("math-branches-map", "Branches of Mathematics Map", "Concept Maps")
def build_branches() -> Walkthrough:
    wt = Walkthrough(
        "math-branches-map", "Branches of Mathematics: What Comes Before What", "Concept Maps",
        concept="arithmetic \\to algebra \\to trigonometry \\to calculus \\to differential equations",
        summary="Each branch of math builds on earlier ones. Arrows point from a prerequisite to the branch "
                "that uses it, so any path from the top shows a workable order of study.",
        width=700, height=420, level="101",
    )

    def center(k):
        name, layer, x, desc = NODES[k]
        return x, LAYER_Y[layer]

    def scene(c, stage):
        layers = min(stage, 5)
        path_edges = set(zip(PATH, PATH[1:])) if stage == 6 else set()
        for a, b in EDGES:
            if NODES[a][1] < layers and NODES[b][1] < layers:
                ax, ay = center(a)
                bx, by = center(b)
                on = (a, b) in path_edges
                # leave from the bottom of a, arrive at the top of b
                sx, sy = ax + (bx - ax) * 0.18, ay + BOX_H / 2
                ex, ey = bx - (bx - ax) * 0.12, by - BOX_H / 2 - 2
                if NODES[b][1] - NODES[a][1] == 0:
                    continue
                if a == "calc" and b == "stat":
                    # same layer neighbor: run sideways
                    continue
                c.arrow(sx, sy, ex, ey, color=theme.ORANGE if on else theme.MUTED, width=3 if on else 1.8)
        if layers >= 4:
            # calculus also feeds statistics (same layer): short sideways arrow
            ax, ay = center("calc")
            bx, by = center("stat")
            on = False
            c.arrow(ax - BOX_W / 2 - 2, ay, bx + BOX_W / 2 + 4, by, color=theme.MUTED, width=1.8, dash="5 4")
            c.text((ax + bx) / 2, ay - 10, "helps", size=11, color=theme.SOFT_INK, halo=True)
        for k, (name, layer, x, desc) in NODES.items():
            if layer >= layers:
                # a faint placeholder hints at what is still to come
                c.rect(x - BOX_W / 2, LAYER_Y[layer] - BOX_H / 2, BOX_W, BOX_H, color=theme.GRID, width=1.5,
                       dash="5 4", rx=8)
                c.text(x, LAYER_Y[layer], "?", size=15, color=theme.MUTED)
                continue
            col = LAYER_COL[layer]
            y = LAYER_Y[layer]
            on_path = stage == 6 and k in PATH
            new = layer == layers - 1 and stage <= 5
            c.rect(x - BOX_W / 2, y - BOX_H / 2, BOX_W, BOX_H, color=theme.ORANGE if on_path else col,
                   fill=theme.HIGHLIGHT if (new or on_path) else theme.fill(col, "1a"),
                   width=3.2 if on_path else 2, rx=8)
            c.text(x, y - 7, name, size=15, weight="bold", color=col)
            c.text(x, y + 11, desc, size=11, color=theme.SOFT_INK)
        for i in range(layers):
            c.text(14, LAYER_Y[i], f"{i + 1}", size=13, color=LAYER_COL[i], weight="bold")
        if stage == 6:
            c.text(630, 380, "one route", size=13, color=theme.ORANGE, weight="bold")
            c.text(630, 398, "top to bottom", size=13, color=theme.ORANGE, weight="bold")

    wt.step("Start with arithmetic",
            "Arithmetic is the floor everything stands on: counting, the four operations, and fractions.",
            math="layer 1: arithmetic", fresh=True)(_stage(scene, 1))
    wt.step("Build algebra and geometry",
            "Algebra uses arithmetic on unknown numbers. Geometry uses it on lengths and angles. Each arrow "
            "means the upper branch is needed for the lower one.",
            math="arithmetic \\to algebra,  arithmetic \\to geometry", fresh=True)(_stage(scene, 2))
    wt.step("Branch out",
            "Trigonometry needs both algebra and geometry. Probability and linear algebra grow out of algebra.",
            math="algebra + geometry \\to trigonometry", fresh=True)(_stage(scene, 3))
    wt.step("Reach calculus and statistics",
            "Calculus studies change and leans on functions and trigonometry. Statistics grows from "
            "probability and borrows tools from calculus.",
            math="trigonometry \\to calculus,  probability \\to statistics", fresh=True)(_stage(scene, 4))
    wt.step("Combine branches",
            "Differential equations need calculus and linear algebra together. They describe anything that "
            "changes, from cooling coffee to orbiting planets.",
            math="calculus + linear algebra \\to differential equations", fresh=True)(_stage(scene, 5))
    wt.step("Follow one path",
            "Pick a goal and walk the arrows backward to find what to learn first. The highlighted route is a "
            "common order of study.",
            math="arithmetic \\to algebra \\to trigonometry \\to calculus \\to ODEs", fresh=True)(_stage(scene, 6))
    return wt
