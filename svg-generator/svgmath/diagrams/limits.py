"""Limits: secant lines closing in on a tangent, and the epsilon-delta picture."""

from __future__ import annotations

import math

from .. import theme
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._calculus_tools import num, table_rows


# ---------------------------------------------------------------------------
# Secant to tangent
# ---------------------------------------------------------------------------


@diagram("secant-to-tangent", "Secant Lines to a Tangent Line", "Calculus")
def secant_to_tangent() -> Walkthrough:
    f = lambda x: x * x
    x0 = 1.0
    hs = [2.0, 1.0, 0.5]
    colors = [theme.ORANGE, theme.PURPLE, theme.SKY]
    slope = lambda h: (f(x0 + h) - f(x0)) / h

    wt = Walkthrough(
        "secant-to-tangent", "Secant Lines to a Tangent Line", "Calculus",
        concept="f'(1) = lim_{h \\to 0} (f(1 + h) - f(1))/h = lim_{h \\to 0} (2 + h) = 2",
        summary="A secant line through two points of a curve has a slope you can compute. Slide the second "
                "point toward the first and the secant slopes close in on the slope of the tangent line.",
        width=700, height=400, level="301",
    )
    TX, TY, COLS, RH = 452, 70, (64, 104, 80), 32

    @wt.setup
    def _(c):
        p = Plane(c, box=(50, 34, 360, 330), x=(-0.6, 3.4), y=(-1, 10))
        p.grid(step=1, ystep=1)
        p.axes(step=1, ystep=2)
        p.plot(f, -0.6, 3.4, color=theme.INK)
        X, Y = p.px(2.45, 8.4)
        c.math(X, Y, "y = x^2", size=17, anchor="end", halo=True)
        c.text(TX + sum(COLS) / 2, TY - 22, "secant through P and Q", size=14, color=theme.SOFT_INK)
        table_rows(c, TX, TY, COLS, [["h", "Q", "slope"]], row_h=RH, header=True)
        return p

    @wt.step("Pick a point on the curve", "The point P = (1, 1) sits on the parabola y = x². "
             "Find the steepness of the curve exactly at P.", math="f(x) = x^2, P = (1, 1)")
    def _(c, p):
        p.point(x0, f(x0), "P", color=theme.INK, offset=(-12, -14), anchor="end")

    def secant_step(i):
        h, col = hs[i], colors[i]
        m = slope(h)
        qx, qy = x0 + h, f(x0 + h)

        def draw(c, p):
            new = c.is_new
            p.line_through(x0, f(x0), qx, qy, color=col, width=2.4 if new else 1.6, dash=None if new else "6 5")
            p.point(qx, qy, "Q" if new else None, color=col, offset=(-12, -12), anchor="end")
            if new:
                p.segment(x0, f(x0), qx, f(x0), color=col, width=2)
                p.segment(qx, f(x0), qx, qy, color=col, width=2)
                X0, Y0 = p.px(x0, f(x0))
                X1, _ = p.px(qx, f(x0))
                c.text((X0 + X1) / 2, Y0 + 14, f"h = {num(h)}", size=14, color=col, math=True, halo=True)
                X, Y = p.px(qx, (f(x0) + qy) / 2)
                c.text(X + 8, Y, num(qy - f(x0)), size=14, color=col, anchor="start", math=True, halo=True)
            table_rows(c, TX, TY + RH * (i + 1), COLS,
                       [[num(h), f"({num(qx)}, {num(qy)})", num(m)]], row_h=RH, colors=[col])
        return draw, m

    d, m = secant_step(0)
    wt.step("Draw a secant line", "Take a second point Q = (3, 9), a distance h = 2 to the right. "
            "The line through P and Q rises 8 over a run of 2.",
            math=f"slope = (f(3) - f(1))/2 = 8/2 = {num(m)}")(d)

    d, m = secant_step(1)
    wt.step("Move Q closer", "With h = 1 the point Q = (2, 4) is closer to P. The secant line tilts down "
            "and its slope drops.", math=f"slope = (f(2) - f(1))/1 = 3/1 = {num(m)}")(d)

    d, m = secant_step(2)
    wt.step("Move Q closer again", "With h = 0.5 the secant line nearly matches the curve near P. "
            "Each slope equals 2 + h, so the slopes shrink toward 2.",
            math=f"slope = (2.25 - 1)/0.5 = {num(m)}")(d)

    @wt.step("Let h go to zero", "As h shrinks to zero, Q slides onto P and the secant lines settle on one "
             "line. That limit is the tangent line, and its slope 2 is the derivative at x = 1.",
             math="f'(1) = lim_{h \\to 0} (2 + h) = 2")
    def _(c, p):
        p.line_through(x0, f(x0), x0 + 1, f(x0) + 2, color=theme.GREEN, width=3.2)
        p.point(x0, f(x0), None, color=theme.INK)
        X, Y = p.px(2.0, 3.0)
        c.text(X + 6, Y + 24, "tangent, slope 2", size=15, color=theme.GREEN, anchor="start", halo=True)
        table_rows(c, TX, TY + RH * 4, COLS, [["\\to 0", "\\to P", "2"]], row_h=RH, colors=[theme.GREEN])
        c.text(TX + sum(COLS) / 2, TY + RH * 5 + 26, "slope = 2 + h", size=17, color=theme.SOFT_INK, math=True)

    return wt


