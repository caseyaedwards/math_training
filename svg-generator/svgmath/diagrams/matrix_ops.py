"""Matrix arithmetic: multiplication layouts and Gaussian elimination."""

from __future__ import annotations

from fractions import Fraction
from types import SimpleNamespace
from typing import List, Sequence, Tuple

from .. import theme
from ..plane import Plane
from ..registry import diagram
from ..svg import Element, math_tspans
from ..walkthrough import Walkthrough
from ._linalg import E1, E2, RESULT, U, V, band, boxed, draw_matrix, light_axes, num, tip, vec

ROW = U  # a row of the left matrix
COL = V  # a column of the right matrix

MUL_A = [[1, 0, 2], [1, 1, -1]]
MUL_B = [[2, 1], [1, 0], [1, 2]]


def matprod(A: Sequence[Sequence], B: Sequence[Sequence]) -> List[List]:
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def colored_line(c, x, y, pieces: Sequence[Tuple[str, str]], size: float = 19, anchor: str = "start"):
    """Draws one line of math whose pieces each have their own color.

    The pieces go into nested tspans of a single text element, so the browser handles the spacing.
    Spaces become no-break spaces because SVG collapses ordinary ones at tspan edges.
    """
    el = Element("text", x=x, y=y, font_size=size, fill=theme.INK, text_anchor=anchor,
                 font_family=theme.SERIF, dominant_baseline="central")
    for s_, col in pieces:
        ts = el.add(Element("tspan", fill=col))
        math_tspans(ts, s_.replace(" ", "\u00a0"))
    return c.add(el)


def paren(v) -> str:
    s = num(v)
    return f"({s})" if s.startswith("-") else s


