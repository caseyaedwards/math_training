"""Rigid transformations on a coordinate grid: translate, reflect, rotate."""

from __future__ import annotations

import math

from .. import theme
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._geo import away, centroid

ORIG, TRANS, REFL, ROT = theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE


@diagram("rigid-transformations", "Rigid Transformations", "Geometry")
def rigid() -> Walkthrough:
    tri = [(1, 1), (4, 1), (2, 3)]
    names = ["A", "B", "C"]
    shift = (5, 3)
    translate = lambda p: (p[0] + shift[0], p[1] + shift[1])
    reflect = lambda p: (p[0], -p[1])
    rotate = lambda p: (-p[1], p[0])
    images = {
        "t": [translate(p) for p in tri],
        "f": [reflect(p) for p in tri],
        "r": [rotate(p) for p in tri],
    }
    sides = [math.dist(tri[i], tri[(i + 1) % 3]) for i in range(3)]

    def fmt_pt(p):
        return "(" + ", ".join(str(int(v)).replace("-", "−") for v in p) + ")"

    wt = Walkthrough(
        "rigid-transformations", "Rigid Transformations", "Geometry",
        concept="slide or flip or turn \\implies congruent image",
        summary="Translations, reflections, and rotations move a figure without stretching it. The image "
                "A′B′C′ is congruent to ABC: every side and angle stays the same.",
        width=700, height=440, level="201",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(10, 18, 540, 404), x=(-4.6, 10.4), y=(-4.4, 7.4), equal=True)
        p.grid(step=1)
        p.axes(step=1, ystep=1, labels=False)
        for v in (-4, -2, 2, 4, 6, 8):
            if p.xmin < v < p.xmax:
                c.text(p.X(v), p.Y(0) + 14, str(v).replace("-", "−"), size=11, color=theme.SOFT_INK, halo=True)
        for v in (-4, -2, 2, 4, 6):
            c.text(p.X(0) - 8, p.Y(v), str(v).replace("-", "−"), size=11, color=theme.SOFT_INK, anchor="end",
                   halo=True)
        return p

    def draw(c, p, pts, col, prime="", coords=True, side_out=True, nudge=None):
        p.region(pts, color=col, opacity=0.25, outline=col, width=2.5)
        g = centroid(pts)
        for (x, y), nm in zip(pts, names):
            X, Y = p.px(x, y)
            gx, gy = p.px(*g)
            dx, dy = (nudge or {}).get(nm, (X - gx, Y - gy))
            L = math.hypot(dx, dy) or 1
            c.dot(X, Y, r=4, color=col)
            lab = nm + prime
            c.text(X + dx / L * 15, Y + dy / L * 15, lab, size=15, color=col, halo=True, weight="bold", math=True)

    def coords_of(key):
        return [(f"{n}′{fmt_pt(q)}", None) for n, q in zip(names, images[key])]

    def panel(c, lines, col):
        """Writes the rule and the point list in the side panel."""
        x0 = 572
        for i, (s, cc) in enumerate(lines):
            c.text(x0, 50 + i * 24, s, size=15, color=cc or col, anchor="start")

    @wt.step("Start with triangle ABC", "The blue triangle has corners A(1, 1), B(4, 1), and C(2, 3). Every "
             "move below keeps the same triangle, just somewhere else.",
             math="A(1, 1), B(4, 1), C(2, 3)")
    def _(c, p):
        draw(c, p, tri, ORIG)
        panel(c, [(f"{n}{fmt_pt(q)}", ORIG) for n, q in zip(names, tri)] + [("", None), ("AB = 3", ORIG),
                  (f"BC ≈ {sides[1]:.2f}", ORIG), (f"CA ≈ {sides[2]:.2f}", ORIG)], ORIG)

    @wt.step("Translate: slide", f"Slide every point {shift[0]} right and {shift[1]} up. The arrows are all the "
             "same length and point the same way.",
             math=f"(x, y) \\to (x + {shift[0]}, y + {shift[1]})", fresh=True)
    def _(c, p):
        draw(c, p, tri, ORIG, coords=False)
        for a, b in zip(tri, images["t"]):
            p.vector(*a, *b, color=TRANS, width=2, dash="6 4")
        draw(c, p, images["t"], TRANS, "′")
        panel(c, [("slide", None), (f"x + {shift[0]}, y + {shift[1]}", None), ("", None)] + coords_of("t"), TRANS)

    @wt.step("Reflect: flip over the x-axis", "Flip the triangle over the x-axis like a pancake. Each point "
             "keeps its x and flips the sign of y. The order A, B, C now runs the other way around.",
             math="(x, y) \\to (x, -y)", fresh=True)
    def _(c, p):
        p.hline(0, color=REFL, width=3, dash=None)
        draw(c, p, tri, ORIG, coords=False)
        for a, b in zip(tri, images["f"]):
            p.segment(*a, *b, color=REFL, width=1.6, dash="4 4")
        draw(c, p, images["f"], REFL, "′")
        panel(c, [("flip", None), ("mirror: x-axis", None), ("", None)] + coords_of("f"), REFL)

    @wt.step("Rotate: turn 90° about the origin", "Turn the triangle a quarter turn counterclockwise around "
             "the origin. Each point stays the same distance from O.",
             math="(x, y) \\to (-y, x)", fresh=True)
    def _(c, p):
        draw(c, p, tri, ORIG, coords=False)
        for a, b in zip(tri, images["r"]):
            r = math.hypot(*a)
            a0 = math.degrees(math.atan2(a[1], a[0]))
            O = p.px(0, 0)
            c.arc(*O, p.length(r), a0 + 4, a0 + 86, color=ROT, width=1.8, arrow=True, dash="5 4")
        A, A2 = p.px(*tri[0]), p.px(*images["r"][0])
        O = p.px(0, 0)
        c.line(*O, *A, color=ROT, width=1.4)
        c.line(*O, *A2, color=ROT, width=1.4)
        draw(c, p, images["r"], ROT, "′", nudge={"A": (-1, 0.6)})
        c.text(O[0] - 10, O[1] + 14, "O", size=14, math=True, weight="bold", anchor="end")
        panel(c, [("turn 90°", None), ("center O(0, 0)", None), ("", None)] + coords_of("r"), ROT)

    @wt.step("Compare all three", "Slide, flip, or turn: the side lengths and angles never change. Each "
             "image is congruent to ABC. Only its position, and for the flip its facing, change.",
             math=f"AB = A′B′ = 3, BC = B′C′ \\approx {sides[1]:.2f}, CA = C′A′ \\approx {sides[2]:.2f}", fresh=True)
    def _(c, p):
        draw(c, p, tri, ORIG, coords=False)
        draw(c, p, images["t"], TRANS, "′", coords=False)
        draw(c, p, images["f"], REFL, "′", coords=False)
        draw(c, p, images["r"], ROT, "′", coords=False, nudge={"A": (-1, 0.6)})
        for pts, col in ((tri, ORIG), (images["t"], TRANS), (images["f"], REFL), (images["r"], ROT)):
            A, B = p.px(*pts[0]), p.px(*pts[1])
            m = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
            q = away(m, p.px(*centroid(pts)), 13)
            c.text(q[0], q[1], "3", size=13, color=col, halo=True, weight="bold")
        panel(c, [("original", ORIG), ("slide", TRANS), ("flip", REFL), ("turn", ROT), ("", None),
                  ("all congruent", theme.INK)], theme.INK)

    return wt
