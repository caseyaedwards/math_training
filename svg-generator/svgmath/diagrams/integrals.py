"""Integrals: the fundamental theorem as accumulation, and volumes of revolution by disks."""

from __future__ import annotations

import math

from .. import theme
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._calculus_tools import num, tangent


# ---------------------------------------------------------------------------
# Fundamental theorem of calculus
# ---------------------------------------------------------------------------


@diagram("fundamental-theorem", "Fundamental Theorem of Calculus", "Calculus")
def fundamental_theorem() -> Walkthrough:
    f = lambda t: t / 2 + 1
    A = lambda x: x * x / 4 + x
    strips = [theme.GREEN, theme.SKY, theme.GREEN, theme.SKY]

    wt = Walkthrough(
        "fundamental-theorem", "Fundamental Theorem of Calculus", "Calculus",
        concept="A(x) = \\int_0^x f(t) dt \\implies A'(x) = f(x)",
        summary="Let A(x) be the area under f from 0 to x. Push x to the right and the area grows at a rate "
                "equal to the current height f(x). So the area function is an antiderivative of f.",
        width=660, height=480, level="301",
    )

    @wt.setup
    def _(c):
        top = Plane(c, box=(80, 40, 500, 170), x=(-0.3, 4.6), y=(-0.4, 3.4))
        top.grid(step=0.5, ystep=1)
        top.axes(step=1, ystep=1, xlabel="t", ylabel="")
        top.plot(f, -0.3, 4.6, color=theme.INK)
        c.math(top.X(4.35), top.Y(f(4.35)) - 18, "f(t) = t/2 + 1", size=16, anchor="end", halo=True)
        bot = Plane(c, box=(80, 275, 500, 180), x=(-0.3, 4.6), y=(-0.8, 8.8))
        bot.grid(step=0.5, ystep=2)
        bot.axes(step=1, ystep=2, ylabel="")
        c.text(24, top.Y(1.5), "rate", size=13, color=theme.SOFT_INK, anchor="start")
        c.text(24, top.Y(1.5) + 18, "f(t)", size=15, math=True, anchor="start")
        c.text(24, bot.Y(4.5), "area so far", size=13, color=theme.SOFT_INK, anchor="start")
        c.text(24, bot.Y(4.5) + 18, "A(x)", size=15, color=theme.GREEN, math=True, anchor="start")
        return top, bot

    @wt.step("Shade the area up to x", "Start at t = 0 and shade under f up to x = 1. Call that area A(1). "
             "A trapezoid with sides 1 and 1.5 and width 1 has area 1.25.",
             math=f"A(1) = \\int_0^1 f(t) dt = {num(A(1))}")
    def _(c, pp):
        top, bot = pp
        if c.is_new:
            top.shade_under(f, 0, 1, color=theme.GREEN, opacity=0.35)
            top.vline(1, color=theme.GREEN, dash=None, width=2.5, y0=0, y1=f(1))
            c.text(top.X(0.5), top.Y(0.5), num(A(1)), size=14, color=theme.INK, math=True, halo=True)
            c.text(top.X(1), top.Y(f(1)) - 34, "x = 1", size=14, color=theme.GREEN, math=True, halo=True)
        bot.point(1, A(1), "(1, 1.25)", color=theme.GREEN, offset=(-10, -12), anchor="end", size=14)

    @wt.step("Slide x to the right", "Each extra unit of width adds a strip, and the strips get taller. "
             "Plot the running total below: A(2) = 3, A(3) = 5.25, A(4) = 8.",
             math="A: 1.25 \\to 3 \\to 5.25 \\to 8 (steps 1.75, 2.25, 2.75)")
    def _(c, pp):
        top, bot = pp
        for i in range(4):
            top.shade_under(f, i, i + 1, color=strips[i], opacity=0.3)
            c.text(top.X(i + (0.5 if i < 3 else 0.72)), top.Y(0.5), num(A(i + 1) - A(i)), size=14, color=theme.INK, math=True,
                   halo=True)
        for i in range(2, 5):
            bot.point(i, A(i), f"({i}, {num(A(i))})", color=theme.GREEN, offset=(-10, -12), anchor="end",
                      size=14)

    @wt.step("Connect the running totals", "The area function A(x) = x²/4 + x passes through every dot. "
             "It climbs faster as f gets taller.",
             math="A(x) = x^2/4 + x")
    def _(c, pp):
        top, bot = pp
        bot.plot(A, 0, 4.4, color=theme.GREEN)
        c.math(bot.X(2.55), bot.Y(6.8), "A(x) = x^2/4 + x", size=16, color=theme.GREEN, anchor="end", halo=True)

    @wt.step("Add one thin strip", "Push x from 3 to 3.4. The new sliver is almost a rectangle of height "
             "f(3) = 2.5 and width 0.4, so A grows by about 2.5 × 0.4 = 1.",
             math=f"A(3.4) - A(3) = {num(A(3.4) - A(3))} \\approx f(3) \\cdot 0.4 = 1")
    def _(c, pp):
        top, bot = pp
        if c.is_new:
            top.rect(3, 0, 3.4, f(3), color=theme.ORANGE, fill=theme.fill(theme.ORANGE, "55"), width=2)
            c.text(top.X(3.2), top.Y(f(3.4)) - 14, "0.4", size=13, color=theme.ORANGE, math=True, halo=True)
            bot.segment(3, A(3), 3.4, A(3), color=theme.ORANGE, width=2)
            bot.segment(3.4, A(3), 3.4, A(3.4), color=theme.ORANGE, width=2.5)
            c.text(bot.X(3.4) + 8, bot.Y((A(3) + A(3.4)) / 2), f"+{num(A(3.4) - A(3))}", size=13,
                   color=theme.ORANGE, math=True, anchor="start", halo=True)
        top.segment(3, 0, 3, f(3), color=theme.ORANGE, width=3.5)
        c.text(top.X(3) - 8, top.Y(f(3)) - 16, "f(3) = 2.5", size=13, color=theme.ORANGE, math=True,
               anchor="end", halo=True)

    @wt.step("Height becomes slope", "Shrink the strip and the ratio becomes exact: the slope of A at x is "
             "the height of f at x. Heights 1.5, 2, 2.5 on top match slopes 1.5, 2, 2.5 below.",
             math="A'(x) = f(x), so \\int_a^b f(t) dt = A(b) - A(a)")
    def _(c, pp):
        top, bot = pp
        for x in (1, 2, 3):
            top.segment(x, 0, x, f(x), color=theme.ORANGE, width=3.5)
            tangent(bot, x, A(x), f(x), half=46, color=theme.ORANGE, width=3)
            X, Y = bot.px(x, A(x))
            c.text(X + 14, Y + 16, f"slope {num(f(x))}", size=12, color=theme.ORANGE, anchor="start", halo=True)
            if x < 3:
                c.text(top.X(x) - 6, top.Y(f(x)) - 14, num(f(x)), size=13, color=theme.ORANGE, math=True,
                       anchor="end", halo=True)

    return wt