@diagram("matrix-multiplication", "Matrix Multiplication: Row Times Column", "Linear Algebra")
def build_matmul() -> Walkthrough:
    A, B = MUL_A, MUL_B
    C = matprod(A, B)
    m, n, p_ = len(A), len(B), len(B[0])
    wt = Walkthrough(
        "matrix-multiplication", "Matrix Multiplication: Row Times Column", "Linear Algebra",
        concept="(AB)_{ij} = row i of A \\cdot column j of B",
        summary="Each entry of a product matrix is one row of the left matrix times one column of the right "
                "matrix: multiply matching entries and add.",
        width=680, height=380, level="301",
    )
    CW, CH = 44, 36
    X0, LOG_X, MID = 236, 452, 236

    @wt.setup
    def _(c):
        bx = draw_matrix(c, X0, 18, B, cw=CW, ch=CH, size=19)
        ax = draw_matrix(c, X0 - 34 - (3 * CW + 12), 164, A, cw=CW, ch=CH, size=19)
        cx = draw_matrix(c, X0, 164, [["?", "?"], ["?", "?"]], cw=CW, ch=CH, size=19, color=theme.MUTED)
        c.math(ax.x - 12, ax.cy, "A =", anchor="end", size=20)
        c.math(bx.x - 12, bx.cy, "B =", anchor="end", size=20)
        c.text(ax.cx, ax.bottom + 16, f"{m} × {n}", size=14, color=theme.SOFT_INK)
        c.text(bx.x - 34, bx.cy + 26, f"{n} × {p_}", size=14, color=theme.SOFT_INK)
        c.text(cx.cx, cx.bottom + 16, f"AB is {m} × {p_}", size=14, color=RESULT)
        c.text(LOG_X, 30, "entries so far", size=14, color=theme.SOFT_INK, anchor="start", weight="bold")
        return SimpleNamespace(A=ax, B=bx, C=cx)

    def fill_entry(c, s, i, j, new):
        x, y = s.C.cell(i, j)
        c.rect(x - CW / 2 + 2, y - CH / 2 + 2, CW - 4, CH - 4, color="none", fill=theme.PAPER, rx=5)
        if new:
            c.rect(x - CW / 2 + 2, y - CH / 2 + 2, CW - 4, CH - 4, color="none", fill=theme.fill(RESULT, "40"), rx=5)
        c.math(x, y, num(C[i][j]), size=19, color=RESULT, weight="bold" if new else None)

    def entry_step(i, j):
        terms = [(A[i][k], B[k][j]) for k in range(n)]
        expr = " + ".join(f"{paren(a)}\\cdot{paren(b)}" for a, b in terms)

        def draw(c, s):
            if c.is_new:
                band(c, s.A.row_band(i), ROW)
                band(c, s.B.col_band(j), COL)
                ax, ay = s.A.cell(i, n - 1)
                tx, ty = s.C.cell(i, j)
                c.line(s.A.right + 4, ay, s.C.x - 4, ty, color=ROW, width=1.6, dash="5 4")
                bx_, by_ = s.B.cell(n - 1, j)
                c.line(bx_, s.B.bottom + 4, tx, s.C.y - 4, color=COL, width=1.6, dash="5 4")
                pieces = []
                for k, (a, b) in enumerate(terms):
                    if k:
                        pieces.append((" + ", theme.INK))
                    pieces += [(paren(a), ROW), (" \\cdot ", theme.INK), (paren(b), COL)]
                pieces.append((f" = {num(C[i][j])}", RESULT))
                colored_line(c, MID, 318, pieces, size=21, anchor="middle")
                c.text(MID, 288, f"row {i + 1} of A times column {j + 1} of B", size=14, color=theme.SOFT_INK)
            fill_entry(c, s, i, j, c.is_new)
            k = i * p_ + j
            c.math(LOG_X, 60 + 30 * k, f"c_{{{i + 1}{j + 1}}} = {expr} = {num(C[i][j])}", anchor="start", size=15,
                   color=RESULT if c.is_new else theme.SOFT_INK)

        title = f"Entry ({i + 1}, {j + 1}): row {i + 1} times column {j + 1}"
        return title, expr, draw

    @wt.step("Check that the shapes fit",
             "A is 2 by 3 and B is 3 by 2. The inner sizes match (3 and 3), so the product exists. "
             "The outer sizes give its shape: 2 by 2.",
             math=f"({m} \\times {n})({n} \\times {p_}) \\to {m} \\times {p_}")
    def _(c, s):
        if c.is_new:
            c.text(MID, 300, "inner sizes match: 3 = 3", size=15, color=theme.INK)
            c.text(MID, 326, "each ? is one row times one column", size=14, color=theme.SOFT_INK)

    texts = {
        (0, 0): "Slide along row 1 of A and down column 1 of B. Multiply the pairs and add them up.",
        (0, 1): "Keep row 1 and move to column 2. The zero in B wipes out the middle term.",
        (1, 0): "Drop to row 2 of A and go back to column 1. The entry lands where the row and column meet.",
        (1, 1): "The last pair: row 2 times column 2. A negative entry pulls the sum below zero.",
    }
    for i in range(m):
        for j in range(p_):
            title, expr, draw = entry_step(i, j)
            wt.step(title, texts[(i, j)], math=f"{expr} = {num(C[i][j])}")(draw)

    @wt.step("Read the product",
             "All four entries are filled in. Each one came from one row and one column. "
             "Try BA: it comes out 3 by 3, a different matrix entirely.",
             math=f"AB = [[{num(C[0][0])}, {num(C[0][1])}], [{num(C[1][0])}, {num(C[1][1])}]]")
    def _(c, s):
        if c.is_new:
            c.rect(s.C.x - 6, s.C.y - 6, s.C.w + 12, s.C.h + 12, color=RESULT, width=2.2, rx=8)
            c.text(MID, 300, "4 entries = 4 row-column pairs", size=15, color=theme.INK)
            c.text(MID, 326, "each pair: 3 products, then a sum", size=14, color=theme.SOFT_INK)

    return wt


