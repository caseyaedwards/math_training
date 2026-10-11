"""Triangle diagrams: the Pythagorean theorem and similar triangles."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import angle_mark, right_angle, segment_label
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._geo import centroid, num, rich, word

A_COL, B_COL, C_COL = theme.BLUE, theme.ORANGE, theme.GREEN
TRI = theme.PURPLE


def _unit_grid(p: Plane, origin, u, v, n, m, color):
    """Draws the n x m unit cells of a square spanned by unit vectors u and v from origin (world)."""
    ox, oy = origin
    for i in range(1, n):
        a = (ox + u[0] * i, oy + u[1] * i)
        b = (a[0] + v[0] * m, a[1] + v[1] * m)
        p.segment(*a, *b, color=color, width=1, stroke_opacity=0.6)
    for j in range(1, m):
        a = (ox + v[0] * j, oy + v[1] * j)
        b = (a[0] + u[0] * n, a[1] + u[1] * n)
        p.segment(*a, *b, color=color, width=1, stroke_opacity=0.6)


@diagram("pythagorean-theorem", "Pythagorean Theorem", "Geometry")
def pythagorean() -> Walkthrough:
    a, b = 3, 4
    c_len = math.hypot(a, b)
    wt = Walkthrough(
        "pythagorean-theorem", "Pythagorean Theorem", "Geometry",
        concept="a^2 + b^2 = c^2",
        summary="The squares on the two legs of a right triangle together have the same area as the square "
                "on the hypotenuse. Counting tiles shows it for 3-4-5; rearranging four triangles proves it.",
        width=700, height=440, level="201",
    )
    # right angle at the origin: leg a up the y-axis, leg b along the x-axis
    O, Pa, Pb = (0, 0), (0, a), (b, 0)
    n = (a / c_len, b / c_len)  # unit normal pointing away from the triangle, off the hypotenuse
    u_c = (-b / c_len, a / c_len)  # unit vector along the hypotenuse from Pb to Pa
    hyp_sq = [Pb, Pa, (Pa[0] + n[0] * c_len, Pa[1] + n[1] * c_len), (Pb[0] + n[0] * c_len, Pb[1] + n[1] * c_len)]

    def triangle(c, p):
        p.polygon([O, Pb, Pa], color=theme.INK, fill=theme.fill(TRI, "40"), width=2.5)
        right_angle(c, p.px(*O), p.px(*Pb), p.px(*Pa), s=14)

    @wt.setup
    def _(c):
        return Plane(c, box=(20, 15, 660, 415), x=(-4, 10), y=(-4.6, 7.4), equal=True)

    @wt.step("Draw a right triangle", f"The legs are a = {a} and b = {b}. They meet at a right angle. The "
             "long side across from the right angle is the hypotenuse c.",
             math=f"a = {a}, b = {b}, c = ?")
    def _(c, p):
        triangle(c, p)
        segment_label(c, p.px(*Pa), p.px(*O), f"a = {a}", color=A_COL, offset=14, side=1)
        segment_label(c, p.px(*O), p.px(*Pb), f"b = {b}", color=B_COL, offset=14, side=1)
        if c.is_new:
            segment_label(c, p.px(*Pb), p.px(*Pa), "c", color=C_COL, offset=14, side=1)

    @wt.step("Build a square on leg a", f"A square with side {a} holds {a} × {a} = {a * a} unit tiles.",
             math=f"a^2 = {a}^2 = {a * a}")
    def _(c, p):
        p.region([(0, 0), (0, a), (-a, a), (-a, 0)], color=A_COL, opacity=0.25, outline=A_COL, width=2.5)
        _unit_grid(p, (-a, 0), (1, 0), (0, 1), a, a, A_COL)
        p.label(-a / 2, a / 2, f"a² = {a * a}", color=A_COL, size=20, weight="bold")

    @wt.step("Build a square on leg b", f"A square with side {b} holds {b} × {b} = {b * b} tiles.",
             math=f"b^2 = {b}^2 = {b * b}")
    def _(c, p):
        p.region([(0, 0), (b, 0), (b, -b), (0, -b)], color=B_COL, opacity=0.25, outline=B_COL, width=2.5)
        _unit_grid(p, (0, -b), (1, 0), (0, 1), b, b, B_COL)
        p.label(b / 2, -b / 2, f"b² = {b * b}", color=B_COL, size=20, weight="bold")

    @wt.step("Build a square on the hypotenuse", f"The tilted square on c holds {num(c_len * c_len)} tiles. "
             f"That is exactly {a * a} + {b * b}, so c = {num(c_len)}.",
             math=f"c^2 = {a * a} + {b * b} = {num(c_len ** 2)}, c = {num(c_len)}")
    def _(c, p):
        p.region(hyp_sq, color=C_COL, opacity=0.25, outline=C_COL, width=2.5)
        _unit_grid(p, Pb, u_c, n, int(round(c_len)), int(round(c_len)), C_COL)
        g = centroid(hyp_sq)
        p.label(*g, f"c² = {num(c_len ** 2)}", color=C_COL, size=20, weight="bold")
        segment_label(c, p.px(*Pb), p.px(*Pa), f"c = {num(c_len)}", color=C_COL, offset=12, side=1)
        rich(c, 560, 380, [(f"{a * a}", A_COL), (" + ", theme.INK), (f"{b * b}", B_COL), (" = ", theme.INK),
                           (f"{num(c_len ** 2)}", C_COL)], size=24)

    # -- rearrangement proof --------------------------------------------------

    s = a + b

    def big(p, ox, tris, holes):
        p.rect(ox, 0, ox + s, s, color=theme.INK, width=2.5)
        for pts in tris:
            p.polygon([(ox + x, y) for x, y in pts], color=theme.INK, fill=theme.fill(TRI, "55"), width=1.5)
        for pts, col, lab in holes:
            q = [(ox + x, y) for x, y in pts]
            p.region(q, color=col, opacity=0.28, outline=col, width=2)
            g = centroid(q)
            p.label(*g, lab, color=col, size=20, weight="bold")

    left_tris = [[(0, 0), (a, 0), (0, b)], [(a, 0), (s, 0), (s, a)], [(s, a), (s, s), (b, s)],
                 [(b, s), (0, s), (0, b)]]
    right_tris = [[(a, 0), (s, 0), (s, a)], [(a, 0), (s, a), (a, a)], [(0, a), (a, a), (a, s)],
                  [(0, a), (a, s), (0, s)]]

    def frame(c, p2, both=True):
        """Labels the pieces of each big square's bottom and left edges with a and b."""
        for ox, left_split in ((0, b), (s + 1.6, a))[: 2 if both else 1]:
            for x0, x1, lab, col in ((0, a, f"a = {a}", A_COL), (a, s, f"b = {b}", B_COL)):
                c.text(*p2.px(ox + (x0 + x1) / 2, -0.4), lab, size=14, math=True, color=col)
            first = (f"b = {b}", B_COL) if left_split == b else (f"a = {a}", A_COL)
            second = (f"a = {a}", A_COL) if left_split == b else (f"b = {b}", B_COL)
            for y0, y1, (lab, col) in ((0, left_split, first), (left_split, s, second)):
                c.text(*p2.px(ox - 0.15, (y0 + y1) / 2), lab, size=14, math=True, color=col, anchor="end")

    @wt.step("Arrange four copies in a big square", f"Put four copies of the triangle inside a square with "
             f"side a + b = {s}. They leave a tilted square hole with side c.",
             math=f"big square = 4 triangles + c^2", fresh=True)
    def _(c, p):
        p2 = Plane(c, box=(20, 20, 660, 400), x=(-1.3, 2 * s + 1.7), y=(-1, s + 0.6), equal=True)
        frame(c, p2, both=False)
        big(p2, 0, left_tris, [([(a, 0), (s, a), (b, s), (0, b)], C_COL, f"c² = {num(c_len ** 2)}")])
        c.text(*p2.px(s / 2, s + 0.35), "arrangement 1", size=14, color=theme.SOFT_INK)

    @wt.step("Rearrange the same four triangles", "Slide the triangles into two rectangles. Now the holes "
             "are the squares on a and b. Same big square, same triangles, so the holes have equal area.",
             math=f"c^2 = a^2 + b^2, so {num(c_len ** 2)} = {a * a} + {b * b}", fresh=True)
    def _(c, p):
        p2 = Plane(c, box=(20, 20, 660, 400), x=(-1.3, 2 * s + 1.7), y=(-1, s + 0.6), equal=True)
        frame(c, p2)
        big(p2, 0, left_tris, [([(a, 0), (s, a), (b, s), (0, b)], C_COL, f"c² = {num(c_len ** 2)}")])
        ox = s + 1.6
        big(p2, ox, right_tris, [([(0, 0), (a, 0), (a, a), (0, a)], A_COL, f"a² = {a * a}"),
                                 ([(a, a), (s, a), (s, s), (a, s)], B_COL, f"b² = {b * b}")])
        c.text(*p2.px(s / 2, s + 0.35), "arrangement 1", size=14, color=theme.SOFT_INK)
        c.text(*p2.px(ox + s / 2, s + 0.35), "arrangement 2", size=14, color=theme.SOFT_INK)
        c.text(*p2.px(s + 0.8, s / 2), "=", size=34, color=theme.INK)

    return wt


