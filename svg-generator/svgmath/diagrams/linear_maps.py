"""Matrices as maps of the plane: transformations, determinants, eigenvectors, rotations."""

from __future__ import annotations

import math
from types import SimpleNamespace

from .. import theme
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._linalg import (E1, E2, RESULT, U, V, apply, band, boxed, det, draw_matrix, light_axes, matmul, num, tip,
                      vec, warped_grid)

SQUARE = theme.fill(theme.YELLOW, "88")
PANEL_X = 22


def panel_matrix(c, A, name="A", y=46, x=PANEL_X, cw=40):
    """Draws 'name =' and the 2x2 matrix A with green and red columns."""
    c.math(x, y + 36, f"{name} =", anchor="start", size=19)
    return draw_matrix(c, x + 46, y, [[num(A[0][0]), num(A[0][1])], [num(A[1][0]), num(A[1][1])]],
                       cw=cw, ch=30, col_colors=[E1, E2])


def note(c, y, s, color=theme.INK, size=16, x=PANEL_X):
    """Writes one line of math in the left panel."""
    c.math(x, y, s, anchor="start", size=size, color=color)


def unit_square(p, color=SQUARE):
    p.polygon([(0, 0), (1, 0), (1, 1), (0, 1)], color="none", fill=color)


def basis(p, M=None, width=3.4, labels=True, dash=None, l1="e_1", l2="e_2", o1=(0, -14), o2=(16, 0), at=0.5):
    """Draws the images of e1 and e2 under M (identity when M is None)."""
    M = M or ((1, 0), (0, 1))
    a = (M[0][0], M[1][0])
    b = (M[0][1], M[1][1])
    vec(p, 0, 0, *a, E1, width=width, dash=dash)
    vec(p, 0, 0, *b, E2, width=width, dash=dash)
    if labels:
        tip(p, a[0] * at, a[1] * at, l1, E1, dx=o1[0], dy=o1[1])
        tip(p, b[0] * at, b[1] * at, l2, E2, dx=o2[0], dy=o2[1])


def para(p, M, fill=theme.fill(RESULT, "33"), outline=RESULT):
    a = apply(M, 1, 0)
    b = apply(M, 0, 1)
    p.polygon([(0, 0), a, (a[0] + b[0], a[1] + b[1]), b], color=outline, fill=fill, width=1.6)


@diagram("matrix-transformation", "Matrix as a Linear Transformation", "Linear Algebra")
def build_transformation() -> Walkthrough:
    A = ((2, 1), (0, 1))
    x = (1, 2)
    Ax = apply(A, *x)
    c1, c2 = apply(A, 1, 0), apply(A, 0, 1)
    wt = Walkthrough(
        "matrix-transformation", "Matrix as a Linear Transformation", "Linear Algebra",
        concept="A x = x_1 (first column) + x_2 (second column)",
        summary="A 2 by 2 matrix moves every point of the plane. The columns tell you where the two basis "
                "vectors land, and the rest of the grid follows along.",
        width=680, height=400, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(190, 22, 440, 356), x=(-1.2, 5.4), y=(-1.1, 3.4), equal=True)
        light_axes(p)
        return SimpleNamespace(p=p, box=panel_matrix(c, A))

    def img_arrows(p):
        vec(p, 0, 0, *c1, E1, width=3.6)
        vec(p, 0, 0, *c2, E2, width=3.6)
        tip(p, c1[0] * 0.75, c1[1] * 0.75, "A e_1", E1, dx=0, dy=16, size=16)
        tip(p, *c2, "A e_2", E2, dx=6, dy=-14, size=16, anchor="start")

    @wt.step("Start with the grid and the basis vectors",
             "The basis vectors e₁ and e₂ are one step along each axis. "
             "They outline the yellow unit square.",
             math="e_1 = (1, 0), e_2 = (0, 1)")
    def _(c, s):
        p = s.p
        unit_square(p)
        basis(p)
        note(c, 150, "e_1 = (1, 0)", E1)
        note(c, 178, "e_2 = (0, 1)", E2)

    @wt.step("Send e₁ to the first column",
             "Read the first column of A: e₁ lands on (2, 0). The matrix stretches it to twice its length.",
             math=f"A e_1 = ({num(c1[0])}, {num(c1[1])})")
    def _(c, s):
        p = s.p
        if c.is_new:
            band(c, s.box.col_band(0), E1)
        vec(p, 0, 0, *c1, E1, width=3.6)
        tip(p, c1[0] * 0.75, c1[1] * 0.75, "A e_1", E1, dx=0, dy=16, size=16)
        note(c, 220, f"A e_1 = ({num(c1[0])}, {num(c1[1])})", E1)

    @wt.step("Send e₂ to the second column",
             "The second column says e₂ lands on (1, 1). It leans over to the right.",
             math=f"A e_2 = ({num(c2[0])}, {num(c2[1])})")
    def _(c, s):
        p = s.p
        if c.is_new:
            band(c, s.box.col_band(1), E2)
        vec(p, 0, 0, *c2, E2, width=3.6)
        tip(p, *c2, "A e_2", E2, dx=6, dy=-14, size=16, anchor="start")
        note(c, 248, f"A e_2 = ({num(c2[0])}, {num(c2[1])})", E2)

    def moved_grid(c, p):
        warped_grid(p, A, color=theme.fill(theme.SKY, "cc"), width=1.4)
        para(p, A)
        unit_square(p, color=theme.fill(theme.YELLOW, "55"))
        basis(p, labels=False, width=2, dash="5 4")
        img_arrows(p)
        note(c, 150, "e_1 = (1, 0)", E1)
        note(c, 178, "e_2 = (0, 1)", E2)
        note(c, 220, f"A e_1 = ({num(c1[0])}, {num(c1[1])})", E1)
        note(c, 248, f"A e_2 = ({num(c2[0])}, {num(c2[1])})", E2)
        X, Y = p.px(1.5, 0.5)
        c.text(X, Y, "area 2", size=13, color=RESULT, halo=True)

    @wt.step("Carry the whole grid along",
             "Every grid line follows the basis vectors. Lines stay straight, parallel, and evenly spaced, "
             "and the origin stays put. The unit square becomes a parallelogram.",
             math="square \\to parallelogram with sides (2, 0) and (1, 1)", fresh=True)
    def _(c, s):
        p = s.p
        moved_grid(c, p)

    @wt.step("Transform any vector with the columns",
             "The vector (1, 2) means one e₁ plus two e₂. After the map it is one first column plus "
             "two second columns. No grid paper needed.",
             math=f"A({x[0]}, {x[1]}) = {x[0]}({num(c1[0])}, {num(c1[1])}) + {x[1]}({num(c2[0])}, {num(c2[1])})"
                  f" = ({num(Ax[0])}, {num(Ax[1])})", fresh=True)
    def _(c, s):
        p = s.p
        moved_grid(c, p)
        vec(p, 0, 0, *x, U, width=2.6, dash="6 4")
        tip(p, *x, f"x = ({x[0]}, {x[1]})", U, dx=10, dy=-6, anchor="start", size=15)
        vec(p, *c1, c1[0] + c2[0], c1[1] + c2[1], E2, width=2.6)
        vec(p, c1[0] + c2[0], c1[1] + c2[1], *Ax, E2, width=2.6)
        vec(p, 0, 0, *Ax, RESULT, width=3.8)
        tip(p, *Ax, f"A x = ({num(Ax[0])}, {num(Ax[1])})", RESULT, dx=12, dy=-8, size=16, anchor="start")
        note(c, 290, f"A x = ({num(Ax[0])}, {num(Ax[1])})", RESULT)

    return wt


