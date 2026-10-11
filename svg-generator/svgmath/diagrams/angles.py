"""Angle diagrams: triangle angle sum, parallel lines, polygon angle sums."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import angle_mark, callout, table
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._geo import away, centroid, heading, lerp, polar, rich, word

A_COL, B_COL, C_COL = theme.ORANGE, theme.BLUE, theme.GREEN


def _apex(A, B, a_deg, b_deg):
    """Returns the apex of the triangle on base AB with base angles a_deg and b_deg (pixels, AB level)."""
    L = B[0] - A[0]
    h = L / (1 / math.tan(math.radians(a_deg)) + 1 / math.tan(math.radians(b_deg)))
    return (A[0] + h / math.tan(math.radians(a_deg)), A[1] - h)


# ---------------------------------------------------------------------------
# Triangle angle sum
# ---------------------------------------------------------------------------


@diagram("triangle-angle-sum", "Triangle Angle Sum", "Geometry")
def triangle_angle_sum() -> Walkthrough:
    a, b = 55, 45
    cang = 180 - a - b
    wt = Walkthrough(
        "triangle-angle-sum", "Triangle Angle Sum", "Geometry",
        concept="a + b + c = 180\\deg",
        summary="Draw a line through the top corner, parallel to the base. The three angles of the triangle "
                "line up along that line, and a straight line is 180°.",
        width=680, height=345, level="201",
    )
    A, B = (90.0, 305.0), (500.0, 305.0)
    C = _apex(A, B, a, b)
    L, R = (20.0, C[1]), (660.0, C[1])

    def base(c):
        c.polygon([A, B, C], color=theme.INK, width=2.5)
        for p, s in ((A, "A"), (B, "B"), (C, "C")):
            q = away(p, centroid([A, B, C]), 22)
            c.text(q[0], q[1] + (0 if p is not C else -4), s, size=17, math=True, weight="bold")

    @wt.setup
    def _(c):
        base(c)

    @wt.step("Mark the three angles", "Any triangle has three corners. Here the angles are 55°, 45°, "
             "and 80°. Each color stays with its angle.",
             math=f"a = {a}\\deg, b = {b}\\deg, c = {cang}\\deg")
    def _(c):
        angle_mark(c, A, B, C, r=40, color=A_COL, label=f"a = {a}°", label_r=78)
        angle_mark(c, B, A, C, r=40, color=B_COL, label=f"b = {b}°", label_r=80)
        angle_mark(c, C, A, B, r=44, color=C_COL, label=f"c = {cang}°", label_r=72)

    @wt.step("Draw a parallel line through C", "Draw a line through the top corner C that never meets "
             "the base AB. The two lines run side by side like rails.", math="line through C \\parallel AB")
    def _(c):
        c.line(*L, *R, color=theme.SOFT_INK, width=2.5)
        # arrow chevrons mark the two parallel lines
        for y in (C[1], A[1]):
            x = 600 if y == C[1] else 330
            c.polyline([(x - 6, y - 6), (x + 2, y), (x - 6, y + 6)], color=theme.SOFT_INK, width=2)
        c.text(70, C[1] - 16, "parallel to AB", size=13, color=theme.SOFT_INK, anchor="start")

    @wt.step("Copy angle a to the top", "Side CA crosses both rails, forming a Z. Alternate angles in a Z "
             "are equal, so the left angle at C is also 55°.", math=f"left angle at C = a = {a}\\deg")
    def _(c):
        if c.is_new:
            c.polyline([(C[0] - 150, C[1]), C, A, (A[0] + 150, A[1])], color=A_COL, width=9,
                       stroke_opacity=0.25)
            c.text(C[0] - 120, C[1] + 70, "Z shape", size=13, color=A_COL, anchor="middle", weight="bold")
        angle_mark(c, C, L, A, r=44, color=A_COL, label=f"{a}°", label_r=68)

    @wt.step("Copy angle b to the top", "Side CB makes a backward Z with the rails. The right angle at C "
             "matches b, so it is 45°.", math=f"right angle at C = b = {b}\\deg")
    def _(c):
        if c.is_new:
            c.polyline([(C[0] + 160, C[1]), C, B, (B[0] - 160, B[1])], color=B_COL, width=9,
                       stroke_opacity=0.25)
            c.text(C[0] + 175, C[1] + 60, "backward Z", size=13, color=B_COL, anchor="middle", weight="bold")
        angle_mark(c, C, R, B, r=44, color=B_COL, label=f"{b}°", label_r=68)

    @wt.step("Read the straight line", "At C the three angles a, c, and b fill the straight line with no "
             "gap and no overlap. A straight line is 180°, so the angles add to 180°. Every triangle, no "
             "exceptions.", math=f"a + c + b = {a}\\deg + {cang}\\deg + {b}\\deg = 180\\deg")
    def _(c):
        rich(c, 540, 160, [(f"{a}°", A_COL), (" + ", theme.INK), (f"{cang}°", C_COL), (" + ", theme.INK),
                           (f"{b}°", B_COL), (" = 180°", theme.INK)], size=20)
        c.text(540, 188, "three angles on one straight line", size=13, color=theme.SOFT_INK)

    return wt


@diagram("triangle-angle-sum-tear", "Triangle Angle Sum: Tear the Corners", "Geometry")
def triangle_angle_sum_tear() -> Walkthrough:
    a, b = 65, 45
    cang = 180 - a - b
    wt = Walkthrough(
        "triangle-angle-sum-tear", "Triangle Angle Sum: Tear the Corners", "Geometry",
        concept="a + b + c = 180\\deg",
        summary="Tear the three corners off a paper triangle and set them point to point. They always make "
                "a straight line.",
        width=680, height=350, level="201",
    )
    A, B = (40.0, 310.0), (360.0, 310.0)
    C = _apex(A, B, a, b)
    T = (530.0, 250.0)  # where the torn corners meet
    t = 0.4  # how far along each side the tear runs

    def cut(p, q):
        return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)

    def piece(V, P, Q, start):
        """Moves the corner piece at V so its tip sits on T and its angle starts at heading start."""
        h1, h2 = heading(V, P), heading(V, Q)
        if (h2 - h1) % 360 > 180:
            P, Q, h1 = Q, P, h2
        rot = math.radians(start - h1)
        out = []
        for X in (V, cut(V, P), cut(V, Q)):
            dx, dy = X[0] - V[0], -(X[1] - V[1])
            rx = dx * math.cos(rot) - dy * math.sin(rot)
            ry = dx * math.sin(rot) + dy * math.cos(rot)
            out.append((T[0] + rx, T[1] - ry))
        return out

    corners = [(A, B, C, A_COL, a, 180 - a), (C, A, B, C_COL, cang, b), (B, A, C, B_COL, b, 0)]

    @wt.setup
    def _(c):
        return None

    @wt.step("Draw a paper triangle", "Cut a triangle out of paper. Any shape works, so pick a lopsided "
             "one to keep yourself honest.", math=f"a = {a}\\deg, b = {b}\\deg, c = {cang}\\deg")
    def _(c):
        c.polygon([A, B, C], color=theme.INK, fill=theme.PANEL, width=2.5)
        for V, P, Q, col, ang, _s in corners:
            angle_mark(c, V, P, Q, r=30, color=col, label=f"{ang}°", label_r=50)

    @wt.step("Tear off the corners", "Rip each corner off along the dashed lines. Each piece carries "
             "one angle, and the middle piece goes in the recycling.", math="three pieces: a, b, c")
    def _(c):
        for V, P, Q, col, ang, _s in corners:
            c.polygon([V, cut(V, P), cut(V, Q)], color="none", fill=theme.fill(col, "30"))
            c.line(*cut(V, P), *cut(V, Q), color=theme.RED, width=2, dash="6 4")
        c.text(200, 332, "tear along the dashed lines", size=13, color=theme.RED)

    @wt.step("Line them up point to point", "Put the three tips together with no gaps. The outer edges "
             "make one straight line, so the angles add to 180°.",
             math=f"{a}\\deg + {cang}\\deg + {b}\\deg = 180\\deg")
    def _(c):
        c.line(T[0] - 150, T[1], T[0] + 140, T[1], color=theme.SOFT_INK, width=2)
        for V, P, Q, col, ang, st in corners:
            pts = piece(V, P, Q, st)
            c.polygon(pts, color=col, fill=theme.fill(col, "40"), width=2)
            lab = polar(T[0], T[1], 42, st + ang / 2)
            c.text(lab[0], lab[1], f"{ang}°", size=15, math=True, color=col, halo=True)
        c.dot(*T, r=4)
        rich(c, T[0], T[1] + 30, [(f"{a}°", A_COL), (" + ", theme.INK), (f"{cang}°", C_COL),
                                   (" + ", theme.INK), (f"{b}°", B_COL), (" = 180°", theme.INK)], size=18)
        c.text(T[0], T[1] + 56, "a straight line", size=13, color=theme.SOFT_INK)
        c.curved_arrow(330, 150, 420, 150, bend=-0.35, color=theme.MUTED, width=1.5)

    return wt


# ---------------------------------------------------------------------------
# Parallel lines and a transversal
# ---------------------------------------------------------------------------


@diagram("parallel-lines-transversal", "Parallel Lines and a Transversal", "Geometry")
def parallel_lines() -> Walkthrough:
    th = 62  # transversal direction, degrees from the right-hand line direction
    sm, lg = th, 180 - th
    wt = Walkthrough(
        "parallel-lines-transversal", "Parallel Lines and a Transversal", "Geometry",
        concept="eight angles, two sizes: x and 180\\deg - x",
        summary="A line crossing two parallel lines makes eight angles but only two sizes. Corresponding "
                "and alternate interior angles are equal; co-interior angles add to 180°.",
        width=680, height=400, level="201",
    )
    y1, y2 = 120.0, 290.0
    P = (300.0, y1)
    Q = (P[0] - (y2 - y1) / math.tan(math.radians(th)), y2)
    # ray directions at each crossing, in order: right, up-transversal, left, down-transversal
    dirs = [0, th, 180, 180 + th]
    sizes = [sm, lg, sm, lg]
    names = ["upper right", "upper left", "lower left", "lower right"]

    def mark(c, V, k, emph=True, r=30):
        col = A_COL if sizes[k] == sm else B_COL
        p1 = polar(V[0], V[1], 50, dirs[k])
        p2 = polar(V[0], V[1], 50, dirs[(k + 1) % 4])
        mid_dir = dirs[k] + sizes[k] / 2
        if emph:
            angle_mark(c, V, p1, p2, r=r, color=col)
        lx, ly = polar(V[0], V[1], r + 20, mid_dir)
        c.text(lx, ly, f"{sizes[k]}°", size=15, math=True, color=col if emph else theme.MUTED, halo=True)

    def shape(c, pts, color, label, at):
        c.polyline(pts, color=color, width=10, stroke_opacity=0.22)
        c.text(at[0], at[1], label, size=20, color=color, weight="bold", halo=True)

    @wt.setup
    def _(c):
        for y, name in ((y1, "line 1"), (y2, "line 2")):
            c.line(30, y, 650, y, color=theme.INK, width=2.5)
            c.polyline([(596, y - 6), (604, y), (596, y + 6)], color=theme.INK, width=2)
            c.polyline([(606, y - 6), (614, y), (606, y + 6)], color=theme.INK, width=2)
            c.text(640, y - 16, name, size=13, color=theme.SOFT_INK, anchor="end")
        t0 = polar(P[0], P[1], 100, th)
        t1 = polar(Q[0], Q[1], 100, 180 + th)
        c.line(*t0, *t1, color=theme.PURPLE, width=2.5)
        c.text(t0[0] + 8, t0[1] + 4, "transversal", size=13, color=theme.PURPLE, anchor="start")
        c.rect(30, y1, 620, y2 - y1, color="none", fill=theme.fill(theme.SKY, "14"))
        c.text(555, (y1 + y2) / 2, "interior", size=13, color=theme.SOFT_INK)
        c.text(555, y1 - 40, "exterior", size=13, color=theme.SOFT_INK)
        c.text(555, y2 + 40, "exterior", size=13, color=theme.SOFT_INK)
        return None

    @wt.step("Start with one angle", f"Two parallel lines (the arrows say so) are cut by a transversal. "
             f"The upper right angle at the top crossing is {sm}°.", math=f"{sm}\\deg")
    def _(c):
        mark(c, P, 0)

    @wt.step("Fill in the top crossing", f"Angles on a straight line add to 180°, so the neighbor is "
             f"{lg}°. Vertical angles, across the X, are equal.",
             math=f"{sm}\\deg + {lg}\\deg = 180\\deg")
    def _(c):
        for k in (1, 2, 3):
            mark(c, P, k)

    @wt.step("Corresponding angles are equal", "Slide the top crossing down the transversal and it lands "
             "on the bottom crossing exactly. Angles in the same spot match. Look for an F.",
             math=f"top upper right = bottom upper right = {sm}\\deg", fresh=True)
    def _(c):
        for k in range(4):
            mark(c, P, k, emph=(k == 0))
        mark(c, Q, 0)
        shape(c, [polar(*P, 90, th), P, (P[0] + 120, P[1]), P, Q, (Q[0] + 120, Q[1])], theme.RED, "F",
              (P[0] + 140, P[1] - 20))

    @wt.step("Alternate interior angles are equal", "Between the lines, on opposite sides of the "
             "transversal, the angles match. They make a Z.",
             math=f"top lower left = bottom upper right = {sm}\\deg", fresh=True)
    def _(c):
        for k in range(4):
            mark(c, P, k, emph=(k == 2))
        mark(c, Q, 0)
        shape(c, [(P[0] - 150, P[1]), P, Q, (Q[0] + 150, Q[1])], theme.RED, "Z", (P[0] - 165, P[1] - 20))

    @wt.step("Co-interior angles add to 180°", "Between the lines, on the same side, the angles are "
             "partners, not twins. They make a C (or a U) and add to 180°.",
             math=f"{lg}\\deg + {sm}\\deg = 180\\deg", fresh=True)
    def _(c):
        for k in range(4):
            mark(c, P, k, emph=(k == 3))
        mark(c, Q, 0)
        shape(c, [(P[0] + 140, P[1]), P, Q, (Q[0] + 140, Q[1])], theme.RED, "C", ((P[0] + Q[0]) / 2 + 60, (y1 + y2) / 2))

    @wt.step("All eight angles, two sizes", f"Every angle is either {sm}° (orange) or {lg}° (blue). Find "
             "one, and you have all eight.", math=f"{sm}\\deg + {lg}\\deg = 180\\deg", fresh=True)
    def _(c):
        for k in range(4):
            mark(c, P, k)
            mark(c, Q, k)

    return wt


# ---------------------------------------------------------------------------
# Polygon interior angles
# ---------------------------------------------------------------------------


def _hexagon(turns=(55, 70, 50, 65, 60, 60), first=(1.0, 0.8, 1.1, 0.9), h0=-35.0, size=300.0,
             center=(225.0, 210.0)):
    """Builds a convex hexagon with whole-degree exterior turns, so every printed angle is exact.

    The first four sides have the given lengths; the last two are solved so the outline closes.
    Returns pixel points in counterclockwise order (math sense), vertex k at the start of side k.
    """
    heads, h = [], h0
    for t in turns:
        heads.append(h)
        h += t
    u = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in heads]
    sx = sum(L * u[i][0] for i, L in enumerate(first))
    sy = sum(L * u[i][1] for i, L in enumerate(first))
    (a1, b1), (a2, b2) = u[4], u[5]
    det = a1 * b2 - a2 * b1
    L5 = (-sx * b2 + a2 * sy) / det
    L6 = (-a1 * sy + sx * b1) / det
    lengths = list(first) + [L5, L6]
    assert min(lengths) > 0, lengths
    pts, x, y = [], 0.0, 0.0
    for L, (ux, uy) in zip(lengths, u):
        pts.append((x, y))
        x, y = x + L * ux, y + L * uy
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    k = size / max(max(xs) - min(xs), max(ys) - min(ys))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [(center[0] + (q[0] - mx) * k, center[1] - (q[1] - my) * k) for q in pts]


@diagram("polygon-angles", "Polygon Interior Angles", "Geometry")
def polygon_angles() -> Walkthrough:
    pts = _hexagon()
    n = len(pts)
    wt = Walkthrough(
        "polygon-angles", "Polygon Interior Angles", "Geometry",
        concept="sum of interior angles = (n - 2) \\times 180\\deg",
        summary="From one corner, diagonals cut an n-sided polygon into n − 2 triangles. Each triangle adds "
                "180°, so the interior angles add to (n − 2) × 180°.",
        width=700, height=420, level="201",
    )
    V0 = pts[0]
    cen = centroid(pts)
    tri_cols = [theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE]

    def interior(k):
        p, v, q = pts[k - 1], pts[k], pts[(k + 1) % n]
        a1, a2 = heading(v, p), heading(v, q)
        return (a1 - a2) % 360  # the polygon runs counterclockwise, so the interior is on this side

    angs = [interior(k) for k in range(n)]
    total = sum(angs)

    @wt.setup
    def _(c):
        c.polygon(pts, color=theme.INK, width=2.5)
        for k, p in enumerate(pts):
            c.dot(*p, r=4)
        return None

    @wt.step("Draw a polygon", f"This polygon has six sides, so n = {n}. The question: what do its "
             "six inside angles add to? Measuring each one is slow, so cheat with triangles.",
             math=f"n = {n}, sum = ?")
    def _(c):
        for k, p in enumerate(pts):
            c.arc(p[0], p[1], 20, heading(p, pts[(k + 1) % n]), heading(p, pts[(k + 1) % n]) + angs[k],
                  color=theme.SOFT_INK, width=1.5)
            q = away(p, cen, 24)
            c.text(q[0], q[1], f"{angs[k]:.0f}°", size=13, color=theme.SOFT_INK)

    @wt.step("Draw diagonals from one corner", f"From one corner, draw a diagonal to every corner that "
             f"is not a neighbor. The corner skips itself and its two neighbors, so it gets {word(n - 3)}.", math=f"{n} - 3 = {n - 3} diagonals")
    def _(c):
        for k in range(2, n - 1):
            c.line(*V0, *pts[k], color=theme.RED, width=2, dash="7 4")
        c.dot(*V0, r=7, color=theme.RED)
        q = away(V0, cen, 46)
        c.text(q[0], q[1] + 12, "start", size=13, color=theme.RED)

    @wt.step("Count the triangles", f"The diagonals cut the polygon into {word(n - 2)} triangles. Two corners "
             "are neighbors of the start, so you always get two fewer triangles than sides.",
             math=f"n - 2 = {n - 2} triangles")
    def _(c):
        for i in range(n - 2):
            tri = [V0, pts[i + 1], pts[i + 2]]
            c.polygon(tri, color="none", fill=theme.fill(tri_cols[i], "38"))
            g = centroid(tri)
            c.circle(g[0], g[1], 13, color=tri_cols[i], fill=theme.PAPER, width=2)
            c.text(g[0], g[1], str(i + 1), size=14, weight="bold", color=tri_cols[i])
        for k in range(2, n - 1):
            c.line(*V0, *pts[k], color=theme.RED, width=2, dash="7 4")

    @wt.step("Add 180° per triangle", "The triangle corners together fill the polygon corners exactly. "
             f"So the polygon angles add to {word(n - 2)} times 180°.",
             math=f"({n} - 2) \\times 180\\deg = {(n - 2) * 180}\\deg")
    def _(c):
        rich(c, 530, 60, [(f"{n - 2} × 180° = {(n - 2) * 180}°", theme.INK)], size=22)
        c.text(530, 90, f"check: {' + '.join(f'{a:.0f}' for a in angs)} = {total:.0f}", size=12,
               color=theme.SOFT_INK)

    @wt.step("Use the rule for any n", "The same trick works for every polygon. Each extra side adds one "
             "triangle and 180° more.", math="sum = (n - 2) \\times 180\\deg")
    def _(c):
        rows = [["n", "triangles", "sum"]]
        for k in range(3, 9):
            rows.append([str(k), str(k - 2), f"{(k - 2) * 180}°"])
        table(c, 410, 140, rows, col_w=[50, 90, 80], row_h=30, size=15,
              highlight={(n - 2, None): theme.HIGHLIGHT})

    return wt


@diagram("polygon-exterior-angles", "Polygon Exterior Angles", "Geometry")
def polygon_exterior() -> Walkthrough:
    pts = _hexagon()
    n = len(pts)
    cen = centroid(pts)
    turns = []
    for k in range(n):
        h_in = heading(pts[k - 1], pts[k])
        h_out = heading(pts[k], pts[(k + 1) % n])
        turns.append((h_out - h_in) % 360)
    wt = Walkthrough(
        "polygon-exterior-angles", "Polygon Exterior Angles", "Geometry",
        concept="sum of exterior angles = 360\\deg",
        summary="Walk around a polygon and turn at each corner. You make one full turn, so the exterior "
                "angles of any convex polygon add to 360°.",
        width=700, height=420, level="201",
    )
    cols = [theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE, theme.RED, theme.SKY]

    @wt.setup
    def _(c):
        c.polygon(pts, color=theme.INK, width=2.5)
        return None

    @wt.step("Extend each side", "At each corner, keep walking straight for a moment. The angle "
             "between the extension and the next side is the exterior angle.",
             math="exterior + interior = 180\\deg")
    def _(c):
        for k in range(n):
            p, q = pts[k - 1], pts[k]
            e = polar(q[0], q[1], 60, heading(p, q))
            c.line(*q, *e, color=theme.MUTED, width=1.6, dash="5 4")
            c.arrow(*lerp(p, q, 0.42), *lerp(p, q, 0.58), color=theme.SOFT_INK, width=2)
        if c.is_new:
            k = 3
            p, q, r = pts[k - 1], pts[k], pts[(k + 1) % n]
            e = polar(q[0], q[1], 60, heading(p, q))
            angle_mark(c, q, r, p, r=30, color=theme.SOFT_INK)
            angle_mark(c, q, e, r, r=30, color=theme.RED)
            ext = turns[k]
            callout(c, 450, 70, f"interior {180 - ext:.0f}° + exterior {ext:.0f}° = 180°, because they "
                    "share a straight line", target=(q[0] + 10, q[1] - 12), width=210, color=theme.INK)

    @wt.step("Turn at each corner", "Walking counterclockwise, you turn left by the exterior angle at "
             "every corner. Six corners, six turns.",
             math=" + ".join(f"{t:.0f}\\deg" for t in turns))
    def _(c):
        for k in range(n):
            p, q = pts[k - 1], pts[k]
            e = polar(q[0], q[1], 60, heading(p, q))
            angle_mark(c, q, e, pts[(k + 1) % n], r=26, color=cols[k])
            lab = polar(q[0], q[1], 50, heading(p, q) + turns[k] / 2)
            c.text(lab[0], lab[1], f"{turns[k]:.0f}°", size=13, color=cols[k], halo=True)

    @wt.step("One lap is one full turn", "Back at the start you face the same way you began, so the "
             "turns make one full circle. This is true for every convex polygon, even a 100-gon.",
             math=f"{' + '.join(f'{t:.0f}' for t in turns)} = {sum(turns):.0f}\\deg")
    def _(c):
        O = (560.0, 210.0)
        start = 0.0
        for k in range(n):
            c.arc(O[0], O[1], 90, start, start + turns[k], color="none", fill=theme.fill(cols[k], "55"),
                  sector=True)
            c.arc(O[0], O[1], 90, start, start + turns[k], color=cols[k], width=2.5)
            lab = polar(O[0], O[1], 112, start + turns[k] / 2)
            c.text(lab[0], lab[1], f"{turns[k]:.0f}°", size=13, color=cols[k])
            start += turns[k]
        c.dot(*O, r=4)
        c.text(O[0], O[1] + 130, "all turns together = 360°", size=14)

    return wt
