"""Vectors in the plane: components, addition, linear combinations, and the dot product."""

from __future__ import annotations

import math

from .. import theme
from ..annotate import angle_mark, brace, right_angle
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._linalg import E1, RESULT, U, V, boxed, light_axes, num, offset_segment, tip, vec


@diagram("vector-components", "Vector Components and Magnitude", "Linear Algebra")
def build_components() -> Walkthrough:
    vx, vy = 3, 4
    mag = math.hypot(vx, vy)
    ux, uy = vx / mag, vy / mag
    wt = Walkthrough(
        "vector-components", "Vector Components and Magnitude", "Linear Algebra",
        concept="v = (v_x, v_y), |v| = sqrt(v_x^2 + v_y^2)",
        summary="A vector is an arrow from the origin. Its components say how far it goes along each axis, "
                "and the Pythagorean theorem gives its length.",
        width=640, height=400, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(40, 24, 560, 352), x=(-1, 6.5), y=(-0.9, 5), equal=True)
        light_axes(p)
        return p

    @wt.step("Draw the vector as an arrow",
             "The vector v starts at the origin and ends at the point (3, 4). "
             "The arrow has a direction and a length.",
             math=f"v = ({vx}, {vy})")
    def _(c, p):
        vec(p, 0, 0, vx, vy, U)
        p.c.dot(*p.px(vx, vy), r=4.5, color=U)
        tip(p, vx, vy, f"({vx}, {vy})", U, dx=14, dy=-4, anchor="start")
        tip(p, vx / 2, vy / 2, "v", U, dx=-16, dy=-10, size=19)

    @wt.step("Walk along the x-axis",
             "The first component is the horizontal distance. Go 3 units to the right.",
             math=f"v_x = {vx}")
    def _(c, p):
        vec(p, 0, 0, vx, 0, V, width=3)
        tip(p, vx / 2, 0, f"v_x = {vx}", V, dy=38)

    @wt.step("Climb parallel to the y-axis",
             "The second component is the vertical distance. From (3, 0) go 4 units up. "
             "The two components meet at a right angle.",
             math=f"v_y = {vy}")
    def _(c, p):
        vec(p, vx, 0, vx, vy, E1, width=3)
        right_angle(c, p.px(vx, 0), p.px(0, 0), p.px(vx, vy), s=13, color=theme.SOFT_INK)
        tip(p, vx, vy * 0.42, f"v_y = {vy}", E1, dx=12, dy=0, anchor="start")

    @wt.step("Measure the length",
             "The arrow is the hypotenuse of a right triangle with legs 3 and 4. "
             "The Pythagorean theorem gives its length, and the old 3-4-5 triangle shows up again.",
             math=f"|v| = sqrt({vx}^2 + {vy}^2) = sqrt({vx * vx + vy * vy}) = {num(mag)}")
    def _(c, p):
        p.region([(0, 0), (vx, 0), (vx, vy)], color=U, opacity=0.1)
        X, Y = p.px(vx * 0.62, vy * 0.62)
        boxed(c, X - 66, Y - 16, f"|v| = {num(mag)}", U, size=17)
        tip(p, vx * 0.68, vy * 0.22, f"{vx}^2 + {vy}^2 = {num(mag)}^2", theme.SOFT_INK, dy=0, size=15)

    @wt.step("Shrink to a unit vector",
             "Divide each component by the length 5. The result points the same way and has length 1, "
             "so it ends on the unit circle.",
             math=f"v/|v| = ({vx}/{num(mag)}, {vy}/{num(mag)}) = ({num(ux)}, {num(uy)})")
    def _(c, p):
        p.parametric(math.cos, math.sin, 0, math.pi / 2, color=theme.MUTED, width=1.6, dash="5 4")
        vec(p, 0, 0, ux, uy, RESULT, width=4)
        tip(p, 1.05, 0.25, "1", theme.SOFT_INK, dx=6, dy=0, size=14, anchor="start")
        tip(p, -0.12, 1.05, f"({num(ux)}, {num(uy)})", RESULT, dx=0, dy=0, anchor="end", size=15)

    return wt