# ---------------------------------------------------------------------------
# Disk method
# ---------------------------------------------------------------------------


def _disk(p: Plane, x0: float, x1: float, r: float, color, opacity: str = "55", tilt: float = 0.22):
    """Draws a coin-shaped slab of radius r between x0 and x1, seen slightly from the side."""
    if r <= 0:
        return
    c = p.c
    X0, X1, Yc = p.X(x0), p.X(x1), p.Y(0)
    R = r * p.sy
    rx = tilt * R
    c.ellipse(X0, Yc, rx, R, color=color, fill=theme.fill(color, opacity), width=1.2)
    c.rect(X0, Yc - R, X1 - X0, 2 * R, color="none", fill=theme.fill(color, opacity))
    c.line(X0, Yc - R, X1, Yc - R, color=color, width=1.2)
    c.line(X0, Yc + R, X1, Yc + R, color=color, width=1.2)
    c.ellipse(X1, Yc, rx, R, color=color, fill=theme.fill(color, "88"), width=1.2)


@diagram("disk-method", "Volume of Revolution: Disk Method", "Calculus")
def disk_method() -> Walkthrough:
    f = math.sqrt
    a, b = 0.0, 4.0
    exact = math.pi * b * b / 2  # pi * integral of x from 0 to 4

    def left_sum(n):
        dx = (b - a) / n
        return sum(math.pi * f(a + i * dx) ** 2 * dx for i in range(n))

    v8, v16 = left_sum(8), left_sum(16)

    wt = Walkthrough(
        "disk-method", "Volume of Revolution: Disk Method", "Calculus",
        concept="V = \\int_a^b \\pi f(x)^2 dx = \\int_0^4 \\pi x dx = 8\\pi",
        summary="Spin a flat region around the x-axis to get a solid. Slice the solid into thin disks, add "
                "their volumes, and let the disks get thin: the sum becomes an integral.",
        width=700, height=400, level="301",
    )
    PX = 520  # left edge of the tally panel

    @wt.setup
    def _(c):
        p = Plane(c, box=(40, 40, 450, 330), x=(-0.5, 4.8), y=(-2.4, 2.4))
        p.grid(step=0.5, ystep=0.5)
        p.axes(step=1, ystep=1)
        c.text(PX, 40, "volume tally", size=14, color=theme.SOFT_INK, anchor="start", weight="bold")
        return p

    def tally(c, row, s, col):
        c.text(PX, 72 + row * 30, s, size=15, color=col, anchor="start", math=True)

    @wt.step("Start with a flat region", "Shade the region under y = √x from x = 0 to x = 4. It is flat, "
             "like a paper cutout.", math="y = sqrt(x), 0 \\leq x \\leq 4")
    def _(c, p):
        if c.is_new:
            p.shade_under(f, a, b, color=theme.BLUE, opacity=0.3)
        p.plot(f, 0, 4.6, color=theme.BLUE)
        c.math(p.X(4.6), p.Y(f(4.6)) - 18, "y = sqrt(x)", size=16, color=theme.BLUE, anchor="end", halo=True)

    @wt.step("Spin it around the x-axis", "Rotate the cutout a full turn about the x-axis. It sweeps out a "
             "solid shaped like a bullet nose, with a round face of radius 2 at x = 4.",
             math="radius at x = sqrt(x)")
    def _(c, p):
        p.plot(lambda x: -f(x), 0, 4, color=theme.BLUE, dash="7 5" if not c.is_new else None, width=2)
        p.plot(f, 0, 4, color=theme.BLUE, width=2)
        X4, Yc, R = p.X(b), p.Y(0), f(b) * p.sy
        c.ellipse(X4, Yc, 0.22 * R, R, color=theme.BLUE, fill=theme.fill(theme.BLUE, "22"), width=2)
        if c.is_new:
            p.region([(x / 40 * 4, f(x / 40 * 4)) for x in range(41)] +
                     [(x / 40 * 4, -f(x / 40 * 4)) for x in range(40, -1, -1)], color=theme.BLUE, opacity=0.12)
            c.arc(p.X(-0.25), Yc, 26, 110, -110, color=theme.PURPLE, width=2.2, arrow=True)
            c.text(p.X(-0.25) - 32, Yc - 36, "spin", size=13, color=theme.PURPLE, halo=True)
            c.text(X4 + 0.22 * R + 6, Yc - R / 2, "r = 2", size=14, color=theme.BLUE, math=True, anchor="start",
                   halo=True)

    @wt.step("Cut one thin disk", "Slice the solid at x = 2.5 with thickness Δx = 0.5. The slice is a coin: "
             "radius √2.5, face area π · 2.5, volume π · 2.5 · 0.5.",
             math="\\Delta V = \\pi r^2 \\Delta x = \\pi (sqrt(2.5))^2 (0.5) = 1.25\\pi")
    def _(c, p):
        _disk(p, 2.5, 3.0, f(2.5), theme.ORANGE)
        if c.is_new:
            X0, X1, Yc = p.X(2.5), p.X(3.0), p.Y(0)
            R = f(2.5) * p.sy
            c.line(X1 + 22, Yc, X1 + 22, Yc - R, color=theme.ORANGE, width=2)
            c.text(X1 + 28, Yc - R / 2, "r = sqrt(2.5)", size=14, color=theme.ORANGE, math=True, anchor="start",
                   halo=True)
            c.text((X0 + X1) / 2, p.Y(-2.05), "\\Delta x = 0.5", size=14, color=theme.ORANGE, math=True,
                   halo=True)
        tally(c, 0, f"1 disk: 1.25\\pi \\approx {num(1.25 * math.pi, 2)}", theme.ORANGE)

    @wt.step("Stack eight disks", "Fill the solid with eight disks of width 0.5, each sized by the curve "
             "at its left edge. The stack leaves small gaps, so it comes up a bit short.",
             math=f"\\sum \\pi x_i \\cdot 0.5 = 7\\pi \\approx {num(v8, 2)}", fresh=True)
    def _(c, p):
        p.plot(f, 0, 4, color=theme.BLUE, width=1.6)
        p.plot(lambda x: -f(x), 0, 4, color=theme.BLUE, width=1.6)
        for i in range(8):
            _disk(p, i * 0.5, (i + 1) * 0.5, f(i * 0.5), theme.ORANGE, opacity="44")
        tally(c, 0, f"1 disk: 1.25\\pi \\approx {num(1.25 * math.pi, 2)}", theme.ORANGE)
        tally(c, 1, f"8 disks: 7\\pi \\approx {num(v8, 2)}", theme.ORANGE)

    @wt.step("Make the disks thin", "With 16 disks the total is 7.5π. As Δx goes to zero the sum becomes "
             "an integral, and the bullet holds exactly 8π cubic units.",
             math=f"V = \\int_0^4 \\pi x dx = \\pi x^2/2 |_0^4 = 8\\pi \\approx {num(exact, 2)}", fresh=True)
    def _(c, p):
        for i in range(16):
            _disk(p, i * 0.25, (i + 1) * 0.25, f(i * 0.25), theme.PURPLE, opacity="44", tilt=0.18)
        p.plot(f, 0, 4, color=theme.BLUE, width=2)
        p.plot(lambda x: -f(x), 0, 4, color=theme.BLUE, width=2)
        tally(c, 0, f"1 disk: 1.25\\pi \\approx {num(1.25 * math.pi, 2)}", theme.ORANGE)
        tally(c, 1, f"8 disks: 7\\pi \\approx {num(v8, 2)}", theme.ORANGE)
        tally(c, 2, f"16 disks: 7.5\\pi \\approx {num(v16, 2)}", theme.PURPLE)
        tally(c, 3, f"exact: 8\\pi \\approx {num(exact, 2)}", theme.GREEN)

    return wt