@diagram("matrix-multiplication-columns", "Matrix Multiplication: Column Picture", "Linear Algebra")
def build_matmul_columns() -> Walkthrough:
    A, B = MUL_A, MUL_B
    C = matprod(A, B)
    cols = [(A[0][k], A[1][k]) for k in range(3)]
    colors = [E1, E2, U]
    names = ["a_1", "a_2", "a_3"]
    wt = Walkthrough(
        "matrix-multiplication-columns", "Matrix Multiplication: Column Picture", "Linear Algebra",
        concept="column j of AB = A (column j of B) = b_{1j} a_1 + b_{2j} a_2 + b_{3j} a_3",
        summary="Each column of AB is a mix of the columns of A. The matching column of B says how much "
                "of each to use.",
        width=700, height=400, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(256, 18, 410, 364), x=(-0.9, 5.8), y=(-2.0, 3.6), equal=True)
        light_axes(p)
        c.math(18, 58, "A =", anchor="start", size=19)
        ab = draw_matrix(c, 60, 24, A, cw=40, ch=30, col_colors=colors)
        for k in range(3):
            x, _ = ab.cell(0, k)
            c.math(x, ab.y - 10, names[k], size=14, color=colors[k])
        c.math(18, 178, "B =", anchor="start", size=19)
        bb = draw_matrix(c, 60, 128, B, cw=40, ch=30)
        return SimpleNamespace(p=p, A=ab, B=bb)

    def path(p, weights, faded=False):
        """Draws the tip-to-tail trip for one column of B. Yields each leg for labeling."""
        x, y = 0.0, 0.0
        with p.c.group(opacity=0.3 if faded else 1):
            for k, w in enumerate(weights):
                if w == 0:
                    continue
                nx, ny = x + w * cols[k][0], y + w * cols[k][1]
                vec(p, x, y, nx, ny, colors[k], width=3.4)
                yield k, w, ((x + nx) / 2, (y + ny) / 2)
                x, y = nx, ny
        vec(p, 0, 0, x, y, RESULT, width=3.4)

    def leg_label(p, k, w, mid, off):
        dx, dy, anc = off
        tip(p, *mid, (f"{num(w)}" if w != 1 else "") + names[k], colors[k], dx=dx, dy=dy, size=16, anchor=anc)

    def faint_columns(p):
        for k, (vx, vy) in enumerate(cols):
            vec(p, 0, 0, vx, vy, theme.MUTED, width=1.6)

    W1 = [B[k][0] for k in range(3)]
    W2 = [B[k][1] for k in range(3)]
    OFF1 = {0: (-12, -6, "end"), 1: (-10, 0, "end"), 2: (8, -14, "start")}
    OFF2 = {0: (-10, -8, "end"), 2: (14, -12, "start")}

    def landing(p, j):
        lx, ly = C[0][j], C[1][j]
        if j == 0:
            tip(p, lx, ly, f"({lx}, {ly})", RESULT, dx=12, dy=4, anchor="start", size=16)
        else:
            tip(p, lx, ly, f"({lx}, {ly})", RESULT, dx=0, dy=18, size=16)

    @wt.step("Draw the columns of A",
             "A has three columns, and each one is an arrow in the plane. "
             "Every column of the product is built from these three.",
             math="a_1 = (1, 1), a_2 = (0, 1), a_3 = (2, -1)")
    def _(c, s):
        p = s.p
        offsets = [(-14, -10), (16, -4), (10, 16)]
        for k, (vx, vy) in enumerate(cols):
            vec(p, 0, 0, vx, vy, colors[k], width=3)
            tip(p, vx, vy, names[k], colors[k], dx=offsets[k][0], dy=offsets[k][1], size=17)

    @wt.step("Mix them with column 1 of B",
             "Column 1 of B is (2, 1, 1). Take two of a₁, then one of a₂, then one of a₃, tip to tail. "
             "The trip ends at (4, 2), the first column of AB.",
             math=f"2a_1 + 1a_2 + 1a_3 = ({C[0][0]}, {C[1][0]})", fresh=True)
    def _(c, s):
        p = s.p
        band(c, s.B.col_band(0), RESULT)
        faint_columns(p)
        for k, w, mid in path(p, W1):
            leg_label(p, k, w, mid, OFF1[k])
        landing(p, 0)

    @wt.step("Mix them with column 2 of B",
             "Column 2 of B is (1, 0, 2). Take one of a₁, skip a₂ since its weight is 0, then two of a₃. "
             "The trip ends at (5, −1).",
             math=f"1a_1 + 0a_2 + 2a_3 = ({C[0][1]}, {C[1][1]})", fresh=True)
    def _(c, s):
        p = s.p
        band(c, s.B.col_band(1), RESULT)
        faint_columns(p)
        for _k in path(p, W1, faded=True):
            pass
        landing(p, 0)
        for k, w, mid in path(p, W2):
            leg_label(p, k, w, mid, OFF2[k])
        landing(p, 1)

    @wt.step("Stack the results as columns",
             "The two landing points are the two columns of AB. Row times column gives the same numbers, "
             "one entry at a time.",
             math=f"AB = [[{C[0][0]}, {C[0][1]}], [{C[1][0]}, {C[1][1]}]]", fresh=True)
    def _(c, s):
        p = s.p
        faint_columns(p)
        for w in (W1, W2):
            for _k in path(p, w, faded=True):
                pass
        landing(p, 0)
        landing(p, 1)
        tip(p, C[0][0] * 0.5, C[1][0] * 0.5, "column 1", RESULT, dx=14, dy=-14, size=14)
        tip(p, C[0][1] * 0.45, C[1][1] * 0.45, "column 2", RESULT, dx=0, dy=16, size=14)
        c.math(18, 300, "AB =", anchor="start", size=19)
        draw_matrix(c, 66, 266, C, cw=40, ch=30, color=RESULT)

    return wt


