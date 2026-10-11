"""Modular arithmetic on a clock: wrapping around, remainders, and congruence classes."""

from __future__ import annotations

import math

from .. import theme
from ..registry import diagram
from ..walkthrough import Walkthrough


@diagram("modular-clock", "Modular Arithmetic on a Clock", "Number Theory")
def build() -> Walkthrough:
    M, START, ADD = 12, 9, 5
    total = START + ADD
    res = total % M
    wt = Walkthrough(
        "modular-clock", "Modular Arithmetic on a Clock", "Number Theory",
        concept=f"{START} + {ADD} = {total} \\equiv {res} (mod {M})",
        summary="Counting mod 12 wraps around a circle of 12 spots, like a clock. Numbers that land on the "
                "same spot are congruent: they leave the same remainder after dividing by 12.",
        width=700, height=420, level="201",
    )
    CX, CY = 220, 212
    R_TRACK, R_HOP = 72, 56
    RINGS = [100, 138, 176]  # label radius for lap 0, 1, 2
    PX = 430  # right panel left edge
    START_C, HOP_C, CLASS_C, CLASS2_C = theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE

    def ang(k):
        return math.radians(90 - 360 / M * k)

    def at(k, r):
        a = ang(k)
        return CX + r * math.cos(a), CY - r * math.sin(a)

    def lap_labels(c, lap, color, size, bold=False, skip=()):
        for k in range(M):
            n = lap * M + k
            if n in skip:
                continue
            x, y = at(k, RINGS[lap])
            c.text(x, y, str(n), size=size, color=color, weight="bold" if bold else None, halo=True)

    def panel(c, i, s, color=theme.INK, size=17, math=True):
        c.text(PX, 60 + i * 36, s, size=size, color=color, anchor="start", math=math)

    @wt.step("Count around a circle", f"Put 0 to {M - 1} around a circle. After {M - 1} the count wraps back "
             "to 0, the way a clock goes from 11 back to 12. Mod 12 just means: count on this circle.",
             math=f"spots: 0, 1, 2, \\ldots, {M - 1}")
    def _(c):
        c.circle(CX, CY, R_TRACK, color=theme.SOFT_INK, width=2)
        for k in range(M):
            c.dot(*at(k, R_TRACK), r=4, color=theme.SOFT_INK)
        lap_labels(c, 0, theme.INK, 17, bold=True)
        panel(c, 0, "mod 12: a 12-spot circle", theme.SOFT_INK, 15, math=False)
        panel(c, 1, "11 + 1 lands on 0", theme.SOFT_INK, 15, math=False)
        if c.is_new:
            c.arc(CX, CY, 124, 90 + 30 - 4, 90 + 4, color=HOP_C, width=2.5, arrow=True)
            c.text(*at(11.5, 146), "wrap!", size=13, color=HOP_C, weight="bold")
            c.text(CX, CY - 10, "a clock face", size=13, color=theme.SOFT_INK)
            c.text(CX, CY + 10, "with 12 renamed 0", size=13, color=theme.SOFT_INK)
            panel(c, 2, "10 + 4 lands on 2", theme.SOFT_INK, 15, math=False)

    @wt.step(f"Start at {START} and add {ADD}", f"Take {ADD} hops clockwise from {START}. The hops pass 0 "
             f"and land on {res}. Nine o'clock plus five hours is two o'clock.",
             math=f"{START} + {ADD} \\to {res}")
    def _(c):
        c.dot(*at(START, R_TRACK), r=9, color=START_C)
        sx, sy = at(START, R_TRACK)
        c.text(sx + 4, sy + 22, "start", size=12, color=START_C, halo=True)
        for i in range(ADD):
            k = START + i
            a0 = 90 - 360 / M * k
            c.arc(CX, CY, R_HOP, a0 - 3, a0 - 360 / M + 3, color=HOP_C, width=2.6, arrow=True)
            x, y = at(k + 0.5, R_HOP - 14)
            c.text(x, y, str(i + 1), size=11, color=HOP_C, weight="bold")
        c.dot(*at(res, R_TRACK), r=9, color=CLASS_C)
        c.text(CX, CY, f"+{ADD}", size=20, color=HOP_C, weight="bold")
        panel(c, 3, f"{START} + {ADD} = {total}", HOP_C)
        panel(c, 4, f"lands on {res}", CLASS_C, 17, math=False)

    @wt.step("Keep counting: the second lap", f"Write the second lap, {M} to {2 * M - 1}, on an outer ring. "
             f"{total} sits just outside {res}. So {total} and {res} are the same spot on the circle.",
             math=f"{total} = 1 \\times {M} + {res}")
    def _(c):
        lap_labels(c, 1, theme.SOFT_INK, 14, skip=(total,))
        x, y = at(res, RINGS[1])
        c.text(x, y, str(total), size=15, color=HOP_C, weight="bold", halo=True)
        c.text(PX, 22, "rings = laps around the circle", size=13, color=theme.SOFT_INK, anchor="start")
        panel(c, 5, f"{total} = 1 \\times {M} + {res}", HOP_C)
        panel(c, 6, f"so {total} \\equiv {res} (mod {M})", CLASS_C)

    @wt.step("Numbers on one spoke are congruent", f"Add a third lap. The spoke through {res} holds "
             f"{res}, {res + M}, {res + 2 * M}, and so on, plus −{M - res} if you walk backward. They all "
             f"leave remainder {res} after dividing by {M}. That set is a congruence class.",
             math=f"\\ldots \\equiv {res - M} \\equiv {res} \\equiv {res + M} \\equiv {res + 2 * M} (mod {M})")
    def _(c):
        lap_labels(c, 2, theme.MUTED, 13, skip=(res + 2 * M,))
        x0, y0 = at(res, R_TRACK)
        x1, y1 = at(res, RINGS[2] + 20)
        c.line(x0, y0, x1, y1, color=CLASS_C, width=8, opacity=0.25)
        for lap in range(3):
            x, y = at(res, RINGS[lap])
            c.circle(x, y, 15, color=CLASS_C, width=2)
            c.text(x, y, str(res + lap * M), size=15, color=CLASS_C, weight="bold", halo=True)
        c.rect(PX - 8, 312, 262, 64, color=CLASS_C, fill=theme.fill(CLASS_C, "18"), width=1.5, rx=8)
        c.text(PX + 4, 330, f"class of {res}: remainder {res}", size=14, color=CLASS_C, anchor="start", weight="bold")
        c.math(PX + 4, 356, f"{{\\ldots, {res - M}, {res}, {res + M}, {res + 2 * M}, \\ldots}}", size=17,
               color=CLASS_C, anchor="start")

    @wt.step(f"Every number lands on one of {M} spokes", f"Each spoke is its own class, so the integers "
             f"split into exactly {M} classes. Two numbers are congruent when {M} divides their difference. "
             "For example, 24 and 0 share the top spoke.",
             math=f"a \\equiv b (mod {M})  \\iff  {M} divides a - b")
    def _(c):
        x0, y0 = at(0, R_TRACK)
        x1, y1 = at(0, RINGS[2] + 20)
        c.line(x0, y0, x1, y1, color=CLASS2_C, width=8, opacity=0.25)
        for lap in range(3):
            x, y = at(0, RINGS[lap])
            c.circle(x, y, 15, color=CLASS2_C, width=2)
            c.text(x, y, str(lap * M), size=15, color=CLASS2_C, weight="bold", halo=True)
        c.text(PX, 400, f"{M} spokes = {M} classes: 0, 1, \\ldots, {M - 1}".replace("\\ldots", "…"), size=14,
               color=CLASS2_C, anchor="start", weight="bold")

    return wt