@diagram("vector-addition", "Vector Addition", "Linear Algebra")
def build_addition() -> Walkthrough:
    u = (4, 1)
    v = (1, 3)
    s = (u[0] + v[0], u[1] + v[1])
    wt = Walkthrough(
        "vector-addition", "Vector Addition", "Linear Algebra",
        concept="u + v = (u_x + v_x, u_y + v_y) = v + u",
        summary="To add two vectors, place the tail of the second at the tip of the first. "
                "Either order lands on the same point, which is the far corner of a parallelogram.",
        width=640, height=400, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(40, 24, 560, 352), x=(-0.9, 6.4), y=(-0.9, 4.9), equal=True)
        light_axes(p)
        return p

    @wt.step("Draw both vectors from the origin",
             "The vector u goes 4 right and 1 up. The vector v goes 1 right and 3 up.",
             math=f"u = ({u[0]}, {u[1]}), v = ({v[0]}, {v[1]})")
    def _(c, p):
        vec(p, 0, 0, *u, U)
        vec(p, 0, 0, *v, V)
        tip(p, u[0] * 0.6, u[1] * 0.6, "u", U, dx=4, dy=18, size=19)
        tip(p, v[0] * 0.5, v[1] * 0.5, "v", V, dx=-16, dy=-2, size=19)
        tip(p, *u, f"({u[0]}, {u[1]})", U, dx=10, dy=14, anchor="start", size=15)
        tip(p, *v, f"({v[0]}, {v[1]})", V, dx=-8, dy=-6, anchor="end", size=15)

    @wt.step("Move v to the tip of u",
             "Slide a copy of v so its tail sits on the tip of u. "
             "Sliding keeps its length and direction.",
             math=f"tail at ({u[0]}, {u[1]})")
    def _(c, p):
        a = p.px(v[0] * 0.5, v[1] * 0.5)
        b = p.px(u[0] + v[0] * 0.5, u[1] + v[1] * 0.5)
        if c.is_new:
            c.curved_arrow(a[0] + 10, a[1] - 4, b[0] - 10, b[1] - 4, bend=-0.18, color=theme.MUTED,
                           width=1.6, dash="5 4")
        vec(p, *u, s[0], s[1], V)
        tip(p, u[0] + v[0] * 0.5, u[1] + v[1] * 0.5, "v", V, dx=16, dy=6, size=19)

    @wt.step("Draw the sum",
             "The sum runs from the origin to the tip of the copied v. "
             "Add the components to get its coordinates.",
             math=f"u + v = ({u[0]} + {v[0]}, {u[1]} + {v[1]}) = ({s[0]}, {s[1]})")
    def _(c, p):
        vec(p, 0, 0, *s, RESULT, width=3.6)
        p.c.dot(*p.px(*s), r=4.5, color=RESULT)
        tip(p, *s, f"({s[0]}, {s[1]})", RESULT, dx=12, dy=-12, anchor="start")
        tip(p, s[0] * 0.55, s[1] * 0.55, "u + v", RESULT, dx=-26, dy=-12)

    @wt.step("Add in the other order",
             "Put u at the tip of v instead. The path lands on the same point, so u + v = v + u. "
             "The two paths outline a parallelogram. Addition does not care who goes first.",
             math=f"v + u = ({s[0]}, {s[1]}) = u + v")
    def _(c, p):
        p.region([(0, 0), u, s, v], color=RESULT, opacity=0.1)
        vec(p, *v, *s, U, dash="7 4")
        tip(p, v[0] + u[0] * 0.5, v[1] + u[1] * 0.5, "u", U, dx=-4, dy=-16, size=19)

    return wt


