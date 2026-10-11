"""Solving equations and inequalities: balance scales and number lines."""

from __future__ import annotations

from .. import theme
from ..annotate import hop, number_line
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._algebra_helpers import colored_math, thick_ray

X_COL = theme.BLUE
ONE_COL = theme.ORANGE
SOL_COL = theme.GREEN

# ---------------------------------------------------------------------------
# Balance scale
# ---------------------------------------------------------------------------

BEAM_Y = 290
TRAY_Y = 268  # top of each tray, where items rest
LEFT_C, RIGHT_C = 175, 505
XBOX = 40
UNIT = 26


def _scale_frame(c):
    c.rect(40, BEAM_Y - 4, 600, 8, color="none", fill=theme.SOFT_INK, rx=3)
    c.polygon([(340, BEAM_Y + 4), (300, 345), (380, 345)], color=theme.INK, fill=theme.PANEL, width=2)
    c.line(270, 346, 410, 346, color=theme.INK, width=3)
    for cx in (LEFT_C, RIGHT_C):
        c.rect(cx - 4, TRAY_Y + 10, 8, BEAM_Y - TRAY_Y - 14, color="none", fill=theme.SOFT_INK)
        c.rect(cx - 130, TRAY_Y, 260, 10, color=theme.INK, fill=theme.PANEL, width=1.6, rx=4)
    c.text(340, 366 - 6, "level beam = both sides equal", size=theme.SMALL_SIZE, color=theme.SOFT_INK)


def _xbox(c, x, y_bottom, ghost=False):
    y = y_bottom - XBOX
    if ghost:
        c.rect(x, y, XBOX, XBOX, color=theme.RED, dash="5 4", width=1.6, rx=4)
    else:
        c.rect(x, y, XBOX, XBOX, color=X_COL, fill=theme.fill(X_COL, "40"), width=2, rx=4)
        c.text(x + XBOX / 2, y + XBOX / 2, "x", size=22, color=X_COL, math=True)


def _unit(c, x, y_bottom, ghost=False):
    y = y_bottom - UNIT
    if ghost:
        c.rect(x, y, UNIT, UNIT, color=theme.RED, dash="4 3", width=1.5, rx=3)
    else:
        c.rect(x, y, UNIT, UNIT, color=ONE_COL, fill=theme.fill(ONE_COL, "55"), width=1.6, rx=3)
        c.text(x + UNIT / 2, y + UNIT / 2, "1", size=13, color=theme.INK)


def _unit_block(c, x, n_cols, n, ghost=False, gap=4):
    """Stacks n unit weights on the tray in rows of n_cols, starting at left x."""
    for i in range(n):
        r, k = divmod(i, n_cols)
        _unit(c, x + k * (UNIT + gap), TRAY_Y - r * (UNIT + 2), ghost)


def _stacks(c, x, n_stacks, height, pitch):
    """Draws n_stacks columns of `height` unit weights, columns `pitch` apart."""
    for s in range(n_stacks):
        for r in range(height):
            _unit(c, x + s * pitch, TRAY_Y - r * (UNIT + 2))


def _group_box(c, x, w, h, label):
    c.rect(x - 3, TRAY_Y - h - 4, w + 6, h + 7, color=SOL_COL, dash="6 4", width=2, rx=6)
    c.text(x + w / 2, TRAY_Y - h - 18, label, size=theme.SMALL_SIZE, color=SOL_COL, weight="bold")