# ---------------------------------------------------------------------------
# Epsilon-delta
# ---------------------------------------------------------------------------


@diagram("epsilon-delta", "Limits: The Epsilon-Delta Picture", "Calculus")
def epsilon_delta() -> Walkthrough:
    f = lambda x: x * x / 2
    finv = lambda y: math.sqrt(2 * y)
    a, L = 2.0, 2.0

    def window(eps):
        lo, hi = finv(L - eps), finv(L + eps)
        return lo, hi, min(a - lo, hi - a)

    e1, e2 = 0.5, 0.25
    lo1, hi1, d1 = window(e1)
    lo2, hi2, d2 = window(e2)

    wt = Walkthrough(
        "epsilon-delta", "Limits: The Epsilon-Delta Picture", "Calculus",
        concept="lim_{x \\to c} f(x) = L: for every \\epsilon > 0 some \\delta > 0 gives "
                "|x - c| < \\delta \\implies |f(x) - L| < \\epsilon",
        summary="A limit is a promise: however thin a band you draw around L, you can find a window around c "
                "whose part of the graph stays inside the band.",
        width=680, height=420, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(60, 30, 500, 340), x=(-0.2, 3.3), y=(-0.3, 4.4))
        p.grid(step=0.5, ystep=0.5)
        p.axes(step=0.5, ystep=1)
        return p

    def band(c, p, eps, col, labels=True, opacity=0.2):
        p.region([(p.xmin, L - eps), (p.xmax, L - eps), (p.xmax, L + eps), (p.xmin, L + eps)],
                 color=col, opacity=opacity)
        lc = col if labels else theme.MUTED
        p.hline(L + eps, color=lc, dash="5 4", width=1.4)
        p.hline(L - eps, color=lc, dash="5 4", width=1.4)
        if labels:
            X = p.X(p.xmax) + 8
            c.math(X, p.Y(L + eps), "L + \\epsilon", size=15, color=col, anchor="start")
            c.math(X, p.Y(L - eps), "L - \\epsilon", size=15, color=col, anchor="start")
            c.math(p.X(3.05), p.Y(L + eps / 2), f"\\epsilon = {num(eps)}", size=14, color=col, anchor="end")

    def strip(c, p, d, col, labels=True, opacity=0.2):
        p.region([(a - d, p.ymin), (a + d, p.ymin), (a + d, p.ymax), (a - d, p.ymax)], color=col, opacity=opacity)
        lc = col if labels else theme.MUTED
        p.vline(a - d, color=lc, dash="5 4", width=1.4)
        p.vline(a + d, color=lc, dash="5 4", width=1.4)
        if labels:
            Y = p.top - 12
            c.math(p.X(a - d) - 4, Y, "c - \\delta", size=15, color=col, anchor="end")
            c.math(p.X(a + d) + 4, Y, "c + \\delta", size=15, color=col, anchor="start")

    @wt.step("Name the limit", "The curve y = x²/2 approaches the height L = 2 as x approaches c = 2. "
             "The question is how close x must be to c to keep f(x) close to L.",
             math="lim_{x \\to 2} x^2/2 = 2")
    def _(c, p):
        p.plot(f, -0.2, 3.0, color=theme.INK, width=3)
        c.math(p.X(2.85), p.Y(3.3), "y = x^2/2", size=17, anchor="start", halo=True)
        p.segment(a, 0, a, L, color=theme.SOFT_INK, dash="4 4", width=1.4)
        p.segment(0, L, a, L, color=theme.SOFT_INK, dash="4 4", width=1.4)
        p.point(a, L, None, color=theme.INK)
        c.math(p.X(a), p.Y(0) + 36, "c = 2", size=15, halo=True)
        c.math(p.X(0.06), p.Y(L) - 11, "L = 2", size=15, anchor="start", halo=True)

    @wt.step("Draw an epsilon band", "Choose a tolerance ε = 0.5 and shade every height within ε of L. "
             "The goal is to keep the graph inside this orange band.",
             math=f"|f(x) - 2| < {num(e1)}")
    def _(c, p):
        if c.is_new:
            band(c, p, e1, theme.ORANGE)
        else:
            band(c, p, e1, theme.ORANGE, opacity=0.14)
        p.plot(f, -0.2, 3.0, color=theme.INK, width=3)

    @wt.step("Find where the graph enters the band", "Follow each band edge across to the curve and down "
             "to the x-axis. Between those two x-values, the graph stays inside the band.",
             math=f"sqrt(3) \\approx {num(lo1)} < x < sqrt(5) \\approx {num(hi1)}")
    def _(c, p):
        for xv, yv in ((lo1, L - e1), (hi1, L + e1)):
            p.segment(xv, yv, xv, 0, color=theme.BLUE, dash="4 3", width=1.6)
            p.point(xv, yv, None, color=theme.BLUE, r=4)
            p.point(xv, 0, None, color=theme.BLUE, r=4)
        c.math(p.X(lo1) - 4, p.Y(0) + 34, num(lo1), size=14, color=theme.BLUE, anchor="end", halo=True)
        c.math(p.X(hi1) + 4, p.Y(0) + 34, num(hi1), size=14, color=theme.BLUE, anchor="start", halo=True)

    @wt.step("Choose delta", "Take δ as the smaller distance from c to those x-values, so the window "
             "is the same on both sides. Every x in the blue window gives f(x) inside the orange band.",
             math=f"\\delta = sqrt(5) - 2 \\approx {num(d1)}")
    def _(c, p):
        if c.is_new:
            strip(c, p, d1, theme.BLUE)
            p.plot(f, a - d1, a + d1, color=theme.GREEN, width=5)

    @wt.step("Shrink epsilon", "A thinner band, ε = 0.25, needs a narrower window, δ ≈ 0.121. "
             "Because a matching δ exists for every ε > 0, the limit is 2.",
             math=f"\\epsilon = {num(e2)} \\to \\delta \\approx {num(d2)}", fresh=True)
    def _(c, p):
        band(c, p, e1, theme.ORANGE, labels=False, opacity=0.07)
        band(c, p, e2, theme.ORANGE)
        strip(c, p, d1, theme.BLUE, labels=False, opacity=0.06)
        strip(c, p, d2, theme.BLUE)
        p.plot(f, -0.2, 3.0, color=theme.INK, width=3)
        p.plot(f, a - d2, a + d2, color=theme.GREEN, width=5)
        p.point(a, L, None, color=theme.INK, r=4)
        c.math(p.X(a), p.Y(0) + 36, "c = 2", size=15, halo=True)
        c.math(p.X(0.06), p.Y(L) - 11, "L = 2", size=15, anchor="start", halo=True)

    return wt