@diagram("linear-combinations", "Linear Combinations and Span", "Linear Algebra")
def build_combinations() -> Walkthrough:
    u = (1, 1)
    v = (-2, 1)
    a, b = 2, -1
    au = (a * u[0], a * u[1])
    bv = (b * v[0], b * v[1])
    t = (au[0] + bv[0], au[1] + bv[1])
    wt = Walkthrough(
        "linear-combinations", "Linear Combinations and Span", "Linear Algebra",
        concept="a u + b v, with a, b \\in \\mathbb{R}",
        summary="Stretch two vectors by numbers and add the results. Two vectors that point in different "
                "directions reach every point of the plane this way, so their span is the whole plane.",
        width=660, height=390, level="301",
    )

    def base(p):
        vec(p, 0, 0, *u, U)
        vec(p, 0, 0, *v, V)
        tip(p, *u, "u", U, dx=-2, dy=-16, size=19)
        tip(p, *v, "v", V, dx=-4, dy=-16, size=19)

    def target(p):
        X, Y = p.px(*t)
        p.c.circle(X, Y, 9, color=theme.INK, width=2)
        p.c.dot(X, Y, r=3, color=theme.INK)
        tip(p, *t, f"target ({t[0]}, {t[1]})", theme.INK, dx=14, dy=0, anchor="start", size=16)

    @wt.setup
    def _(c):
        p = Plane(c, box=(30, 24, 600, 344), x=(-3.2, 6.6), y=(-1.8, 3.4), equal=True)
        light_axes(p)
        return p

    @wt.step("Pick two vectors and a target",
             "Start with u and v. The goal is to reach the point (4, 1) using only stretched copies of "
             "u and v.",
             math=f"u = ({u[0]}, {u[1]}), v = ({v[0]}, {v[1]})")
    def _(c, p):
        base(p)
        target(p)

    @wt.step("Stretch u by 2",
             "Multiplying by a scalar changes the length but keeps the line. "
             "Every multiple of u sits on the dashed line through u.",
             math=f"{a}u = ({au[0]}, {au[1]})")
    def _(c, p):
        p.line_through(0, 0, *u, color=U, width=1.2, dash="6 5")
        vec(p, 0, 0, *au, U, width=4.2)
        tip(p, *au, f"{a}u", U, dx=-14, dy=-12, size=19)

    @wt.step("Flip v with a negative scalar",
             "Multiplying by −1 reverses the direction. The vector −v lies on the same line as v "
             "but points the other way.",
             math=f"{b}v = ({bv[0]}, {bv[1]})")
    def _(c, p):
        p.line_through(0, 0, *v, color=V, width=1.2, dash="6 5")
        vec(p, 0, 0, *bv, V, width=4.2)
        tip(p, *bv, "-v", V, dx=-12, dy=20, size=19)

    @wt.step("Add the scaled vectors",
             "Place −v at the tip of 2u. The path ends exactly on the target, "
             "so 2 and −1 are the weights that work.",
             math=f"{a}u + ({b})v = ({au[0]}, {au[1]}) + ({bv[0]}, {bv[1]}) = ({t[0]}, {t[1]})")
    def _(c, p):
        vec(p, *au, *t, V, width=3.2, dash="7 4")
        vec(p, 0, 0, *t, RESULT, width=3.6)
        tip(p, t[0] * 0.55, t[1] * 0.55, "2u - v", RESULT, dx=8, dy=16, size=18)

    @wt.step("See the span",
             "The skewed grid shows every combination with whole-number weights. Weights in between "
             "fill the gaps, so u and v reach every point. Their span is the whole plane.",
             math="span(u, v) = \\mathbb{R}^2", fresh=True)
    def _(c, p):
        with c.group(clip_path=p.clip):
            for k in range(-8, 9):
                p.c.line(*p.px(k * v[0] - 20 * u[0], k * v[1] - 20 * u[1]),
                         *p.px(k * v[0] + 20 * u[0], k * v[1] + 20 * u[1]),
                         color=theme.fill(U, "60"), width=1.3)
                p.c.line(*p.px(k * u[0] - 20 * v[0], k * u[1] - 20 * v[1]),
                         *p.px(k * u[0] + 20 * v[0], k * u[1] + 20 * v[1]),
                         color=theme.fill(V, "70"), width=1.3)
        base(p)
        vec(p, 0, 0, *au, U, width=3.2)
        vec(p, *au, *t, V, width=3.2, dash="7 4")
        vec(p, 0, 0, *t, RESULT, width=3.6)
        target(p)
        tip(p, *t, "= 2u - v", RESULT, dx=14, dy=20, anchor="start", size=16)
        for (wa, wb, name, dx, dy) in [(1, 1, "u + v", -12, -14), (-1, 0, "-u", -12, 10)]:
            q = (wa * u[0] + wb * v[0], wa * u[1] + wb * v[1])
            p.c.dot(*p.px(*q), r=4, color=theme.INK)
            tip(p, *q, name, theme.INK, dx=dx, dy=dy, size=15, anchor="end" if dx < 0 else "start")

    return wt