def orientation_arc(p, M, r=0.55, color=theme.INK, label=None, label_at=None):
    """Draws an arrow arc from the image of e1 toward the image of e2 near the origin."""
    a = apply(M, 1, 0)
    b = apply(M, 0, 1)
    d0 = math.degrees(math.atan2(a[1], a[0]))
    d1 = math.degrees(math.atan2(b[1], b[0]))
    sweep = (d1 - d0 + 540) % 360 - 180  # shortest signed turn
    X, Y = p.px(0, 0)
    p.c.arc(X, Y, p.length(r), d0 + 0.12 * sweep, d0 + 0.88 * sweep, color=color, width=2.2, arrow=True)
    if label:
        if label_at is None:
            mid = math.radians(d0 + sweep / 2)
            label_at = ((r + 0.45) * math.cos(mid), (r + 0.45) * math.sin(mid))
        tip(p, *label_at, label, color, dy=0, size=14)
    return sweep


@diagram("determinant-area", "Determinant as Area Scale Factor", "Linear Algebra")
def build_determinant() -> Walkthrough:
    A = ((3, 1), (1, 2))
    F = ((1, 3), (2, 1))  # columns swapped
    Z = ((2, 1), (2, 1))  # dependent columns
    dA, dF, dZ = det(A), det(F), det(Z)
    wt = Walkthrough(
        "determinant-area", "Determinant as Area Scale Factor", "Linear Algebra",
        concept="det [[a, b], [c, d]] = ad - bc = area scale factor",
        summary="The determinant says how much a matrix scales area. Its sign says whether the map keeps "
                "or flips orientation, and zero means the plane gets squashed flat.",
        width=680, height=400, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(200, 22, 440, 356), x=(-0.9, 4.9), y=(-0.8, 4.3), equal=True)
        light_axes(p)
        return p

    def matrix_panel(c, M, name, d, color):
        box = panel_matrix(c, M, name=name)
        note(c, box.bottom + 30, "det = ad - bc", theme.INK, size=16)
        note(c, box.bottom + 60, f"= {num(M[0][0])}\\cdot{num(M[1][1])} - {num(M[0][1])}\\cdot{num(M[1][0])} = {num(d)}",
             color, size=17)
        return box

    @wt.step("Start with the unit square",
             "The square with sides e₁ and e₂ has area 1. Watch what the matrix does to it.",
             math="area = 1")
    def _(c, p):
        unit_square(p)
        basis(p)
        tip(p, 0.62, 0.62, "area 1", theme.INK, dy=0, size=14)
        if c.is_new:
            note(c, 70, "area before = 1", theme.INK)

    @wt.step("Apply the matrix",
             "The columns (3, 1) and (1, 2) are where e₁ and e₂ land. "
             "The unit square becomes the purple parallelogram they span.",
             math=f"det A = 3\\cdot2 - 1\\cdot1 = {num(dA)}", fresh=True)
    def _(c, p):
        unit_square(p)
        para(p, A)
        basis(p, A, l1="(3, 1)", l2="(1, 2)", o1=(16, 14), o2=(-30, -8), at=1)
        orientation_arc(p, A, r=1.0, color=theme.INK, label="counterclockwise", label_at=(1.85, 1.3))
        X, Y = p.px(2.3, 1.75)
        c.text(X, Y, f"area {num(dA)}", size=16, color=RESULT, weight="bold", halo=True)
        matrix_panel(c, A, "A", dA, RESULT)

    @wt.step("Every area scales by the same factor",
             "The whole grid moves with the matrix. Each unit square turns into a copy of the "
             "parallelogram, so every shape grows by a factor of five.",
             math=f"new area = {num(dA)} \\times old area", fresh=True)
    def _(c, p):
        warped_grid(p, A, color=theme.fill(theme.SKY, "cc"), width=1.4)
        unit_square(p)
        para(p, A)
        basis(p, A, labels=False)
        for (i, j) in [(0, 0), (0, 1), (1, -1)]:
            cx, cy = apply(A, i + 0.5, j + 0.5)
            if p.contains(cx, cy):
                tip(p, cx, cy, f"area {num(dA)}", RESULT, dy=0, size=15)
        matrix_panel(c, A, "A", dA, RESULT)

    @wt.step("Swap the columns and flip the sign",
             "Swapping the columns makes the same parallelogram, but e₁ and e₂ trade places. "
             "The turn from the first column to the second now runs clockwise, like a mirror image.",
             math=f"det = 1\\cdot1 - 3\\cdot2 = {num(dF)}", fresh=True)
    def _(c, p):
        unit_square(p)
        para(p, F, fill=theme.fill(theme.RED, "22"), outline=theme.RED)
        basis(p, F, l1="(1, 2)", l2="(3, 1)", o1=(-30, -8), o2=(16, 14), at=1)
        orientation_arc(p, F, r=1.0, color=theme.INK, label="clockwise", label_at=(1.75, 1.3))
        box = matrix_panel(c, F, "B", dF, theme.RED)
        note(c, box.bottom + 100, "area 5, flipped", theme.RED, size=15)

    @wt.step("A zero determinant squashes the plane",
             "When the columns point along the same line, the square collapses onto that line. "
             "Its area is 0, and no matrix can undo the squash.",
             math=f"det = 2\\cdot1 - 1\\cdot2 = {num(dZ)}", fresh=True)
    def _(c, p):
        unit_square(p)
        p.line_through(0, 0, 1, 1, color=theme.MUTED, width=1.4, dash="6 5")
        p.segment(0, 0, 3, 3, color=RESULT, width=7, stroke_opacity=0.35)
        vec(p, 0, 0, 2, 2, E1, width=3.4)
        vec(p, 0, 0, 1, 1, E2, width=3.4)
        tip(p, 2, 2, "(2, 2)", E1, dx=12, dy=4, anchor="start", size=15)
        tip(p, 1, 1, "(1, 1)", E2, dx=-12, dy=-6, anchor="end", size=15)
        tip(p, 3, 3, "flat, area 0", RESULT, dx=12, dy=0, anchor="start", size=15)
        matrix_panel(c, Z, "C", dZ, RESULT)

    return wt


