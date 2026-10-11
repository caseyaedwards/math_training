"""Graphs of sine: unwrapping the unit circle and transforming the wave."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import angle_mark, brace, dimension
from ..plane import Plane, pi_label
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._trigkit import maybe_faded, num

SIN = theme.RED
ANG = theme.ORANGE
TAU = 2 * math.pi


@diagram("sine-from-circle", "Sine Wave from the Unit Circle", "Trigonometry")
def sine_from_circle() -> Walkthrough:
    wt = Walkthrough(
        "sine-from-circle", "Sine Wave from the Unit Circle", "Trigonometry",
        concept="y = sin \\theta is the height of the point at angle \\theta",
        summary="Walk a point around the unit circle and record its height at each angle. Laid out flat, "
                "those heights trace the sine wave.",
        width=720, height=340, level="201",
    )
    th0 = math.pi / 3
    YR = (-1.3, 1.3)

    @wt.setup
    def _(c):
        L = Plane(c, box=(8, 24, 300, 300), x=(-1.25, 1.25), y=YR, equal=True)
        L.axes(xlabel="", ylabel="", ticks=False, arrows=False, color=theme.MUTED)
        L.circle(0, 0, 1, color=theme.INK, width=2)
        R = Plane(c, box=(336, 24, 344, 300), x=(-0.25, TAU + 0.2), y=YR)
        R.axes(xlabel="\\theta", ylabel="", step=math.pi / 2, ystep=1, xfmt=lambda v: pi_label(v, 2))
        return {"L": L, "R": R}

    def carry(c, d, th, color=SIN, width=4, dot=6, label=None, faint=False):
        L, R = d["L"], d["R"]
        P = L.px(math.cos(th), math.sin(th))
        F = L.px(math.cos(th), 0)
        G = R.px(th, math.sin(th))
        B = R.px(th, 0)
        c.line(*F, *P, color=color, width=width)
        c.dot(*P, r=dot, color=theme.INK)
        c.line(*P, *G, color=color, width=1.2, dash="4 4", opacity=0.6 if faint else 1)
        c.line(*B, *G, color=color, width=width)
        c.dot(*G, r=dot, color=color)
        return P, G

    @wt.step("Pick an angle on the circle",
             "Start at angle θ = π/3 (60°) on the unit circle. The graph on the right uses θ as its "
             "horizontal axis, measured in radians.",
             math="\\theta = \\pi/3 \\approx 1.047")
    def _(c, d):
        L = d["L"]
        with maybe_faded(c, not c.is_new, 0.35):
            o, P = L.px(0, 0), L.px(math.cos(th0), math.sin(th0))
            c.line(*o, *P, color=theme.GREEN, width=3)
            angle_mark(c, o, L.px(1, 0), P, r=26, label="π/3", color=ANG, label_r=44)
            c.dot(*P, r=6, color=theme.INK)

    @wt.step("Measure the height",
             f"The height of the point above the horizontal axis is sin θ. At π/3 it is √3/2 ≈ "
             f"{num(math.sin(th0))}.",
             math=f"sin(\\pi/3) = √3/2 \\approx {num(math.sin(th0))}")
    def _(c, d):
        L = d["L"]
        with maybe_faded(c, not c.is_new, 0.35):
            P = L.px(math.cos(th0), math.sin(th0))
            F = L.px(math.cos(th0), 0)
            c.line(*F, *P, color=SIN, width=4)
            c.text(F[0] + 8, (F[1] + P[1]) / 2, "sin θ", size=15, color=SIN, math=True, anchor="start", halo=True)

    @wt.step("Carry the height across",
             "Copy that same height to the graph, standing at θ = π/3 on the horizontal axis. The dashed "
             "line keeps the height honest.",
             math=f"(\\theta, sin \\theta) = (\\pi/3, {num(math.sin(th0))})")
    def _(c, d):
        with maybe_faded(c, not c.is_new, 0.35):
            P, G = carry(c, d, th0)
            if c.is_new:
                c.text(G[0] + 8, G[1] - 12, f"(π/3, {num(math.sin(th0))})", size=13, color=SIN,
                       anchor="start", halo=True)

    @wt.step("Repeat for many angles",
             "Do the same every π/4. The heights rise to 1 at π/2, fall to 0 at π, reach −1 at 3π/2, "
             "and return to 0 at 2π.",
             math="sin 0 = 0, sin(\\pi/2) = 1, sin \\pi = 0, sin(3\\pi/2) = -1, sin 2\\pi = 0")
    def _(c, d):
        L, R = d["L"], d["R"]
        with maybe_faded(c, not c.is_new, 0.45):
            for k in range(9):
                th = k * math.pi / 4
                P, G = carry(c, d, th, color=theme.BLUE, width=2.5, dot=4, faint=True)
                spots = {0: (1.1, -0.13), 2: (-0.17, 1.12), 4: (-1.1, -0.13), 6: (-0.2, -1.12)}
                if k in spots:
                    X, Y = L.px(*spots[k])
                    c.text(X, Y, pi_label(th, 2), size=13, color=theme.BLUE, halo=True)

    @wt.step("Connect the dots",
             "Join the heights with a smooth curve. The wave repeats every 2π because the point "
             "keeps going around the same circle, like a hamster on a wheel.",
             math="y = sin \\theta, period 2\\pi, range [-1, 1]")
    def _(c, d):
        R = d["R"]
        R.plot(math.sin, 0, TAU, color=SIN, width=3)
        X, Y = R.px(math.pi / 2, 1)
        c.text(X, Y - 14, "max 1", size=13, color=SIN, halo=True)
        X, Y = R.px(3 * math.pi / 2, -1)
        c.text(X, Y + 16, "min −1", size=13, color=SIN, halo=True)
        X, Y = R.px(TAU * 0.78, 0.8)
        c.text(X, Y, "y = sin θ", size=17, color=SIN, math=True, halo=True)

    return wt


@diagram("sinusoid-transformations", "Amplitude, Period, and Phase Shift", "Trigonometry")
def sinusoid() -> Walkthrough:
    A, B, Cs = 2.0, 3.0, math.pi / 2
    shift = Cs / B
    period = TAU / B

    def f0(x):
        return math.sin(x)

    def f1(x):
        return A * math.sin(x)

    def f2(x):
        return A * math.sin(B * x)

    def f3(x):
        return A * math.sin(B * x - Cs)

    wt = Walkthrough(
        "sinusoid-transformations", "Amplitude, Period, and Phase Shift", "Trigonometry",
        concept="y = A sin(B(x - h)): amplitude |A|, period 2\\pi/B, shift h",
        summary="Build y = 2 sin(3x − π/2) from y = sin x one change at a time: stretch it taller, squeeze it "
                "narrower, then slide it right.",
        width=720, height=380, level="201",
    )
    AMP, PER, SH = theme.BLUE, theme.ORANGE, theme.GREEN
    curves = [(f0, theme.INK), (f1, AMP), (f2, PER), (f3, SH)]

    @wt.setup
    def _(c):
        p = Plane(c, box=(48, 30, 632, 320), x=(-0.35, TAU + 0.25), y=(-2.7, 2.7))
        p.grid(step=math.pi / 6, ystep=1)
        p.axes(xlabel="x", ylabel="", step=math.pi / 6, ystep=1, xfmt=lambda v: pi_label(v, 6))
        return p

    def curve(c, p, i, label, at):
        f, col = curves[i]
        with maybe_faded(c, not c.is_new, 0.28):
            p.plot(f, -0.35, TAU + 0.25, color=col, width=3 if c.is_new else 2)
        if c.is_new:
            c.text(*p.px(*at), label, size=16, color=col, math=True, halo=True)

    @wt.step("Start with y = sin x",
             "The basic wave goes from −1 to 1 and repeats every 2π. Every other sine wave is this one, "
             "stretched, squeezed, or slid.",
             math="y = sin x: amplitude 1, period 2\\pi")
    def _(c, p):
        curve(c, p, 0, "y = sin x", (2.75, 1.2))
        if c.is_new:
            dimension(c, p.px(TAU, -1.3), p.px(0, -1.3), "period 2π", offset=0.01, color=theme.INK, size=14)

    @wt.step("Stretch up by 2",
             "Multiply the output by 2. Every height doubles, so the peaks reach 2 and the troughs reach "
             "−2. The period does not change.",
             math="y = 2 sin x: amplitude 2")
    def _(c, p):
        curve(c, p, 1, "y = 2 sin x", (2.85, 1.95))
        if c.is_new:
            X0, Y0 = p.px(math.pi / 2, 1)
            X1, Y1 = p.px(math.pi / 2, 2)
            c.arrow(X0, Y0 - 4, X1, Y1 + 6, color=AMP, width=2)
            c.text(X0 + 8, (Y0 + Y1) / 2, "×2", size=14, color=AMP, anchor="start", halo=True)
            brace(c, *p.px(3 * math.pi / 2 + 0.12, 0), *p.px(3 * math.pi / 2 + 0.12, -2),
                  label="amplitude 2", color=AMP, depth=10, math_label=False, size=14)

    @wt.step("Squeeze sideways by 3",
             f"Replace x with 3x. The wave runs three times as fast, so one full cycle fits in "
             f"2π/3 ≈ {num(period, 3)} instead of 2π.",
             math=f"y = 2 sin 3x: period 2\\pi/3 \\approx {num(period, 3)}")
    def _(c, p):
        curve(c, p, 2, "y = 2 sin 3x", (4.45, 2.45))
        if c.is_new:
            dimension(c, p.px(0, 2.3), p.px(period, 2.3), "period 2π/3", offset=0.01, color=PER, size=14)

    @wt.step("Slide right by π/6",
             "Factor the inside: 3x − π/2 = 3(x − π/6). The minus sign means the wave slides right by "
             "π/6, not left. Every peak moves over by the same amount.",
             math="2 sin(3x - \\pi/2) = 2 sin(3(x - \\pi/6))")
    def _(c, p):
        curve(c, p, 3, "y = 2 sin(3x − π/2)", (5.1, -2.45))
        if c.is_new:
            for k in range(3):
                x0 = math.pi / 6 + k * period
                c.arrow(*p.px(x0 + 0.04, 2.3), *p.px(x0 + shift - 0.02, 2.3), color=SH, width=2.2)
                c.text(*p.px(x0 + shift / 2, 2.55), "π/6", size=13, color=SH, math=True, halo=True)

    @wt.step("Read the final wave",
             "The final wave has amplitude 2, period 2π/3, and starts its first cycle at x = π/6. "
             "Three knobs, one wave.",
             math="y = 2 sin(3x - \\pi/2): amplitude 2, period 2\\pi/3, shift \\pi/6 right", fresh=True)
    def _(c, p):
        with c.group(opacity=0.3):
            p.plot(f0, -0.35, TAU + 0.25, color=theme.INK, width=2)
        p.plot(f3, -0.35, TAU + 0.25, color=SH, width=3)
        X, Y = p.px(shift, 0)
        c.arrow(*p.px(0, 0.4), *p.px(shift, 0.4), color=SH, width=2.2)
        c.text(*p.px(shift / 2, 0.72), "shift π/6", size=13, color=SH, halo=True)
        c.dot(X, Y, r=6, color=SH)
        X2, Y2 = p.px(shift + period, 0)
        c.dot(X2, Y2, r=6, color=SH)
        dimension(c, p.px(shift + period, -2.3), p.px(shift, -2.3), "one cycle 2π/3", offset=0.01,
                  color=PER, size=14)
        peak = shift + period / 4
        c.arrow(*p.px(peak, 0.06), *p.px(peak, 1.94), color=AMP, width=2, both=True)
        c.text(*p.px(peak, 2.42), "amplitude 2", size=14, color=AMP, halo=True)
        c.text(*p.px(5.1, -2.45), "y = 2 sin(3x − π/2)", size=16, color=SH, math=True, halo=True)

    return wt