def row_op(M, target, source, factor):
    """Returns a copy of M with row target replaced by row target - factor * row source."""
    out = [list(r) for r in M]
    out[target] = [a - factor * b for a, b in zip(M[target], M[source])]
    return out


@diagram("gaussian-elimination", "Gaussian Elimination", "Linear Algebra")
def build_gauss() -> Walkthrough:
    F = Fraction
    M0 = [[F(1), F(1), F(1), F(6)], [F(2), F(1), F(-1), F(1)], [F(1), F(-1), F(2), F(5)]]
    ops = []  # (target, source, factor)
    M = M0
    states = [M0]
    for col in range(2):
        for r in range(col + 1, 3):
            f = M[r][col] / M[col][col]
            if f:
                ops.append((r, col, f))
                M = row_op(M, r, col, f)
                states.append(M)
    U_ = states[-1]
    z = U_[2][3] / U_[2][2]
    y = (U_[1][3] - U_[1][2] * z) / U_[1][1]
    x = (U_[0][3] - U_[0][1] * y - U_[0][2] * z) / U_[0][0]
    for row in M0:
        assert row[0] * x + row[1] * y + row[2] * z == row[3]
    assert len(ops) == 3

    wt = Walkthrough(
        "gaussian-elimination", "Gaussian Elimination", "Linear Algebra",
        concept="row operations: R_i \\to R_i - k R_j",
        summary="Subtract multiples of one row from another to clear out the entries below each pivot. "
                "The staircase that remains solves from the bottom up.",
        width=700, height=280, level="301",
    )
    CW, CH = 42, 34
    LX, RX, MY = 18, 420, 40

    def mat(c, X, M, fills=None, cell_color=None):
        return draw_matrix(c, X, MY, [[num(v) for v in r] for r in M], cw=CW, ch=CH, size=18, aug=3,
                           fills=fills, cell_color=cell_color)

    def op_text(t, s_, f):
        k = "" if f == 1 else f"{num(f)}"
        sign = "-" if f > 0 else "+"
        return f"R_{t + 1} \\to R_{t + 1} {sign} {k if f > 0 else num(-f)}R_{s_ + 1}"

    def equations(c, X, M, color_rows=None):
        names = ["x", "y", "z"]
        for r, row in enumerate(M):
            terms = []
            for k in range(3):
                v = row[k]
                if v == 0:
                    continue
                coef = "" if abs(v) == 1 else num(abs(v))
                sign = "-" if v < 0 else "+"
                if not terms:
                    terms.append(("-" if v < 0 else "") + coef + names[k])
                else:
                    terms.append(f" {sign} {coef}{names[k]}")
            s_ = "".join(terms) + f" = {num(row[3])}"
            col = (color_rows or {}).get(r, theme.INK)
            c.math(X, MY + 6 + (r + 0.5) * CH, s_, anchor="start", size=16, color=col)

    def arrow(c, label, sub=None):
        x1, x2 = LX + 4 * CW + 12 + 16, RX - 16
        y = MY + 6 + 1.5 * CH
        c.arrow(x1, y, x2, y, color=theme.INK, width=2)
        c.text((x1 + x2) / 2, y - 18, label, size=17, math=True, color=V, weight="bold")
        if sub:
            c.text((x1 + x2) / 2, y + 18, sub, size=13, color=theme.SOFT_INK)

    @wt.step("Write the system as an augmented matrix",
             "Each equation becomes a row: the coefficients of x, y, z, then a bar, then the right side. "
             "Same information, less ink.",
             math="x + y + z = 6, 2x + y - z = 1, x - y + 2z = 5")
    def _(c):
        equations(c, LX + 10, M0)
        x1, x2 = 210, RX - 16
        y = MY + 6 + 1.5 * CH
        c.arrow(x1, y, x2, y, color=theme.INK, width=2)
        c.text((x1 + x2) / 2, y - 16, "copy the numbers", size=13, color=theme.SOFT_INK)
        box = mat(c, RX, M0)
        for k, name in enumerate(["x", "y", "z", "rhs"]):
            cx, _ = box.cell(0, k)
            c.math(cx, MY - 10, name, size=14, color=theme.SOFT_INK)
        c.text(RX + box.w / 2, box.bottom + 40, "goal: zeros below the diagonal", size=14, color=theme.SOFT_INK)

    sub_texts = [
        "Subtract two times row 1 from row 2. The x term in row 2 disappears.",
        "Subtract row 1 from row 3. Now column 1 has zeros under its pivot.",
        "Subtract two times the new row 2 from row 3. The y term in row 3 disappears too.",
    ]

    def make_op_step(i):
        t, s_, f = ops[i]
        before, after = states[i], states[i + 1]

        def draw(c):
            fb = {(s_, k): theme.fill(ROW, "30") for k in range(4)}
            fb.update({(t, k): theme.fill(V, "30") for k in range(4)})
            mat(c, LX, before, fills=fb)
            arrow(c, op_text(t, s_, f), sub=f"subtract {num(f) + ' × ' if f != 1 else ''}row {s_ + 1}")
            fa = {(t, k): theme.fill(V, "30") for k in range(4)}
            box = mat(c, RX, after, fills=fa, cell_color={(t, s_): E1})
            zx, zy = box.cell(t, s_)
            c.circle(zx, zy, 15, color=E1, width=2.2)
            c.text(LX + 2 * CW + 6, MY + 3 * CH + 40, f"pivot row R_{s_ + 1}", size=14, color=ROW, math=True)
            c.text(RX + 2 * CW + 6, MY + 3 * CH + 40, f"new zero in R_{t + 1}", size=14, color=E1, math=True)
            # arithmetic for the changed row
            fs = "" if f == 1 else f"{num(f)}\\cdot"
            terms = [f"{num(a)} - {fs}{paren(b)}" for a, b in zip(before[t], before[s_])]
            res = [num(v) for v in after[t]]
            c.math(wt.width / 2, MY + 3 * CH + 84,
                   f"new R_{t + 1} = ({', '.join(terms[:3])} | {terms[3]}) = ({', '.join(res[:3])} | {res[3]})",
                   size=16, color=V)

        return draw

    for i in range(3):
        t, s_, f = ops[i]
        wt.step(f"Clear an entry with {['the first', 'a second', 'a third'][i]} row operation", sub_texts[i],
                math=op_text(t, s_, f), fresh=True)(make_op_step(i))

    def staircase(c):
        fills = {(r, r): theme.fill(theme.YELLOW, "88") for r in range(3)}
        box = mat(c, LX, U_, fills=fills)
        c.text(LX + 2 * CW + 6, MY + 3 * CH + 40, "pivots on the staircase", size=14, color=theme.SOFT_INK)
        x1, x2 = LX + 4 * CW + 12 + 16, RX - 40
        y = MY + 6 + 1.5 * CH
        c.arrow(x1, y, x2, y, color=theme.INK, width=2)
        c.text((x1 + x2) / 2, y - 16, "read rows as equations", size=13, color=theme.SOFT_INK)
        return box

    @wt.step("Solve the bottom row",
             "The last row now says 7z = 21, with no x or y left. Divide to get z.",
             math=f"7z = 21 \\implies z = {num(z)}", fresh=True)
    def _(c):
        staircase(c)
        equations(c, RX, U_, color_rows={2: RESULT})
        c.math(RX, MY + 3 * CH + 40, f"z = 21/7 = {num(z)}", anchor="start", size=18, color=RESULT)

    @wt.step("Substitute upward",
             "Put z = 3 into row 2 to get y, then put y and z into row 1 to get x. "
             "Each row up has only one unknown left.",
             math=f"(x, y, z) = ({num(x)}, {num(y)}, {num(z)})", fresh=True)
    def _(c):
        staircase(c)
        equations(c, RX, U_)
        lines = [
            (f"-y - 3({num(z)}) = -11 \\implies y = {num(y)}", E2),
            (f"x + {num(y)} + {num(z)} = 6 \\implies x = {num(x)}", E1),
        ]
        for k, (s_, col) in enumerate(lines):
            c.math(RX, MY + 3 * CH + 34 + 28 * k, s_, anchor="start", size=16, color=col)
        boxed(c, LX + 110, MY + 3 * CH + 96, f"(x, y, z) = ({num(x)}, {num(y)}, {num(z)})", RESULT, size=18)

    return wt