@diagram("determinant-formula", "Why the Determinant Is ad − bc", "Linear Algebra")
def build_det_formula() -> Walkthrough:
    a, c_, b, d = 3, 1, 1, 2  # columns (a, c) and (b, d)
    W, H = a + b, c_ + d
    box_area = W * H
    tri_ac = a * c_ / 2
    tri_bd = b * d / 2
    rect_bc = b * c_
    area = box_area - 2 * tri_ac - 2 * tri_bd - 2 * rect_bc
    assert abs(area - (a * d - b * c_)) < 1e-9
    wt = Walkthrough(
        "determinant-formula", "Why the Determinant Is ad − bc", "Linear Algebra",
        concept="(a + b)(c + d) - ac - bd - 2bc = ad - bc",
        summary="Put the parallelogram in a box and cut away the corners. What is left has area ad − bc, "
                "which is the determinant.",
        width=680, height=400, level="301",
    )
    pieces = {
        "ac": [[(0, 0), (a, 0), (a, c_)], [(b, d), (a + b, c_ + d), (b, c_ + d)]],
        "bd": [[(0, 0), (b, d), (0, d)], [(a, c_), (a + b, c_ + d), (a + b, c_)]],
        "bc": [[(a, 0), (a + b, 0), (a + b, c_), (a, c_)], [(0, d), (b, d), (b, c_ + d), (0, c_ + d)]],
    }
    colors = {"ac": U, "bd": theme.ORANGE, "bc": theme.SOFT_INK}
    areas = {"ac": tri_ac, "bd": tri_bd, "bc": rect_bc}

    def centroid(pts):
        return (sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts))

    @wt.setup
    def _(c):
        p = Plane(c, box=(200, 22, 450, 340), x=(-0.7, 4.6), y=(-0.9, 3.5), equal=True)
        p.grid(step=1)
        p.axes(step=1, ystep=1, labels=False)
        panel_matrix(c, ((a, b), (c_, d)))
        return p

    def shade(p, key):
        for pts in pieces[key]:
            p.polygon(pts, color=colors[key], fill=theme.fill(colors[key], "40"), width=1.4)
            tip(p, *centroid(pts), num(areas[key]), colors[key], dy=0, size=15)

    def tally(c, k):
        lines = [
            (f"box = {W} \\times {H} = {box_area}", theme.INK),
            (f"- 2 \\times {num(tri_ac)} = - {num(2 * tri_ac)}", U),
            (f"- 2 \\times {num(tri_bd)} = - {num(2 * tri_bd)}", theme.ORANGE),
            (f"- 2 \\times {num(rect_bc)} = - {num(2 * rect_bc)}", theme.SOFT_INK),
        ]
        for i, (s, col) in enumerate(lines[:k]):
            note(c, 150 + 28 * i, s, col, size=16)

    @wt.step("Put the parallelogram in a box",
             "The columns (3, 1) and (1, 2) span the purple parallelogram. "
             "The smallest box around it is four wide and three tall.",
             math=f"box = (a + b)(c + d) = {W} \\times {H} = {box_area}")
    def _(c, p):
        p.rect(0, 0, W, H, color=theme.SOFT_INK, width=1.6, dash="6 4")
        para(p, ((a, b), (c_, d)))
        basis(p, ((a, b), (c_, d)), labels=False)
        tip(p, a, c_, f"({a}, {c_})", E1, dx=14, dy=12, anchor="start", size=15)
        tip(p, b, d, f"({b}, {d})", E2, dx=12, dy=4, anchor="start", size=15)
        bx = p.Y(0) + 22
        for x0, x1, s in [(0, a, f"a = {a}"), (a, W, f"b = {b}")]:
            c.line(p.X(x0) + 2, bx, p.X(x1) - 2, bx, color=theme.SOFT_INK, width=1.2)
            c.text((p.X(x0) + p.X(x1)) / 2, bx + 14, s, size=14, color=theme.SOFT_INK, math=True)
        lx = p.X(0) - 18
        for y0, y1, s in [(0, d, f"d = {d}"), (d, H, f"c = {c_}")]:
            c.line(lx, p.Y(y0) - 2, lx, p.Y(y1) + 2, color=theme.SOFT_INK, width=1.2)
            c.text(lx - 6, (p.Y(y0) + p.Y(y1)) / 2, s, size=14, color=theme.SOFT_INK, math=True, anchor="end")
        tally(c, 1 if c.is_new else 0)

    @wt.step("Cut off the two blue triangles",
             "Each blue triangle has legs a = 3 and c = 1, so its area is ac/2.",
             math=f"2 \\times ac/2 = ac = {num(2 * tri_ac)}")
    def _(c, p):
        shade(p, "ac")
        if c.is_new:
            tally(c, 2)

    @wt.step("Cut off the two orange triangles",
             "Each orange triangle has legs b = 1 and d = 2, so its area is bd/2.",
             math=f"2 \\times bd/2 = bd = {num(2 * tri_bd)}")
    def _(c, p):
        shade(p, "bd")
        if c.is_new:
            tally(c, 3)

    @wt.step("Cut off the two corner rectangles",
             "Two small rectangles, each b by c, fill the last corners.",
             math=f"2 \\times bc = {num(2 * rect_bc)}")
    def _(c, p):
        shade(p, "bc")
        if c.is_new:
            tally(c, 4)

    @wt.step("Subtract to get the determinant",
             "Take the corners away from the box. The algebra cancels to ad − bc, "
             "the same number the formula gives. No magic, just bookkeeping.",
             math=f"{box_area} - {num(2 * tri_ac)} - {num(2 * tri_bd)} - {num(2 * rect_bc)} = {num(area)}"
                  f" = {a}\\cdot{d} - {b}\\cdot{c_}")
    def _(c, p):
        tally(c, 4)
        c.line(PANEL_X, 258, PANEL_X + 160, 258, color=theme.INK, width=1.2)
        note(c, 280, f"area = {num(area)} = ad - bc", RESULT, size=17)
        X, Y = p.px(W / 2, H / 2)
        c.text(X, Y, num(area), size=22, weight="bold", color=RESULT, halo=True)

    return wt