@diagram("dot-product-projection", "Dot Product as Projection", "Linear Algebra")
def build_dot() -> Walkthrough:
    u = (2, 4)
    v = (4, 3)
    w = (-3, 4)
    dot = u[0] * v[0] + u[1] * v[1]
    nu = math.hypot(*u)
    nv = math.hypot(*v)
    shadow = dot / nv
    proj = (shadow * v[0] / nv, shadow * v[1] / nv)
    theta = math.degrees(math.acos(dot / (nu * nv)))
    wdot = w[0] * v[0] + w[1] * v[1]
    wt = Walkthrough(
        "dot-product-projection", "Dot Product as Projection", "Linear Algebra",
        concept="u \\cdot v = u_x v_x + u_y v_y = |u| |v| cos \\theta",
        summary="The dot product multiplies the length of the shadow that u casts on v by the length of v. "
                "Perpendicular vectors cast no shadow, so their dot product is zero.",
        width=660, height=400, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(30, 24, 600, 352), x=(-3.9, 6.2), y=(-0.9, 4.9), equal=True)
        light_axes(p)
        return p

    @wt.step("Draw two vectors and the angle between them",
             "The vectors u and v share a tail at the origin. The angle θ between them controls "
             "how much u points along v.",
             math=f"u = ({u[0]}, {u[1]}), v = ({v[0]}, {v[1]}), \\theta \\approx {theta:.1f}\\deg")
    def _(c, p):
        vec(p, 0, 0, *u, U)
        vec(p, 0, 0, *v, V)
        angle_mark(c, p.px(0, 0), p.px(*v), p.px(*u), r=40, label="\\theta", color=theme.SOFT_INK, fill=False)
        tip(p, *u, f"u = ({u[0]}, {u[1]})", U, dx=-6, dy=-16, size=17)
        tip(p, *v, f"v = ({v[0]}, {v[1]})", V, dx=12, dy=-6, size=17, anchor="start")

    @wt.step("Drop a perpendicular onto v",
             "Shine light straight down onto the line through v. The dashed line from the tip of u "
             "meets that line at a right angle.",
             math="shadow foot = (" + num(round(proj[0], 3)) + ", " + num(round(proj[1], 3)) + ")")
    def _(c, p):
        p.line_through(0, 0, *v, color=theme.MUTED, width=1.2, dash="6 5")
        p.segment(*u, *proj, color=theme.SOFT_INK, width=1.8, dash="6 4")
        right_angle(c, p.px(*proj), p.px(*u), p.px(0, 0), s=12, color=theme.SOFT_INK)

    @wt.step("Measure the shadow",
             "The shadow of u on v runs from the origin to the foot of the perpendicular. "
             "Its length is |u| cos θ.",
             math=f"|u| cos \\theta = sqrt({u[0] ** 2 + u[1] ** 2}) \\cdot cos({theta:.1f}\\deg) = {num(round(shadow, 6))}")
    def _(c, p):
        A, B = offset_segment(p, (0, 0), proj, 9)
        c.line(*A, *B, color=E1, width=6)
        c.line(*p.px(*proj), *B, color=E1, width=1.2, dash="3 3")
        brace(c, B[0] + 4, B[1] + 4, A[0] + 4, A[1] + 4, label=f"shadow = {num(round(shadow, 6))}",
              color=E1, depth=12)

    @wt.step("Multiply shadow by length",
             "Scale the shadow by the length of v. The product equals the sum of the products "
             "of matching components.",
             math=f"u \\cdot v = {num(round(shadow, 6))} \\times {num(nv)} = {u[0]}\\cdot{v[0]} + {u[1]}\\cdot{v[1]} = {dot}")
    def _(c, p):
        X, Y = p.px(4.75, 1.6)
        boxed(c, X, Y, f"|v| = sqrt({v[0]}^2 + {v[1]}^2) = {num(nv)}", V)
        boxed(c, X, Y + 38, f"u \\cdot v = {num(round(shadow, 6))} \\times {num(nv)} = {dot}", RESULT)

    @wt.step("Perpendicular vectors give zero",
             "The vector w meets v at a right angle, so it casts no shadow on v. "
             "Its dot product with v is zero.",
             math=f"w \\cdot v = ({w[0]})\\cdot{v[0]} + {w[1]}\\cdot{v[1]} = {wdot}")
    def _(c, p):
        vec(p, 0, 0, *w, RESULT)
        right_angle(c, p.px(0, 0), p.px(*v), p.px(*w), s=13, color=RESULT)
        tip(p, *w, f"w = ({w[0]}, {w[1]})", RESULT, dx=10, dy=-6, anchor="start", size=17)
        tip(p, w[0] * 0.5, w[1] * 0.5, f"w \\cdot v = {wdot}", RESULT, dx=-14, dy=-6, anchor="end", size=16)

    return wt