@diagram("balance-scale", "Solving an Equation on a Balance Scale", "Algebra")
def build_balance() -> Walkthrough:
    wt = Walkthrough(
        "balance-scale", "Solving an Equation on a Balance Scale", "Algebra",
        concept="3x + 4 = 19 \\implies 3x = 15 \\implies x = 5",
        summary="An equation is a level balance. Do the same thing to both pans and it stays level, "
                "so you can strip away weights until one x sits alone.",
        width=680, height=380, level="201",
    )
    a, b, rhs = 3, 4, 19
    rest = rhs - b
    x_val = rest // a
    pitch = XBOX + 14  # x boxes and stacks of ones share a spacing, so groups line up

    def left_x0(n_x, with_units):
        w = n_x * pitch - 14 + (20 + 2 * UNIT + 4 if with_units else 0)
        return LEFT_C - w / 2

    def right_x0(n_stacks, with_units):
        w = n_stacks * pitch - 14 - (XBOX - UNIT) + (24 + 2 * UNIT + 4 if with_units else 0)
        return RIGHT_C - w / 2

    def tags(c, x0, r0, units):
        """Small count labels above each pile."""
        c.text(x0 + (a * pitch - 14) / 2, TRAY_Y - XBOX - 14, f"{a} boxes", size=13, color=X_COL)
        c.text(r0 + (a * pitch - 14 - (XBOX - UNIT)) / 2, TRAY_Y - x_val * (UNIT + 2) - 14,
               f"{rest} ones", size=13, color=ONE_COL)
        if units:
            ux = x0 + a * pitch - 14 + 20
            rx = r0 + (a - 1) * pitch + UNIT + 24
            for gx in (ux, rx):
                c.text(gx + UNIT + 2, TRAY_Y - 2 * (UNIT + 2) - 12, f"{b} ones", size=13, color=ONE_COL)

    @wt.setup
    def _(c):
        _scale_frame(c)

    @wt.step("Load the scale", f"The left pan holds {a} mystery boxes, each weighing x, plus {b} ones. "
             f"The right pan holds {rhs} ones. The beam is level, so both sides weigh the same.",
             math=f"{a}x + {b} = {rhs}", fresh=True)
    def _(c):
        x0 = left_x0(a, True)
        for i in range(a):
            _xbox(c, x0 + i * pitch, TRAY_Y)
        _unit_block(c, x0 + a * pitch - 14 + 20, 2, b)
        r0 = right_x0(a, True)
        _stacks(c, r0, a, x_val, pitch)
        _unit_block(c, r0 + (a - 1) * pitch + UNIT + 24, 2, b)
        tags(c, x0, r0, True)
        colored_math(c, LEFT_C, 46, [(f"{a}x", X_COL), (f" + {b}", ONE_COL)], size=26)
        c.text(340, 46, "=", size=30, color=theme.INK)
        colored_math(c, RIGHT_C, 46, [(f"{rhs}", ONE_COL)], size=26)

    @wt.step(f"Take {b} ones off each pan", f"Lift {b} ones off the left and {b} ones off the right. "
             "Equal weights leave both pans, so the beam does not budge.",
             math=f"{a}x + {b} - {b} = {rhs} - {b}", fresh=True)
    def _(c):
        x0 = left_x0(a, True)
        for i in range(a):
            _xbox(c, x0 + i * pitch, TRAY_Y)
        ux = x0 + a * pitch - 14 + 20
        _unit_block(c, ux, 2, b, ghost=True)
        r0 = right_x0(a, True)
        _stacks(c, r0, a, x_val, pitch)
        rx = r0 + (a - 1) * pitch + UNIT + 24
        _unit_block(c, rx, 2, b, ghost=True)
        for gx in (ux, rx):
            c.arrow(gx + UNIT + 2, TRAY_Y - 2 * UNIT - 8, gx + UNIT + 2, TRAY_Y - 2 * UNIT - 50,
                    color=theme.RED, width=2.2)
            c.text(gx + UNIT + 2, TRAY_Y - 2 * UNIT - 64, f"−{b}", size=16, color=theme.RED, weight="bold")
        colored_math(c, LEFT_C, 46, [(f"{a}x", X_COL), (f" + {b}", ONE_COL), (f" - {b}", theme.RED)], size=26)
        c.text(340, 46, "=", size=30, color=theme.INK)
        colored_math(c, RIGHT_C, 46, [(f"{rhs}", ONE_COL), (f" - {b}", theme.RED)], size=26)

    @wt.step("See what is left", f"The left pan holds only the {a} boxes. The right pan holds "
             f"{rest} ones, stacked in {a} columns of {x_val}.", math=f"{a}x = {rest}", fresh=True)
    def _(c):
        x0 = left_x0(a, False)
        for i in range(a):
            _xbox(c, x0 + i * pitch, TRAY_Y)
        _stacks(c, right_x0(a, False), a, x_val, pitch)
        tags(c, x0, right_x0(a, False), False)
        colored_math(c, LEFT_C, 46, [(f"{a}x", X_COL)], size=26)
        c.text(340, 46, "=", size=30, color=theme.INK)
        colored_math(c, RIGHT_C, 46, [(f"{rest}", ONE_COL)], size=26)

    @wt.step(f"Split each pan into {a} equal groups", f"Divide both sides by {a}. Each box on the left "
             f"matches one stack of {x_val} on the right, group for group.",
             math=f"{a}x / {a} = {rest} / {a}", fresh=True)
    def _(c):
        x0 = left_x0(a, False)
        r0 = right_x0(a, False)
        for i in range(a):
            _xbox(c, x0 + i * pitch, TRAY_Y)
            _group_box(c, x0 + i * pitch, XBOX, XBOX, f"{i + 1}")
        _stacks(c, r0, a, x_val, pitch)
        sh = x_val * (UNIT + 2) - 2
        for i in range(a):
            _group_box(c, r0 + i * pitch, UNIT, sh, f"{i + 1}")
        colored_math(c, LEFT_C, 46, [(f"{a}x", X_COL), (f" / {a}", SOL_COL)], size=26)
        c.text(340, 46, "=", size=30, color=theme.INK)
        colored_math(c, RIGHT_C, 46, [(f"{rest}", ONE_COL), (f" / {a}", SOL_COL)], size=26)

    @wt.step("Keep one group per pan", f"One box balances one stack of {x_val} ones, so x = {x_val}. "
             f"Check it: {a} boxes of {x_val} plus {b} ones weigh {a * x_val + b}, the same as the right pan.",
             math=f"x = {x_val};   {a} \\cdot {x_val} + {b} = {a * x_val + b}", fresh=True)
    def _(c):
        _xbox(c, LEFT_C - XBOX / 2, TRAY_Y)
        _stacks(c, RIGHT_C - UNIT / 2, 1, x_val, pitch)
        c.circle(LEFT_C, TRAY_Y - XBOX / 2, 34, color=SOL_COL, width=2.5)
        c.text(LEFT_C + 90, TRAY_Y - 30, "one x", size=15, color=X_COL)
        c.text(RIGHT_C + 80, TRAY_Y - 70, f"{x_val} ones", size=15, color=ONE_COL)
        colored_math(c, LEFT_C, 46, [("x", X_COL)], size=26)
        c.text(340, 46, "=", size=30, color=theme.INK)
        colored_math(c, RIGHT_C, 46, [(f"{x_val}", SOL_COL)], size=26)
        c.label_box(340, 120, f"x = {x_val}", size=20, color=SOL_COL, border=SOL_COL, math=True)

    return wt


