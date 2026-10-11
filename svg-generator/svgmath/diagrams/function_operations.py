"""Operations on functions: transformations, inverses, and composition."""

from __future__ import annotations

import math

from .. import theme
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._function_kit import ball, ctable, machine, num, tag

CAT = "Functions"


# ---------------------------------------------------------------------------
# Transformations of y = x^2
# ---------------------------------------------------------------------------


@diagram("function-transformations", "Transforming y = x²", CAT)
def build_transformations() -> Walkthrough:
    wt = Walkthrough(
        "function-transformations", "Transforming y = x²", CAT,
        concept="y = x^2 \\to y = -2(x - 2)^2 + 4",
        summary="Build y = −2(x − 2)² + 4 from y = x² one move at a time: shift right, stretch, reflect, "
                "shift up. Follow two points to see what each move does.",
        width=720, height=440, level="201",
    )
    # (equation, move note, color, f, vertex, tracked point)
    stages = [
        ("y = x^2", "start", theme.BLUE, lambda x: x * x),
        ("y = (x - 2)^2", "right 2", theme.ORANGE, lambda x: (x - 2) ** 2),
        ("y = 2(x - 2)^2", "stretch × 2", theme.GREEN, lambda x: 2 * (x - 2) ** 2),
        ("y = -2(x - 2)^2", "flip over x-axis", theme.RED, lambda x: -2 * (x - 2) ** 2),
        ("y = -2(x - 2)^2 + 4", "up 4", theme.PURPLE, lambda x: -2 * (x - 2) ** 2 + 4),
    ]
    # the vertex and the point that starts at (1, 1), after each move
    V = [(0, 0), (2, 0), (2, 0), (2, 0), (2, 4)]
    P = [(1, 1), (3, 1), (3, 2), (3, -2), (3, 2)]
    # label offsets for P, chosen so labels clear the curve
    p_off = [(12, 12), (12, 12), (12, 10), (12, -12), (12, 10)]

    @wt.setup
    def _(c):
        p = Plane(c, box=(40, 30, 450, 395), x=(-3.5, 6.5), y=(-6, 9.5))
        p.grid(step=1, ystep=1)
        p.axes(step=1, ystep=2)
        c.rect(520, 14, 188, 412, color=theme.GRID, fill=theme.PANEL, width=1, rx=8)
        return p

    def draw(c, p, k):
        eq, note, col, fn = stages[k]
        if k > 0:
            p.plot(stages[k - 1][3], color=theme.MUTED, width=2, dash="6 5")
        p.plot(fn, color=col)
        # moves of the two tracked points
        if k > 0:
            for (a, b) in ((V[k - 1], V[k]), (P[k - 1], P[k])):
                if a != b:
                    A, B = p.px(*a), p.px(*b)
                    c.curved_arrow(A[0], A[1], B[0], B[1], bend=0.25, color=theme.INK, width=1.8)
                    c.dot(A[0], A[1], r=4, color=theme.MUTED)
        vx, vy = V[k]
        X, Y = p.px(vx, vy)
        c.dot(X, Y, r=6, color=col)
        vlx, vly, va = {0: (X + 12, Y + 34, "start"), 3: (X - 8, Y - 20, "end"),
                        4: (X - 10, Y - 18, "end")}.get(k, (X, Y + 36, "middle"))
        c.text(vlx, vly, f"V({num(vx)}, {num(vy)})", size=14, color=col, anchor=va, math=True, halo=True)
        X, Y = p.px(*P[k])
        c.dot(X, Y, r=6, color=col)
        ox, oy = p_off[k]
        c.text(X + ox, Y + oy, f"P({num(P[k][0])}, {num(P[k][1])})", size=14, color=col, anchor="start",
               math=True, halo=True)
        # the equation ladder on the right
        c.text(614, 34, "build it one move at a time", size=12, color=theme.SOFT_INK)
        for i in range(k + 1):
            e, n, cc, _ = stages[i]
            y = 70 + i * 74
            if i == k:
                c.rect(528, y - 20, 172, 58, color=cc, fill=theme.PAPER, width=2, rx=6)
            c.math(614, y, e, size=16, color=cc if i == k else theme.SOFT_INK)
            c.text(614, y + 22, n, size=13, color=cc if i == k else theme.MUTED)
            if i < k:
                c.arrow(614, y + 34, 614, y + 52, color=theme.MUTED, width=1.5)

    @wt.step("Start with the parent", "The parent graph y = x² has its vertex V at the origin. Track V and "
             "the point P(1, 1) through every move.", math="y = x^2", fresh=True)
    def _(c, p):
        draw(c, p, 0)

    @wt.step("Shift right 2", "Replace x with x − 2. Every point moves 2 to the right. Yes, minus means "
             "right here. The x inside has to reach 2 to do what x = 0 used to do.",
             math="(x, y) \\to (x + 2, y)", fresh=True)
    def _(c, p):
        draw(c, p, 1)

    @wt.step("Stretch by 2", "Multiply the outside by 2. Every height doubles, so P climbs from 1 to 2. "
             "The vertex sits at height 0, and twice nothing is still nothing.",
             math="(x, y) \\to (x, 2y)", fresh=True)
    def _(c, p):
        draw(c, p, 2)

    @wt.step("Reflect over the x-axis", "Put a minus sign in front. Every height changes sign, so the cup "
             "turns into a cap and P drops to −2.", math="(x, y) \\to (x, -y)", fresh=True)
    def _(c, p):
        draw(c, p, 3)

    @wt.step("Shift up 4", "Add 4 at the end. Every point rises 4, so the vertex lands at (2, 4) and P at "
             "(3, 2). Four moves, one equation.", math="y = -2(x - 2)^2 + 4", fresh=True)
    def _(c, p):
        draw(c, p, 4)

    return wt


