"""Polar coordinates and a four-petal rose traced one stretch at a time."""

from __future__ import annotations

import math

from .. import theme
from ..plane import Plane, pi_label
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._trigkit import num

Q = math.pi / 4


def rose(t: float) -> float:
    return math.cos(2 * t)


# stretches of theta and their colors; each one draws one petal or half petal
STRETCHES = [
    (0, Q, theme.BLUE),
    (Q, 3 * Q, theme.ORANGE),
    (3 * Q, 5 * Q, theme.GREEN),
    (5 * Q, 7 * Q, theme.PURPLE),
    (7 * Q, 8 * Q, theme.BLUE),
]


@diagram("polar-rose", "Polar Coordinates and a Rose Curve", "Trigonometry")
def polar_rose() -> Walkthrough:
    wt = Walkthrough(
        "polar-rose", "Polar Coordinates and a Rose Curve", "Trigonometry",
        concept="r = cos(2\\theta), (r, \\theta) \\to (r cos \\theta, r sin \\theta)",
        summary="A polar point is a direction θ and a distance r. Tracing r = cos 2θ as θ sweeps a full turn "
                "draws a rose with four petals, including two drawn backward when r is negative.",
        width=720, height=440, level="201",
    )

    @wt.setup
    def _(c):
        L = Plane(c, box=(8, 12, 420, 416), x=(-1.25, 1.25), y=(-1.22, 1.22), equal=True)
        o = L.px(0, 0)
        for k in range(1, 5):
            r = k / 4
            L.circle(0, 0, r, color=theme.GRID if k < 4 else theme.MUTED, width=1.2)
        for k in range(12):
            a = k * math.pi / 6
            c.line(*o, *L.px(math.cos(a), math.sin(a)), color=theme.GRID, width=1.2)
            X, Y = L.px(1.12 * math.cos(a), 1.1 * math.sin(a))
            c.text(X, Y, f"{30 * k}°", size=12, color=theme.SOFT_INK)
        for k in (1, 2, 3, 4):
            d = math.radians(-45)
            X, Y = L.px(k / 4 * math.cos(d), k / 4 * math.sin(d))
            c.text(X + 3, Y + 9, num(k / 4), size=11, color=theme.SOFT_INK, anchor="start", halo=True)
        R = Plane(c, box=(470, 90, 226, 250), x=(0, 2 * math.pi + 0.15), y=(-1.25, 1.25))
        R.axes(xlabel="\\theta", ylabel="", step=math.pi / 2, ystep=1, xfmt=lambda v: pi_label(v, 2))
        X, Y = R.px(0, 1.25)
        c.text(X + 8, Y - 4, "r", size=16, math=True, anchor="start")
        c.text(R.left + R.w / 2, 58, "r = cos 2θ against θ", size=14, color=theme.SOFT_INK, math=True)
        return {"L": L, "R": R}

    def trace(c, d, a, b, color, width=3.5):
        L, R = d["L"], d["R"]
        L.polar(rose, a, b, color=color, width=width, n=240)
        R.plot(rose, a, b, color=color, width=2.6)

    @wt.step("Read a point in polar coordinates",
             "A polar point gives a direction θ and a distance r from the center. The point (0.5, 30°) "
             "sits halfway out along the 30° ray. Polar grids are just rings and spokes.",
             math="(r, \\theta) = (0.5, 30°) \\to (0.5 cos 30°, 0.5 sin 30°) \\approx (0.433, 0.25)")
    def _(c, d):
        L = d["L"]
        a = math.radians(30)
        o, P = L.px(0, 0), L.px(0.5 * math.cos(a), 0.5 * math.sin(a))
        c.line(*o, *P, color=theme.INK, width=2.5)
        c.dot(*P, r=6, color=theme.INK)
        c.text(P[0] + 4, P[1] - 18, "(0.5, 30°)", size=14, anchor="start", halo=True)
        X, Y = d["R"].px(math.pi / 6, 0.5)
        c.dot(X, Y, r=4.5, color=theme.INK)

    @wt.step("Trace θ from 0 to π/4",
             "Now let r = cos 2θ. At θ = 0, r = 1. As θ grows to 45°, r shrinks to 0, so the curve "
             "pulls into the center. The point from step 1 lies on this path.",
             math="\\theta: 0, 15°, 30°, 45° \\to r: 1, 0.866, 0.5, 0")
    def _(c, d):
        a, b, col = STRETCHES[0]
        trace(c, d, a, b, col)
        L, R = d["L"], d["R"]
        for deg in (0, 15, 30, 45):
            t = math.radians(deg)
            r = rose(t)
            c.dot(*L.px(r * math.cos(t), r * math.sin(t)), r=4.5, color=col)
            c.dot(*R.px(t, r), r=4, color=col)

    @wt.step("Negative r points backward",
             "From 45° to 135°, cos 2θ is negative. A negative r means walk backward through the center, "
             "so at θ = 90° with r = −1 the point lands at the bottom. This stretch draws the bottom petal.",
             math="\\theta = 90°: r = cos 180° = -1 \\to (0, -1)")
    def _(c, d):
        a, b, col = STRETCHES[1]
        trace(c, d, a, b, col)
        L, R = d["L"], d["R"]
        if c.is_new:
            o = L.px(0, 0)
            c.arrow(*o, *L.px(0, 0.55), color=theme.SOFT_INK, width=1.6, dash="5 4")
            c.text(*L.px(0.06, 0.45), "θ = 90°", size=13, color=theme.SOFT_INK, anchor="start", halo=True)
            c.arrow(*o, *L.px(0, -0.97), color=col, width=2.2)
            c.text(*L.px(0.06, -0.6), "r = −1", size=14, color=col, anchor="start", halo=True)
        c.dot(*L.px(0, -1), r=5, color=col)
        X, Y = R.px(math.pi / 2, -1)
        c.dot(X, Y, r=4, color=col)
        c.text(X, Y + 14, "r < 0", size=12, color=col, halo=True)

    @wt.step("Finish the full turn",
             "Keep going. From 135° to 225°, r is positive again and draws the left petal. From 225° to "
             "315°, r is negative and draws the top petal. The last 45° closes the right petal.",
             math="r > 0: right and left petals; r < 0: bottom and top petals")
    def _(c, d):
        for a, b, col in STRETCHES[2:]:
            trace(c, d, a, b, col)

    @wt.step("Count the petals",
             "Four petals for r = cos 2θ. For r = cos nθ the rule is 2n petals when n is even and n "
             "petals when n is odd. Roses, unlike gardeners, follow rules.",
             math="r = cos(n\\theta): 2n petals (n even), n petals (n odd)")
    def _(c, d):
        L = d["L"]
        spots = [((0.62, 0.0), theme.BLUE), ((0.0, -0.62), theme.ORANGE), ((-0.62, 0.0), theme.GREEN),
                 ((0.0, 0.62), theme.PURPLE)]
        for k, ((x, y), col) in enumerate(spots, 1):
            X, Y = L.px(x, y)
            c.circle(X, Y, 13, color=col, fill=theme.PAPER, width=2)
            c.text(X, Y, str(k), size=14, weight="bold", color=col)

    return wt