EIG_A = ((3, 1), (0, 2))


@diagram("eigenvectors", "Eigenvectors", "Linear Algebra")
def build_eigenvectors() -> Walkthrough:
    A = EIG_A
    x = (1, 1)
    Ax = apply(A, *x)
    v1, l1 = (1, 0), 3
    v2, l2 = (1, -1), 2
    Av1, Av2 = apply(A, *v1), apply(A, *v2)
    assert Av1 == (l1 * v1[0], l1 * v1[1]) and Av2 == (l2 * v2[0], l2 * v2[1])
    wt = Walkthrough(
        "eigenvectors", "Eigenvectors", "Linear Algebra",
        concept="A v = \\lambda v",
        summary="Most vectors change direction when a matrix acts on them. Eigenvectors stay on their own "
                "line and only stretch, by a factor called the eigenvalue.",
        width=680, height=400, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(196, 20, 446, 356), x=(-3.4, 5.4), y=(-2.9, 2.9), equal=True)
        light_axes(p)
        draw_matrix_named(c, A)
        return p

    def eig_line(p, v, color):
        with p.c.group(opacity=0.3):
            p.line_through(0, 0, *v, color=color, width=9)

    @wt.step("Most vectors get knocked off their line",
             "Take x = (1, 1). The matrix sends it to (4, 2), which is not on the dashed line through x. "
             "The direction changed.",
             math=f"A(1, 1) = ({num(Ax[0])}, {num(Ax[1])})")
    def _(c, p):
        p.line_through(0, 0, *x, color=U, width=1.2, dash="6 5")
        vec(p, 0, 0, *x, U, width=3)
        vec(p, 0, 0, *Ax, theme.MUTED, width=3)
        tip(p, *x, "x", U, dx=-10, dy=-12)
        tip(p, *Ax, f"A x = ({num(Ax[0])}, {num(Ax[1])})", theme.SOFT_INK, dx=14, dy=18, size=15)
        X1, Y1 = p.px(*x)
        X2, Y2 = p.px(*Ax)
        c.curved_arrow(X1 + 8, Y1 - 6, X2 - 14, Y2 - 8, bend=0.25, color=theme.MUTED, width=1.4, dash="4 3")
        note(c, 150, f"A(1, 1) = ({num(Ax[0])}, {num(Ax[1])})", theme.SOFT_INK)
        note(c, 174, "off its line", theme.SOFT_INK, size=14)

    @wt.step("Find a direction that stays put",
             "The vector (1, 0) lands on (3, 0). It stays on the x-axis and just gets three times longer. "
             "That makes it an eigenvector with eigenvalue 3.",
             math=f"A(1, 0) = ({num(Av1[0])}, {num(Av1[1])}) = {l1}(1, 0)")
    def _(c, p):
        eig_line(p, v1, E1)
        vec(p, 0, 0, *Av1, E1, width=6)
        vec(p, 0, 0, *v1, theme.INK, width=2.4)
        tip(p, *Av1, f"\\lambda = {l1}", E1, dx=0, dy=-18, size=17)
        note(c, 214, f"A(1, 0) = {l1}(1, 0)", E1)

    @wt.step("Find the second direction",
             "The vector (1, −1) lands on (2, −2). Same line, twice as long. "
             "That is a second eigenvector, with eigenvalue 2.",
             math=f"A(1, -1) = ({num(Av2[0])}, {num(Av2[1])}) = {l2}(1, -1)")
    def _(c, p):
        eig_line(p, v2, E2)
        vec(p, 0, 0, *Av2, E2, width=6)
        vec(p, 0, 0, *v2, theme.INK, width=2.4)
        tip(p, *Av2, f"\\lambda = {l2}", E2, dx=14, dy=4, size=17, anchor="start")
        note(c, 242, f"A(1, -1) = {l2}(1, -1)", E2)

    @wt.step("The whole line comes along",
             "Any multiple of an eigenvector is also an eigenvector. The vector (−1, 1) goes to (−2, 2), "
             "and (−1, 0) goes to (−3, 0). Both lines map onto themselves.",
             math="A(-1, 1) = (-2, 2), A(-1, 0) = (-3, 0)")
    def _(c, p):
        for v, col in [((-1, 0), E1), ((-1, 1), E2)]:
            Av = apply(A, *v)
            vec(p, 0, 0, *Av, col, width=6)
            vec(p, 0, 0, *v, theme.INK, width=2.4)
            tip(p, *Av, f"({num(Av[0])}, {num(Av[1])})", col, dx=0, dy=-16, size=15)

    @wt.step("Get the eigenvalues from a determinant",
             "Av = λv means (A − λI)v = 0 for a nonzero v, so A − λI must squash the plane. "
             "Its determinant is zero, and that pins down λ.",
             math="det(A - \\lambda I) = (3 - \\lambda)(2 - \\lambda) = 0 \\implies \\lambda = 3 or 2")
    def _(c, p):
        note(c, 290, "(3 - \\lambda)(2 - \\lambda) = 0", theme.INK)
        note(c, 318, "\\lambda = 3", E1, size=17)
        note(c, 318, "\\lambda = 2", E2, size=17, x=PANEL_X + 80)

    return wt