# ---------------------------------------------------------------------------
# Linear inequality
# ---------------------------------------------------------------------------


@diagram("inequality-number-line", "Solving a Linear Inequality", "Algebra")
def build_inequality() -> Walkthrough:
    wt = Walkthrough(
        "inequality-number-line", "Solving a Linear Inequality", "Algebra",
        concept="-2x + 3 < 7 \\implies -2x < 4 \\implies x > -2",
        summary="Solve an inequality like an equation, with one catch: multiplying or dividing by a negative "
                "number flips the number line, so the inequality sign flips too.",
        width=680, height=400, level="201",
    )
    YT, YB = 90, 280
    x0, x1 = 110, 610
    m, k, rhs = -2, 3, 7
    bound_u = rhs - k  # -2x < 4
    bound_x = bound_u / m  # x > -2

    @wt.setup
    def _(c):
        return {}

    def lines(c):
        Xt = number_line(c, x0, YT, x1, -8, 8, step=1, label_every=2, size=13)
        Xb = number_line(c, x0, YB, x1, -4, 4, step=1, size=13)
        c.math(48, YT, "-2x", size=20, color=theme.INK)
        c.math(48, YB, "x", size=20, color=theme.INK)
        c.text(48, YT + 22, "values", size=11, color=theme.SOFT_INK)
        c.text(48, YB + 22, "values", size=11, color=theme.SOFT_INK)
        return Xt, Xb

    @wt.step("Subtract 3 from both sides", f"Peel off the + {k} first, just as with an equation. "
             f"The top line shows the values that −2x may take: anything less than {bound_u}.",
             math=f"-2x + 3 - 3 < 7 - 3   so   -2x < {bound_u}")
    def _(c, ctx):
        Xt, Xb = lines(c)
        ctx["Xt"], ctx["Xb"] = Xt, Xb
        thick_ray(c, Xt(bound_u) - 8, x0 - 12, YT)
        c.dot(Xt(bound_u), YT, r=7, color=ONE_COL, hollow=True)
        c.math(Xt(bound_u - 3), YT - 32, f"-2x < {bound_u}", size=20, color=ONE_COL, halo=True)
        c.text(Xt(bound_u) + 8, YT - 32, "open circle: 4 itself fails", size=12, color=theme.SOFT_INK,
               anchor="start")

    @wt.step("Divide by −2 and watch the line flip", "Each value on the top line maps to x = value ÷ (−2). "
             "The arrows cross in the middle: big numbers become small ones, so the order reverses.",
             math=f"{bound_u} / (-2) = {bound_x:g}")
    def _(c, ctx):
        Xt, Xb = ctx["Xt"], ctx["Xb"]
        for u in range(-6, 7, 2):
            hl = u == bound_u
            col = X_COL if hl else theme.MUTED
            c.arrow(Xt(u), YT + 34, Xb(u / m), YB - 12, color=col, width=2.4 if hl else 1.3)
        c.text(540, 175, "÷ (−2)", size=16, color=X_COL, weight="bold")
        c.text(540, 197, "order reverses", size=13, color=theme.SOFT_INK)
        c.text(175, 175, "right ↔ left", size=13, color=theme.SOFT_INK)

    @wt.step("Flip the inequality sign", f"The orange values left of {bound_u} on top land right of "
             f"{bound_x:g} on the bottom. Less-than becomes greater-than.",
             math=f"-2x < {bound_u}  \\implies  x > {bound_x:g}")
    def _(c, ctx):
        Xb = ctx["Xb"]
        thick_ray(c, Xb(bound_x) + 8, x1 + 14, YB)
        c.dot(Xb(bound_x), YB, r=7, color=ONE_COL, hollow=True)
        c.math(Xb(1.2), YB + 48, f"x > {bound_x:g}", size=22, color=ONE_COL)

    @wt.step("Test one point on each side", "Plug in a shaded point and an unshaded point. Only the "
             "shaded one makes the original inequality true, so the shading is right.",
             math="x = 0: -2(0) + 3 = 3 < 7 true;   x = -3: -2(-3) + 3 = 9 < 7 false")
    def _(c, ctx):
        Xb = ctx["Xb"]
        for xv, col, ok in ((0, SOL_COL, True), (-3, theme.RED, False)):
            val = m * xv + k
            c.dot(Xb(xv), YB, r=6, color=col)
            verdict = "true" if ok else "false"
            c.text(Xb(xv), YB + 86, f"x = {xv}: {val} < {rhs} {verdict}".replace("-", "−"), size=14,
                   color=col, weight="bold")
            c.line(Xb(xv), YB + 8, Xb(xv), YB + 14, color=col, width=2)

    return wt