@diagram("elimination-row-picture", "Elimination in the Row Picture", "Linear Algebra")
def build_elim_rows() -> Walkthrough:
    F = Fraction
    M0 = [[F(1), F(1), F(5)], [F(2), F(-1), F(1)]]
    M1 = [M0[0], [a - 2 * b for a, b in zip(M0[1], M0[0])]]
    M2 = [M1[0], [a / M1[1][1] for a in M1[1]]]
    M3 = [[a - b for a, b in zip(M2[0], M2[1])], M2[1]]
    xs, ys = M3[0][2], M3[1][2]
    assert M3[0][:2] == [1, 0] and M3[1][:2] == [0, 1]
    wt = Walkthrough(
        "elimination-row-picture", "Elimination in the Row Picture", "Linear Algebra",
        concept="row operations turn the lines but keep the crossing point",
        summary="Each row of the system is a line. Row operations swap one line for another through the "
                "same crossing point, until the lines are simply x = 2 and y = 3.",
        width=680, height=400, level="301",
    )
    C1, C2 = V, U  # row 1 and row 2 colors

    def line(p, row, color, width=3, dash=None):
        a, b, r = row
        if b == 0:
            p.vline(float(r / a), color=color, width=width, dash=dash)
        else:
            p.plot(lambda x: float((r - a * x) / b), color=color, width=width, dash=dash)

    def eq(row):
        a, b, r = row
        parts = []
        for v, n_ in ((a, "x"), (b, "y")):
            if v == 0:
                continue
            coef = "" if abs(v) == 1 else num(abs(v))
            if parts:
                parts.append(f" {'-' if v < 0 else '+'} {coef}{n_}")
            else:
                parts.append(f"{'-' if v < 0 else ''}{coef}{n_}")
        return "".join(parts) + f" = {num(r)}"

    @wt.setup
    def _(c):
        p = Plane(c, box=(236, 20, 420, 362), x=(-1, 5.4), y=(-1.2, 6.2), equal=True)
        light_axes(p)
        return p

    def panel(c, M, label=None, changed=None):
        fills = {(changed, k): theme.fill(theme.PURPLE, "30") for k in range(3)} if changed is not None else None
        draw_matrix(c, 20, 40, [[num(v) for v in r] for r in M], cw=42, ch=32, aug=2, row_colors=[C1, C2],
                    fills=fills)
        c.math(20, 140, f"R_1:\u00a0{eq(M[0])}", anchor="start", size=16, color=C1)
        c.math(20, 168, f"R_2:\u00a0{eq(M[1])}", anchor="start", size=16, color=C2)
        if label:
            c.text(20, 210, label, size=15, color=RESULT, math=True, anchor="start")

    def crossing(p):
        X, Y = p.px(float(xs), float(ys))
        p.c.dot(X, Y, r=6, color=RESULT)
        tip(p, float(xs), float(ys), f"({num(xs)}, {num(ys)})", RESULT, dx=12, dy=-14, anchor="start", size=16)

    @wt.step("Draw each row as a line",
             "Row 1 is the orange line x + y = 5 and row 2 is the blue line 2x − y = 1. "
             "They cross at the solution.",
             math="x + y = 5, 2x - y = 1")
    def _(c, p):
        panel(c, M0)
        line(p, M0[0], C1)
        line(p, M0[1], C2)
        tip(p, 0.4, 4.6, eq(M0[0]), C1, dx=10, dy=-10, anchor="start", size=15)
        tip(p, 3.1, 5.2, eq(M0[1]), C2, dx=10, dy=0, anchor="start", size=15)
        crossing(p)

    @wt.step("Subtract two times row 1 from row 2",
             "The new row 2 has no x, so its line is flat. It still passes through the crossing point, "
             "because any point on both old lines also satisfies the new row.",
             math="R_2 \\to R_2 - 2R_1: -3y = -9", fresh=True)
    def _(c, p):
        panel(c, M1, label="R_2 \\to R_2 - 2R_1", changed=1)
        line(p, M0[1], C2, width=1.6, dash="6 5")
        line(p, M1[0], C1)
        line(p, M1[1], C2)
        tip(p, 4.3, 3, eq(M1[1]), C2, dy=-14, size=15)
        tip(p, 0.4, 4.6, eq(M1[0]), C1, dx=10, dy=-10, anchor="start", size=15)
        crossing(p)

    @wt.step("Scale row 2",
             "Divide row 2 by −3 to get y = 3. Scaling an equation does not move its line at all. "
             "The numbers just get friendlier.",
             math="R_2 \\to R_2 / (-3): y = 3", fresh=True)
    def _(c, p):
        panel(c, M2, label="R_2 \\to R_2 / (-3)", changed=1)
        line(p, M2[0], C1)
        line(p, M2[1], C2)
        tip(p, 4.3, 3, eq(M2[1]), C2, dy=-14, size=15)
        tip(p, 0.4, 4.6, eq(M2[0]), C1, dx=10, dy=-10, anchor="start", size=15)
        crossing(p)

    @wt.step("Subtract row 2 from row 1",
             "The new row 1 has no y, so its line stands straight up at x = 2. "
             "It pivots about the same crossing point.",
             math="R_1 \\to R_1 - R_2: x = 2", fresh=True)
    def _(c, p):
        panel(c, M3, label="R_1 \\to R_1 - R_2", changed=0)
        line(p, M2[0], C1, width=1.6, dash="6 5")
        line(p, M3[0], C1)
        line(p, M3[1], C2)
        tip(p, 2, 5.4, eq(M3[0]), C1, dx=10, dy=0, anchor="start", size=15)
        tip(p, 4.3, 3, eq(M3[1]), C2, dy=-14, size=15)
        crossing(p)

    @wt.step("Read off the answer",
             "The matrix is now the identity on the left, and the lines are a plain grid crossing. "
             "The right column holds the answer.",
             math=f"x = {num(xs)}, y = {num(ys)}", fresh=True)
    def _(c, p):
        panel(c, M3, label="identity on the left")
        line(p, M3[0], C1)
        line(p, M3[1], C2)
        X, Y = p.px(float(xs), float(ys))
        c.circle(X, Y, 14, color=RESULT, width=2.5)
        crossing(p)
        tip(p, 2, 5.4, eq(M3[0]), C1, dx=10, dy=0, anchor="start", size=15)
        tip(p, 4.3, 3, eq(M3[1]), C2, dy=-14, size=15)
        boxed(c, 120, 270, f"x = {num(xs)}, y = {num(ys)}", RESULT, size=18)

    return wt
