"""Circle diagrams: inscribed angles, area from wedges, circumference by rolling."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import angle_mark, brace, right_angle, tick_marks
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._geo import away, num, polar, rich

INSCRIBED, CENTRAL, ARC = theme.ORANGE, theme.BLUE, theme.GREEN


# ---------------------------------------------------------------------------
# Inscribed angle theorem
# ---------------------------------------------------------------------------


@diagram("inscribed-angle", "Inscribed Angle Theorem", "Geometry")
def inscribed_angle() -> Walkthrough:
    a_deg, b_deg, p_deg = 210, 330, 100  # positions on the circle, math degrees
    central = (b_deg - a_deg) % 360
    d_deg = (p_deg + 180) % 360
    x = (d_deg - a_deg) / 2  # base angle of isosceles triangle OPA
    y = (b_deg - d_deg) / 2
    inscribed = x + y
    wt = Walkthrough(
        "inscribed-angle", "Inscribed Angle Theorem", "Geometry",
        concept="central angle = 2 \\times inscribed angle",
        summary="An angle with its vertex on a circle is half the central angle that stands on the same arc. "
                "Two isosceles triangles explain why.",
        width=680, height=420, level="201",
    )
    O = (260.0, 205.0)
    R = 170.0
    A, B, P, D = (polar(*O, R, t) for t in (a_deg, b_deg, p_deg, d_deg))

    def lab(c, pt, s, color=theme.INK, d=20):
        q = away(pt, O, d)
        c.text(q[0], q[1], s, size=17, math=True, weight="bold", color=color, halo=True)

    @wt.setup
    def _(c):
        c.circle(*O, R, color=theme.INK, width=2)
        c.dot(*O, r=4)
        c.text(O[0] + 16, O[1] - 14, "O", size=16, math=True, weight="bold", halo=True)
        return None

    @wt.step("Pick an arc", "Mark two points A and B on the circle. The green arc between them is the "
             "piece both angles stand on.", math=f"arc AB = {central}\\deg of the circle")
    def _(c):
        c.arc(*O, R, a_deg, b_deg, color=ARC, width=6)
        c.text(O[0], O[1] + R + 22, "arc AB", size=15, color=ARC, weight="bold")
        for pt, s in ((A, "A"), (B, "B")):
            c.dot(*pt, r=5)
            lab(c, pt, s)

    @wt.step("Draw the inscribed angle", "Put a vertex P on the far side of the circle and draw chords to A "
             f"and B. The angle at P measures {num(inscribed)}°.", math=f"\\angle APB = {num(inscribed)}\\deg")
    def _(c):
        c.line(*P, *A, color=INSCRIBED, width=2.5)
        c.line(*P, *B, color=INSCRIBED, width=2.5)
        c.dot(*P, r=5)
        lab(c, P, "P")
        angle_mark(c, P, A, B, r=48, color=INSCRIBED, label=f"{num(inscribed)}°", label_r=68)

    @wt.step("Draw the central angle", "Now draw radii from the center O to A and B. The central angle is "
             f"{central}°, exactly twice the angle at P.",
             math=f"\\angle AOB = {central}\\deg = 2 \\times {num(inscribed)}\\deg")
    def _(c):
        c.line(*O, *A, color=CENTRAL, width=2.5)
        c.line(*O, *B, color=CENTRAL, width=2.5)
        angle_mark(c, O, A, B, r=34, color=CENTRAL, label=f"{central}°", label_r=52)
        if c.is_new:
            rich(c, 560, 80, [(f"{central}°", CENTRAL), (" = 2 × ", theme.INK), (f"{num(inscribed)}°", INSCRIBED)],
                 size=20)

    def frame(c):
        """Redraws the arc, chords, and radii without the angle marks, for the proof steps."""
        c.arc(*O, R, a_deg, b_deg, color=ARC, width=6)
        c.line(*P, *A, color=INSCRIBED, width=2.5)
        c.line(*P, *B, color=INSCRIBED, width=2.5)
        c.line(*O, *A, color=CENTRAL, width=2.5)
        c.line(*O, *B, color=CENTRAL, width=2.5)
        c.line(*P, *D, color=theme.SOFT_INK, width=1.8, dash="7 5")
        for pt, s_ in ((A, "A"), (B, "B"), (P, "P"), (D, "D")):
            c.dot(*pt, r=5)
            lab(c, pt, s_)

    def left_half(c):
        c.polygon([O, P, A], color="none", fill=theme.fill(theme.PURPLE, "30"))
        tick_marks(c, O, P, color=theme.PURPLE)
        tick_marks(c, O, A, color=theme.PURPLE)
        angle_mark(c, P, A, D, r=44, color=theme.PURPLE, label=f"{num(x)}°", label_r=64, size=15)
        angle_mark(c, A, P, O, r=38, color=theme.PURPLE, label=f"{num(x)}°", label_r=56, size=15)
        angle_mark(c, O, A, D, r=36, color=theme.PURPLE, label=f"{num(2 * x)}°", label_r=58, size=15)

    def right_half(c):
        c.polygon([O, P, B], color="none", fill=theme.fill(theme.SKY, "30"))
        tick_marks(c, O, B, color=theme.SKY, count=2)
        angle_mark(c, P, D, B, r=44, color=theme.SKY, label=f"{num(y)}°", label_r=64, size=15)
        angle_mark(c, B, P, O, r=38, color=theme.SKY, label=f"{num(y)}°", label_r=56, size=15)
        angle_mark(c, O, D, B, r=36, color=theme.SKY, label=f"{num(2 * y)}°", label_r=58, size=15)

    @wt.step("Split with a diameter", "Draw the diameter from P through O to D. Triangle OPA has two radii "
             f"for sides, so it is isosceles: both base angles are {num(x)}°. The outside angle at O is "
             f"their sum, {num(2 * x)}°.",
             math=f"\\angle AOD = {num(x)}\\deg + {num(x)}\\deg = {num(2 * x)}\\deg", fresh=True)
    def _(c):
        frame(c)
        left_half(c)

    @wt.step("Repeat on the other side", f"Triangle OPB works the same way with {num(y)}° base angles, "
             f"giving {num(2 * y)}° at O. Add the halves: the center gets double what P gets.",
             math=f"{num(2 * x)}\\deg + {num(2 * y)}\\deg = 2({num(x)}\\deg + {num(y)}\\deg) = {central}\\deg",
             fresh=True)
    def _(c):
        frame(c)
        left_half(c)
        right_half(c)
        rich(c, 570, 70, [(f"{num(2 * x)}°", theme.PURPLE), (" + ", theme.INK), (f"{num(2 * y)}°", theme.SKY),
                          (f" = {central}°", theme.INK)], size=18)
        rich(c, 570, 100, [(f"{num(x)}°", theme.PURPLE), (" + ", theme.INK), (f"{num(y)}°", theme.SKY),
                           (f" = {num(inscribed)}°", theme.INK)], size=18)

    @wt.step("Move P anywhere on the far arc", "Slide P along the circle and the angle never changes. Every "
             f"inscribed angle on arc AB is {num(inscribed)}°, half of the central {central}°.",
             math=f"\\angle APB = \\angle AQB = \\angle ASB = {num(inscribed)}\\deg", fresh=True)
    def _(c):
        c.arc(*O, R, a_deg, b_deg, color=ARC, width=6)
        c.line(*O, *A, color=CENTRAL, width=2.5)
        c.line(*O, *B, color=CENTRAL, width=2.5)
        angle_mark(c, O, A, B, r=34, color=CENTRAL, label=f"{central}°", label_r=52)
        for t, name in ((p_deg, "P"), (60, "Q"), (165, "S")):
            Q = polar(*O, R, t)
            c.line(*Q, *A, color=INSCRIBED, width=2)
            c.line(*Q, *B, color=INSCRIBED, width=2)
            c.dot(*Q, r=5)
            lab(c, Q, name)
            angle_mark(c, Q, A, B, r=38, color=INSCRIBED, label=f"{num(inscribed)}°", label_r=56, size=14)
        for pt, s in ((A, "A"), (B, "B")):
            c.dot(*pt, r=5)
            lab(c, pt, s)
        rich(c, 570, 80, [(f"{central}°", CENTRAL), (" = 2 × ", theme.INK), (f"{num(inscribed)}°", INSCRIBED)],
             size=20)
        c.text(570, 108, "same arc, any vertex", size=13, color=theme.SOFT_INK)

    return wt


@diagram("thales-semicircle", "Angle in a Semicircle", "Geometry")
def thales() -> Walkthrough:
    wt = Walkthrough(
        "thales-semicircle", "Angle in a Semicircle", "Geometry",
        concept="diameter AB \\implies \\angle APB = 90\\deg",
        summary="When the arc is half the circle, the central angle is a straight 180°. Half of that is "
                "90°, so any angle drawn in a semicircle is a right angle.",
        width=680, height=380, level="201",
    )
    O = (340.0, 200.0)
    R = 160.0
    A, B = polar(*O, R, 180), polar(*O, R, 0)

    @wt.setup
    def _(c):
        c.circle(*O, R, color=theme.INK, width=2)
        c.dot(*O, r=4)
        c.text(O[0], O[1] + 18, "O", size=16, math=True, weight="bold")
        return None

    @wt.step("Use a diameter as the arc", "Let A and B sit at opposite ends of a diameter. The central "
             "angle AOB is a straight line: 180°.", math="\\angle AOB = 180\\deg")
    def _(c):
        c.line(*A, *B, color=CENTRAL, width=3)
        c.arc(*O, 30, 0, 180, color=CENTRAL, width=2, fill=theme.fill(CENTRAL, "30"))
        c.text(O[0], O[1] - 46, "180°", size=15, math=True, color=CENTRAL, halo=True)
        c.arc(*O, R, 180, 360, color=ARC, width=6)
        for pt, s, dx in ((A, "A", -16), (B, "B", 16)):
            c.dot(*pt, r=5)
            c.text(pt[0] + dx, pt[1], s, size=17, math=True, weight="bold")

    @wt.step("Halve it", "An inscribed angle is half the central angle on the same arc. Half of 180° "
             "is 90°.", math="180\\deg \\div 2 = 90\\deg")
    def _(c):
        P = polar(*O, R, 125)
        c.line(*P, *A, color=INSCRIBED, width=2.5)
        c.line(*P, *B, color=INSCRIBED, width=2.5)
        c.dot(*P, r=5)
        q = away(P, O, 20)
        c.text(q[0], q[1], "P", size=17, math=True, weight="bold")
        right_angle(c, P, A, B, s=16, color=INSCRIBED)
        c.text(P[0] + 4, P[1] + 38, "90°", size=15, math=True, color=INSCRIBED, halo=True)

    @wt.step("Every point gives a right angle", "Move P anywhere on the circle and the corner stays square. "
             "Carpenters use this trick to check a semicircle.", math="\\angle APB = 90\\deg for every P")
    def _(c):
        for t in (40, 75, 160):
            P = polar(*O, R, t)
            c.line(*P, *A, color=INSCRIBED, width=1.8, stroke_opacity=0.7)
            c.line(*P, *B, color=INSCRIBED, width=1.8, stroke_opacity=0.7)
            c.dot(*P, r=4, color=INSCRIBED)
            right_angle(c, P, A, B, s=12, color=INSCRIBED)

    return wt


# ---------------------------------------------------------------------------
# Area of a circle from wedges
# ---------------------------------------------------------------------------


@diagram("circle-area-wedges", "Area of a Circle", "Geometry")
def circle_area() -> Walkthrough:
    r_val = 3  # cm, the worked example
    wt = Walkthrough(
        "circle-area-wedges", "Area of a Circle", "Geometry",
        concept="A = \\pi r \\times r = \\pi r^2",
        summary="Cut a circle into thin wedges and lay them head to tail. They form a shape close to a "
                "rectangle that is half the circumference long and one radius tall.",
        width=700, height=290, level="201",
    )
    O = (125.0, 145.0)
    R = 90.0
    X0, YT = 270.0, 100.0  # strip: left edge, top of the strip
    TOP, BOT = theme.ORANGE, theme.BLUE  # wedge colors, alternate

    def circle_wedges(c, n):
        w = 360 / n
        for i in range(n):
            col = BOT if i % 2 == 0 else TOP
            c.arc(*O, R, 90 + i * w, 90 + (i + 1) * w, color=theme.PAPER, width=1,
                  fill=theme.fill(col, "66"), sector=True)
        c.circle(*O, R, color=theme.INK, width=2)
        c.line(*O, O[0] + R, O[1], color=theme.GREEN, width=2.5)
        c.text(O[0] + R / 2, O[1] - 12, "r", size=17, math=True, color=theme.GREEN, halo=True)

    def strip(c, n, labels=False):
        w = 360 / n
        s = R * math.radians(w)  # arc length of one wedge
        for i in range(n):
            col = BOT if i % 2 == 0 else TOP
            if i % 2 == 0:  # tip up, arc on the bottom
                cx, cy = X0 + s / 2 + (i // 2) * s, YT
                c.arc(cx, cy, R, 270 - w / 2, 270 + w / 2, color=theme.PAPER, width=1,
                      fill=theme.fill(col, "66"), sector=True)
            else:  # tip down, arc on top
                cx, cy = X0 + s + (i // 2) * s, YT + R
                c.arc(cx, cy, R, 90 - w / 2, 90 + w / 2, color=theme.PAPER, width=1,
                      fill=theme.fill(col, "66"), sector=True)
        return s

    @wt.setup
    def _(c):
        return None

    @wt.step("Start with a circle", f"Take a circle with radius r = {r_val} cm. The distance around it is "
             "the circumference, 2πr. Paint the rim in eight stripes: half of it is blue, half is orange.",
             math=f"C = 2\\pi r = 2\\pi \\cdot {r_val} \\approx {2 * math.pi * r_val:.2f} cm", fresh=True)
    def _(c):
        for i in range(8):
            c.arc(*O, R, 90 + i * 45, 135 + i * 45, color=BOT if i % 2 == 0 else TOP, width=6)
        c.line(*O, O[0] + R, O[1], color=theme.GREEN, width=2.5)
        c.dot(*O, r=4)
        c.text(O[0] + R / 2, O[1] - 14, "r", size=18, math=True, color=theme.GREEN, halo=True)
        c.text(O[0] + R + 24, O[1] - 50, "C = 2πr", size=17, math=True, anchor="start")
        rich(c, 470, 145, [("blue", BOT), (" = πr,  ", theme.INK), ("orange", TOP), (" = πr", theme.INK)],
             size=18)

    @wt.step("Cut it into eight wedges", "Slice it like a pizza. Each wedge is a thin triangle with a curved "
             "bottom edge, and the curved edges together make the circumference.", math="8 wedges", fresh=True)
    def _(c):
        circle_wedges(c, 8)

    @wt.step("Lay the wedges head to tail", "Point the blue wedges up and the orange wedges down, and fit "
             "them together. The blue arcs line the bottom, the orange arcs line the top.",
             math="bottom = top = half the circumference = \\pi r", fresh=True)
    def _(c):
        circle_wedges(c, 8)
        s = strip(c, 8)
        c.curved_arrow(O[0] + R + 10, O[1] - 40, X0 - 10, YT, bend=-0.25, color=theme.MUTED, width=1.5)
        c.text(X0 + 2 * s, YT + R + 22, "blue arcs: πr", size=15, math=True, color=BOT)
        c.text(X0 + 2.5 * s, YT - 22, "orange arcs: πr", size=15, math=True, color=TOP)

    @wt.step("Use thinner wedges", "With 16 wedges the bumps shrink and the sides stand up straighter. The "
             "shape looks more and more like a rectangle.", math="16 wedges", fresh=True)
    def _(c):
        circle_wedges(c, 16)
        strip(c, 16)

    @wt.step("Read the rectangle", f"With very many wedges the shape is a rectangle: πr long and r tall. "
             f"For r = {r_val} cm that is about {math.pi * r_val:.2f} cm by {r_val} cm.",
             math=f"A = \\pi r \\times r = \\pi \\cdot {r_val}^2 \\approx {math.pi * r_val ** 2:.2f} cm²",
             fresh=True)
    def _(c):
        circle_wedges(c, 48)
        s = strip(c, 48)
        L = s * 24
        c.line(X0, YT + R, X0 + L, YT + R, color=BOT, width=4)
        c.line(X0 + s / 2, YT, X0 + s / 2 + L, YT, color=TOP, width=4)
        brace(c, X0 + L, YT + R + 6, X0, YT + R + 6, f"\\pi r \\approx {math.pi * r_val:.2f} cm", color=BOT)
        c.line(X0 + L + s / 2 + 10, YT, X0 + L + s / 2 + 10, YT + R, color=theme.GREEN, width=2.5)
        c.text(X0 + L + s / 2 + 18, YT + R / 2, f"r = {r_val} cm", size=16, math=True, color=theme.GREEN,
               anchor="start")
        c.text(X0 + L / 2, YT - 22, f"area = πr × r ≈ {math.pi * r_val ** 2:.2f} cm²", size=17, math=True)

    return wt


# ---------------------------------------------------------------------------
# Circumference by rolling
# ---------------------------------------------------------------------------


@diagram("circumference-unroll", "Circumference: Roll the Circle", "Geometry")
def circumference() -> Walkthrough:
    d_val = 2  # cm
    wt = Walkthrough(
        "circumference-unroll", "Circumference: Roll the Circle", "Geometry",
        concept="C = \\pi d",
        summary="Roll a circle one full turn along a line. The distance it travels is its circumference, "
                "a little more than three diameters: π of them.",
        width=700, height=390, level="201",
    )
    D = 140.0  # diameter in px
    r = D / 2
    X0, GY = 150.0, 240.0  # start contact point, ground line
    C = math.pi * D
    P_COL, D_COL, C_COL = theme.RED, theme.BLUE, theme.ORANGE

    def wheel(c, t, ghost=False):
        """Draws the circle after rolling a fraction t of a turn, with the marked point."""
        cx = X0 + t * C
        cy = GY - r
        col = theme.MUTED if ghost else theme.INK
        c.circle(cx, cy, r, color=col, width=1.5 if ghost else 2.5, dash="5 4" if ghost else None)
        ang = -90 - 360 * t  # the marked point starts at the bottom and turns clockwise
        p = polar(cx, cy, r, ang)
        c.dot(*p, r=4 if ghost else 6, color=P_COL)
        return (cx, cy), p

    @wt.setup
    def _(c):
        c.line(20, GY, 680, GY, color=theme.INK, width=2)
        return None

    @wt.step("Mark a point on the rim", f"Take a circle with diameter d = {d_val} cm and paint a red dot "
             "where it touches the ground.", math=f"d = {d_val} cm")
    def _(c):
        (cx, cy), p = wheel(c, 0)
        c.line(cx, cy - r, cx, cy + r, color=D_COL, width=3)
        c.text(cx - r - 8, cy, f"d = {d_val} cm", size=16, math=True, color=D_COL, anchor="end", halo=True)

    @wt.step("Roll one full turn", "Roll the circle without slipping until the red dot touches the "
             "ground again. The dot traces a hump called a cycloid.", math="one full turn")
    def _(c):
        pts = []
        for i in range(121):
            t = i / 120
            cx = X0 + t * C
            pts.append(polar(cx, GY - r, r, -90 - 360 * t))
        c.polyline(pts, color=P_COL, width=1.6, dash="4 4")
        for t in (0.25, 0.5, 0.75):
            wheel(c, t, ghost=True)
        wheel(c, 1)
        c.text(X0 + C / 2, GY - 2 * r - 14, "path of the red dot", size=13, color=P_COL, halo=True)

    @wt.step("Measure the trip", "The ground between the two red marks touched every point of the rim "
             "once. So that distance is the circumference C.", math="C = distance rolled")
    def _(c):
        c.line(X0, GY, X0 + C, GY, color=C_COL, width=6)
        c.dot(X0, GY, r=6, color=P_COL)
        c.dot(X0 + C, GY, r=6, color=P_COL)
        brace(c, X0 + C, GY + 8, X0, GY + 8, "C", color=C_COL, size=18)

    @wt.step("Lay diameters along the trip", "Diameters fit three times with a small piece left over. "
             f"The leftover is about {math.pi - 3:.2f} of a diameter.",
             math=f"C = 3d + {math.pi - 3:.2f}d \\approx {math.pi:.2f}d")
    def _(c):
        y = GY + 70
        cols = [D_COL, theme.SKY, D_COL]
        for k in range(3):
            c.line(X0 + k * D, y, X0 + (k + 1) * D, y, color=cols[k], width=7)
            c.text(X0 + (k + 0.5) * D, y + 20, "d", size=17, math=True, color=D_COL)
            c.line(X0 + k * D, y - 9, X0 + k * D, y + 9, color=theme.INK, width=1.5)
        c.line(X0 + 3 * D, y - 9, X0 + 3 * D, y + 9, color=theme.INK, width=1.5)
        c.line(X0 + 3 * D, y, X0 + C, y, color=theme.PURPLE, width=7)
        c.line(X0 + C, y - 9, X0 + C, y + 9, color=theme.INK, width=1.5)
        c.text(X0 + 3 * D + 10, y + 22, f"{math.pi - 3:.2f}d", size=15, math=True, color=theme.PURPLE,
               anchor="start")

    @wt.step("Name the ratio π", f"Every circle, big or small, rolls π ≈ 3.14 diameters per turn. For "
             f"d = {d_val} cm the trip is about {math.pi * d_val:.2f} cm.",
             math=f"C = \\pi d = \\pi \\cdot {d_val} \\approx {math.pi * d_val:.2f} cm")
    def _(c):
        rich(c, X0 + C / 2, 40, [("C ÷ d = ", theme.INK), ("π ≈ 3.14159", C_COL)], size=22)

    return wt