def draw_matrix_named(c, A, name="A"):
    """Draws 'A =' and the matrix in plain ink, for diagrams where the columns carry no color."""
    c.math(PANEL_X, 46 + 36, f"{name} =", anchor="start", size=19)
    return draw_matrix(c, PANEL_X + 46, 46, [[num(A[0][0]), num(A[0][1])], [num(A[1][0]), num(A[1][1])]],
                       cw=40, ch=30)


@diagram("eigenvector-fan", "Eigenvectors in a Fan of Arrows", "Linear Algebra")
def build_eigen_fan() -> Walkthrough:
    A = EIG_A
    n = 16
    angles = [2 * math.pi * k / n for k in range(n)]

    def is_eig(t, lam):
        ux, uy = math.cos(t), math.sin(t)
        ax, ay = apply(A, ux, uy)
        return abs(ax - lam * ux) < 1e-9 and abs(ay - lam * uy) < 1e-9

    eig3 = [t for t in angles if is_eig(t, 3)]
    eig2 = [t for t in angles if is_eig(t, 2)]
    wt = Walkthrough(
        "eigenvector-fan", "Eigenvectors in a Fan of Arrows", "Linear Algebra",
        concept="A v = \\lambda v for only a few directions",
        summary="Draw arrows in every direction, apply the matrix, and compare. Almost every arrow swings "
                "to a new direction. Only the eigenvectors keep theirs.",
        width=680, height=400, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(196, 16, 446, 368), x=(-3.7, 3.7), y=(-2.8, 2.8), equal=True)
        p.grid(step=1)
        p.axes(step=1, ystep=1, labels=False, xlabel="", ylabel="")
        draw_matrix_named(c, A)
        return p

    @wt.step("Draw arrows in every direction",
             "Sixteen arrows of length 1 point all the way around the unit circle.",
             math="v = (cos t, sin t)")
    def _(c, p):
        p.circle(0, 0, 1, color=theme.MUTED, width=1.4)
        for t in angles:
            vec(p, 0, 0, math.cos(t), math.sin(t), theme.SOFT_INK, width=1.8)
        note(c, 150, "16 unit arrows", theme.SOFT_INK, size=15)

    @wt.step("Apply the matrix to every arrow",
             "Each arrow goes to A times itself. The tips now trace an ellipse, and most arrows "
             "swing to a new angle. The thin lines connect each arrow to its image.",
             math="v \\to A v")
    def _(c, p):
        p.parametric(lambda t: apply(A, math.cos(t), math.sin(t))[0],
                     lambda t: apply(A, math.cos(t), math.sin(t))[1], 0, 2 * math.pi,
                     color=theme.fill(RESULT, "88"), width=1.6)
        for t in angles:
            ux, uy = math.cos(t), math.sin(t)
            ax, ay = apply(A, ux, uy)
            p.segment(ux, uy, ax, ay, color=theme.MUTED, width=1, dash="2 3")
            vec(p, 0, 0, ax, ay, theme.fill(RESULT, "aa"), width=1.8)
        note(c, 178, "images A v", RESULT, size=15)
        note(c, 202, "tips form an ellipse", RESULT, size=15)

    @wt.step("Spot the arrows that stay on their line",
             "Along the x-axis the image lies right on top of the arrow, three times as long. "
             "Those arrows are eigenvectors with λ = 3.",
             math="A(\\pm 1, 0) = 3(\\pm 1, 0)")
    def _(c, p):
        for t in eig3:
            ux, uy = math.cos(t), math.sin(t)
            vec(p, 0, 0, 3 * ux, 3 * uy, E1, width=4.5)
            vec(p, 0, 0, ux, uy, theme.INK, width=2.4)
        tip(p, 3, 0, "\\lambda = 3", E1, dx=0, dy=-18, size=17)
        tip(p, -3, 0, "\\lambda = 3", E1, dx=0, dy=-18, size=17)
        note(c, 242, "\\lambda = 3: along (1, 0)", E1, size=15)

    @wt.step("Spot the second pair",
             "Along the diagonal through (1, −1) the image is twice as long and still on the same line. "
             "Every other arrow turns, which is why eigenvectors are special.",
             math="A(1, -1) = 2(1, -1)")
    def _(c, p):
        for t in eig2:
            ux, uy = math.cos(t), math.sin(t)
            vec(p, 0, 0, 2 * ux, 2 * uy, E2, width=4.5)
            vec(p, 0, 0, ux, uy, theme.INK, width=2.4)
        tip(p, math.sqrt(2), -math.sqrt(2), "\\lambda = 2", E2, dx=14, dy=6, size=17, anchor="start")
        tip(p, -math.sqrt(2), math.sqrt(2), "\\lambda = 2", E2, dx=-14, dy=-6, size=17, anchor="end")
        note(c, 270, "\\lambda = 2: along (1, -1)", E2, size=15)

    return wt