# ---------------------------------------------------------------------------
# Absolute value as distance
# ---------------------------------------------------------------------------

CENTER, RADIUS = 2, 3


@diagram("absolute-value-distance", "Absolute Value Inequality as Distance", "Algebra")
def build_abs() -> Walkthrough:
    wt = Walkthrough(
        "absolute-value-distance", "Absolute Value Inequality as Distance", "Algebra",
        concept="|x - 2| < 3 \\iff -1 < x < 5",
        summary="|x − 2| is the distance from x to 2. Asking for a distance under 3 picks out every point "
                "within 3 steps of 2, in either direction.",
        width=680, height=290, level="201",
    )
    Y = 120
    lo, hi = CENTER - RADIUS, CENTER + RADIUS

    @wt.setup
    def _(c):
        return number_line(c, 70, Y, 610, -3, 7)

    @wt.step("Read |x − 2| as a distance", "The bars measure how far x sits from 2, ignoring direction. "
             "So mark 2 as the center.", math="|x - 2| = distance from x to 2")
    def _(c, X):
        c.dot(X(CENTER), Y, r=7, color=theme.PURPLE)
        c.text(X(CENTER), Y + 50, "center 2", size=14, color=theme.PURPLE, weight="bold")

    @wt.step("Walk 3 steps each way", "Step 3 to the right and 3 to the left of the center. Both walks "
             "cover the same distance.", math=f"{CENTER} - {RADIUS} = {lo},   {CENTER} + {RADIUS} = {hi}")
    def _(c, X):
        hop(c, X(CENTER), X(hi), Y, f"{RADIUS}", color=X_COL, height=50, size=16)
        hop(c, X(CENTER), X(lo), Y, f"{RADIUS}", color=X_COL, height=50, size=16)

    @wt.step("Mark the edges with open circles", f"At {lo} and {hi} the distance is exactly 3. "
             "The rule says less than 3, so the edges stay out.", math=f"|{lo} - 2| = 3,   |{hi} - 2| = 3")
    def _(c, X):
        for v in (lo, hi):
            c.dot(X(v), Y, r=7, color=ONE_COL, hollow=True)

    @wt.step("Shade everything closer than 3", "Every point between the edges is within 3 of the "
             "center. One absolute value inequality becomes two plain ones.",
             math=f"-{RADIUS} < x - 2 < {RADIUS}   so   {lo} < x < {hi}")
    def _(c, X):
        thick_ray(c, X(lo) + 8, X(hi) - 8, Y, arrow=False)
        c.dot(X(CENTER), Y, r=7, color=theme.PURPLE)
        for v in (lo, hi):
            c.dot(X(v), Y, r=7, color=ONE_COL, hollow=True)
        c.math(X(CENTER), Y + 82, f"{lo} < x < {hi}", size=20, color=ONE_COL)

    @wt.step("Check one point inside and one outside", "x = 4 is 2 away from the center: in. "
             "x = 6 is 4 away: too far, out.", math="|4 - 2| = 2 < 3 in;   |6 - 2| = 4 > 3 out")
    def _(c, X):
        for xv, col in ((4, SOL_COL), (6, theme.RED)):
            c.dot(X(xv), Y, r=6, color=col)
            d = abs(xv - CENTER)
            rel = "<" if d < RADIUS else ">"
            c.math(X(xv) + (14 if xv == 6 else 0), Y + 122, f"|{xv} - 2| = {d} {rel} 3", size=16, color=col)

    return wt


