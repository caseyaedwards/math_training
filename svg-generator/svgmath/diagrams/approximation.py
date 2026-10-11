"""Approximation with derivatives: Taylor polynomials and Newton's method."""

from __future__ import annotations

import math

from .. import theme
from ..plane import Plane, pi_label
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._calculus_tools import num, table_rows


# ---------------------------------------------------------------------------
# Taylor polynomials of sin x
# ---------------------------------------------------------------------------


def _taylor_sin(n: int):
    """Returns the degree-n Taylor polynomial of sin x about 0 (n odd)."""
    terms = [(k, (-1) ** ((k - 1) // 2) / math.factorial(k)) for k in range(1, n + 1, 2)]
    return lambda x: sum(c * x ** k for k, c in terms)


def _good_radius(P, tol: float = 0.05, step: float = 0.001, top: float = 7.0) -> float:
    """Largest r with |P(t) - sin t| < tol for every t in [0, r]. The error is odd, so this covers [-r, r]."""
    t = 0.0
    while t < top and abs(P(t + step) - math.sin(t + step)) < tol:
        t += step
    return t


@diagram("taylor-polynomials", "Taylor Polynomials of sin x", "Calculus")
def taylor_polynomials() -> Walkthrough:
    degrees = [1, 3, 5, 7]
    colors = [theme.ORANGE, theme.PURPLE, theme.RED, theme.BLUE]
    polys = [_taylor_sin(n) for n in degrees]
    radii = [_good_radius(P) for P in polys]

    wt = Walkthrough(
        "taylor-polynomials", "Taylor Polynomials of sin x", "Calculus",
        concept="sin x = x - x^3/3! + x^5/5! - x^7/7! + \\ldots",
        summary="A Taylor polynomial copies a function's value and derivatives at one point. Each extra term "
                "makes the copy hug the curve over a wider stretch.",
        width=700, height=440, level="301",
    )
    STRIP = 322

    @wt.setup
    def _(c):
        p = Plane(c, box=(40, 24, 610, 270), x=(-6.9, 6.9), y=(-2.2, 2.2))
        p.grid(step=math.pi / 2, ystep=1)
        p.axes(step=math.pi / 2, ystep=1, xfmt=lambda v: pi_label(v, 2))
        p.plot(math.sin, color=theme.INK, width=4)
        c.math(p.X(-4.71), p.Y(1) - 18, "y = sin x", size=17, halo=True)
        c.text(20, STRIP, "where the copy stays within 0.05 of sin x", size=13, color=theme.SOFT_INK,
               anchor="start")
        return p

    def row_y(i):
        return STRIP + 24 + i * 22

    def poly_step(i):
        P, col, r = polys[i], colors[i], radii[i]

        def draw(c, p):
            new = c.is_new
            p.plot(P, color=col if new else theme.fill(col, "66"), width=3.2 if new else 1.8)
            if new:
                # label the curve where it leaves the plane on the right
                t = 0.0
                while abs(P(t)) < 1.95:
                    t += 0.01
                X, Y = p.px(t, math.copysign(1.85, P(t)))
                c.text(X + 10, Y, f"P_{degrees[i]}", size=17, color=col, math=True, anchor="start", halo=True)
            y = row_y(i)
            c.line(p.X(-r), y, p.X(r), y, color=col, width=8)
            c.text(20, y, f"degree {degrees[i]}", size=13, color=col, anchor="start", weight="bold")
            c.text(p.X(r) + 10, y, f"|x| < {num(r, 2)}", size=13, color=col, anchor="start", math=True)
        return draw

    @wt.step("Start at one point", "At x = 0, sin x has value 0 and slope 1, and its later derivatives "
             "repeat 0, −1, 0, 1. A Taylor polynomial copies those numbers.",
             math="sin 0 = 0, slopes at 0: 1, 0, -1, 0, 1, ...")
    def _(c, p):
        p.point(0, 0, None, color=theme.INK, r=6)

    wt.step("Degree 1: the tangent line", "The first copy is the tangent line y = x. It matches the value "
            f"and the slope, and stays within 0.05 of sin x out to |x| ≈ {num(radii[0], 2)}.",
            math="P_1(x) = x")(poly_step(0))
    wt.step("Degree 3: add a bend", "Subtract x³/6. The cubic bends down with the sine curve and stays "
            "close twice as far out.", math="P_3(x) = x - x^3/6")(poly_step(1))
    wt.step("Degree 5: bend back", "Add x⁵/120. The copy now follows the first hill and the first valley "
            "past their tops.", math="P_5(x) = x - x^3/6 + x^5/120")(poly_step(2))
    wt.step("Degree 7: reach further", "Subtract x⁷/5040. Every new term pushes the good stretch further "
            f"out, here to |x| ≈ {num(radii[3], 2)}. Infinitely many terms give sin x everywhere, which is a lot "
            "of homework.",
            math="P_7(x) = x - x^3/6 + x^5/120 - x^7/5040")(poly_step(3))

    return wt


# ---------------------------------------------------------------------------
# Newton's method
# ---------------------------------------------------------------------------


def _sig(v: float, digits: int = 2) -> str:
    """Formats a small positive number in plain decimals with a few significant digits."""
    d = max(0, digits - 1 - math.floor(math.log10(v)))
    return f"{v:.{d}f}"


@diagram("newtons-method", "Newton's Method", "Calculus")
def newtons_method() -> Walkthrough:
    f = lambda x: x * x - 2
    df = lambda x: 2 * x
    xs = [2.0]
    for _ in range(3):
        xs.append(xs[-1] - f(xs[-1]) / df(xs[-1]))
    root = math.sqrt(2)
    colors = [theme.INK, theme.ORANGE, theme.PURPLE, theme.GREEN]

    wt = Walkthrough(
        "newtons-method", "Newton's Method", "Calculus",
        concept="x_{n+1} = x_n - f(x_n)/f'(x_n)",
        summary="Guess a root, replace the curve by its tangent line, and jump to where the tangent crosses "
                "zero. Each jump roughly doubles the number of correct digits.",
        width=720, height=400, level="301",
    )
    TX, TY, COLS, RH = 468, 70, (44, 112, 86), 32

    @wt.setup
    def _(c):
        p = Plane(c, box=(50, 30, 390, 330), x=(1.2, 2.15), y=(-0.7, 2.4))
        p.grid(step=0.05, ystep=0.25)
        p.axes(step=0.25, ystep=0.5, xlabel="")
        p.plot(f, 1.2, 2.15, color=theme.INK)
        c.math(p.X(1.25), p.Y(2.2), "y = x^2 - 2", size=16, anchor="start", halo=True)
        c.text(TX + sum(COLS) / 2, TY - 22, "guesses for the root of x² − 2", size=13, color=theme.SOFT_INK)
        table_rows(c, TX, TY, COLS, [["n", "guess", "error"]], row_h=RH, header=True)
        return p

    def row(c, n):
        table_rows(c, TX, TY + RH * (n + 1), COLS,
                   [[str(n), f"{xs[n]:.7f}".rstrip("0").rstrip("."), _sig(abs(xs[n] - root))]],
                   row_h=RH, colors=[colors[n]])

    @wt.step("Make a first guess", "Find where y = x² − 2 crosses zero, that is √2. Start with the guess "
             "x₀ = 2, where the curve sits at height 2.",
             math="x_0 = 2, f(2) = 2, f'(2) = 4")
    def _(c, p):
        p.point(root, 0, None, color=theme.GREEN, r=5, hollow=True)
        c.text(p.X(root) - 10, p.Y(0) - 18, "root sqrt(2)", size=14, color=theme.GREEN, math=True, anchor="end",
               halo=True)
        p.point(2, 0, None, color=theme.INK, r=5)
        p.segment(2, 0, 2, f(2), color=theme.SOFT_INK, dash="4 3", width=1.4)
        p.point(2, f(2), "(2, 2)", color=theme.INK, offset=(-10, -10), anchor="end", size=14)
        c.text(p.X(2), p.Y(0) + 34, "x_0", size=15, color=theme.INK, math=True)
        row(c, 0)

    def newton_step(n):
        x0, x1, col = xs[n - 1], xs[n], colors[n]

        def draw(c, p):
            new = c.is_new
            p.segment(x0, f(x0), x1, 0, color=col, width=2.6 if new else 1.6)
            if new:
                p.line_through(x0, f(x0), x1, 0, color=col, width=1.2, dash="5 4")
            p.point(x1, 0, None, color=col, r=5)
            if n < 3:
                p.segment(x1, 0, x1, f(x1), color=theme.SOFT_INK, dash="4 3", width=1.4)
                p.point(x1, f(x1), None, color=col, r=4)
                c.text(p.X(x1), p.Y(0) + 34, f"x_{n}", size=15, color=col, math=True,
                       halo=True)
            row(c, n)
            if n == 3 and new:
                zoom_inset(c)
        return draw

    def zoom_inset(c):
        z = Plane(c, box=(486, 262, 214, 112), x=(1.4095, 1.4195), y=(-0.012, 0.016))
        c.rect(z.left, z.top, z.w, z.h, color=theme.MUTED, fill=theme.PAPER, width=1)
        c.text(z.left + z.w / 2, z.top - 12, "zoom near the root", size=13, color=theme.SOFT_INK)
        z.hline(0, color=theme.INK, dash=None, width=1.4)
        z.plot(f, color=theme.INK, width=2.5)
        x2, x3 = xs[2], xs[3]
        z.segment(x2, f(x2), x3, 0, color=theme.GREEN, width=2.4)
        z.segment(x2, 0, x2, f(x2), color=theme.SOFT_INK, dash="4 3", width=1.2)
        z.point(x2, 0, None, color=theme.PURPLE, r=4)
        z.point(x2, f(x2), None, color=theme.PURPLE, r=4)
        z.point(x3, 0, None, color=theme.GREEN, r=5)
        c.text(z.left + z.w - 6, z.Y(0) + 18, f"x_2 = {xs[2]:.5f}", size=12, color=theme.PURPLE, math=True,
               anchor="end")
        c.text(z.X(x3) - 6, z.Y(0) - 14, f"x_3 \\approx sqrt(2)", size=12, color=theme.GREEN, math=True,
               anchor="end", halo=True)

    wt.step("Follow the tangent down", "The tangent at (2, 2) has slope 4. It hits zero 2/4 = 0.5 to the "
            "left, at x₁ = 1.5.",
            math="x_1 = 2 - f(2)/f'(2) = 2 - 2/4 = 1.5")(newton_step(1))
    wt.step("Repeat from the new guess", "Climb to the curve at x₁ = 1.5, where f = 0.25, and slide down "
            "its tangent of slope 3. The next guess is 1.41667.",
            math=f"x_2 = 1.5 - 0.25/3 \\approx {xs[2]:.5f}")(newton_step(2))
    wt.step("Watch the digits pile up", "One more jump lands within 0.000003 of √2. The error column "
            "roughly squares each time, so a few jumps beat a lot of guessing.",
            math=f"x_3 \\approx {xs[3]:.6f}, sqrt(2) \\approx {root:.6f}")(newton_step(3))

    return wt