# ---------------------------------------------------------------------------
# Inverse functions
# ---------------------------------------------------------------------------


@diagram("inverse-functions", "Inverse Functions", CAT)
def build_inverse() -> Walkthrough:
    wt = Walkthrough(
        "inverse-functions", "Inverse Functions: 2ˣ and log₂ x", CAT,
        concept="y = 2^x \\iff x = log_2 y;  graphs mirror across y = x",
        summary="An inverse function undoes the original. Swap every input and output pair, and the graph "
                "flips across the line y = x.",
        width=720, height=440, level="201",
    )
    B, O = theme.BLUE, theme.ORANGE
    xs = [-1, 0, 1, 2, 3]
    pairs = [(x, 2.0 ** x) for x in xs]

    @wt.setup
    def _(c):
        p = Plane(c, box=(20, 26, 440, 405), x=(-3.2, 9.2), y=(-3.2, 9.2), equal=True)
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    TX, TY = 486, 40

    def table(c, swapped):
        rows = []
        for x, y in pairs:
            row = [num(x), num(y)]
            row += [num(y), num(x)] if swapped else ["", ""]
            rows.append(row)
        ctable(c, TX, TY, ["x", "2^x", "x", "log_2 x"], rows, [50, 54, 50, 66], [B, B, O, O], row_h=30)

    @wt.step("Graph y = 2ˣ", "Start with y = 2ˣ. Each step right doubles the height. List five points "
             "in the table.", math="y = 2^x:  (-1, 0.5), (0, 1), (1, 2), (2, 4), (3, 8)")
    def _(c, p):
        p.plot(lambda x: 2 ** x, -3.2, 3.2, color=B)
        for x, y in pairs:
            p.point(x, y, color=B)
        p.label(-0.5, 6.5, "y = 2^x", color=B, anchor="end", size=17)
        table(c, False)

    @wt.step("Draw the mirror y = x", "The line y = x holds every point whose two coordinates match. It "
             "is the mirror for inverses.", math="mirror: y = x")
    def _(c, p):
        p.line_through(0, 0, 1, 1, color=theme.SOFT_INK, width=1.8, dash="8 5")
        p.label(8.4, 7.6, "y = x", color=theme.SOFT_INK, anchor="start", size=16)

    @wt.step("Swap each pair", "Swap x and y in each pair: (2, 4) becomes (4, 2). The dashed links "
             "cross the mirror at right angles, and the mirror cuts each one in half.",
             math="(x, y) \\to (y, x):  (2, 4) \\to (4, 2),  (3, 8) \\to (8, 3)")
    def _(c, p):
        for x, y in pairs:
            p.segment(x, y, y, x, color=theme.MUTED, width=1.4, dash="3 4")
            p.point(y, x, color=O)
        p.label(2.3, 4.35, "(2, 4)", color=B, anchor="end", size=14)
        p.label(4.2, 1.65, "(4, 2)", color=O, anchor="start", size=14)
        p.label(3.3, 8.15, "(3, 8)", color=B, anchor="start", size=14)
        p.label(8.0, 2.45, "(8, 3)", color=O, anchor="middle", size=14)
        table(c, True)

    @wt.step("Connect the swapped points", "The orange points lie on y = log₂ x, the inverse of 2ˣ. It "
             "answers the question: 2 to what power gives x?",
             math="log_2 8 = 3  because  2^3 = 8")
    def _(c, p):
        p.plot(lambda x: math.log2(x) if x > 0 else None, 0.01, 9.2, color=O)
        p.label(8.4, 3.75, "y = log_2 x", color=O, anchor="end", size=17)

    @wt.step("Swap domain and range", "The swap trades the roles of the axes. 2ˣ takes any x and gives "
             "only positive outputs, so log₂ x takes only positive inputs and gives any output.",
             math="log_2(2^x) = x:  the log undoes the power")
    def _(c, p):
        tag(c, 590, 248, "2^x: any x, y > 0", B, size=15)
        tag(c, 590, 284, "log_2 x: x > 0, any y", O, size=15)
        c.text(590, 320, "nearing an axis, never touching it:", size=12, color=theme.SOFT_INK)
        c.text(590, 338, "2ˣ hugs the x-axis,", size=12, color=B)
        c.text(590, 356, "log₂ x hugs the y-axis", size=12, color=O)

    return wt


