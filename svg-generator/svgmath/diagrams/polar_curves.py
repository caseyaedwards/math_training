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


def polar_setup(c, title: str):
    """Draws the polar grid on the left and an r-against-theta graph on the right."""
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
    for k in (2, 3, 4):
        d = math.radians(-45)
        X, Y = L.px(k / 4 * math.cos(d), k / 4 * math.sin(d))
        c.text(X + 3, Y + 9, num(k / 4), size=11, color=theme.SOFT_INK, anchor="start", halo=True)
    R = Plane(c, box=(470, 90, 226, 250), x=(0, 2 * math.pi + 0.15), y=(-1.25, 1.25))
    R.axes(xlabel="\\theta", ylabel="", step=math.pi / 2, ystep=1, xfmt=lambda v: pi_label(v, 2))
    X, Y = R.px(0, 1.25)
    c.text(X + 8, Y - 4, "r", size=16, math=True, anchor="start")
    c.text(R.left + R.w / 2, 58, title, size=14, color=theme.SOFT_INK, math=True)
    return {"L": L, "R": R}


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
        return polar_setup(c, "r = cos 2θ against θ")

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


def rose3(t: float) -> float:
    return math.cos(3 * t)


@diagram("polar-rose-odd", "Rose Curve with an Odd Number of Petals", "Trigonometry")
def polar_rose_odd() -> Walkthrough:
    S = math.pi / 6
    wt = Walkthrough(
        "polar-rose-odd", "Rose Curve with an Odd Number of Petals", "Trigonometry",
        concept="r = cos(3\\theta): 3 petals, traced twice in one full turn",
        summary="The rose r = cos 3θ has three petals, not six. Half a turn already draws all three, and the "
                "second half turn walks over the same petals again.",
        width=720, height=440, level="201",
    )
    parts = [
        (0, S, theme.BLUE, "θ: 0 to 30°, r from 1 to 0"),
        (S, 3 * S, theme.ORANGE, "θ: 30° to 90°, r < 0"),
        (3 * S, 5 * S, theme.GREEN, "θ: 90° to 150°, r > 0"),
        (5 * S, 6 * S, theme.BLUE, "θ: 150° to 180°, r < 0"),
    ]

    @wt.setup
    def _(c):
        return polar_setup(c, "r = cos 3θ against θ")

    def trace(c, d, i, dash=None, width=3.5):
        a, b, col, _ = parts[i]
        d["L"].polar(rose3, a, b, color=col, width=width, n=200, dash=dash)
        d["R"].plot(rose3, a, b, color=col, width=2.6, dash=dash)

    @wt.step("Start the first petal",
             "At θ = 0, r = cos 0 = 1. By θ = 30°, 3θ = 90° and r drops to 0. That is half a petal, "
             "pointing right.",
             math="\\theta: 0 \\to 30°, r: 1 \\to 0")
    def _(c, d):
        trace(c, d, 0)
        c.dot(*d["L"].px(1, 0), r=5, color=theme.BLUE)

    @wt.step("Negative r draws a petal at 240°",
             "From 30° to 90°, r is negative, so each point lands across the center. The petal "
             "appears down and to the left, centered on 60° + 180° = 240°.",
             math="\\theta = 60°: r = cos 180° = -1 \\to direction 240°")
    def _(c, d):
        trace(c, d, 1)
        L = d["L"]
        a = math.radians(240)
        c.dot(*L.px(math.cos(a), math.sin(a)), r=5, color=theme.ORANGE)
        if c.is_new:
            c.arrow(*L.px(0, 0), *L.px(0.5 * math.cos(math.radians(60)), 0.5 * math.sin(math.radians(60))),
                    color=theme.SOFT_INK, width=1.6, dash="5 4")
            X, Y = L.px(0.3, 0.52)
            c.text(X, Y, "θ = 60°", size=13, color=theme.SOFT_INK, anchor="start", halo=True)

    @wt.step("Positive again at 120°",
             "From 90° to 150°, r is positive and the curve draws a petal centered on 120°.",
             math="\\theta = 120°: r = cos 360° = 1")
    def _(c, d):
        trace(c, d, 2)
        L = d["L"]
        a = math.radians(120)
        c.dot(*L.px(math.cos(a), math.sin(a)), r=5, color=theme.GREEN)

    @wt.step("Half a turn finishes the rose",
             "From 150° to 180°, r is negative and closes the first petal from below. After only half a "
             "turn, all three petals are done.",
             math="\\theta = 180°: r = cos 540° = -1 \\to the point (1, 0)")
    def _(c, d):
        trace(c, d, 3)

    @wt.step("The second half retraces",
             "From 180° to 360°, cos 3θ just repeats with the sign flipped, and a flipped r in the opposite "
             "direction is the same point. The pen goes over the same three petals again. Odd n gives n "
             "petals, even n gives 2n.",
             math="r(\\theta + \\pi) = -r(\\theta) \\implies same point")
    def _(c, d):
        d["R"].plot(rose3, math.pi, 2 * math.pi, color=theme.SOFT_INK, width=2, dash="5 4")
        d["L"].polar(rose3, math.pi, 2 * math.pi, color=theme.INK, width=1.4, n=300, dash="4 5")
        L = d["L"]
        for k, ang in enumerate((0, 120, 240), 1):
            a = math.radians(ang)
            X, Y = L.px(0.6 * math.cos(a), 0.6 * math.sin(a))
            col = (theme.BLUE, theme.GREEN, theme.ORANGE)[k - 1]
            c.circle(X, Y, 13, color=col, fill=theme.PAPER, width=2)
            c.text(X, Y, str(k), size=14, weight="bold", color=col)
        X, Y = d["R"].px(1.5 * math.pi, -1.15)
        c.text(X, Y + 22, "second lap", size=12, color=theme.SOFT_INK, halo=True)

    return wt