@diagram("absolute-value-graph", "Absolute Value Inequality on a Graph", "Algebra")
def build_abs_graph() -> Walkthrough:
    wt = Walkthrough(
        "absolute-value-graph", "Absolute Value Inequality on a Graph", "Algebra",
        concept="|x - 2| < 3 \\iff -1 < x < 5",
        summary="Graph y = |x − 2| as a V and the line y = 3. The solutions of |x − 2| < 3 are the x values "
                "where the V dips below the line.",
        width=640, height=420, level="201",
    )
    f = lambda x: abs(x - CENTER)
    lo, hi = CENTER - RADIUS, CENTER + RADIUS

    @wt.setup
    def _(c):
        p = Plane(c, box=(50, 30, 550, 340), x=(-3, 7), y=(-1.5, 6))
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    @wt.step("Graph the V", "y = |x − 2| is the distance from x to 2. It is 0 at x = 2 and climbs "
             "1 unit for every step away, in both directions.", math="y = |x - 2|")
    def _(c, p):
        p.plot(f, color=X_COL)
        p.label(5.5, 5.5, "y = |x - 2|", color=X_COL, size=18)
        p.point(CENTER, 0, "(2, 0)", color=theme.PURPLE, offset=(0, 36), anchor="middle")

    @wt.step("Draw the line y = 3", "The inequality asks where the V stays below a height of 3.",
             math="y = 3")
    def _(c, p):
        p.plot(lambda x: RADIUS, color=ONE_COL, label="y = 3", label_at=6.3)

    @wt.step("Find where they cross", f"The V meets the line at x = {lo} and x = {hi}, which are 3 steps "
             "left and right of 2.", math=f"|{lo} - 2| = 3,   |{hi} - 2| = 3")
    def _(c, p):
        for v in (lo, hi):
            p.point(v, RADIUS, f"({v}, 3)", color=theme.RED, offset=(-12 if v < 2 else 12, 18),
                    anchor="end" if v < 2 else "start")
            p.vline(v, color=theme.RED, y0=0, y1=RADIUS)

    @wt.step("Shade where the V is lower", f"Between the crossings the V sits under the line. Drop "
             "that stretch to the x-axis: the answer is the open interval from −1 to 5.",
             math=f"{lo} < x < {hi}")
    def _(c, p):
        p.shade_between(lambda x: RADIUS, f, lo, hi, color=SOL_COL, opacity=0.25)
        X0, Y0 = p.px(lo, 0)
        X1, _ = p.px(hi, 0)
        c.line(X0 + 7, Y0, X1 - 7, Y0, color=ONE_COL, width=7, opacity=0.8)
        c.dot(X0, Y0, r=7, color=ONE_COL, hollow=True)
        c.dot(X1, Y0, r=7, color=ONE_COL, hollow=True)
        p.label(CENTER, 1.6, "below the line", color=SOL_COL, size=14, math=False)

    return wt
