"""Right-triangle trigonometry and the law of cosines."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import angle_mark, brace, right_angle, segment_label
from ..plane import Plane
from ..registry import diagram
from ..svg import text_width
from ..walkthrough import Walkthrough
from ._trigkit import fraction, num

OPP = theme.RED
ADJ = theme.BLUE
HYP = theme.GREEN
ANG = theme.ORANGE


@diagram("soh-cah-toa", "SOH-CAH-TOA", "Trigonometry")
def soh_cah_toa() -> Walkthrough:
    wt = Walkthrough(
        "soh-cah-toa", "SOH-CAH-TOA", "Trigonometry",
        concept="sin \\theta = opp/hyp, cos \\theta = adj/hyp, tan \\theta = opp/adj",
        summary="In a right triangle, each side gets a name from the point of view of the angle θ. "
                "Sine, cosine, and tangent are the three ratios of those sides.",
        width=720, height=360, level="201",
    )
    theta = 30.0
    k = 150.0  # pixels per unit of length
    hyp_len, opp_len = 2.0, 1.0
    adj_len = math.sqrt(hyp_len ** 2 - opp_len ** 2)
    A = (50.0, 300.0)
    C = (A[0] + adj_len * k, A[1])
    B = (C[0], C[1] - opp_len * k)
    sin_v = opp_len / hyp_len
    cos_v = adj_len / hyp_len
    tan_v = opp_len / adj_len
    assert abs(math.degrees(math.atan2(opp_len, adj_len)) - theta) < 1e-9

    rows = [
        ("SOH", "sin", ("opposite", OPP), ("hypotenuse", HYP), ("1", "2"), sin_v),
        ("CAH", "cos", ("adjacent", ADJ), ("hypotenuse", HYP), ("√3", "2"), cos_v),
        ("TOA", "tan", ("opposite", OPP), ("adjacent", ADJ), ("1", "√3"), tan_v),
    ]
    row_y = [90, 180, 270]

    def triangle(c, values=False):
        c.polygon([A, C, B], color=theme.INK, width=2)
        right_angle(c, C, A, B, s=16)
        angle_mark(c, A, C, B, r=46, label="30°" if values else "\\theta", color=ANG, label_r=66)

    def sides(c, values=False):
        c.line(*A, *C, color=ADJ, width=4.5)
        c.line(*C, *B, color=OPP, width=4.5)
        c.line(*A, *B, color=HYP, width=4.5)
        c.dot(*A, r=3, color=theme.INK)
        c.dot(*B, r=3, color=theme.INK)
        c.dot(*C, r=3, color=theme.INK)
        adj_s = "adjacent = √3" if values else "adjacent"
        opp_s = "opposite = 1" if values else "opposite"
        hyp_s = "hypotenuse = 2" if values else "hypotenuse"
        c.text((A[0] + C[0]) / 2, A[1] + 22, adj_s, color=ADJ, size=16, math=values)
        c.text(C[0] + 14, (C[1] + B[1]) / 2, opp_s, color=OPP, size=16, anchor="start", math=values)
        segment_label(c, A, B, hyp_s, offset=14, color=HYP, size=16, math_label=values)

    def row(c, i, values=False):
        tag, fn, (top, tc), (bot, bc), (nt, nb), v = rows[i]
        y = row_y[i]
        c.text(438, y, tag, size=15, weight="bold", color=theme.SOFT_INK, anchor="start")
        if values:
            c.math(486, y, f"{fn} 30° =", anchor="start")
            fraction(c, 594, y, nt, nb, top_color=tc, bottom_color=bc)
            c.math(622, y, f"= {num(v)}", anchor="start")
        else:
            c.math(486, y, f"{fn} \\theta =", anchor="start")
            fraction(c, 624, y, top, bot, top_color=tc, bottom_color=bc)

    @wt.setup
    def _(c):
        c.line(424, 40, 424, 320, color=theme.GRID, width=1)
        return None

    @wt.step("Mark the angle θ",
             "Start with a right triangle. The small square marks the right angle, and θ marks one of "
             "the other two. Each side gets its name from where it stands relative to θ.",
             math="\\theta + 90° + other angle = 180°")
    def _(c):
        triangle(c)

    @wt.step("Name the three sides",
             "The hypotenuse is the longest side, across from the right angle. The opposite side "
             "sits across from θ. The adjacent side touches θ and is not the hypotenuse.",
             math="opposite, adjacent, hypotenuse")
    def _(c):
        sides(c)

    @wt.step("Sine is opposite over hypotenuse",
             "SOH: divide the opposite side by the hypotenuse. The ratio depends only on θ, not on "
             "the size of the triangle.",
             math="sin \\theta = opposite / hypotenuse")
    def _(c):
        row(c, 0)

    @wt.step("Cosine is adjacent over hypotenuse",
             "CAH: divide the adjacent side by the hypotenuse.",
             math="cos \\theta = adjacent / hypotenuse")
    def _(c):
        row(c, 1)

    @wt.step("Tangent is opposite over adjacent",
             "TOA: divide the opposite side by the adjacent side. Tangent leaves out the hypotenuse, "
             "which takes it well.",
             math="tan \\theta = opposite / adjacent")
    def _(c):
        row(c, 2)

    @wt.step("Work a 30-60-90 triangle",
             "With θ = 30°, the sides are 1, √3, and 2. Read each ratio off the picture. "
             "SOH-CAH-TOA sounds like a sneeze, but it holds all three.",
             math=f"sin 30° = 1/2, cos 30° = √3/2 \\approx {num(cos_v)}, "
                  f"tan 30° = 1/√3 \\approx {num(tan_v)}",
             fresh=True)
    def _(c):
        triangle(c, values=True)
        sides(c, values=True)
        for i in range(3):
            row(c, i, values=True)

    return wt


def _seg_label_pos(p1, p2, label, offset=16, side=1, size=16):
    """Returns where annotate.segment_label puts a label, so a later step can cover it."""
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = dy / L * side, -dx / L * side
    o = offset + abs(nx) * text_width(label, size, "serif") / 2
    return mx + nx * o, my + ny * o


@diagram("law-of-cosines", "Law of Cosines", "Trigonometry")
def law_of_cosines() -> Walkthrough:
    a, b, C_deg = 8.0, 5.0, 60.0
    Cr = math.radians(C_deg)
    proj = b * math.cos(Cr)
    h = b * math.sin(Cr)
    c2 = a * a + b * b - 2 * a * b * math.cos(Cr)
    c_len = math.sqrt(c2)
    pyth = a * a + b * b
    assert abs(c2 - (h * h + (a - proj) ** 2)) < 1e-9

    wt = Walkthrough(
        "law-of-cosines", "Law of Cosines", "Trigonometry",
        concept="c^2 = a^2 + b^2 - 2ab cos C",
        summary="The law of cosines is the Pythagorean theorem with a correction term. The term −2ab cos C "
                "shrinks c when the angle C is acute and grows it when C is obtuse.",
        width=740, height=400, level="201",
    )
    A_COL, B_COL, C_COL, ANG, H_COL = theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE, theme.RED

    Cw, Bw, Aw, Dw = (0.0, 0.0), (a, 0.0), (proj, h), (proj, 0.0)

    @wt.setup
    def _(c):
        p = Plane(c, box=(20, 26, 370, 350), x=(-1.0, 8.8), y=(-2.2, 5.8), equal=True)
        c.line(408, 30, 408, 370, color=theme.GRID, width=1)
        return p

    def P(p, w):
        return p.px(*w)

    def panel(c, i, s, color=theme.INK, size=17):
        c.math(424, 64 + i * 44, s, anchor="start", color=color, size=size)

    @wt.step("Start with two sides and the angle between",
             f"Sides a = {num(a)} and b = {num(b)} meet at the angle C = {num(C_deg)}°. "
             "Find the third side c, across from C.",
             math=f"a = {num(a)}, b = {num(b)}, C = {num(C_deg)}°, c = ?")
    def _(c, p):
        pc, pb, pa = P(p, Cw), P(p, Bw), P(p, Aw)
        c.line(*pc, *pb, color=A_COL, width=4)
        c.line(*pc, *pa, color=B_COL, width=4)
        c.line(*pa, *pb, color=C_COL, width=4)
        angle_mark(c, pc, pb, pa, r=30, label="C", color=ANG, label_r=46)
        for w, s, off in ((Cw, "C", (-14, 10)), (Bw, "B", (14, 10)), (Aw, "A", (0, -18))):
            x, y = P(p, w)
            c.dot(x, y, r=4, color=theme.INK)
            c.text(x + off[0], y + off[1], s, size=16, weight="bold", color=theme.INK)
        segment_label(c, pc, pb, f"a = {num(a)}", color=A_COL, side=-1, offset=14)
        segment_label(c, pc, pa, f"b = {num(b)}", color=B_COL, side=1, offset=14)
        segment_label(c, pa, pb, "c = ?", color=C_COL, side=1, offset=14)
        panel(c, 0, "Find c from a, b, and C.", color=theme.INK, size=16)

    @wt.step("Compare with a right angle",
             f"If C were 90°, the Pythagorean theorem gives c = √{num(pyth)} ≈ {num(math.sqrt(pyth), 2)} "
             "(dashed). The real angle is smaller, so c is shorter. A correction term "
             "accounts for the difference.",
             math=f"C = 90° \\implies c^2 = a^2 + b^2 = {num(pyth)}")
    def _(c, p):
        if not c.is_new:
            return
        ghost = (0.0, b)
        pg, pb, pc = P(p, ghost), P(p, Bw), P(p, Cw)
        c.line(*pc, *pg, color=B_COL, width=2, dash="6 5")
        c.line(*pg, *pb, color=theme.SOFT_INK, width=2, dash="6 5")
        c.text(pg[0] - 12, pg[1], "90°", size=14, color=theme.SOFT_INK, anchor="end")
        x, y = p.px(0.5, 5.45)
        c.text(x, y, f"right-angle c = √{num(pyth)} ≈ {num(math.sqrt(pyth), 2)}", size=14,
               color=theme.SOFT_INK, anchor="start", halo=True)
        panel(c, 1, f"c^2 = a^2 + b^2 = {num(pyth)} when C = 90°", color=theme.SOFT_INK, size=16)

    @wt.step("Drop the height from A",
             "The height h from A splits a into two pieces. The piece next to C has length b cos C, "
             "and h has length b sin C, both from SOH-CAH-TOA in the left triangle.",
             math=f"b cos C = {num(proj)}, h = b sin C \\approx {num(h, 2)}")
    def _(c, p):
        pa, pd, pc, pb = P(p, Aw), P(p, Dw), P(p, Cw), P(p, Bw)
        c.line(*pa, *pd, color=H_COL, width=3, dash="7 4")
        right_angle(c, pd, pb, pa, s=11)
        segment_label(c, pa, pd, "h", color=H_COL, side=-1, offset=10, size=17)
        y = pd[1] + 32
        brace(c, pd[0], y, pc[0], y, label="b cos C", color=B_COL, depth=11, size=15)
        brace(c, pb[0], y, pd[0], y, label="a - b cos C", color=A_COL, depth=11, size=15)
        panel(c, 1, f"b cos C = {num(proj)}", color=B_COL)
        panel(c, 2, f"h = b sin C \\approx {num(h, 2)}", color=H_COL)

    @wt.step("Use Pythagoras on the right triangle",
             "The right part of the picture is a right triangle with legs h and a − b cos C and "
             "hypotenuse c. Apply the Pythagorean theorem to it.",
             math="c^2 = (b sin C)^2 + (a - b cos C)^2")
    def _(c, p):
        pa, pd, pb = P(p, Aw), P(p, Dw), P(p, Bw)
        c.polygon([pa, pd, pb], color="none", fill=theme.fill(C_COL, "26"))
        panel(c, 3, "c^2 = h^2 + (a - b cos C)^2", color=C_COL)

    @wt.step("Expand and simplify",
             "Expanding gives b² sin² C + b² cos² C, which is b² because sin² C + cos² C = 1. "
             "What remains is Pythagoras plus the correction term −2ab cos C.",
             math="c^2 = a^2 + b^2 - 2ab cos C")
    def _(c, p):
        panel(c, 4, "c^2 = a^2 + b^2(sin^2 C + cos^2 C) - 2ab cos C", size=15)
        x, y = 424, 64 + 5 * 44
        c.math(x, y, "c^2 = a^2 + b^2 - 2ab cos C", anchor="start", color=C_COL, size=19)
        w = text_width("c^2 = a^2 + b^2 - 2ab cos C", 19, "serif")
        c.rect(x - 8, y - 17, w + 16, 34, color=C_COL, width=1.5, rx=6)

    @wt.step("Compute c",
             f"Put in the numbers. The correction 2ab cos C = {num(2 * a * b * math.cos(Cr))} "
             f"takes c² down from {num(pyth)} to {num(c2)}.",
             math=f"c^2 = {num(a * a)} + {num(b * b)} - 2({num(a)})({num(b)})(1/2) = {num(c2)}, "
                  f"c = {num(c_len)}")
    def _(c, p):
        pa, pb = P(p, Aw), P(p, Bw)
        c.line(*pa, *pb, color=C_COL, width=5)
        x, y = _seg_label_pos(pa, pb, "c = ?", offset=14, side=1)
        c.label_box(x, y, f"c = {num(c_len)}", color=C_COL, border=C_COL, math=True, size=17)
        c.math(424, 64 + 6 * 44, f"c = √{num(c2)} = {num(c_len)}", anchor="start", color=C_COL, size=19)

    return wt