@diagram("rotation-matrix", "Rotation Matrix", "Linear Algebra")
def build_rotation() -> Walkthrough:
    deg = 30
    t = math.radians(deg)
    ct, st = math.cos(t), math.sin(t)
    R = ((ct, -st), (st, ct))
    r1, r2 = apply(R, 1, 0), apply(R, 0, 1)
    f = lambda v: f"{v:.3f}".rstrip("0").rstrip(".")
    wt = Walkthrough(
        "rotation-matrix", "Rotation Matrix", "Linear Algebra",
        concept="R(\\theta) = [[cos \\theta, -sin \\theta], [sin \\theta, cos \\theta]]",
        summary="To rotate the plane by an angle, track where e₁ and e₂ go on the unit circle. "
                "Those two landing points are the columns of the rotation matrix.",
        width=680, height=400, level="301",
    )

    def matrix_state(c, k):
        """Draws R with column 1 known when k >= 1 and column 2 known when k >= 2."""
        rows = [["cos \\theta" if k >= 1 else "?", "-sin \\theta" if k >= 2 else "?"],
                ["sin \\theta" if k >= 1 else "?", "cos \\theta" if k >= 2 else "?"]]
        fills = {(r, q): theme.PAPER for r in range(2) for q in range(2)}
        c.math(14, 46 + 36, "R =", anchor="start", size=19)
        return draw_matrix(c, 54, 46, rows, cw=64, ch=30, size=16, col_colors=[E1, E2], fills=fills)

    @wt.setup
    def _(c):
        p = Plane(c, box=(196, 18, 446, 360), x=(-1.45, 1.65), y=(-1.15, 1.5), equal=True)
        p.grid(step=0.5)
        p.axes(step=0.5, ystep=0.5, labels=False)
        a = math.radians(225)
        tip(p, math.cos(a), math.sin(a), "radius 1", theme.SOFT_INK, dx=-8, dy=10, size=13, anchor="end")
        p.circle(0, 0, 1, color=theme.MUTED, width=1.6)
        return p

    @wt.step("Start with the unit circle",
             "The basis vectors e₁ and e₂ both sit on the circle of radius 1. Rotate everything by "
             "θ = 30° counterclockwise.",
             math=f"\\theta = {deg}\\deg")
    def _(c, p):
        if c.is_new:
            matrix_state(c, 0)
        vec(p, 0, 0, 1, 0, E1, width=3)
        vec(p, 0, 0, 0, 1, E2, width=3)
        tip(p, 1, 0, "e_1", E1, dx=-4, dy=16)
        tip(p, 0, 1, "e_2", E2, dx=16, dy=12)
        note(c, 150, f"\\theta = {deg}\\deg", theme.INK)

    @wt.step("Rotate e₁",
             "The tip of e₁ slides 30° along the circle. Its new x is cos θ and its new y is sin θ, "
             "the legs of the dashed triangle.",
             math=f"R e_1 = (cos \\theta, sin \\theta) = ({f(r1[0])}, {f(r1[1])})")
    def _(c, p):
        if c.is_new:
            matrix_state(c, 1)
        X, Y = p.px(0, 0)
        c.arc(X, Y, p.length(1), 2, deg - 2, color=E1, width=2, arrow=True, dash="4 3")
        c.arc(X, Y, p.length(0.28), 0, deg, color=E1, width=1.8)
        tip(p, 0.38 * math.cos(t / 2), 0.38 * math.sin(t / 2), "\\theta", E1, dy=0, size=15)
        p.segment(r1[0], 0, *r1, color=E1, width=1.6, dash="5 4")
        p.segment(0, -0.004, r1[0], -0.004, color=E1, width=4)
        tip(p, r1[0] / 2, 0, "cos \\theta", E1, dy=16, size=14)
        tip(p, r1[0], r1[1] * 0.3, "sin \\theta", E1, dx=-6, dy=0, size=14, anchor="end")
        vec(p, 0, 0, *r1, E1, width=3.6)
        tip(p, *r1, "R e_1", E1, dx=10, dy=-14, anchor="start")
        note(c, 178, f"R e_1 = ({f(r1[0])}, {f(r1[1])})", E1)

    @wt.step("Rotate e₂",
             "The tip of e₂ slides 30° too, which moves it left. Its new x is −sin θ and its new y "
             "is cos θ.",
             math=f"R e_2 = (-sin \\theta, cos \\theta) = ({f(r2[0])}, {f(r2[1])})")
    def _(c, p):
        if c.is_new:
            matrix_state(c, 2)
        X, Y = p.px(0, 0)
        c.arc(X, Y, p.length(1), 92, 90 + deg - 2, color=E2, width=2, arrow=True, dash="4 3")
        c.arc(X, Y, p.length(0.28), 90, 90 + deg, color=E2, width=1.8)
        tip(p, 0.4 * math.cos(math.pi / 2 + t / 2), 0.4 * math.sin(math.pi / 2 + t / 2), "\\theta", E2, dy=0,
            size=15)
        p.segment(r2[0], 0, *r2, color=E2, width=1.6, dash="5 4")
        p.segment(0, r2[1], *r2, color=E2, width=1.6, dash="5 4")
        tip(p, r2[0] / 2, r2[1], "-sin \\theta", E2, dy=14, size=14)
        tip(p, r2[0], r2[1] / 2, "cos \\theta", E2, dx=-8, dy=0, size=14, anchor="end")
        vec(p, 0, 0, *r2, E2, width=3.6)
        tip(p, *r2, "R e_2", E2, dx=-12, dy=-12, anchor="end")
        note(c, 206, f"R e_2 = ({f(r2[0])}, {f(r2[1])})", E2)

    @wt.step("Write the landing points as columns",
             "The first column is where e₁ lands and the second column is where e₂ lands. "
             "That is the whole rotation matrix.",
             math=f"R(30\\deg) = [[{f(R[0][0])}, {f(R[0][1])}], [{f(R[1][0])}, {f(R[1][1])}]]")
    def _(c, p):
        matrix_state(c, 2)
        if c.is_new:
            band(c, (54 + 6 - 3, 46 + 3, 64 - 2 + 3, 66), E1)
            band(c, (54 + 6 + 64 - 1, 46 + 3, 64 + 1, 66), E2)
        draw_matrix(c, 54, 240, [[f(R[0][0]), f(R[0][1])], [f(R[1][0]), f(R[1][1])]], cw=64, ch=30, size=16,
                    col_colors=[E1, E2])
        c.math(14, 240 + 36, "=", anchor="start", size=19)

    @wt.step("Rotate a shape",
             "Every point turns by 30° about the origin. The yellow square keeps its size and its "
             "right angles, so the determinant is 1. A rotation never squashes anything.",
             math="det R = cos^2 \\theta + sin^2 \\theta = 1")
    def _(c, p):
        sq = [(0, 0), (1, 0), (1, 1), (0, 1)]
        p.polygon([(0.5 * x, 0.5 * y) for x, y in sq], color=theme.ORANGE, fill=SQUARE, width=1.4)
        p.polygon([apply(R, 0.5 * x, 0.5 * y) for x, y in sq], color=RESULT,
                  fill=theme.fill(RESULT, "40"), width=1.6)
        X, Y = p.px(0, 0)
        corner = apply(R, 0.5, 0.5)
        r = math.hypot(*corner)
        c.arc(X, Y, p.length(r), 47, 45 + deg - 2, color=RESULT, width=1.8, arrow=True)
        note(c, 330, "det R = 1", RESULT)

    return wt