# ---------------------------------------------------------------------------
# Composition as a pipeline
# ---------------------------------------------------------------------------


def _f(x):
    return x * x


def _g(x):
    return x + 1


@diagram("function-composition", "Function Composition", CAT)
def build_composition() -> Walkthrough:
    wt = Walkthrough(
        "function-composition", "Function Composition: Machines in a Row", CAT,
        concept="(f ∘ g)(x) = f(g(x)) = (x + 1)^2,   (g ∘ f)(x) = x^2 + 1",
        summary="Composition feeds the output of one function into another. The machine you reach first "
                "runs first, and swapping the order usually changes the answer.",
        width=720, height=390, level="201",
    )
    G, F = theme.BLUE, theme.ORANGE
    x0 = 3
    fg = _f(_g(x0))
    gf = _g(_f(x0))
    BX = [55, 322, 598]  # ball centers
    M1, M2, MW, MH = 125, 392, 130, 80

    def row(c, cy, first, second, title, title_col):
        a_name, a_rule, a_col = first
        b_name, b_rule, b_col = second
        c.math(360, cy - 72, title, size=17, color=title_col)
        machine(c, M1, cy - MH / 2, MW, MH, a_col, a_name, a_rule, rule_size=18)
        machine(c, M2, cy - MH / 2, MW, MH, b_col, b_name, b_rule, rule_size=18)
        c.arrow(BX[0] + 24, cy, M1 - 22, cy, color=theme.MUTED, width=2)
        c.arrow(M1 + MW + 22, cy, BX[1] - 24, cy, color=theme.MUTED, width=2)
        c.arrow(BX[1] + 24, cy, M2 - 22, cy, color=theme.MUTED, width=2)
        c.arrow(M2 + MW + 22, cy, BX[2] - 24, cy, color=theme.MUTED, width=2)

    def values(c, cy, vals, cols):
        for x, v, col in zip(BX, vals, cols):
            ball(c, x, cy, num(v), col)

    def work(c, cy, a, b, cols):
        c.math(M1 + MW / 2, cy + MH / 2 + 18, a, size=15, color=cols[0])
        c.math(M2 + MW / 2, cy + MH / 2 + 18, b, size=15, color=cols[1])

    def exprs(c, cy, ex, cols):
        for x, e, col in zip(BX, ex, cols):
            c.math(x, cy + 40, e, size=16, color=col, halo=True)

    TOP, BOT = 108, 280

    @wt.step("Line up two machines", "Machine g adds one. Machine f squares. Put g first and f second, so "
             "the output of g drops straight into f.",
             math="g(x) = x + 1,   f(x) = x^2")
    def _(c):
        row(c, TOP, ("g", "x + 1", G), ("f", "x^2", F), "f ∘ g:  g first, then f", theme.INK)

    @wt.step("Run the number 3", "Feed in 3. Machine g gives 4, and f turns 4 into 16. Read f(g(3)) from "
             "the inside out, the same order the machines run.",
             math=f"(f ∘ g)(3) = f(g(3)) = f({_g(x0)}) = {fg}")
    def _(c):
        values(c, TOP, [x0, _g(x0), fg], [theme.INK, G, F])
        work(c, TOP, f"{x0} + 1 = {_g(x0)}", f"{_g(x0)}^2 = {fg}", [G, F])

    @wt.step("Run any x", "Feed in a plain x instead. Machine g hands over x + 1, and f squares the whole "
             "package.", math="(f ∘ g)(x) = (x + 1)^2")
    def _(c):
        exprs(c, TOP, ["x", "x + 1", "(x + 1)^2"], [theme.INK, G, F])

    @wt.step("Swap the order", "Now f runs first. Three squared is 9, and 9 + 1 is 10, not 16. Same "
             "machines, different line, different result.",
             math=f"(g ∘ f)(3) = g(f(3)) = g({_f(x0)}) = {gf}")
    def _(c):
        row(c, BOT, ("f", "x^2", F), ("g", "x + 1", G), "g ∘ f:  f first, then g", theme.INK)
        values(c, BOT, [x0, _f(x0), gf], [theme.INK, F, G])
        work(c, BOT, f"{x0}^2 = {_f(x0)}", f"{_f(x0)} + 1 = {gf}", [F, G])

    @wt.step("Compare the formulas", "In general (x + 1)² and x² + 1 differ, so order matters. Putting on "
             "socks, then shoes, beats the reverse.",
             math="(x + 1)^2 = x^2 + 2x + 1 \\neq x^2 + 1")
    def _(c):
        exprs(c, BOT, ["x", "x^2", "x^2 + 1"], [theme.INK, F, G])
        tag(c, 360, 372, f"(f ∘ g)(3) = {fg}  \\neq  (g ∘ f)(3) = {gf}", theme.RED, size=15)

    return wt


