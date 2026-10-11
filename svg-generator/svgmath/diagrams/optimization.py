"""Optimization: the biggest open box from a square sheet."""

from __future__ import annotations

from .. import theme
from ..annotate import dimension
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._calculus_tools import num, tangent

SIDE = 12.0


def V(x: float) -> float:
    return x * (SIDE - 2 * x) ** 2


def dV(x: float) -> float:
    return (SIDE - 2 * x) * (SIDE - 6 * x)


@diagram("optimization-box", "Optimization: The Biggest Box", "Calculus")
def optimization_box() -> Walkthrough:
    xbest = SIDE / 6
    vbest = V(xbest)
    trials = [1, 2, 3, 4, 5]

    wt = Walkthrough(
        "optimization-box", "Optimization: The Biggest Box", "Calculus",
        concept="V(x) = x(12 - 2x)^2, V'(x) = (12 - 2x)(12 - 6x) = 0 \\implies x = 2",
        summary="Cut squares from the corners of a 12 by 12 sheet and fold up the sides. Write the volume as a "
                "function of the cut, then find where its slope is zero.",
        width=720, height=440, level="301",
    )
    U = 13  # pixels per inch on the sheet and box drawings
    SX, SY = 64, 46  # top-left of the sheet

    @wt.setup
    def _(c):
        p = Plane(c, box=(390, 40, 300, 340), x=(-0.3, 6.4), y=(-12, 150))
        p.grid(step=1, ystep=25)
        p.axes(step=1, ystep=50, ylabel="V")
        return p

    @wt.step("Cut the corners", "Start with a 12 × 12 sheet of cardboard. Cut a square of side x from "
             "each corner. Here x = 2, but x can be anything from 0 to 6.",
             math="sheet 12 \\times 12, cut x \\times x at each corner")
    def _(c, p):
        x = xbest
        S = SIDE * U
        k = x * U
        c.rect(SX, SY, S, S, color=theme.INK, fill=theme.fill(theme.SKY, "22"), width=2)
        for cx, cy in ((SX, SY), (SX + S - k, SY), (SX, SY + S - k), (SX + S - k, SY + S - k)):
            c.rect(cx, cy, k, k, color=theme.RED, fill=theme.fill(theme.RED, "44"), width=1.5, dash="4 3")
        # fold lines
        for t in (k, S - k):
            c.line(SX + k, SY + t, SX + S - k, SY + t, color=theme.SOFT_INK, width=1, dash="3 4")
            c.line(SX + t, SY + k, SX + t, SY + S - k, color=theme.SOFT_INK, width=1, dash="3 4")
        dimension(c, (SX, SY), (SX + S, SY), "12", offset=14, color=theme.INK)
        dimension(c, (SX, SY + S), (SX, SY), "12", offset=14, color=theme.INK)
        c.text(SX + S - k / 2, SY + S - k / 2, "x", size=15, color=theme.RED, math=True)
        c.text(SX + k / 2, SY + k / 2, "x", size=15, color=theme.RED, math=True)
        c.text(SX + S / 2, SY + S / 2, "12 - 2x", size=15, color=theme.BLUE, math=True, halo=True)

    @wt.step("Fold up the sides", "Fold along the dashed lines. The box is x tall with a square floor "
             "12 − 2x wide, so its volume is x times the floor area.",
             math="V(x) = x(12 - 2x)^2")
    def _(c, p):
        x = xbest
        w, h = (SIDE - 2 * x) * U, x * U
        d = w * 0.45  # oblique depth
        bx, by = 70, 330  # front-bottom-left corner
        front = [(bx, by), (bx + w, by), (bx + w, by - h), (bx, by - h)]
        top_back = [(bx + d, by - h - d), (bx + w + d, by - h - d)]
        c.polygon([(bx + d, by - d), (bx + w + d, by - d), (bx + w + d, by - h - d), (bx + d, by - h - d)],
                  color=theme.MUTED, fill=theme.fill(theme.SKY, "22"), width=1.2, dash="4 3")
        c.polygon([(bx, by), (bx + w, by), (bx + w + d, by - d), (bx + d, by - d)], color=theme.BLUE,
                  fill=theme.fill(theme.BLUE, "33"), width=1.5)
        side = [(bx + w, by), (bx + w + d, by - d), (bx + w + d, by - h - d), (bx + w, by - h)]
        c.polygon(side, color="none", fill=theme.PAPER)
        c.polygon(side, color=theme.INK, fill=theme.fill(theme.SKY, "55"), width=1.8)
        c.polygon(front, color="none", fill=theme.PAPER)
        c.polygon(front, color=theme.INK, fill=theme.fill(theme.SKY, "44"), width=1.8)
        c.line(bx, by - h, top_back[0][0], top_back[0][1], color=theme.INK, width=1.8)
        c.line(top_back[0][0], top_back[0][1], top_back[1][0], top_back[1][1], color=theme.INK, width=1.8)
        c.line(bx + w + d, by - h - d, bx + w, by - h, color=theme.INK, width=1.8)
        c.text(bx - 8, by - h / 2, "x", size=15, color=theme.RED, math=True, anchor="end")
        c.text(bx + w / 2, by + 16, "12 - 2x", size=15, color=theme.BLUE, math=True)
        c.text(bx + w + d / 2 + 12, by - d / 2 + 4, "12 - 2x", size=15, color=theme.BLUE, math=True,
               anchor="start")
        c.text(bx + w / 2 + d / 2, by - h - d - 16, f"x = 2: V = 2 \\cdot 8^2 = {num(V(2))}", size=14,
               color=theme.PURPLE, math=True)

    @wt.step("Try a few cuts", "Compute the volume for x = 1 through 5 and plot each one. Small cuts "
             "make a flat tray, big cuts make a tall skinny tower. The best is somewhere between.",
             math="V(1) = 100, V(2) = 128, V(3) = 108, V(4) = 64, V(5) = 20")
    def _(c, p):
        for x in trials:
            p.point(x, V(x), None, color=theme.PURPLE, r=5)
            if c.is_new:
                X, Y = p.px(x, V(x))
                c.text(X, Y - 14 if x != 2 else Y - 16, num(V(x)), size=13, color=theme.PURPLE, math=True,
                       halo=True)

    @wt.step("Draw the volume curve", "Every cut between 0 and 6 gives a volume. At x = 0 the box has no "
             "height, and at x = 6 it has no floor, which makes it more of a sculpture.",
             math="V(0) = 0, V(6) = 0")
    def _(c, p):
        p.plot(V, 0, 6, color=theme.PURPLE)
        c.math(p.X(4.4), p.Y(V(4.4)) - 30, "V(x)", size=16, color=theme.PURPLE, anchor="start", halo=True)

    @wt.step("Find the flat top", "At the peak the slope is zero. Set V'(x) = 0: the factor 12 − 6x is "
             "zero at x = 2, which gives the biggest box, 128 cubic inches.",
             math=f"V'(x) = (12 - 2x)(12 - 6x) = 0 \\implies x = 2, V = {num(vbest)}")
    def _(c, p):
        tangent(p, xbest, vbest, 0, half=70, color=theme.GREEN, width=3)
        p.segment(xbest, 0, xbest, vbest, color=theme.GREEN, dash="4 4", width=1.4)
        X, Y = p.px(xbest, vbest)
        c.dot(X, Y, r=7, color=theme.GREEN)
        c.text(X - 68, Y - 13, "slope 0", size=13, color=theme.GREEN, anchor="start", halo=True)
        c.label_box(p.X(4.6), p.Y(122), f"max: x = 2, V = {num(vbest)}", color=theme.GREEN, border=theme.GREEN,
                    size=14)

    return wt