@diagram("transformation-composition", "Composing Transformations", "Linear Algebra")
def build_composition() -> Walkthrough:
    S = ((1, 1), (0, 1))  # shear
    R = ((0, -1), (1, 0))  # quarter turn
    RS = matmul(R, S)  # shear first, then rotate
    SR = matmul(S, R)  # rotate first, then shear
    wt = Walkthrough(
        "transformation-composition", "Composing Transformations", "Linear Algebra",
        concept="(R S) x = R(S x), and R S \\neq S R",
        summary="Doing one map after another multiplies their matrices, with the first map on the right. "
                "Shear then rotate lands somewhere different from rotate then shear, so order matters.",
        width=720, height=430, level="301",
    )
    PW, GAP, X0 = 150, 56, 14
    ROWS = (44, 252)
    cols = [X0 + i * (PW + GAP) for i in range(3)]
    RX = cols[2] + PW + 22

    def mini(c, i, row):
        p = Plane(c, box=(cols[i], ROWS[row], PW, PW), x=(-1.6, 2.4), y=(-0.9, 2.4), equal=True)
        p.grid(step=1, color=theme.GRID)
        p.segment(-1.6, 0, 2.4, 0, color=theme.MUTED, width=1.2)
        p.segment(0, -0.9, 0, 2.4, color=theme.MUTED, width=1.2)
        c.rect(cols[i], ROWS[row], PW, PW, color=theme.GRID, width=1)
        return p

    def shape(p, M, label=None):
        a, b = apply(M, 1, 0), apply(M, 0, 1)
        p.polygon([(0, 0), a, (a[0] + b[0], a[1] + b[1]), b], color=RESULT, fill=theme.fill(RESULT, "33"),
                  width=1.4)
        vec(p, 0, 0, *a, E1, width=2.6)
        vec(p, 0, 0, *b, E2, width=2.6)

    def step_arrow(c, i, row, name):
        y = ROWS[row] + PW / 2
        x1, x2 = cols[i] + PW + 6, cols[i + 1] - 6
        c.arrow(x1, y, x2, y, color=theme.INK, width=2)
        c.text((x1 + x2) / 2, y - 14, name, size=17, math=True, weight="bold")
        M = S if name == "S" else R
        draw_matrix(c, (x1 + x2) / 2 - 25, y + 10, [[num(M[0][0]), num(M[0][1])], [num(M[1][0]), num(M[1][1])]],
                    cw=19, ch=19, size=13, pad=3, col_colors=[E1, E2])

    def result(c, row, M, name):
        y = ROWS[row] + 30
        c.math(RX, y - 16, f"{name} =", anchor="start", size=17)
        draw_matrix(c, RX + 8, y + 2, [[num(M[0][0]), num(M[0][1])], [num(M[1][0]), num(M[1][1])]],
                    cw=34, ch=28, size=17, col_colors=[E1, E2])

    @wt.setup
    def _(c):
        c.text(X0, 24, "Shear first, then rotate", size=15, weight="bold", anchor="start", color=theme.INK)
        c.text(X0, 232, "Rotate first, then shear", size=15, weight="bold", anchor="start", color=theme.INK)
        c.text(X0 + 220, 24, "S = shear", anchor="start", size=13, color=theme.SOFT_INK)
        c.text(X0 + 310, 24, "R = quarter turn counterclockwise", anchor="start", size=13, color=theme.SOFT_INK)
        return None

    @wt.step("Start with the same square twice",
             "Both rows begin with the unit square, e₁ in green and e₂ in red. "
             "S is a shear that pushes the top to the right. R turns the plane a quarter turn.",
             math="S = [[1, 1], [0, 1]], R = [[0, -1], [1, 0]]")
    def _(c):
        for row in (0, 1):
            p = mini(c, 0, row)
            shape(p, ((1, 0), (0, 1)))

    @wt.step("Top row: shear",
             "The shear keeps e₁ fixed and slides e₂ over to (1, 1). The square leans right.",
             math="S e_1 = (1, 0), S e_2 = (1, 1)")
    def _(c):
        step_arrow(c, 0, 0, "S")
        shape(mini(c, 1, 0), S)

    @wt.step("Top row: then rotate",
             "Turn the leaning shape a quarter turn. The combined map is R times S, "
             "with the first map written on the right.",
             math=f"R S = [[{num(RS[0][0])}, {num(RS[0][1])}], [{num(RS[1][0])}, {num(RS[1][1])}]]")
    def _(c):
        step_arrow(c, 1, 0, "R")
        shape(mini(c, 2, 0), RS)
        result(c, 0, RS, "RS")

    @wt.step("Bottom row: rotate",
             "Now rotate the square first. It turns into the second quadrant and stays a square.",
             math="R e_1 = (0, 1), R e_2 = (-1, 0)")
    def _(c):
        step_arrow(c, 0, 1, "R")
        shape(mini(c, 1, 1), R)

    @wt.step("Bottom row: then shear",
             "Shear the turned square. The combined map is S times R.",
             math=f"S R = [[{num(SR[0][0])}, {num(SR[0][1])}], [{num(SR[1][0])}, {num(SR[1][1])}]]")
    def _(c):
        step_arrow(c, 1, 1, "S")
        shape(mini(c, 2, 1), SR)
        result(c, 1, SR, "SR")

    @wt.step("Compare the results",
             "The two final shapes point different ways, and the two matrices differ. "
             "Matrix multiplication is not commutative, much like socks and shoes.",
             math="R S \\neq S R")
    def _(c):
        y = (ROWS[0] + PW + ROWS[1]) / 2 + 6
        c.text(RX + 45, y, "≠", size=34, color=theme.RED, weight="bold")
        for row, other in ((0, SR), (1, RS)):
            p = Plane(c, box=(cols[2], ROWS[row], PW, PW), x=(-1.6, 2.4), y=(-0.9, 2.4), equal=True)
            a, b = apply(other, 1, 0), apply(other, 0, 1)
            p.polygon([(0, 0), a, (a[0] + b[0], a[1] + b[1]), b], color=theme.SOFT_INK, width=1.4, dash="4 3")
        c.text(cols[2] + PW / 2, ROWS[0] + PW + 14, "dashed: the other order", size=12, color=theme.SOFT_INK)

    return wt