@diagram("function-composition-graph", "Composition on a Graph", CAT)
def build_composition_graph() -> Walkthrough:
    wt = Walkthrough(
        "function-composition-graph", "Composition on a Graph", CAT,
        concept="f(g(1)):  up to g, across to y = x, up to f",
        summary="You can compose functions on a graph without any algebra. Go up to g, slide across to the "
                "line y = x to turn the output into an input, then go up to f.",
        width=680, height=430, level="201",
    )
    G, F, FG = theme.BLUE, theme.ORANGE, theme.PURPLE
    x0 = 1
    g1 = _g(x0)
    fg1 = _f(g1)

    @wt.setup
    def _(c):
        p = Plane(c, box=(50, 30, 480, 385), x=(-2.5, 4.5), y=(-1.2, 9.5))
        p.grid(step=1)
        p.axes(step=1, ystep=1)
        return p

    @wt.step("Draw f, g, and y = x", "Graph g(x) = x + 1 and f(x) = x². Add the helper line y = x. It "
             "turns any height into the same x.", math="g(x) = x + 1,   f(x) = x^2,   y = x")
    def _(c, p):
        p.plot(_g, -2.5, 4.5, color=G, width=2.5)
        p.plot(_f, -2.5, 3.08, color=F, width=2.5)
        p.line_through(0, 0, 1, 1, color=theme.SOFT_INK, width=1.6, dash="8 5")
        p.label(-1.3, 6.8, "f(x) = x^2", color=F, anchor="end", size=16)
        p.label(4.45, 6.2, "g(x) = x + 1", color=G, anchor="end", size=16)
        p.label(4.35, 3.6, "y = x", color=theme.SOFT_INK, anchor="end", size=15)

    @wt.step("Go up to g", "Start at x = 1 and go up until you hit g. The height there is g(1) = 2.",
             math=f"g({x0}) = {g1}")
    def _(c, p):
        p.vector(x0, 0, x0, g1, color=G, width=2.5)
        p.point(x0, 0, "x = 1", color=theme.INK, offset=(10, 32))
        p.point(x0, g1, f"({x0}, {g1})", color=G, offset=(-10, -14), anchor="end")

    @wt.step("Slide across to y = x", "The output 2 has to become the next input. Slide sideways to the "
             "line y = x, which puts you right above x = 2.", math=f"height {g1} \\to x = {g1}")
    def _(c, p):
        p.vector(x0, g1, g1, g1, color=theme.SOFT_INK, width=2.5)
        p.point(g1, g1, f"({g1}, {g1})", color=theme.SOFT_INK, offset=(10, 14))

    @wt.step("Go up to f", "From (2, 2) go up to f. The height there is f(2) = 4, so f(g(1)) = 4. Three "
             "moves, no algebra.", math=f"f(g({x0})) = f({g1}) = {fg1}")
    def _(c, p):
        p.vector(g1, g1, g1, fg1, color=F, width=2.5)
        p.point(g1, fg1, f"({g1}, {fg1})", color=F, offset=(-12, -12), anchor="end")

    @wt.step("Plot the whole composition", "Repeat for every x and you trace y = (x + 1)², the graph of "
             "f ∘ g. It passes through (1, 4), the point the three moves found.",
             math="(f ∘ g)(x) = (x + 1)^2,   (f ∘ g)(1) = 4")
    def _(c, p):
        p.plot(lambda x: (x + 1) ** 2, -2.5, 4.5, color=FG, width=3)
        p.segment(x0, 0, x0, fg1, color=FG, width=1.4, dash="3 4")
        p.point(x0, fg1, "(1, 4)", color=FG, offset=(-10, -12), anchor="end")
        p.label(-0.2, 8.7, "y = (x + 1)^2", color=FG, anchor="end", size=16)

    return wt