# ---------------------------------------------------------------------------
# Similar triangles
# ---------------------------------------------------------------------------


@diagram("similar-triangles", "Similar Triangles and Scale Factor", "Geometry")
def similar() -> Walkthrough:
    k = 2
    small = [(0, 0), (3, 0), (1, 2)]
    off = 5
    bigt = [(off + k * x, k * y) for x, y in small]
    area_small = 0.5 * 3 * 2
    side = [math.dist(small[i], small[(i + 1) % 3]) for i in range(3)]
    wt = Walkthrough(
        "similar-triangles", "Similar Triangles and Scale Factor", "Geometry",
        concept="sides \\times k, area \\times k^2",
        summary="Scaling a triangle by k keeps its angles and multiplies every side by k. The area grows by "
                "k², because k² copies of the small triangle tile the big one.",
        width=700, height=380, level="201",
    )
    S_COL, L_COL = theme.BLUE, theme.ORANGE
    names_s = ["A", "B", "C"]

    @wt.setup
    def _(c):
        p = Plane(c, box=(20, 10, 660, 340), x=(-1, 11.6), y=(-0.9, 4.9), equal=True)
        p.grid(step=1)
        return p

    def draw_tri(c, p, pts, col, names, prime=""):
        p.polygon(pts, color=col, fill=theme.fill(col, "30"), width=2.5)
        g = centroid(pts)
        for (x, y), nm in zip(pts, names):
            X, Y = p.px(x, y)
            gx, gy = p.px(*g)
            dx, dy = X - gx, Y - gy
            L = math.hypot(dx, dy)
            c.text(X + dx / L * 16, Y + dy / L * 16, nm + prime, size=16, math=True, color=col, weight="bold",
                   halo=True)

    @wt.step("Start with a triangle", f"Triangle ABC has base 3 and height 2 on the grid. Its area is "
             f"half of base times height, {num(area_small)} square units.",
             math=f"area = 1/2 \\cdot 3 \\cdot 2 = {num(area_small)}")
    def _(c, p):
        draw_tri(c, p, small, S_COL, names_s)

    @wt.step("Scale it by k = 2", "Double every length. The new triangle A′B′C′ has base 6 and "
             "height 4, and it looks like the same triangle seen up close.", math=f"k = {k}")
    def _(c, p):
        draw_tri(c, p, bigt, L_COL, names_s, "′")
        for pts, col, f in ((small, S_COL, 1), (bigt, L_COL, k)):
            apex, base0, base1 = pts[2], pts[0], pts[1]
            p.segment(apex[0], apex[1], apex[0], 0, color=col, width=1.6, dash="5 4")
            p.label(apex[0] + 0.12, apex[1] * 0.3, f"h = {2 * f}", color=col, size=14, anchor="start")
            p.label((base0[0] + base1[0]) / 2, -0.42, f"base {3 * f}", color=col, size=14)

    @wt.step("The angles stay the same", "Scaling stretches the sides but never bends a corner. Matching "
             "angles are equal, which is what similar means.", math="\\angle A = \\angle A′, \\angle B = "
             "\\angle B′, \\angle C = \\angle C′")
    def _(c, p):
        for pts, col in ((small, S_COL), (bigt, L_COL)):
            P = [p.px(*q) for q in pts]
            for i, cnt in zip(range(3), (1, 2, 3)):
                angle_mark(c, P[i], P[(i + 1) % 3], P[(i + 2) % 3], r=22 + 4 * cnt, count=cnt,
                           color=theme.PURPLE, fill=False)

    @wt.step("Every side doubles", "Each side of A′B′C′ is twice the matching side of ABC. The ratio of "
             f"matching sides is the scale factor k = {k}.",
             math=f"6/3 = {num(k * side[1])}/{num(side[1])} = {num(k * side[2])}/{num(side[2])} = {k}")
    def _(c, p):
        for pts, col, f in ((small, S_COL, 1), (bigt, L_COL, k)):
            P = [p.px(*q) for q in pts]
            for i in (1, 2):
                j = (i + 1) % 3
                segment_label(c, P[i], P[j], num(side[i] * f), color=col, offset=16, side=-1, size=14)

    @wt.step("Area grows by k²", f"Join the midpoints of A′B′C′. It splits into {word(k * k)} copies of ABC, "
             f"so the area is {k}² = {k * k} times as big. Twice as wide and twice as tall makes four times "
             "the paint.", math=f"area = {k}^2 \\times {num(area_small)} = {num(k * k * area_small)}")
    def _(c, p):
        A2, B2, C2 = bigt
        m_ab = ((A2[0] + B2[0]) / 2, 0)
        m_bc = ((B2[0] + C2[0]) / 2, (B2[1] + C2[1]) / 2)
        m_ca = ((C2[0] + A2[0]) / 2, (C2[1] + A2[1]) / 2)
        p.polygon([m_ab, m_bc, m_ca], color=L_COL, width=2, dash="6 4")
        for i, tri in enumerate(([A2, m_ab, m_ca], [m_ab, B2, m_bc], [m_ca, m_bc, C2], [m_ab, m_bc, m_ca])):
            g = centroid(tri)
            X, Y = p.px(*g)
            c.circle(X, Y, 11, color=L_COL, fill=theme.PAPER, width=1.5)
            c.text(X, Y, str(i + 1), size=13, weight="bold", color=L_COL)
        rich(c, *p.px(4.1, 4.3), [(f"{num(area_small)}", S_COL), (f" × {k * k} = ", theme.INK),
                                   (f"{num(k * k * area_small)}", L_COL)], size=20)

    return wt
