"""Sequence diagrams: arithmetic and geometric sequences, Fibonacci squares, and the Sierpinski triangle."""

from __future__ import annotations

import math
from fractions import Fraction

from .. import theme
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough

COLORS = [theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE, theme.SKY, theme.RED]


def _stage(scene, stage):
    def draw(c, ctx):
        scene(c, stage)
    return draw


# ---------------------------------------------------------------------------
# Arithmetic versus geometric
# ---------------------------------------------------------------------------


@diagram("arithmetic-geometric-sequences", "Arithmetic and Geometric Sequences", "Sequences and Series")
def build_arith_geo() -> Walkthrough:
    wt = Walkthrough(
        "arithmetic-geometric-sequences", "Arithmetic versus Geometric Sequences", "Sequences and Series",
        concept="a_n = a_1 + (n - 1)d    versus    g_n = g_1 r^{n-1}",
        summary="An arithmetic sequence adds the same number each step, so its dots lie on a line. A geometric "
                "sequence multiplies by the same number each step, so its jumps keep growing.",
        width=700, height=400, level="201",
    )
    a1, d = 3, 2
    g1, r = 3, 2
    N = 4
    arith = [a1 + (n - 1) * d for n in range(1, N + 1)]
    geo = [g1 * r ** (n - 1) for n in range(1, N + 1)]
    A_COL, G_COL, STEP_COL = theme.BLUE, theme.ORANGE, theme.GREEN

    @wt.setup
    def _(c):
        pa = Plane(c, box=(60, 50, 250, 300), x=(0, 4.7), y=(0, 26))
        pg = Plane(c, box=(410, 50, 250, 300), x=(0, 4.7), y=(0, 26))
        for p in (pa, pg):
            p.grid(step=1, ystep=5)
            p.axes(step=1, ystep=5, xlabel="n", ylabel="")
        c.text(185, 22, "arithmetic: add 2", size=16, weight="bold", color=A_COL)
        c.text(535, 22, "geometric: multiply by 2", size=16, weight="bold", color=G_COL)
        return pa, pg

    def dots(p, vals, col):
        for n, v in enumerate(vals, 1):
            p.point(n, v, label=str(v), color=col, r=6, offset=(-10, -14), anchor="end", math=False, size=15)

    def steps(p, vals, col, lab):
        for n in range(1, len(vals)):
            v0, v1 = vals[n - 1], vals[n]
            p.segment(n, v0, n + 1, v0, color=theme.MUTED, width=1.5, dash="4 3")
            X, Y0 = p.px(n + 1, v0)
            _, Y1 = p.px(n + 1, v1)
            p.c.arrow(X, Y0, X, Y1 + 8, color=col, width=2.4)
            p.c.text(X + 7, (Y0 + Y1) / 2, lab(v0, v1), size=13, color=col, anchor="start", weight="bold",
                     halo=True)

    @wt.step("Plot an arithmetic sequence",
             "Start at 3 and add 2 each time: 3, 5, 7, 9. Plot term n against its position n.",
             math="a_n: " + ", ".join(str(v) for v in arith))
    def _(c, ctx):
        dots(ctx[0], arith, A_COL)

    @wt.step("Find the common difference",
             "Every step up is the same size, +2. That fixed gap is the common difference d.",
             math=f"d = 5 - 3 = 7 - 5 = 9 - 7 = {d}")
    def _(c, ctx):
        steps(ctx[0], arith, STEP_COL, lambda a, b: f"+{b - a}")

    @wt.step("Plot a geometric sequence",
             "Start at 3 again, but multiply by 2 each time: 3, 6, 12, 24. Same start, very different "
             "ambitions.", math="g_n: " + ", ".join(str(v) for v in geo))
    def _(c, ctx):
        dots(ctx[1], geo, G_COL)

    @wt.step("Find the common ratio",
             "Each term is twice the one before, so the jumps double: +3, +6, +12. The fixed number is the "
             "ratio r, not the gap.", math=f"r = 6/3 = 12/6 = 24/12 = {r}")
    def _(c, ctx):
        steps(ctx[1], geo, STEP_COL, lambda a, b: f"×{b // a} (+{b - a})")

    @wt.step("Compare the shapes",
             "Equal steps put the arithmetic dots on a straight line. Doubling puts the geometric dots on a "
             "curve that bends upward and soon leaves the chart.",
             math=f"a_n = {a1} + {d}(n - 1),   g_n = {g1}\\cdot{r}^{{n-1}}")
    def _(c, ctx):
        pa, pg = ctx
        pa.plot(lambda x: a1 + d * (x - 1), 0.3, 4.6, color=A_COL, width=1.8, dash="6 4")
        pg.plot(lambda x: g1 * r ** (x - 1), 0.3, 4.6, color=G_COL, width=1.8, dash="6 4")
        pa.label(1.6, 21, f"a_n = {a1} + {d}(n - 1)", color=A_COL, size=16)
        pg.label(1.7, 21, f"g_n = {g1}\\cdot{r}^{{n-1}}", color=G_COL, size=16)
        pa.label(2.6, 17, f"n = 10:  {a1 + 9 * d}", color=A_COL, size=14)
        pg.label(2.0, 17, f"n = 10:  {g1 * r ** 9}", color=G_COL, size=14)

    return wt


