"""The unit circle: coordinates, radians, the Pythagorean identity, and tangent."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import angle_mark, brace, right_angle
from ..plane import Plane, pi_label
from ..registry import diagram
from ..svg import text_width
from ..walkthrough import Walkthrough
from ._trigkit import arc_label, deg_text, maybe_faded, num, polar_px

COS = theme.BLUE
SIN = theme.RED
ANG = theme.ORANGE
TAN = theme.PURPLE

# exact labels for the special angles, as (cos, sin) strings for the first quadrant
_EXACT = {30: ("√3/2", "1/2"), 45: ("√2/2", "√2/2"), 60: ("1/2", "√3/2")}
_FAMILY = {30: theme.ORANGE, 45: theme.GREEN, 60: theme.PURPLE}


def _signed(s: str, v: float) -> str:
    return ("−" + s) if v < 0 else s


@diagram("unit-circle", "The Unit Circle", "Trigonometry")
def unit_circle() -> Walkthrough:
    wt = Walkthrough(
        "unit-circle", "The Unit Circle", "Trigonometry",
        concept="P(\\theta) = (cos \\theta, sin \\theta) on x^2 + y^2 = 1",
        summary="Walk an angle θ around a circle of radius 1. The point where it lands has coordinates "
                "(cos θ, sin θ), so the circle is a lookup table for sine and cosine.",
        width=700, height=460, level="201",
    )
    th = 40.0
    cx, sy = math.cos(math.radians(th)), math.sin(math.radians(th))

    @wt.setup
    def _(c):
        p = Plane(c, box=(20, 22, 660, 416), x=(-1.9, 1.9), y=(-1.21, 1.21), equal=True)
        p.axes(xlabel="x", ylabel="", ticks=False)
        p.circle(0, 0, 1, color=theme.INK, width=2.2)
        for (x, y, s, off, anc) in ((1, 0, "(1, 0)", (8, 14), "start"), (0, 1, "(0, 1)", (10, -14), "start"),
                                    (-1, 0, "(−1, 0)", (-8, 14), "end"), (0, -1, "(0, −1)", (10, 14), "start")):
            p.point(x, y, s, color=theme.INK, r=4, offset=off, anchor=anc, math=False, size=13)
        return p

    @wt.step("Draw a circle of radius 1",
             "Center a circle at the origin with radius 1. Every point on it is exactly 1 away from "
             "the center, which is all the circle has ever wanted.",
             math="x^2 + y^2 = 1")
    def _(c, p):
        a = math.radians(125)
        p.segment(0, 0, math.cos(a), math.sin(a), color=theme.GREEN, width=3)
        p.label(math.cos(a) / 2 - 0.2, math.sin(a) / 2 - 0.06, "r = 1", color=theme.GREEN, size=16)
        p.label(-1.4, -0.85, "x^2 + y^2 = 1", color=theme.INK, size=17)

    @wt.step("A point at angle θ is (cos θ, sin θ)",
             f"Turn {num(th)}° counterclockwise from the positive x-axis. The horizontal leg is "
             f"cos θ and the vertical leg is sin θ.",
             math=f"P({num(th)}°) = (cos {num(th)}°, sin {num(th)}°) \\approx ({num(cx)}, {num(sy)})")
    def _(c, p):
        with maybe_faded(c, not c.is_new, 0.35):
            o, P, F = p.px(0, 0), p.px(cx, sy), p.px(cx, 0)
            c.line(*o, *P, color=theme.GREEN, width=3)
            c.line(*o, *F, color=COS, width=4)
            c.line(*F, *P, color=SIN, width=4)
            right_angle(c, F, o, P, s=11)
            angle_mark(c, o, F, P, r=34, label="\\theta", color=ANG, label_r=50)
            c.dot(*P, r=6, color=theme.INK)
            c.text(P[0] + 10, P[1] - 16, "(cos θ, sin θ)", size=16, math=True, anchor="start", halo=True)
            c.text(P[0] + 10, P[1] + 4, f"≈ ({num(cx)}, {num(sy)})", size=14, color=theme.SOFT_INK,
                   anchor="start", halo=True)
            c.text((o[0] + F[0]) / 2, o[1] + 16, f"cos θ ≈ {num(cx)}", size=14, color=COS, math=True,
                   halo=True)
            c.text(F[0] + 8, (F[1] + P[1]) / 2 + 6, f"sin θ ≈ {num(sy)}", size=14, color=SIN, math=True,
                   anchor="start", halo=True)

    def special(c, p, deg, fam):
        a = math.radians(deg)
        x, y = math.cos(a), math.sin(a)
        col = _FAMILY[fam]
        p.segment(0, 0, x, y, color=col, width=1.6)
        X, Y = p.px(x, y)
        c.dot(X, Y, r=5.5, color=col)
        ex, ey = _EXACT[fam]
        s = f"{deg}°  ({_signed(ex, x)}, {_signed(ey, y)})"
        right = x > 0
        RX, RY = p.px(0.8 * x, 0.8 * y)
        c.text(RX, RY, pi_label(a, 12), size=12, color=col, halo=True)
        LX, LY = p.px(1.09 * x, 1.09 * y)
        c.text(LX + (2 if right else -2), LY, s, size=14, color=col, anchor="start" if right else "end",
               halo=True)

    @wt.step("Learn three special angles",
             "At 30°, 45°, and 60° (π/6, π/4, π/3 in radians), the coordinates are exact. Only three "
             "numbers appear: 1/2, √2/2, and √3/2. Cosine and sine swap them between 30° and 60°.",
             math="P(30°) = (√3/2, 1/2), P(45°) = (√2/2, √2/2), P(60°) = (1/2, √3/2)", fresh=True)
    def _(c, p):
        for d in (30, 45, 60):
            special(c, p, d, d)

    @wt.step("Mirror them into every quadrant",
             "Reflect the three points across the axes. The same three numbers return in every "
             "quadrant, and only the signs change.",
             math="P(180° - \\theta) = (-cos \\theta, sin \\theta), P(360° - \\theta) = (cos \\theta, -sin \\theta)")
    def _(c, p):
        for base in (30, 45, 60):
            for d in (180 - base, 180 + base, 360 - base):
                special(c, p, d, base)

    @wt.step("Read the signs by quadrant",
             "Cosine is the x-coordinate, so it is negative on the left. Sine is the y-coordinate, so it "
             "is negative below. One rhyme to remember: All Students Take Calculus.",
             math="QI (+, +), QII (−, +), QIII (−, −), QIV (+, −)")
    def _(c, p):
        corners = (
            (1.85, 1.15, "end", "QI: cos +, sin +", "All positive"),
            (-1.85, 1.15, "start", "QII: cos −, sin +", "Sine positive"),
            (-1.85, -1.05, "start", "QIII: cos −, sin −", "Tangent positive"),
            (1.85, -1.05, "end", "QIV: cos +, sin −", "Cosine positive"),
        )
        for x, y, anc, s, s2 in corners:
            X, Y = p.px(x, y)
            c.text(X, Y, s, size=15, weight="bold", anchor=anc, color=theme.INK, halo=True)
            c.text(X, Y + 18, s2, size=13, anchor=anc, color=theme.SOFT_INK, halo=True)

    return wt


@diagram("radians", "Radian Measure", "Trigonometry")
def radians() -> Walkthrough:
    wt = Walkthrough(
        "radians", "Radian Measure", "Trigonometry",
        concept="\\theta (radians) = arc length / radius, full turn = 2\\pi",
        summary="A radian is the angle you get when an arc as long as the radius wraps around the circle. "
                "About 6.28 radii fit around the rim, so a full turn is 2π radians.",
        width=700, height=420, level="201",
    )
    CX, CY, R = 220.0, 212.0, 150.0
    one = math.degrees(1)
    full = 2 * math.pi
    left = full - 6

    @wt.setup
    def _(c):
        c.circle(CX, CY, R, color=theme.MUTED, width=2)
        c.dot(CX, CY, r=4, color=theme.INK)
        c.line(450, 40, 450, 380, color=theme.GRID, width=1)
        return None

    def panel(c, i, s, color=theme.INK, size=17):
        c.math(468, 70 + i * 50, s, anchor="start", color=color, size=size)

    @wt.step("Take a circle and its radius",
             "Draw a circle and one radius r. The radius is the ruler for this whole diagram.",
             math="r = radius")
    def _(c):
        c.line(CX, CY, CX + R, CY, color=theme.BLUE, width=3.5)
        c.text(CX + R / 2, CY + 16, "r", size=18, color=theme.BLUE, math=True)
        panel(c, 0, "r = the ruler", color=theme.BLUE)

    @wt.step("Bend the radius onto the rim",
             "Lay a piece of string as long as r along the circle, starting at the right. The arc "
             "has the same length as the radius.",
             math="arc length = r")
    def _(c):
        c.arc(CX, CY, R, 0, one, color=theme.BLUE, width=6)
        x, y = polar_px(CX, CY, R, one)
        c.line(CX, CY, x, y, color=theme.BLUE, width=3.5)
        arc_label(c, CX, CY, R + 30, one / 2, "arc = r", color=theme.BLUE, size=16)
        c.text(CX + 70 * math.cos(math.radians(one + 8)) - 22, CY - 70 * math.sin(math.radians(one + 8)),
               "r", size=18, color=theme.BLUE, math=True, halo=True)

    @wt.step("That angle is one radian",
             f"The angle that cuts off an arc equal to the radius is 1 radian. It is a bit less than "
             f"60°, about {num(one, 1)}°.",
             math=f"1 rad = 180°/\\pi \\approx {num(one, 2)}°")
    def _(c):
        c.arc(CX, CY, 40, 0, one, color="none", fill=theme.fill(ANG, "40"), sector=True)
        c.arc(CX, CY, 40, 0, one, color=ANG, width=2)
        arc_label(c, CX, CY, 62, one / 2, "1 rad", color=ANG, size=16)
        panel(c, 1, f"1 rad \\approx {num(one, 1)}°", color=ANG)

    @wt.step("Count radii around the circle",
             f"Keep laying radius-length arcs end to end. Six fit, with {num(left, 3)} of a radius "
             "left over. The circle does not divide evenly, which is π being π.",
             math=f"6 + {num(left, 3)} = {num(full, 3)} radii")
    def _(c):
        cols = [theme.BLUE, theme.GREEN]
        for k in range(1, 6):
            a0, a1 = k * one, (k + 1) * one
            c.arc(CX, CY, R, a0, a1, color=cols[k % 2], width=6)
        for k in range(1, 7):
            x0, y0 = polar_px(CX, CY, R - 9, k * one)
            x1, y1 = polar_px(CX, CY, R + 9, k * one)
            c.line(x0, y0, x1, y1, color=theme.INK, width=2)
            arc_label(c, CX, CY, R + 24, k * one, str(k), color=theme.INK, size=15, math_text=False)
        c.arc(CX, CY, R, 6 * one, 360, color=theme.RED, width=6)
        arc_label(c, CX, CY, R - 30, (6 * one + 360) / 2, num(left, 2), color=theme.RED, size=14,
                  math_text=False)
        panel(c, 2, f"6 radii + {num(left, 3)} = {num(full, 3)}", color=theme.GREEN)

    @wt.step("A full turn is 2π radians",
             "The exact count is 2π, about 6.283. Half a turn is π radians, which is 180°. Divide by "
             "π and multiply by 180 to switch to degrees.",
             math="2\\pi rad = 360°, \\pi rad = 180°, 1° = \\pi/180 rad")
    def _(c):
        x, y = polar_px(CX, CY, R, 180)
        c.dot(x, y, r=6, color=theme.PURPLE)
        c.text(x - 8, y + 20, "π", size=19, color=theme.PURPLE, math=True, anchor="end", halo=True)
        c.text(CX + R + 10, CY - 16, "0 = 2π", size=16, color=theme.PURPLE, math=True, anchor="start",
               halo=True)
        c.line(CX - R, CY, CX + R, CY, color=theme.PURPLE, width=1.5, dash="6 5")
        panel(c, 3, "\\pi rad = 180°", color=theme.PURPLE)
        panel(c, 4, f"2\\pi rad = 360°", color=theme.PURPLE)
        panel(c, 5, f"1° = \\pi/180 \\approx {num(math.pi / 180, 4)} rad", color=theme.SOFT_INK, size=16)

    return wt


@diagram("pythagorean-identity", "The Pythagorean Identity", "Trigonometry")
def pythagorean_identity() -> Walkthrough:
    wt = Walkthrough(
        "pythagorean-identity", "The Pythagorean Identity", "Trigonometry",
        concept="sin^2 \\theta + cos^2 \\theta = 1",
        summary="The point (cos θ, sin θ) sits on a circle of radius 1. Its right triangle has legs cos θ "
                "and sin θ and hypotenuse 1, so Pythagoras gives sin²θ + cos²θ = 1.",
        width=700, height=410, level="201",
    )
    cx, sy = 0.6, 0.8
    th = math.degrees(math.atan2(sy, cx))
    HYP = theme.GREEN

    @wt.setup
    def _(c):
        p = Plane(c, box=(16, 18, 404, 380), x=(-1.1, 1.5), y=(-1.05, 1.5), equal=True)
        p.axes(xlabel="x", ylabel="", ticks=False)
        p.circle(0, 0, 1, color=theme.MUTED, width=2)
        c.line(436, 30, 436, 390, color=theme.GRID, width=1)
        return p

    def panel(c, i, s, color=theme.INK, size=17):
        c.math(452, 60 + i * 46, s, anchor="start", color=color, size=size)

    def triangle(c, p, x, y):
        o, F, P = p.px(0, 0), p.px(x, 0), p.px(x, y)
        c.line(*o, *P, color=HYP, width=4)
        c.line(*o, *F, color=COS, width=4)
        c.line(*F, *P, color=SIN, width=4)
        right_angle(c, F, o, P, s=11)
        c.dot(*P, r=5.5, color=theme.INK)
        return o, F, P

    @wt.step("Pick a point on the unit circle",
             f"Take the angle θ ≈ {num(th, 2)}°. Its point on the unit circle is (0.6, 0.8), "
             "a 3-4-5 triangle shrunk to fit.",
             math=f"(cos \\theta, sin \\theta) = ({num(cx)}, {num(sy)})")
    def _(c, p):
        o, P = p.px(0, 0), p.px(cx, sy)
        c.line(*o, *P, color=HYP, width=3)
        angle_mark(c, o, p.px(1, 0), P, r=30, label="\\theta", color=ANG, label_r=46)
        c.dot(*P, r=5.5, color=theme.INK)
        c.text(P[0] + 10, P[1] - 12, "(0.6, 0.8)", size=15, anchor="start", halo=True)
        panel(c, 0, f"\\theta \\approx {num(th, 2)}°", color=ANG)

    @wt.step("See the right triangle",
             "Drop a line from the point to the x-axis. The legs are cos θ and sin θ, and the "
             "hypotenuse is the radius, 1.",
             math="legs: cos \\theta = 0.6, sin \\theta = 0.8; hypotenuse: 1")
    def _(c, p):
        o, F, P = triangle(c, p, cx, sy)
        c.text((o[0] + F[0]) / 2, o[1] + 16, "cos θ = 0.6", size=14, color=COS, math=True, halo=True)
        c.text(F[0] + 8, (F[1] + P[1]) / 2, "sin θ = 0.8", size=14, color=SIN, math=True, anchor="start",
               halo=True)
        c.text((o[0] + P[0]) / 2 - 10, (o[1] + P[1]) / 2 - 4, "1", size=17, color=HYP, math=True,
               anchor="end", halo=True)
        panel(c, 1, "cos \\theta = 0.6", color=COS)
        panel(c, 2, "sin \\theta = 0.8", color=SIN)

    @wt.step("Build a square on each side",
             "Put a square on every side of the triangle. The square on cos θ has area 0.36, the square "
             "on sin θ has area 0.64, and the square on the radius has area 1.",
             math=f"cos^2 \\theta = {num(cx * cx)}, sin^2 \\theta = {num(sy * sy)}, 1^2 = 1")
    def _(c, p):
        # square on the cos leg, below the x-axis
        p.region([(0, 0), (cx, 0), (cx, -cx), (0, -cx)], color=COS, opacity=0.2, outline=COS)
        # square on the sin leg, to the right
        p.region([(cx, 0), (cx + sy, 0), (cx + sy, sy), (cx, sy)], color=SIN, opacity=0.2, outline=SIN)
        # square on the hypotenuse, outward (up and to the left)
        nx, ny = -sy, cx
        p.region([(0, 0), (cx, sy), (cx + nx, sy + ny), (nx, ny)], color=HYP, opacity=0.18, outline=HYP)
        p.label(cx / 2, -cx * 0.65, f"cos^2 \\theta = {num(cx * cx)}", color=COS, size=14)
        p.label(cx + sy / 2 + 0.07, 0.12, f"sin^2 \\theta = {num(sy * sy)}", color=SIN, size=14)
        p.label((cx + nx) / 2, (sy + ny) / 2 + 0.05, "1^2 = 1", color=HYP, size=15)
        panel(c, 3, f"cos^2 \\theta = {num(cx * cx)}", color=COS)
        panel(c, 4, f"sin^2 \\theta = {num(sy * sy)}", color=SIN)

    @wt.step("Add the two small squares",
             "The two small squares fill exactly the big one. That is the Pythagorean theorem, "
             "written in trig clothes.",
             math=f"{num(sy * sy)} + {num(cx * cx)} = 1 \\implies sin^2 \\theta + cos^2 \\theta = 1")
    def _(c, p):
        x, y = 452, 60 + 5 * 46
        s = "sin^2 \\theta + cos^2 \\theta = 1"
        c.math(x, y, s, anchor="start", color=HYP, size=20)
        w = text_width(s, 20, "serif")
        c.rect(x - 8, y - 18, w + 16, 36, color=HYP, width=1.5, rx=6)
        c.math(452, y + 40, f"{num(sy * sy)} + {num(cx * cx)} = 1", anchor="start", color=theme.INK, size=17)

    @wt.step("It works in every quadrant",
             "Try θ = 150°. Now cos θ is negative, but squaring removes the sign. The legs still "
             "square to 0.75 and 0.25, which add to 1.",
             math="(-√3/2)^2 + (1/2)^2 = 3/4 + 1/4 = 1", fresh=True)
    def _(c, p):
        a = math.radians(150)
        x, y = math.cos(a), math.sin(a)
        o, F, P = triangle(c, p, x, y)
        angle_mark(c, o, p.px(1, 0), P, r=26, label="150°", color=ANG, label_r=50)
        c.text((o[0] + F[0]) / 2, o[1] + 16, f"cos θ ≈ {num(x)}", size=14, color=COS, math=True, halo=True)
        c.text(P[0] - 6, P[1] - 18, "sin θ = 0.5", size=14, color=SIN, math=True, anchor="start",
               halo=True)
        panel(c, 0, "\\theta = 150°", color=ANG)
        panel(c, 1, f"cos^2 \\theta = (-√3/2)^2 = 0.75", color=COS)
        panel(c, 2, f"sin^2 \\theta = (1/2)^2 = 0.25", color=SIN)
        panel(c, 3, "0.75 + 0.25 = 1", color=HYP)
        c.text(452, 60 + 4 * 46, "Squares never go negative.", color=theme.SOFT_INK, size=15, anchor="start")

    return wt


@diagram("tangent-line-segment", "Tangent on the Unit Circle", "Trigonometry")
def tangent_segment() -> Walkthrough:
    wt = Walkthrough(
        "tangent-line-segment", "Tangent on the Unit Circle", "Trigonometry",
        concept="tan \\theta = sin \\theta / cos \\theta, undefined at \\theta = \\pi/2 + k\\pi",
        summary="Extend the radius until it hits the vertical line x = 1. The height where it hits is "
                "tan θ. As θ nears 90°, the radius runs parallel to the line and the height runs off to "
                "infinity.",
        width=720, height=420, level="201",
    )
    th = 50.0
    t = math.radians(th)
    tv = math.tan(t)
    YR = (-1.9, 1.9)

    @wt.setup
    def _(c):
        L = Plane(c, box=(8, 12, 310, 396), x=(-1.15, 1.8), y=YR, equal=True)
        L.axes(xlabel="", ylabel="", ticks=False, arrows=False)
        L.circle(0, 0, 1, color=theme.MUTED, width=2)
        R = Plane(c, box=(350, 12, 330, 396), x=(-math.pi / 2 - 0.3, 3 * math.pi / 2 + 0.3), y=YR)
        return {"L": L, "R": R}

    def left_pts(L):
        return L.px(0, 0), L.px(math.cos(t), math.sin(t)), L.px(1, 0), L.px(1, tv), L.px(math.cos(t), 0)

    @wt.step("Draw the line x = 1",
             "Draw the vertical line that touches the unit circle at (1, 0). It is called a tangent "
             "line because it only touches, and that is where the name of the function comes from.",
             math="tangent line: x = 1")
    def _(c, d):
        L = d["L"]
        c.line(*L.px(1, YR[0]), *L.px(1, YR[1]), color=theme.INK, width=2)
        c.dot(*L.px(1, 0), r=4.5, color=theme.INK)
        X, Y = L.px(1, YR[0] + 0.2)
        c.text(X + 8, Y, "x = 1", size=15, math=True, anchor="start", halo=True)
        X, Y = L.px(1, 0)
        c.text(X + 8, Y + 14, "(1, 0)", size=13, anchor="start", halo=True)

    @wt.step("Extend the radius to the line",
             f"Turn θ = {num(th)}° and extend the radius until it hits x = 1. The height of the hit "
             f"point is tan θ.",
             math=f"tan {num(th)}° \\approx {num(tv)}")
    def _(c, d):
        L = d["L"]
        o, P, A, T, F = left_pts(L)
        c.line(*o, *T, color=theme.INK, width=1.6, dash="6 4")
        c.line(*o, *P, color=theme.GREEN, width=3)
        c.line(*A, *T, color=TAN, width=5)
        c.dot(*T, r=5, color=TAN)
        angle_mark(c, o, A, P, r=24, label="\\theta", color=ANG, label_r=38)
        c.text(T[0] + 8, (A[1] + T[1]) / 2, "tan θ", size=16, color=TAN, math=True, anchor="start", halo=True)
        c.text(T[0] + 8, (A[1] + T[1]) / 2 + 18, f"≈ {num(tv, 2)}", size=14, color=TAN, anchor="start",
               halo=True)

    @wt.step("Two similar triangles",
             "The small triangle has legs cos θ and sin θ. The big one has legs 1 and tan θ. Same angle, "
             "same shape, so the ratios match.",
             math=f"tan \\theta / 1 = sin \\theta / cos \\theta \\approx {num(math.sin(t))}/{num(math.cos(t))}")
    def _(c, d):
        L = d["L"]
        o, P, A, T, F = left_pts(L)
        c.line(*o, *F, color=COS, width=4)
        c.line(*F, *P, color=SIN, width=4)
        right_angle(c, F, o, P, s=8)
        right_angle(c, A, o, T, s=8)
        c.text((o[0] + F[0]) / 2, o[1] + 14, "cos θ", size=13, color=COS, math=True, halo=True)
        X, Y = L.px(math.cos(t) + 0.03, 0.22)
        c.text(X, Y, "sin θ", size=13, color=SIN, math=True, anchor="start", halo=True)
        brace(c, A[0], o[1] + 26, o[0], o[1] + 26, label="1", color=theme.INK, depth=9, size=15)

    @wt.step("Plot the height against θ",
             "Carry the height tan θ across to a graph, the same way a sine graph is built. At "
             f"θ = {num(t, 3)} rad the graph is {num(tv, 3)} high.",
             math=f"(\\theta, tan \\theta) \\approx ({num(t, 3)}, {num(tv, 3)})")
    def _(c, d):
        L, R = d["L"], d["R"]
        R.axes(xlabel="\\theta", ylabel="", step=math.pi / 2, ystep=1, xfmt=lambda v: pi_label(v, 2))
        with maybe_faded(c, not c.is_new, 1.0):
            R.plot(math.tan, -math.pi / 2 + 0.01, math.pi / 2 - 0.01, color=TAN, width=2.5)
        _, _, _, T, _ = left_pts(L)
        G = R.px(t, tv)
        c.line(T[0], T[1], G[0], G[1], color=TAN, width=1.4, dash="5 4")
        c.line(*R.px(t, 0), *G, color=TAN, width=4)
        c.dot(*G, r=5, color=TAN)
        c.text((R.X(0) + R.X(-math.pi / 2)) / 2, G[1] - 14, f"({num(t, 2)}, {num(tv, 2)})", size=12,
               color=TAN,
               halo=True)

    @wt.step("Asymptotes at ±π/2",
             "As θ nears 90°, the extended radius gets closer to parallel with x = 1 and the hit "
             "point flies off the top. At 90° they never meet, so tan θ is undefined. The pattern "
             "repeats every π.",
             math="tan \\theta = sin \\theta / cos \\theta, cos(\\pi/2) = 0, period \\pi")
    def _(c, d):
        L, R = d["L"], d["R"]
        for k in (-1, 1, 3):
            R.vline(k * math.pi / 2, color=theme.RED, width=1.6, dash="6 5")
        R.plot(math.tan, math.pi / 2 + 0.01, 3 * math.pi / 2 - 0.01, color=TAN, width=2.5)
        X, Y = R.px(math.pi / 2, YR[1] - 0.15)
        c.text(X + 6, Y, "θ = π/2", size=13, color=theme.RED, math=True, anchor="start", halo=True)
        X, Y = R.px(-math.pi / 2, YR[1] - 0.15)
        c.text(X + 6, Y, "−π/2", size=13, color=theme.RED, math=True, anchor="start", halo=True)
        X, Y = R.px(3 * math.pi / 2, YR[1] - 0.15)
        c.text(X - 6, Y, "3π/2", size=13, color=theme.RED, math=True, anchor="end", halo=True)
        # a steep radius on the left: 80 degrees leaves the picture
        a = math.radians(80)
        o = L.px(0, 0)
        top = L.px(YR[1] / math.tan(a), YR[1])
        c.line(*o, *top, color=theme.RED, width=1.6, dash="3 4")
        c.text(top[0] - 4, top[1] + 12, "80°", size=13, color=theme.RED, anchor="end", halo=True)

    return wt


@diagram("arc-length-sector", "Arc Length and Sector Area", "Trigonometry")
def arc_length_sector() -> Walkthrough:
    r, th = 3.0, 2.0
    s_len = r * th
    area = r * r * th / 2
    deg = math.degrees(th)
    wt = Walkthrough(
        "arc-length-sector", "Arc Length and Sector Area", "Trigonometry",
        concept="s = r\\theta, A = r^2\\theta/2 (\\theta in radians)",
        summary="With the angle in radians, the arc length is the radius times the angle, and the sector area "
                "is half the radius squared times the angle. Radians make both formulas short.",
        width=720, height=420, level="201",
    )
    CX, CY, K = 200.0, 250.0, 52.0  # pixels per unit
    R = r * K
    S_COL, A_COL, R_COL = theme.BLUE, theme.GREEN, theme.INK

    @wt.setup
    def _(c):
        c.circle(CX, CY, R, color=theme.MUTED, width=1.6, dash="5 5")
        c.dot(CX, CY, r=4, color=theme.INK)
        c.line(420, 30, 420, 400, color=theme.GRID, width=1)
        return None

    def panel(c, i, s, color=theme.INK, size=17):
        c.math(436, 64 + i * 50, s, anchor="start", color=color, size=size)

    @wt.step("Draw a sector",
             f"Take radius r = {num(r)} and angle θ = {num(th)} radians, about {num(deg, 1)}°. The sector is "
             "the pizza slice between the two radii.",
             math=f"r = {num(r)}, \\theta = {num(th)} rad \\approx {num(deg, 1)}°")
    def _(c):
        x1, y1 = polar_px(CX, CY, R, deg)
        c.line(CX, CY, CX + R, CY, color=R_COL, width=2.5)
        c.line(CX, CY, x1, y1, color=R_COL, width=2.5)
        c.text(CX + R / 2, CY + 16, f"r = {num(r)}", size=15, math=True, halo=True)
        c.arc(CX, CY, 36, 0, deg, color=ANG, width=2)
        arc_label(c, CX, CY, 56, deg / 2, f"θ = {num(th)}", color=ANG, size=15)
        panel(c, 0, f"r = {num(r)}, \\theta = {num(th)} rad")

    @wt.step("Arc length is r times θ",
             f"One radian cuts off one radius of arc, so {num(th)} radians cut off {num(th)} radii. "
             f"The arc is {num(th)} × {num(r)} = {num(s_len)} long.",
             math=f"s = r\\theta = {num(r)} \\times {num(th)} = {num(s_len)}")
    def _(c):
        one = math.degrees(1)
        c.arc(CX, CY, R, 0, one, color=S_COL, width=6)
        c.arc(CX, CY, R, one, deg, color=theme.SKY, width=6)
        for k in (0, 1, 2):
            x0, y0 = polar_px(CX, CY, R - 8, k * one)
            x1, y1 = polar_px(CX, CY, R + 8, k * one)
            c.line(x0, y0, x1, y1, color=theme.INK, width=2)
        arc_label(c, CX, CY, R + 22, one / 2, "r", color=S_COL, size=16)
        arc_label(c, CX, CY, R + 22, one * 1.5, "r", color=S_COL, size=16)
        arc_label(c, CX, CY, R + 46, deg / 2 + 10, f"s = {num(s_len)}", color=S_COL, size=17)
        panel(c, 1, f"s = r\\theta = {num(s_len)}", color=S_COL)

    @wt.step("Area is the same slice of the disk",
             f"The whole disk has area πr² and a full turn is 2π radians. The sector takes θ/(2π) of it, "
             f"which simplifies to r²θ/2 = {num(area)}.",
             math=f"A = (\\theta/2\\pi)\\cdot \\pi r^2 = r^2\\theta/2 = 9 \\cdot 2/2 = {num(area)}")
    def _(c):
        c.arc(CX, CY, R, 0, deg, color="none", fill=theme.fill(A_COL, "33"), sector=True)
        arc_label(c, CX, CY, R * 0.6, deg / 2, f"A = {num(area)}", color=A_COL, size=17)
        panel(c, 2, f"A = r^2\\theta/2 = {num(area)}", color=A_COL)
        panel(c, 3, f"disk: \\pi r^2 \\approx {num(math.pi * r * r, 2)}", color=theme.SOFT_INK, size=16)

    @wt.step("Degrees need an extra factor",
             f"In degrees the same arc needs the clumsy factor π/180: s = r · {num(deg, 1)}° · π/180. "
             "Radians bake that factor in, which is why calculus prefers them.",
             math=f"s = 2\\pi r \\cdot ({num(deg, 2)}°/360°) \\approx {num(s_len, 2)}")
    def _(c):
        panel(c, 4, f"degrees: s = r \\cdot \\theta° \\cdot \\pi/180", color=theme.SOFT_INK, size=16)
        panel(c, 5, f"= {num(r)} \\cdot {num(deg, 2)} \\cdot \\pi/180 \\approx {num(s_len, 2)}",
              color=theme.SOFT_INK, size=16)

    return wt
