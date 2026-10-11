"""The chain rule as linked rates: stacked number lines, and a belt-and-pulley machine."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import brace, number_line
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._calculus_tools import num

X0 = 1.0
DX = 0.05
U0, U1 = X0 ** 2, (X0 + DX) ** 2
Y0, Y1 = math.sin(U0), math.sin(U1)
DU_DX = 2 * X0
DY_DU = math.cos(U0)
DY_DX = DU_DX * DY_DU
COS1 = f"{DY_DU:.3f}"

CX, CU, CY = theme.BLUE, theme.ORANGE, theme.GREEN


@diagram("chain-rule", "Chain Rule: Stretch Factors Multiply", "Calculus")
def chain_rule() -> Walkthrough:
    wt = Walkthrough(
        "chain-rule", "Chain Rule: Stretch Factors Multiply", "Calculus",
        concept="d/dx sin(x^2) = cos(x^2) \\cdot 2x",
        summary="Send a tiny interval through x → x² → sin. Each function stretches or squeezes it by its "
                "own derivative, and the two factors multiply.",
        width=700, height=420, level="301",
    )
    L, R = 170, 640
    rows = {"x": 80, "u": 210, "y": 340}

    @wt.setup
    def _(c):
        Xs = {}
        for key, y in rows.items():
            Xs[key] = number_line(c, L, y, R, 0.7, 1.3, step=0.1, minor=2, size=12, color=theme.SOFT_INK)
        c.text(24, rows["x"], "x", size=20, color=CX, math=True, anchor="start", weight="bold")
        c.text(24, rows["u"], "u = x^2", size=20, color=CU, math=True, anchor="start")
        c.text(24, rows["y"], "y = sin u", size=20, color=CY, math=True, anchor="start")
        c.text(24, rows["x"] + 24, "input", size=12, color=theme.SOFT_INK, anchor="start")
        c.text(24, rows["u"] + 24, "inner output", size=12, color=theme.SOFT_INK, anchor="start")
        c.text(24, rows["y"] + 24, "outer output", size=12, color=theme.SOFT_INK, anchor="start")
        return Xs["x"]

    def seg(c, X, y, a, b, col):
        c.rect(X(a), y - 7, X(b) - X(a), 14, color=col, fill=theme.fill(col, "66"), width=2, rx=3)

    def funnel(c, X, ya, a0, a1, yb, b0, b1, col):
        c.polygon([(X(a0), ya + 9), (X(a1), ya + 9), (X(b1), yb - 9), (X(b0), yb - 9)], color="none",
                  fill=theme.fill(col, "26"))
        c.line(X(a0), ya + 9, X(b0), yb - 9, color=col, width=1.2, dash="4 3")
        c.line(X(a1), ya + 9, X(b1), yb - 9, color=col, width=1.2, dash="4 3")

    @wt.step("Follow one input", "Put x = 1 into the machine. Squaring gives u = 1, and sine gives "
             "y ≈ 0.841. So far, nothing but plugging in.",
             math=f"x = 1 \\to u = 1 \\to y = sin 1 \\approx {num(Y0)}")
    def _(c, X):
        ry = rows
        c.dot(X(X0), ry["x"], r=6, color=CX)
        c.dot(X(U0), ry["u"], r=6, color=CU)
        c.dot(X(Y0), ry["y"], r=6, color=CY)
        if c.is_new:
            c.arrow(X(X0), ry["x"] + 30, X(U0), ry["u"] - 12, color=theme.SOFT_INK, width=1.6)
            c.arrow(X(U0), ry["u"] + 30, X(Y0), ry["y"] - 12, color=theme.SOFT_INK, width=1.6)
            c.text(X(X0) + 12, (ry["x"] + ry["u"]) / 2, "square it", size=13, color=theme.SOFT_INK,
                   anchor="start", halo=True)
            c.text((X(U0) + X(Y0)) / 2 + 22, (ry["u"] + ry["y"]) / 2, "take sine", size=13,
                   color=theme.SOFT_INK, anchor="start", halo=True)
        c.text(X(Y0) - 10, ry["y"] - 18, num(Y0), size=13, color=CY, math=True, anchor="end", halo=True)

    @wt.step("Nudge the input", "Widen the input to a small interval of length Δx = 0.05, from 1 to 1.05.",
             math="\\Delta x = 0.05")
    def _(c, X):
        seg(c, X, rows["x"], X0, X0 + DX, CX)
        brace(c, X(X0), rows["x"] - 12, X(X0 + DX), rows["x"] - 12, "\\Delta x = 0.05", color=CX, size=15)

    @wt.step("The inner function stretches it", "Squaring maps [1, 1.05] onto [1, 1.1025], about twice as "
             "long. Near x = 1 the factor is the derivative of x², which is 2x = 2.",
             math=f"\\Delta u = {num(U1 - U0, 4)} \\approx 2 \\cdot \\Delta x, du/dx = 2x = {num(DU_DX)}")
    def _(c, X):
        funnel(c, X, rows["x"], X0, X0 + DX, rows["u"], U0, U1, CU)
        seg(c, X, rows["u"], U0, U1, CU)
        c.label_box(X(U1) + 70, (rows["x"] + rows["u"]) / 2, "stretch × 2", color=CU, border=CU, size=15)
        c.text(X(U1) + 10, rows["u"] - 20, f"\\Delta u = {num(U1 - U0, 4)}", size=14, color=CU,
               math=True, anchor="start", halo=True)

    @wt.step("The outer function squeezes it", "Sine maps [1, 1.1025] onto an interval about half as long. "
             "Near u = 1 the factor is the derivative of sin u, which is cos 1 ≈ 0.540.",
             math=f"\\Delta y = {num(Y1 - Y0, 4)} \\approx {COS1} \\cdot \\Delta u, dy/du = cos 1")
    def _(c, X):
        funnel(c, X, rows["u"], U0, U1, rows["y"], Y0, Y1, CY)
        seg(c, X, rows["y"], Y0, Y1, CY)
        c.label_box(X(U1) + 70, (rows["u"] + rows["y"]) / 2, f"squeeze × {COS1}", color=CY, border=CY,
                    size=15)
        c.text(X(Y0) - 60, rows["y"] - 22, f"\\Delta y = {num(Y1 - Y0, 4)}", size=14, color=CY, math=True,
               anchor="end", halo=True)

    @wt.step("Multiply the factors", "Stretch by 2, then squeeze by 0.540: the total factor is about 1.081. "
             "The measured ratio Δy/Δx ≈ 1.02 gets closer to 1.081 as Δx shrinks.",
             math=f"dy/dx = cos(x^2) \\cdot 2x = {COS1} \\cdot 2 \\approx {num(DY_DX)}")
    def _(c, X):
        c.label_box(560, 26, f"total × {num(DY_DX)}", color=theme.PURPLE, border=theme.PURPLE, size=16)
        c.text(560, 50, f"measured: {num(Y1 - Y0, 4)} / 0.05 = {num((Y1 - Y0) / DX, 3)}", size=13,
               color=theme.SOFT_INK)

    return wt


# ---------------------------------------------------------------------------
# Belts and pulleys
# ---------------------------------------------------------------------------


def _belt(c, c1, r1, c2, r2, color):
    """Draws an open belt around two pulleys whose centers share a height."""
    d = c2[0] - c1[0]
    th = math.acos((r1 - r2) / d)
    for s in (1, -1):
        p1 = (c1[0] + r1 * math.cos(th), c1[1] - s * r1 * math.sin(th))
        p2 = (c2[0] + r2 * math.cos(th), c2[1] - s * r2 * math.sin(th))
        c.line(*p1, *p2, color=color, width=3)


def _pulley(c, x, y, r, color, label=None, spokes=6, fill=True):
    c.circle(x, y, r, color=color, fill=theme.fill(color, "22") if fill else theme.PAPER, width=3)
    for k in range(spokes):
        a = 2 * math.pi * k / spokes
        c.line(x, y, x + 0.8 * r * math.cos(a), y + 0.8 * r * math.sin(a), color=color, width=1.2)
    c.circle(x, y, 5, color=color, fill=color, width=1)


@diagram("chain-rule-pulleys", "Chain Rule: Belts and Pulleys", "Calculus")
def chain_rule_pulleys() -> Walkthrough:
    wt = Walkthrough(
        "chain-rule-pulleys", "Chain Rule: Belts and Pulleys", "Calculus",
        concept="dy/dx = dy/du \\cdot du/dx",
        summary="Think of x, u, and y as pulleys joined by belts. Each belt multiplies the turning rate, and "
                "the rates multiply down the line.",
        width=720, height=340, level="301",
    )
    Y = 165
    PX, PU, PY = 120, 350, 575
    rx = 70
    ru = rx / DU_DX            # u spins twice as fast as x
    ru2 = 44                   # second pulley on the u axle
    ry = ru2 / DY_DU           # y spins cos(1) times as fast as u

    @wt.setup
    def _(c):
        _belt(c, (PX, Y), rx, (PU, Y), ru, CU)
        _belt(c, (PU, Y), ru2, (PY, Y), ry, CY)
        _pulley(c, PX, Y, rx, CX)
        _pulley(c, PU, Y, ru2, CY, spokes=8, fill=False)
        _pulley(c, PU, Y, ru, CU)
        _pulley(c, PY, Y, ry, CY)
        c.text(PX, Y + rx + 22, "x pulley", size=14, color=CX, weight="bold")
        c.text(PU, Y + ru2 + 34, "u axle", size=14, color=CU, weight="bold")
        c.text(PY, Y + ry + 22, "y pulley", size=14, color=CY, weight="bold")
        return None

    def turn(c, x, r, label, col):
        c.arc(x, Y, r + 12, 120, 60, color=col, width=2.4, arrow=True)
        c.text(x, Y - r - 30, label, size=15, color=col, math=True, halo=True)

    @wt.step("Build the machine", "Three pulleys stand for x, u = x², and y = sin u. Belts link them, "
             "and the sizes are set for the moment x = 1.",
             math=f"radii: {num(rx, 0)}, {num(ru, 0)} and {num(ru2, 0)}, {num(ry, 1)}")
    def _(c, _ctx):
        c.text((PX + rx + PU - ru2) / 2, Y, f"radii {num(rx, 0)} : {num(ru, 0)}", size=13, color=CU, halo=True)
        c.text((PU + ru2 + PY - ry) / 2, Y, f"radii {num(ru2, 0)} : {num(ry, 1)}", size=13, color=CY, halo=True)

    @wt.step("Turn the input a little", "Give the x pulley a small turn Δx. Everything downstream "
             "moves too.", math="input turn: \\Delta x")
    def _(c, _ctx):
        turn(c, PX, rx, "\\Delta x", CX)

    @wt.step("The first belt doubles it", "The u pulley is half as wide as the x pulley, so it turns twice "
             "as far. That ratio is du/dx = 2x = 2 at x = 1.",
             math="\\Delta u \\approx 2 \\Delta x, du/dx = 2")
    def _(c, _ctx):
        turn(c, PU, ru2, "2 \\Delta x", CU)

    @wt.step("The second belt slows it", "The y pulley is wider than the pulley that drives it, so y turns "
             "only 0.540 as far as u. That ratio is dy/du = cos u = cos 1.",
             math=f"\\Delta y \\approx {COS1} \\Delta u, dy/du = cos 1 \\approx {COS1}")
    def _(c, _ctx):
        turn(c, PY, ry, f"{COS1} \\cdot 2 \\Delta x", CY)

    @wt.step("Multiply along the chain", "One small turn of x becomes 1.081 turns of y: 2 from the first "
             "belt times 0.540 from the second. At another x the pulleys change size, which no real "
             "mechanic tolerates.",
             math=f"dy/dx = dy/du \\cdot du/dx = {COS1} \\cdot 2 \\approx {num(DY_DX)}")
    def _(c, _ctx):
        c.label_box(PY, 300, f"y turns {num(DY_DX)} \\Delta x", color=theme.PURPLE, border=theme.PURPLE,
                    size=16, math=True)

    return wt
