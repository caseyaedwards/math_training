"""Area by cutting and rearranging: parallelograms, triangles, trapezoids."""

from __future__ import annotations

from .. import theme
from ..annotate import brace, right_angle
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._geo import centroid, num, rich

BASE, HEIGHT, PIECE, SHAPE = theme.BLUE, theme.ORANGE, theme.RED, theme.SKY


def _poly_area(pts):
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


@diagram("area-parallelogram-triangle", "Area of a Parallelogram and a Triangle", "Geometry")
def parallelogram() -> Walkthrough:
    b, h, lean = 6, 4, 2
    para = [(0, 0), (b, 0), (b + lean, h), (lean, h)]
    cut = [(0, 0), (lean, 0), (lean, h)]  # the triangle that slides
    moved = [(x + b, y) for x, y in cut]
    rect_area = b * h
    assert abs(_poly_area(para) - rect_area) < 1e-9
    wt = Walkthrough(
        "area-parallelogram-triangle", "Area of a Parallelogram and a Triangle", "Geometry",
        concept="parallelogram: A = b \\cdot h, triangle: A = 1/2 \\cdot b \\cdot h",
        summary="Cut a triangle off one end of a parallelogram and slide it to the other end: you get a "
                "rectangle with the same base and height. A triangle is half of such a parallelogram.",
        width=700, height=380, level="201",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(30, 20, 640, 330), x=(-1, 11), y=(-1.2, 5.2), equal=True)
        p.grid(step=1)
        return p

    def base_height(c, p, x0=0, x1=b, hx=lean, show_h=True):
        brace(c, *p.px(x1, -0.1), *p.px(x0, -0.1), f"b = {b}", color=BASE, size=17)
        if show_h:
            p.segment(hx, 0, hx, h, color=HEIGHT, width=2.5, dash="7 4")
            right_angle(c, p.px(hx, 0), p.px(hx + 1, 0), p.px(hx, 1), s=12, color=HEIGHT)
            p.label(hx + 0.35, h / 2, f"h = {h}", color=HEIGHT, size=17, anchor="start")

    @wt.step("Draw a parallelogram", f"This parallelogram has base b = {b} and leans over by {lean}. "
             f"Its height h = {h} is the straight-up distance between the top and bottom, not the slanted side.",
             math=f"b = {b}, h = {h}")
    def _(c, p):
        if c.is_new:
            p.region(para, color=SHAPE, opacity=0.3, outline=theme.INK, width=2.5)
            base_height(c, p)

    @wt.step("Cut off a triangle", f"Cut straight down along the height. A right triangle with legs {lean} "
             f"and {h} falls off the left end.", math=f"triangle: {lean} by {h}")
    def _(c, p):
        if c.is_new:
            p.region(para, color=SHAPE, opacity=0.3, outline=theme.INK, width=2.5)
            p.region(cut, color=PIECE, opacity=0.35, outline=PIECE, width=2.5)
            base_height(c, p)
            c.text(*p.px(lean + 0.4, h + 0.45), "cut here", size=14, color=PIECE, anchor="start")

    @wt.step("Slide it to the other end", f"Move the triangle {b} units to the right. Its slanted edge fits "
             "the slanted edge on the right exactly, like a puzzle piece.", math=f"slide right {b}")
    def _(c, p):
        if c.is_new:
            p.region([(lean, 0), (b, 0), (b + lean, h), (lean, h)], color=SHAPE, opacity=0.3, outline=theme.INK,
                     width=2.5)
            p.polygon(cut, color=PIECE, width=1.5, dash="5 4")
            p.region(moved, color=PIECE, opacity=0.35, outline=PIECE, width=2.5)
            g0, g1 = p.px(*centroid(cut)), p.px(*centroid(moved))
            c.arrow(g0[0] + 10, g0[1] - 70, g1[0] - 10, g1[1] - 70, color=PIECE, width=2)
            c.text((g0[0] + g1[0]) / 2, g0[1] - 84, f"slide {b} right", size=14, color=PIECE, halo=True)
            base_height(c, p, show_h=False)

    @wt.step("Read the rectangle", f"The pieces now form a {b} by {h} rectangle with {rect_area} unit "
             "squares. Nothing was added or lost, so the parallelogram has the same area.",
             math=f"A = b \\cdot h = {b} \\times {h} = {rect_area}")
    def _(c, p):
        if not c.is_new:
            return
        rect = [(lean, 0), (b + lean, 0), (b + lean, h), (lean, h)]
        p.region(rect, color=SHAPE, opacity=0.3, outline=theme.INK, width=2.5)
        p.region(moved, color=PIECE, opacity=0.35, outline=PIECE, width=1.5)
        brace(c, *p.px(b + lean, -0.1), *p.px(lean, -0.1), f"b = {b}", color=BASE, size=17)
        brace(c, *p.px(b + lean + 0.1, h), *p.px(b + lean + 0.1, 0), f"h = {h}", color=HEIGHT, size=17)
        for i in range(b):
            for j in range(h):
                c.text(*p.px(lean + i + 0.5, j + 0.5), str(j * b + i + 1), size=11, color=theme.SOFT_INK)
        rich(c, *p.px(4.9, h + 0.7), [(f"{b}", BASE), (" × ", theme.INK), (f"{h}", HEIGHT),
                                       (f" = {rect_area}", theme.INK)], size=20)

    @wt.step("A triangle is half a parallelogram", f"Draw a diagonal across the parallelogram. It splits "
             f"into two copies of the same triangle, so one triangle gets half: {rect_area} ÷ 2 = "
             f"{rect_area // 2}.", math=f"A = 1/2 \\cdot b \\cdot h = 1/2 \\cdot {b} \\cdot {h} = {rect_area // 2}")
    def _(c, p):
        tri = [(0, 0), (b, 0), (lean, h)]
        other = [(b, 0), (b + lean, h), (lean, h)]
        p.region(tri, color=theme.GREEN, opacity=0.35, outline=theme.GREEN, width=2.5)
        p.region(other, color=theme.MUTED, opacity=0.2, outline=theme.MUTED, width=1.5)
        p.polygon(other, color=theme.MUTED, width=1.5, dash="5 4")
        base_height(c, p)
        c.text(*p.px(*centroid(tri)), f"{rect_area // 2}", size=20, weight="bold", color=theme.GREEN, halo=True)
        c.text(*p.px(*centroid(other)), f"{rect_area // 2}", size=20, weight="bold", color=theme.SOFT_INK,
               halo=True)
        c.text(*p.px(9.3, 3.2), "two copies", size=14, color=theme.SOFT_INK)
        c.text(*p.px(9.3, 2.7), f"{rect_area // 2} + {rect_area // 2} = {rect_area}", size=14, color=theme.SOFT_INK)

    return wt