@diagram("column-row-picture", "Solving Ax = b: Row and Column Pictures", "Linear Algebra")
def build_column_row() -> Walkthrough:
    A = ((2, -1), (1, 1))
    b = (1, 5)
    dA = det(A)
    sol = ((b[0] * A[1][1] - A[0][1] * b[1]) / dA, (A[0][0] * b[1] - A[1][0] * b[0]) / dA)
    xs, ys = sol
    a1, a2 = (A[0][0], A[1][0]), (A[0][1], A[1][1])
    s1 = (xs * a1[0], xs * a1[1])
    assert apply(A, xs, ys) == (b[0], b[1])
    wt = Walkthrough(
        "column-row-picture", "Solving Ax = b: Row and Column Pictures", "Linear Algebra",
        concept="2x - y = 1, x + y = 5: x (2, 1) + y (-1, 1) = (1, 5)",
        summary="The row picture draws each equation as a line and finds where they cross. "
                "The column picture asks how much of each column it takes to reach b. Both give the same answer.",
        width=720, height=400, level="301",
    )

    @wt.setup
    def _(c):
        left = Plane(c, box=(16, 54, 322, 336), x=(-1.2, 5.2), y=(-1, 6), equal=True)
        right = Plane(c, box=(374, 54, 306, 336), x=(-2.2, 5.2), y=(-1, 6), equal=True)
        for p in (left, right):
            light_axes(p)
        c.text(left.left + left.w / 2, 16, "Row picture: lines in the (x, y) plane", size=14, weight="bold")
        c.text(right.left + right.w / 2, 16, "Column picture: combine the columns", size=14, weight="bold")
        c.line(360, 30, 360, 390, color=theme.GRID, width=1.2)
        return SimpleNamespace(L=left, R=right)

    @wt.step("Draw the first equation as a line",
             "Every point on the blue line solves 2x − y = 1. One equation alone has endless solutions.",
             math="2x - y = 1")
    def _(c, s):
        p = s.L
        p.plot(lambda x: 2 * x - 1, color=U, width=3)
        tip(p, 0.95, 2 * 0.95 - 1, "2x - y = 1", U, dx=40, dy=8, size=15)

    @wt.step("Add the second line",
             "The orange line holds every solution of x + y = 5. The one point on both lines solves the system.",
             math=f"x = {num(xs)}, y = {num(ys)}")
    def _(c, s):
        p = s.L
        p.plot(lambda x: 5 - x, color=V, width=3)
        tip(p, 4.2, 0.8, "x + y = 5", V, dx=-10, dy=16, size=15, anchor="end")
        X, Y = p.px(xs, ys)
        c.dot(X, Y, r=6, color=RESULT)
        tip(p, xs, ys, f"({num(xs)}, {num(ys)})", RESULT, dx=-12, dy=-4, anchor="end", size=16)

    @wt.step("Switch to the column picture",
             "Read the matrix by columns instead. The question becomes: how many copies of each column "
             "add up to b = (1, 5)?",
             math="x (2, 1) + y (-1, 1) = (1, 5)")
    def _(c, s):
        p = s.R
        vec(p, 0, 0, *a1, E1, width=3)
        vec(p, 0, 0, *a2, E2, width=3)
        tip(p, *a1, f"a_1 = ({a1[0]}, {a1[1]})", E1, dx=8, dy=12, anchor="start", size=15)
        tip(p, *a2, f"a_2 = ({a2[0]}, {a2[1]})", E2, dx=-6, dy=-12, anchor="end", size=15)
        X, Y = p.px(*b)
        c.circle(X, Y, 9, color=theme.INK, width=2)
        c.dot(X, Y, r=3, color=theme.INK)
        tip(p, *b, f"b = ({b[0]}, {b[1]})", theme.INK, dx=0, dy=-20, size=15)

    @wt.step("Combine the columns",
             "Take two of the first column, then three of the second, tip to tail. The path ends exactly on b.",
             math=f"{num(xs)}(2, 1) + {num(ys)}(-1, 1) = ({num(s1[0])}, {num(s1[1])}) + "
                  f"({num(ys * a2[0])}, {num(ys * a2[1])}) = (1, 5)")
    def _(c, s):
        p = s.R
        vec(p, 0, 0, *s1, E1, width=4)
        vec(p, *s1, *b, E2, width=4)
        tip(p, s1[0] * 0.75, s1[1] * 0.75, f"{num(xs)}a_1", E1, dx=-10, dy=-12, size=16, anchor="end")
        tip(p, (s1[0] + b[0]) / 2, (s1[1] + b[1]) / 2, f"{num(ys)}a_2", E2, dx=14, dy=-4, anchor="start",
            size=16)

    @wt.step("Match the two pictures",
             "The crossing point on the left and the weights on the right are the same pair of numbers. "
             "Two pictures, one answer.",
             math=f"(x, y) = ({num(xs)}, {num(ys)})")
    def _(c, s):
        X, Y = s.L.px(xs, ys)
        c.circle(X, Y, 14, color=RESULT, width=2.5)
        boxed(c, s.L.X(4.0), s.L.Y(3.9), f"x = {num(xs)}, y = {num(ys)}", RESULT, size=16)
        boxed(c, s.R.X(3.6), s.R.Y(4.7), f"weights {num(xs)} and {num(ys)}", RESULT, size=16)

    return wt
