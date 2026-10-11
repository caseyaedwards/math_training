"""Compass and straightedge constructions."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import angle_mark, dimension, right_angle, tick_marks
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._geo import dist, heading, num, polar

A_COL, B_COL, LINE_COL = theme.BLUE, theme.ORANGE, theme.GREEN


@diagram("perpendicular-bisector", "Perpendicular Bisector Construction", "Geometry")
def perpendicular_bisector() -> Walkthrough:
    cm = 40.0  # pixels per centimeter
    ab_cm, r_cm = 7.0, 5.0
    wt = Walkthrough(
        "perpendicular-bisector", "Perpendicular Bisector Construction", "Geometry",
        concept="PA = PB \\implies P lies on the perpendicular bisector of AB",
        summary="Two arcs of the same radius, one from each end of a segment, cross at two points. The line "
                "through those points cuts the segment in half at a right angle.",
        width=680, height=440, level="201",
    )
    A = (200.0, 220.0)
    B = (A[0] + ab_cm * cm, A[1])
    R = r_cm * cm
    half = ab_cm * cm / 2
    hgt = math.sqrt(R * R - half * half)
    M = (A[0] + half, A[1])
    P, Q = (M[0], M[1] - hgt), (M[0], M[1] + hgt)
    span = 22  # degrees of arc drawn on each side of a crossing
    angP = heading(A, P)  # direction from A to P

    def arcs(c, center, col):
        for target in (P, Q):
            h = heading(center, target)
            c.arc(center[0], center[1], R, h - span, h + span, color=col, width=2.5)

    @wt.setup
    def _(c):
        return None

    @wt.step("Draw the segment", f"Start with segment AB, {num(ab_cm)} cm long. The goal: find its exact "
             "middle and a line at right angles to it, with no ruler markings and no protractor.",
             math=f"AB = {num(ab_cm)} cm")
    def _(c):
        c.line(*A, *B, color=theme.INK, width=3)
        for pt, s, dx in ((A, "A", -18), (B, "B", 18)):
            c.dot(*pt, r=5)
            c.text(pt[0] + dx, pt[1], s, size=18, math=True, weight="bold")
        if c.is_new:
            dimension(c, B, A, f"{num(ab_cm)} cm", offset=34)

    @wt.step("Swing arcs from A", f"Open the compass wider than half of AB, here {num(r_cm)} cm. Put the "
             "point on A and draw an arc above and below the segment.", math=f"r = {num(r_cm)} cm")
    def _(c):
        arcs(c, A, A_COL)
        if c.is_new:
            c.line(*A, *polar(*A, R, angP + 12), color=A_COL, width=1.5, dash="5 4")
            lx, ly = polar(*A, R / 2, angP + 12)
            c.text(lx - 10, ly - 8, f"r = {num(r_cm)} cm", size=15, math=True, color=A_COL, anchor="end", halo=True)

    @wt.step("Swing arcs from B", "Keep the same opening. Put the point on B and draw two more arcs. "
             "They cross the first pair at P and Q.", math="same r from both ends")
    def _(c):
        arcs(c, B, B_COL)
        for pt, s, dy in ((P, "P", -20), (Q, "Q", 22)):
            c.dot(*pt, r=5, color=theme.INK)
            c.text(pt[0] + 24, pt[1], s, size=18, math=True, weight="bold", anchor="start", halo=True)

    @wt.step("Join P and Q", f"Draw the line through P and Q. It crosses AB at M, the midpoint, and "
             f"meets AB at a right angle. Each half is {num(ab_cm / 2)} cm.",
             math=f"AM = MB = {num(ab_cm / 2)} cm, PQ \\perp AB")
    def _(c):
        c.line(P[0], P[1] - 40, Q[0], Q[1] + 40, color=LINE_COL, width=3)
        right_angle(c, M, B, P, s=16, color=LINE_COL)
        tick_marks(c, A, M, color=theme.INK)
        tick_marks(c, M, B, color=theme.INK)
        c.dot(*M, r=5, color=LINE_COL)
        c.text(M[0] - 16, M[1] + 20, "M", size=18, math=True, weight="bold", color=LINE_COL, halo=True)

    @wt.step("See why it works", f"P is {num(r_cm)} cm from A and {num(r_cm)} cm from B, because both "
             "arcs used the same radius. Every point that is equally far from A and B sits on this line.",
             math=f"PA = PB = {num(r_cm)} cm, QA = QB = {num(r_cm)} cm")
    def _(c):
        for pt in (P, Q):
            c.line(*pt, *A, color=A_COL, width=2, dash="6 4")
            c.line(*pt, *B, color=B_COL, width=2, dash="6 4")
            tick_marks(c, pt, A, count=2, color=A_COL)
            tick_marks(c, pt, B, count=2, color=B_COL)
        c.text(570, 90, "equal distances", size=14, color=theme.SOFT_INK)
        c.text(570, 112, f"PA = PB = {num(r_cm)} cm", size=15, math=True)

    return wt


@diagram("angle-bisector", "Angle Bisector Construction", "Geometry")
def angle_bisector() -> Walkthrough:
    theta = 64.0
    wt = Walkthrough(
        "angle-bisector", "Angle Bisector Construction", "Geometry",
        concept="\\angle AVD = \\angle DVB = \\theta / 2",
        summary="The same compass trick splits an angle in half: mark equal distances on both sides, then "
                "find a point equally far from those two marks.",
        width=680, height=380, level="201",
    )
    V = (110.0, 320.0)
    L = 470.0
    A_end = polar(*V, 290 / math.sin(math.radians(theta)), theta)
    B_end = polar(*V, L, 0)
    r1 = 170.0
    X, Y = polar(*V, r1, theta), polar(*V, r1, 0)
    r2 = 140.0
    # the second arcs cross on the bisector, at distance d from V
    half_chord = dist(X, Y) / 2
    to_mid = r1 * math.cos(math.radians(theta / 2))
    d = to_mid + math.sqrt(r2 * r2 - half_chord * half_chord)
    D = polar(*V, d, theta / 2)

    @wt.setup
    def _(c):
        c.line(*V, *A_end, color=theme.INK, width=3)
        c.line(*V, *B_end, color=theme.INK, width=3)
        c.dot(*V, r=5)
        c.text(V[0] - 16, V[1] + 4, "V", size=18, math=True, weight="bold")
        return None

    @wt.step("Start with an angle", f"Angle V measures {num(theta)}°. The goal is two equal halves of "
             f"{num(theta / 2)}° each, using only a compass and a straightedge.", math=f"\\angle V = {num(theta)}\\deg")
    def _(c):
        angle_mark(c, V, A_end, B_end, r=60, color=theme.PURPLE)
        lx, ly = polar(*V, 80, theta * 0.78)
        c.text(lx, ly, f"{num(theta)}°", size=16, math=True, color=theme.PURPLE, halo=True)

    @wt.step("Mark equal distances", "With the compass point on V, swing one arc that crosses both sides. "
             "Call the crossings X and Y. Now VX = VY.", math="VX = VY")
    def _(c):
        c.arc(*V, r1, -8, theta + 8, color=theme.SOFT_INK, width=2)
        for pt, s, off in ((X, "X", (-26, 4)), (Y, "Y", (10, 20))):
            c.dot(*pt, r=5, color=theme.INK)
            c.text(pt[0] + off[0], pt[1] + off[1], s, size=17, math=True, weight="bold", halo=True)

    @wt.step("Swing arcs from X and Y", "Use one opening for both. The two arcs cross at D, which is "
             "equally far from X and Y.", math="XD = YD")
    def _(c):
        for ctr, col in ((X, A_COL), (Y, B_COL)):
            h = heading(ctr, D)
            c.arc(*ctr, r2, h - 18, h + 18, color=col, width=2.5)
        c.dot(*D, r=5)
        c.text(D[0] + 14, D[1] - 14, "D", size=17, math=True, weight="bold", halo=True)

    @wt.step("Draw the bisector", f"The ray from V through D splits the angle into two {num(theta / 2)}° "
             "halves. Triangles VXD and VYD match side for side, so their angles at V match too.",
             math=f"{num(theta)}\\deg \\div 2 = {num(theta / 2)}\\deg")
    def _(c):
        E = polar(*V, 440, theta / 2)
        c.line(*V, *E, color=LINE_COL, width=3)
        c.line(*X, *D, color=A_COL, width=1.6, dash="5 4")
        c.line(*Y, *D, color=B_COL, width=1.6, dash="5 4")
        angle_mark(c, V, A_end, E, r=100, color=LINE_COL, label=f"{num(theta / 2)}°", label_r=122, fill=False)
        angle_mark(c, V, E, B_end, r=100, color=LINE_COL, label=f"{num(theta / 2)}°", label_r=122, fill=False)
        for i, line in enumerate(("VX = VY  (first arc)", "XD = YD  (second arcs)", "VD = VD  (shared side)")):
            c.text(470, 250 + i * 24, line, size=15, math=True, anchor="start")

    return wt