@diagram("area-trapezoid", "Area of a Trapezoid", "Geometry")
def trapezoid() -> Walkthrough:
    a, b, h, lean = 3, 6, 3, 1  # top base a, bottom base b
    trap = [(0, 0), (b, 0), (lean + a, h), (lean, h)]
    mx, my = (b + lean + a) / 2, h / 2  # midpoint of the right slanted side
    flipped = [(2 * mx - x, 2 * my - y) for x, y in trap]  # copy turned 180 degrees about that midpoint
    area = (a + b) * h / 2
    assert abs(_poly_area(trap) - area) < 1e-9
    wt = Walkthrough(
        "area-trapezoid", "Area of a Trapezoid", "Geometry",
        concept="A = 1/2 \\cdot (a + b) h",
        summary="Two copies of a trapezoid, one turned upside down, make a parallelogram with base a + b. "
                "The trapezoid is half of it.",
        width=700, height=340, level="201",
    )
    T_COL, F_COL = theme.SKY, theme.PURPLE

    @wt.setup
    def _(c):
        p = Plane(c, box=(30, 20, 640, 300), x=(-1, 11), y=(-1.9, 4.2), equal=True)
        p.grid(step=1)
        return p

    @wt.step("Draw a trapezoid", f"The trapezoid has parallel sides a = {a} on top and b = {b} on the "
             f"bottom, with height h = {h}.", math=f"a = {a}, b = {b}, h = {h}")
    def _(c, p):
        p.region(trap, color=T_COL, opacity=0.35, outline=theme.INK, width=2.5)
        brace(c, *p.px(lean, h + 0.1), *p.px(lean + a, h + 0.1), f"a = {a}", color=theme.GREEN)
        brace(c, *p.px(b, -0.1), *p.px(0, -0.1), f"b = {b}", color=theme.BLUE)
        p.segment(lean, 0, lean, h, color=theme.ORANGE, width=2.5, dash="7 4")
        p.label(lean + 0.2, h / 2, f"h = {h}", color=theme.ORANGE, anchor="start", size=16)

    @wt.step("Add an upside-down copy", f"Turn a second copy upside down and set it beside the first. "
             f"Its long side b = {b} now runs along the top.", math="two trapezoids")
    def _(c, p):
        p.region(flipped, color=F_COL, opacity=0.3, outline=theme.INK, width=2.5)
        brace(c, *p.px(a + lean, h + 0.1), *p.px(a + lean + b, h + 0.1), f"b = {b}", color=theme.BLUE)
        brace(c, *p.px(b + a, -0.1), *p.px(b, -0.1), f"a = {a}", color=theme.GREEN)
        p.point(mx, my, color=theme.INK, r=4)
        c.curved_arrow(*p.px(mx + 0.9, my - 0.3), *p.px(mx + 0.9, my + 0.6), bend=-0.8, color=theme.SOFT_INK,
                       width=1.5)

    @wt.step("Read the parallelogram, then halve it", f"Together they make a parallelogram with base "
             f"a + b = {a + b} and height {h}, area {(a + b) * h}. One trapezoid is half: {num(area)}.",
             math=f"A = 1/2 \\cdot ({a} + {b}) \\cdot {h} = {num(area)}")
    def _(c, p):
        p.polygon([(0, 0), (a + b, 0), (a + b + lean, h), (lean, h)], color=theme.INK, width=3.5)
        c.text(*p.px(*centroid(trap)), num(area), size=20, weight="bold", color=theme.INK, halo=True)
        c.text(*p.px(*centroid(flipped)), num(area), size=20, weight="bold", color=theme.INK, halo=True)
        rich(c, *p.px(5, -1.5), [("whole: ", theme.SOFT_INK), (f"({a} + {b}) × {h} = {(a + b) * h}", theme.INK)],
             size=17)

    return wt