# ---------------------------------------------------------------------------
# Fibonacci squares and spiral
# ---------------------------------------------------------------------------


def fib_squares(sizes):
    """Places Fibonacci squares in a spiral. Returns a list of (x, y, s, direction)."""
    dirs = ["down", "right", "up", "left"]
    out = []
    bx0 = by0 = bx1 = by1 = None
    for i, s in enumerate(sizes):
        d = dirs[i % 4]
        if i == 0:
            x, y = 0, 0
            bx0, by0, bx1, by1 = 0, 0, s, s
        else:
            if d == "right":
                x, y = bx1, by0
            elif d == "up":
                x, y = bx0, by1
            elif d == "left":
                x, y = bx0 - s, by0
            else:
                x, y = bx0, by0 - s
            bx0, by0 = min(bx0, x), min(by0, y)
            bx1, by1 = max(bx1, x + s), max(by1, y + s)
        out.append((x, y, s, d))
    return out, (bx0, by0, bx1, by1)


@diagram("fibonacci-spiral", "Fibonacci Spiral and the Golden Ratio", "Sequences and Series")
def build_fibonacci() -> Walkthrough:
    wt = Walkthrough(
        "fibonacci-spiral", "Fibonacci Squares and the Golden Ratio", "Sequences and Series",
        concept="F_{n+1}/F_n \\to \\phi = (1 + sqrt(5))/2 \\approx 1.618",
        summary="Squares with Fibonacci side lengths 1, 1, 2, 3, 5, 8 tile a rectangle, and quarter circles "
                "through them trace a spiral. The ratio of neighboring Fibonacci numbers closes in on the "
                "golden ratio.",
        width=700, height=360, level="201",
    )
    fib = [1, 1]
    while len(fib) < 12:
        fib.append(fib[-1] + fib[-2])
    sizes = fib[:6]
    squares, bbox = fib_squares(sizes)
    PHI = (1 + math.sqrt(5)) / 2
    start = {"down": 180, "right": 270, "up": 0, "left": 90}
    centre = {"down": (1, 1), "right": (0, 1), "up": (0, 0), "left": (1, 0)}  # corner as fractions of s

    def scene(c, stage):
        bx0, by0, bx1, by1 = bbox
        p = Plane(c, box=(24, 40, 400, 260), x=(bx0, bx1), y=(by0, by1), equal=True)
        shown = {1: 2, 2: 4, 3: 6, 4: 6, 5: 6}[stage]
        for i in range(shown):
            x, y, s, d = squares[i]
            col = COLORS[i % len(COLORS)]
            p.rect(x, y, x + s, y + s, color=theme.INK, fill=theme.fill(col, "40"), width=1.6)
            X, Y = p.px(x + s / 2, y + s / 2)
            c.text(X, Y, str(s), size=min(13 + 4 * s, 34), weight="bold", color=col, halo=True)
        if stage >= 3:
            X0, Y0 = p.px(bx0, by0)
            X1, Y1 = p.px(bx1, by1)
            c.text((X0 + X1) / 2, Y0 + 18, f"{bx1 - bx0}", size=15, weight="bold")
            c.text(X1 + 8, (Y0 + Y1) / 2, f"{by1 - by0}", size=15, weight="bold", anchor="start")
        if stage >= 4:
            for i in range(shown):
                x, y, s, d = squares[i]
                fx, fy = centre[d]
                cx, cy = p.px(x + fx * s, y + fy * s)
                c.arc(cx, cy, s * p.sx, start[d], start[d] + 90, color=theme.RED, width=3)
        # right panel
        tx = 460
        if stage <= 3:
            c.text(tx, 50, "Fibonacci: add the last two", size=15, weight="bold", anchor="start")
            for i in range(2, shown):
                c.math(tx, 84 + (i - 2) * 30, f"{fib[i - 2]} + {fib[i - 1]} = {fib[i]}", size=17,
                       anchor="start", color=COLORS[i % len(COLORS)])
            if stage == 1:
                c.text(tx, 84, "Two squares of side 1 start it off.", size=14, anchor="start",
                       color=theme.SOFT_INK)
            if stage == 3:
                c.text(tx, 230, "Each new square sits on the long side", size=13, anchor="start",
                       color=theme.SOFT_INK)
                c.text(tx, 250, "of the rectangle built so far.", size=13, anchor="start", color=theme.SOFT_INK)
        if stage == 4:
            c.text(tx, 50, "one quarter circle per square", size=15, weight="bold", anchor="start",
                   color=theme.RED)
            for i, s in enumerate(sizes):
                c.text(tx, 84 + i * 26, f"radius {s}", size=14, anchor="start", color=COLORS[i % len(COLORS)])
            c.text(tx, 250, "Corners line up, so the arcs join", size=13, anchor="start", color=theme.SOFT_INK)
            c.text(tx, 270, "into one smooth spiral.", size=13, anchor="start", color=theme.SOFT_INK)
        if stage == 5:
            q = Plane(c, box=(475, 34, 195, 210), x=(0.5, 10.5), y=(0.9, 2.1))
            q.grid(step=1, ystep=0.25)
            q.axes(step=2, ystep=0.5, xlabel="n", ylabel="", yfmt=lambda v: f"{v:g}")
            q.hline(PHI, color=theme.GREEN, width=1.8, dash="6 4")
            q.label(10.4, PHI + 0.12, "\\phi", color=theme.GREEN, size=17, anchor="end")
            pts = []
            for n in range(1, 11):
                ratio = fib[n] / fib[n - 1]
                pts.append(q.px(n, ratio))
            c.polyline(pts, color=theme.RED, width=1.5)
            for n in range(1, 11):
                q.point(n, fib[n] / fib[n - 1], r=3.8, color=theme.RED)
            for j, n in enumerate((3, 4, 5, 10)):
                c.text(470 + (j % 2) * 110, 296 + (j // 2) * 20,
                       f"{fib[n]}/{fib[n - 1]} = {fib[n] / fib[n - 1]:.3f}", size=12, anchor="start",
                       color=theme.RED)
            c.text(470, 342, f"φ = (1 + √5)/2 = {PHI:.4f}", size=13, anchor="start", color=theme.GREEN,
                   weight="bold")

    wt.step("Start with two unit squares",
            "The Fibonacci sequence starts 1, 1. Draw two squares of side 1 side by side.",
            math="F_1 = 1,  F_2 = 1", fresh=True)(_stage(scene, 1))
    wt.step("Add squares of side 2 and 3",
            "Each new side is the sum of the two before it: 1 + 1 = 2, then 1 + 2 = 3. Each square fits "
            "exactly along the long edge of the shape so far.", math="F_3 = 2,  F_4 = 3",
            fresh=True)(_stage(scene, 2))
    wt.step("Grow to a 13 by 8 rectangle",
            "Squares of side 5 and 8 come next. The six squares tile a rectangle 13 wide and 8 tall, and both "
            "sides are Fibonacci numbers too.", math="F_5 = 5,  F_6 = 8,  13/8 = 1.625",
            fresh=True)(_stage(scene, 3))
    wt.step("Draw the spiral",
            "Draw a quarter circle in each square, centered on a corner, with radius equal to the side. The "
            "arcs meet end to end and spiral outward.", math="radius = 1, 1, 2, 3, 5, 8",
            fresh=True)(_stage(scene, 4))
    wt.step("Watch the ratios settle",
            f"Divide each Fibonacci number by the one before it. The ratios swing above and below, then "
            f"settle on the golden ratio φ ≈ {PHI:.3f}.",
            math=f"{fib[10]}/{fib[9]} \\approx {fib[10] / fib[9]:.4f} \\approx \\phi", fresh=True)(_stage(scene, 5))
    return wt


# ---------------------------------------------------------------------------
# Sierpinski triangle
# ---------------------------------------------------------------------------


def sierpinski(tri, depth):
    """Returns the list of remaining triangles after `depth` removals."""
    if depth == 0:
        return [tri]
    a, b, c = tri
    ab = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    bc = ((b[0] + c[0]) / 2, (b[1] + c[1]) / 2)
    ca = ((c[0] + a[0]) / 2, (c[1] + a[1]) / 2)
    out = []
    for t in ((a, ab, ca), (ab, b, bc), (ca, bc, c)):
        out += sierpinski(t, depth - 1)
    return out


@diagram("sierpinski-triangle", "Sierpinski Triangle", "Sequences and Series")
def build_sierpinski() -> Walkthrough:
    wt = Walkthrough(
        "sierpinski-triangle", "Sierpinski Triangle: Area Left After Each Step", "Sequences and Series",
        concept="area after n steps = (3/4)^n \\to 0",
        summary="Remove the middle quarter of a triangle, then the middle of each piece that remains, forever. "
                "Each step keeps 3/4 of the area, so the area shrinks like (3/4)^n toward zero.",
        width=700, height=390, level="201",
    )
    L, B, S = 30, 362, 360
    T = (L + S / 2, B - S * math.sqrt(3) / 2)
    big = ((L, B), (L + S, B), T)
    G = theme.GREEN

    def scene(c, stage):
        n = min(stage - 1, 4)
        c.polygon(list(big), color=theme.MUTED, fill=theme.PAPER, width=1.2)
        for t in sierpinski(big, n):
            c.polygon(list(t), color=theme.PAPER if n >= 3 else theme.INK, fill=theme.fill(G, "cc"),
                      width=0.6 if n >= 3 else 1.2)
        c.polygon(list(big), color=theme.INK, width=1.8)
        area = Fraction(3, 4) ** n
        count = 3 ** n
        if stage == 6:
            head = f"step 10:  {3 ** 10} triangles,  area ≈ {0.75 ** 10:.3f}  (step 4 drawn)"
        elif n:
            head = f"step {n}:  {count} triangles,  area = {area.numerator}/{area.denominator}"
        else:
            head = "step 0:  1 triangle,  area = 1"
        c.text(30, 24, head, size=15, anchor="start", weight="bold")
        if stage == 2:
            m = sierpinski(big, 1)
            mid = (m[0][1], m[1][2], m[0][2])
            cx = sum(p[0] for p in mid) / 3
            cy = sum(p[1] for p in mid) / 3
            c.text(cx, cy, "removed: 1/4", size=14, color=theme.RED, weight="bold", halo=True)
        if stage == 5:
            sub = sierpinski(big, 1)[0]
            c.polygon(list(sub), color=theme.ORANGE, width=3.5, dash="7 4")
            c.text(68, 186, "half-size", size=14, color=theme.ORANGE, weight="bold")
            c.text(68, 204, "copy", size=14, color=theme.ORANGE, weight="bold")
            for t in sierpinski(big, 1)[1:]:
                c.polygon(list(t), color=theme.ORANGE, width=1.6, dash="3 4")
        # bar chart of remaining area; world x = n + 1 keeps bar 0 off the y-axis
        nmax = 10 if stage == 6 else n
        q = Plane(c, box=(470, 50, 200, 280), x=(0, 11.7), y=(0, 1.08))
        q.grid(step=1, ystep=0.25)
        q.axes(step=1, ystep=0.25, xlabel="n", ylabel="", yfmt=lambda v: f"{v:g}",
               xfmt=lambda v: str(int(round(v)) - 1) if int(round(v)) % 2 == 1 else "")
        for k in range(nmax + 1):
            v = 0.75 ** k
            q.rect(k + 0.65, 0, k + 1.35, v, color=G, fill=theme.fill(G, "99" if k == n else "55"), width=1.2)
        c.text(570, 30, "area left", size=14, color=theme.SOFT_INK)
        if stage < 6:
            X, Y = q.px(n + 1, 0.75 ** n)
            c.text(X + 6, Y - 12, f"{float(area):.3f}", size=12, color=G, weight="bold", anchor="start",
                   halo=True)
        else:
            X, Y = q.px(11, 0.75 ** 10)
            c.text(X, Y - 14, f"{0.75 ** 10:.3f}", size=12, color=G, weight="bold", halo=True)
            c.text(570, 362, "the bars shrink toward 0", size=13, color=theme.SOFT_INK)

    wt.step("Start with a solid triangle",
            "Take an equilateral triangle and call its area 1.", math="A_0 = 1", fresh=True)(_stage(scene, 1))
    wt.step("Remove the middle",
            "Join the midpoints of the sides. This cuts the triangle into four equal copies; remove the "
            "middle one and keep three.", math="A_1 = 3/4", fresh=True)(_stage(scene, 2))
    wt.step("Repeat on each piece",
            "Do the same to each of the three triangles. Each keeps 3/4 of its area, so the total is "
            "3/4 of 3/4.", math="A_2 = (3/4)^2 = 9/16", fresh=True)(_stage(scene, 3))
    wt.step("Repeat again",
            "Now there are 27 triangles. Every step multiplies the count by 3 and the area by 3/4.",
            math="A_3 = (3/4)^3 = 27/64", fresh=True)(_stage(scene, 4))
    wt.step("Spot the self-similarity",
            "The bottom-left corner is a half-size copy of the whole picture, and so are the other two "
            "corners. Zoom into any corner and the same pattern appears.",
            math="A_4 = (3/4)^4 = 81/256 \\approx 0.316", fresh=True)(_stage(scene, 5))
    wt.step("Let the area vanish",
            f"After ten steps only {0.75 ** 10:.3f} of the area is left. Keep going forever and the area goes "
            "to zero, yet a shape with infinitely many triangles remains.",
            math="A_n = (3/4)^n \\to 0", fresh=True)(_stage(scene, 6))
    return wt


@diagram("sierpinski-pascal", "Sierpinski Triangle in Pascal's Triangle", "Sequences and Series")
def build_sierpinski_pascal() -> Walkthrough:
    wt = Walkthrough(
        "sierpinski-pascal", "Sierpinski Triangle Inside Pascal's Triangle", "Sequences and Series",
        concept="C(n, k) odd  \\iff  the cell is part of the Sierpinski pattern",
        summary="Color the odd numbers in Pascal's triangle and the Sierpinski triangle appears. The same "
                "pattern comes from adding neighbors, with no geometry at all.",
        width=700, height=400, level="201",
    )
    R = 16
    rows = [[1]]
    for n in range(1, R):
        prev = rows[-1]
        rows.append([1] + [prev[k - 1] + prev[k] for k in range(1, n)] + [1])
    CW, RH, TOPY = 40, 22, 30
    CX = 350

    def cell(n, k):
        return CX + (k - n / 2) * CW, TOPY + n * RH

    def scene(c, stage):
        nrows = {1: 6, 2: 8, 3: 16, 4: 16}[stage]
        for n in range(nrows):
            for k in range(n + 1):
                v = rows[n][k]
                x, y = cell(n, k)
                odd = v % 2 == 1
                if stage >= 2 and odd:
                    c.rect(x - CW / 2 + 1, y - RH / 2 + 1, CW - 2, RH - 2, color="none",
                           fill=theme.fill(theme.GREEN, "bb"), rx=3)
                if stage <= 2:
                    c.text(x, y, str(v), size=12 if v < 1000 else 10,
                           color=theme.INK if (stage < 2 or odd) else theme.MUTED)
                elif stage >= 3 and not odd:
                    c.rect(x - CW / 2 + 1, y - RH / 2 + 1, CW - 2, RH - 2, color="none", fill=theme.GRID, rx=3)
        if stage == 1:
            x1, y1 = cell(4, 1)
            x2, y2 = cell(4, 2)
            x3, y3 = cell(5, 2)
            c.line(x1, y1 + 7, x3 - 4, y3 - 7, color=theme.ORANGE, width=1.6)
            c.line(x2, y2 + 7, x3 + 4, y3 - 7, color=theme.ORANGE, width=1.6)
            c.text(x3 + 120, y3, "4 + 6 = 10", size=14, color=theme.ORANGE, anchor="start", weight="bold")
        if stage >= 2:
            c.rect(24, 23, 20, 14, color="none", fill=theme.fill(theme.GREEN, "bb"), rx=3)
            c.text(52, 30, "odd", size=13, anchor="start", color=theme.SOFT_INK)
            c.rect(24, 45, 20, 14, color="none", fill=theme.GRID, rx=3)
            c.text(52, 52, "even", size=13, anchor="start", color=theme.SOFT_INK)
        if stage == 4:
            # outline the three half-size copies
            for (n0, k0) in ((0, 0), (8, 0), (8, 8)):
                a = cell(n0, k0)
                b = cell(n0 + 7, k0)
                d = cell(n0 + 7, k0 + 7)
                pts = [(a[0], a[1] - RH / 2 - 2), (b[0] - CW / 2 - 2, b[1] + RH / 2 + 2),
                       (d[0] + CW / 2 + 2, d[1] + RH / 2 + 2)]
                c.polygon(pts, color=theme.ORANGE, width=2.5, dash="6 4")
            c.text(560, 120, "three copies of", size=14, color=theme.ORANGE, anchor="start")
            c.text(560, 140, "the top 8 rows", size=14, color=theme.ORANGE, anchor="start")
            c.text(560, 160, "and a hole of", size=14, color=theme.ORANGE, anchor="start")
            c.text(560, 180, "even numbers", size=14, color=theme.ORANGE, anchor="start")

    wt.step("Build Pascal's triangle",
            "Each number is the sum of the two numbers above it, and every row starts and ends with 1.",
            math="C(n, k) = C(n - 1, k - 1) + C(n - 1, k)", fresh=True)(_stage(scene, 1))
    wt.step("Color the odd numbers",
            "Shade every odd entry green and leave the even ones gray. Odd plus odd is even, so holes open "
            "where two odd numbers meet.", math="odd + odd = even,  odd + even = odd", fresh=True)(_stage(scene, 2))
    wt.step("Run sixteen rows",
            "Drop the digits and keep only the colors. Sixteen rows show the Sierpinski triangle, made by "
            "addition alone.", math="rows 0 to 15", fresh=True)(_stage(scene, 3))
    wt.step("Find the copies",
            "The top eight rows appear three times, around an upside-down block of even numbers. That is the "
            "same remove-the-middle rule as the geometric picture.",
            math="16 rows = 3 copies of 8 rows + an even hole", fresh=True)(_stage(scene, 4))
    return wt
