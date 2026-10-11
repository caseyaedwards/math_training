"""Area models for algebra: algebra tiles, FOIL, difference of squares, completing the square."""

from __future__ import annotations

from .. import theme
from ..annotate import brace
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._algebra_helpers import colored_math, tile

AB = ("a", "b")  # drawn as two pieces so both letters stay italic
SQ_COL = theme.BLUE
X_COL = theme.GREEN
ONE_COL = theme.ORANGE

# ---------------------------------------------------------------------------
# Algebra tiles
# ---------------------------------------------------------------------------


@diagram("algebra-tiles", "Factoring with Algebra Tiles", "Algebra")
def build_tiles() -> Walkthrough:
    wt = Walkthrough(
        "algebra-tiles", "Factoring with Algebra Tiles", "Algebra",
        concept="x^2 + 5x + 6 = (x + 2)(x + 3)",
        summary="Factoring means arranging the tiles of a polynomial into one rectangle. The sides of that "
                "rectangle are the factors.",
        width=680, height=400, level="201",
    )
    X, U, G = 100, 32, 6  # pixel length of x, of 1, and the gap between pool tiles
    p_, q_ = 2, 3  # rows of ones and columns of ones: p + q = 5, p * q = 6
    n_x, n_1 = p_ + q_, p_ * q_
    OX, OY = 110, 120  # rectangle origin
    SQ = (356, 70)
    bars = [(474 + i * (U + G), 70) for i in range(n_x)]
    units = [(356 + i * (U + G), 220) for i in range(n_1)]

    def ghost(c, x, y, w, h, col):
        c.rect(x, y, w, h, color="none", fill=theme.PAPER)
        tile(c, x, y, w, h, col, dashed=True)

    @wt.setup
    def _(c):
        return None

    @wt.step("Lay out the tiles", f"A big square is x by x, a bar is x by 1, and a small square is 1 by 1. "
             f"The polynomial asks for one big square, {n_x} bars, and {n_1} small squares.",
             math=f"x^2 + {n_x}x + {n_1}")
    def _(c):
        c.text(510, 44, "the pieces", size=14, color=theme.SOFT_INK, weight="bold")
        if c.is_new:
            c.rect(OX - 20, OY - 20, 240, 220, color=theme.MUTED, dash="6 5", width=1.5, rx=8)
            c.text(OX + 100, OY + 90, "goal: one rectangle,", size=14, color=theme.SOFT_INK)
            c.text(OX + 100, OY + 110, "no gaps, no overlaps", size=14, color=theme.SOFT_INK)
        tile(c, *SQ, X, X, SQ_COL, "x^2", size=22)
        for bx, by in bars:
            tile(c, bx, by, U, X, X_COL, "x")
        for ux, uy in units:
            tile(c, ux, uy, U, U, ONE_COL, "1", size=15)
        c.text(SQ[0] + X / 2, 190, "1 big square", size=13, color=SQ_COL)
        c.text(bars[0][0] + (n_x * (U + G) - G) / 2, 190, f"{n_x} bars", size=13, color=X_COL)
        c.text(units[0][0] + (n_1 * (U + G) - G) / 2, 272, f"{n_1} small squares", size=13, color=ONE_COL)

    @wt.step("Place the square and split the bars", f"Put x² in the corner. Split the {n_x} bars into "
             f"{q_} on the right and {p_} below, because {p_} + {q_} = {n_x} and {p_} × {q_} = {n_1}.",
             math=f"{p_} + {q_} = {n_x},   {p_} \\cdot {q_} = {n_1}")
    def _(c):
        ghost(c, *SQ, X, X, SQ_COL)
        for bx, by in bars:
            ghost(c, bx, by, U, X, X_COL)
        tile(c, OX, OY, X, X, SQ_COL, "x^2", size=22)
        for i in range(q_):
            tile(c, OX + X + i * U, OY, U, X, X_COL, "x")
        for j in range(p_):
            tile(c, OX, OY + X + j * U, X, U, X_COL, "x")
        # side markings: x and 1s along the top and left
        c.math(OX + X / 2, OY - 14, "x", size=17, color=SQ_COL)
        for i in range(q_):
            c.text(OX + X + i * U + U / 2, OY - 14, "1", size=14, color=ONE_COL)
        c.math(OX - 14, OY + X / 2, "x", size=17, color=SQ_COL)
        for j in range(p_):
            c.text(OX - 14, OY + X + j * U + U / 2, "1", size=14, color=ONE_COL)

    @wt.step("Fill the corner with the ones", f"The empty corner is {p_} by {q_}, which holds exactly "
             f"{n_1} small squares. No tile is left over and no gap remains, so the tiles make a rectangle.",
             math=f"{p_} \\times {q_} = {n_1} ones")
    def _(c):
        for ux, uy in units:
            ghost(c, ux, uy, U, U, ONE_COL)
        for j in range(p_):
            for i in range(q_):
                tile(c, OX + X + i * U, OY + X + j * U, U, U, ONE_COL, "1", size=14)
        c.text(510, 330, "pool empty: every tile used", size=14, color=theme.SOFT_INK)

    @wt.step("Read the length and the width", f"The top edge is x + {q_} and the left edge is x + {p_}. "
             "Area equals length times width, so those two sides are the factors.",
             math=f"x^2 + {n_x}x + {n_1} = (x + {p_})(x + {q_})")
    def _(c):
        W, H = X + q_ * U, X + p_ * U
        brace(c, OX, OY - 30, OX + W, OY - 30, f"x + {q_}", color=theme.INK, size=18)
        brace(c, OX - 30, OY + H, OX - 30, OY, f"x + {p_}", color=theme.INK, size=18)
        c.rect(OX, OY, W, H, color=theme.INK, width=3)

    return wt


# ---------------------------------------------------------------------------
# FOIL as area
# ---------------------------------------------------------------------------


def _boxed_product(c, ox, oy, cols, rows, cells, tags=None):
    """Draws a grid of rectangles. cols, rows: [(pixel size, label, color)]. cells[r][k]: (label, color)."""
    y = oy
    for r, (h, _, _) in enumerate(rows):
        x = ox
        for k, (w, _, _) in enumerate(cols):
            lab, col = cells[r][k]
            c.rect(x, y, w, h, color=col, fill=theme.fill(col, "33"), width=2)
            pieces = lab if isinstance(lab, tuple) else (lab,)
            colored_math(c, x + w / 2, y + h / 2, [(t, col) for t in pieces], size=22 if min(w, h) > 60 else 18)
            if tags:
                c.text(x + 10, y + 12, tags[r][k], size=13, color=col, weight="bold", anchor="start")
            x += w
        y += h


def _side_labels(c, ox, oy, cols, rows):
    x = ox
    for w, lab, col in cols:
        c.line(x + 3, oy - 10, x + w - 3, oy - 10, color=col, width=3)
        c.math(x + w / 2, oy - 28, lab, size=20, color=col)
        x += w
    y = oy
    for h, lab, col in rows:
        c.line(ox - 10, y + 3, ox - 10, y + h - 3, color=col, width=3)
        c.math(ox - 30, y + h / 2, lab, size=20, color=col)
        y += h


@diagram("binomial-area-model", "Multiplying Binomials as Area (FOIL)", "Algebra")
def build_foil() -> Walkthrough:
    wt = Walkthrough(
        "binomial-area-model", "Multiplying Binomials as Area (FOIL)", "Algebra",
        concept="(x + 3)(x + 2) = x^2 + 5x + 6,   (a + b)^2 = a^2 + 2ab + b^2",
        summary="A product of two sums is the area of a rectangle cut into four boxes. FOIL is a checklist "
                "for visiting each box once.",
        width=680, height=400, level="201",
    )
    XP, UP = 150, 40
    m, n = 3, 2
    cols = [(XP, "x", SQ_COL), (m * UP, f"{m}", ONE_COL)]
    rows = [(XP, "x", SQ_COL), (n * UP, f"{n}", theme.PURPLE)]
    OX, OY = 90, 70
    cells = [[("x^2", SQ_COL), (f"{m}x", ONE_COL)], [(f"{n}x", theme.PURPLE), (f"{m * n}", X_COL)]]
    tags = [["F", "I"], ["O", "L"]]
    W, H = XP + m * UP, XP + n * UP
    LX = 410  # left edge of the list on the right

    @wt.setup
    def _(c):
        return None

    @wt.step("Draw a rectangle with sides x + 3 and x + 2", "The top edge is x plus 3 and the left edge is "
             "x plus 2. Their product is the area of this rectangle.", math=f"area = (x + {m})(x + {n})")
    def _(c):
        c.rect(OX, OY, W, H, color=theme.INK, width=2.5)
        _side_labels(c, OX, OY, cols, rows)

    @wt.step("Cut it into four boxes", "Slice where x ends on each side. Each box pairs one piece of the top "
             "with one piece of the left.", math="4 boxes = 2 pieces \\times 2 pieces")
    def _(c):
        _boxed_product(c, OX, OY, cols, rows, cells)

    @wt.step("Name each box with FOIL", "First, Outer, Inner, Last: each letter visits one box. "
             "Every box gets counted once, and none gets counted twice.",
             math=f"x \\cdot x,   x \\cdot {n},   {m} \\cdot x,   {m} \\cdot {n}")
    def _(c):
        _boxed_product(c, OX, OY, cols, rows, cells, tags)
        lines = [("F", "First", "x \\cdot x", "x^2", SQ_COL), ("O", "Outer", f"x \\cdot {n}", f"{n}x", theme.PURPLE),
                 ("I", "Inner", f"{m} \\cdot x", f"{m}x", ONE_COL), ("L", "Last", f"{m} \\cdot {n}", f"{m * n}", X_COL)]
        colored_math(c, LX + 120, 60, [("(", theme.INK), ("x", SQ_COL), (f" + {m}", ONE_COL), (")(", theme.INK),
                                        ("x", SQ_COL), (f" + {n}", theme.PURPLE), (")", theme.INK)], size=22)
        for i, (t, name, prod, res, col) in enumerate(lines):
            y = 110 + i * 40
            c.text(LX, y, t, size=17, color=col, weight="bold", anchor="start")
            c.text(LX + 22, y, name, size=14, color=theme.SOFT_INK, anchor="start")
            c.math(LX + 85, y, f"{prod} = {res}", size=19, color=col, anchor="start")

    @wt.step("Add the four areas", f"The two bar-shaped boxes are both x-terms, so they combine: "
             f"{n}x + {m}x = {m + n}x.", math=f"(x + {m})(x + {n}) = x^2 + {m + n}x + {m * n}")
    def _(c):
        c.line(LX, 268, LX + 240, 268, color=theme.INK, width=1.5)
        colored_math(c, LX + 120, 292, [("x^2", SQ_COL), (f" + {n}x", theme.PURPLE), (f" + {m}x", ONE_COL),
                                        (f" + {m * n}", X_COL)], size=20)
        colored_math(c, LX + 120, 330, [("= x^2", SQ_COL), (f" + {m + n}x", theme.INK), (f" + {m * n}", X_COL)],
                     size=22)

    A, B = 190, 90

    @wt.step("Use the same picture for (a + b)²", "A square with side a + b splits the same way: one a² box, "
             "one b² box, and two a-by-b boxes.", math="(a + b)^2 = a^2 + ab + ab + b^2", fresh=True)
    def _(c):
        sc = [(A, "a", SQ_COL), (B, "b", ONE_COL)]
        _side_labels(c, OX, OY, sc, sc)
        _boxed_product(c, OX, OY, sc, sc, [[("a^2", SQ_COL), (AB, theme.PURPLE)],
                                           [(AB, theme.PURPLE), ("b^2", ONE_COL)]])
        colored_math(c, LX + 120, 120, [("(a + b)^2", theme.INK)], size=24)
        colored_math(c, LX + 120, 170, [("= a^2", SQ_COL), (" + 2a", theme.PURPLE), ("b", theme.PURPLE), (" + b^2", ONE_COL)], size=24)

    @wt.step("Do not lose the 2ab", "The classic slip writes (a + b)² as a² + b². The picture shows two "
             "whole rectangles that this slip throws away.",
             math="(a + b)^2 \\neq a^2 + b^2")
    def _(c):
        for x, y, w, h in ((OX + A, OY, B, A), (OX, OY + A, A, B)):
            c.rect(x, y, w, h, color=theme.RED, width=4)
        c.label_box(LX + 120, 240, "a^2 + b^2 misses these", size=17, color=theme.RED, border=theme.RED,
                    math=True)
        c.arrow(LX + 10, 252, OX + A + B / 2 + 14, OY + A / 2 + 30, color=theme.RED, width=1.8)
        c.arrow(LX + 10, 252, OX + A / 2 + 30, OY + A + B / 2, color=theme.RED, width=1.8)

    return wt


@diagram("difference-of-squares", "Difference of Squares as Area", "Algebra")
def build_dos() -> Walkthrough:
    wt = Walkthrough(
        "difference-of-squares", "Difference of Squares as Area", "Algebra",
        concept="a^2 - b^2 = (a + b)(a - b)",
        summary="Cut a small square out of a big one, then slide one leftover strip to the end. The L-shape "
                "becomes a rectangle with sides a + b and a − b.",
        width=680, height=320, level="201",
    )
    a, b = 7, 3
    U = 30
    OX, OY = 90, 60

    def P(x, y):
        return OX + x * U, OY + y * U

    def unit_grid(c, x0, y0, w, h):
        for i in range(1, w):
            c.line(OX + (x0 + i) * U, OY + y0 * U, OX + (x0 + i) * U, OY + (y0 + h) * U, color=theme.GRID, width=1)
        for j in range(1, h):
            c.line(OX + x0 * U, OY + (y0 + j) * U, OX + (x0 + w) * U, OY + (y0 + j) * U, color=theme.GRID, width=1)

    def piece(c, x0, y0, w, h, col, label, dashed=False):
        if dashed:
            c.rect(*P(x0, y0), w * U, h * U, color=col, dash="6 4", width=2)
        else:
            c.rect(*P(x0, y0), w * U, h * U, color="none", fill=theme.fill(col, "33"))
            unit_grid(c, x0, y0, w, h)
            c.rect(*P(x0, y0), w * U, h * U, color=col, width=2.2)
        if label:
            X0, Y0 = P(x0 + w / 2, y0 + h / 2)
            c.math(X0, Y0, label, size=18, color=col, halo=True)

    rows = [
        [(f"a^2 = {a * a}", SQ_COL)],
        [(f"{a * a}", SQ_COL), (f" - {b * b}", theme.RED), (f" = {a * a - b * b}", theme.INK)],
        [(f"{a * (a - b)}", SQ_COL), (f" + {(a - b) * b}", ONE_COL), (f" = {a * a - b * b}", theme.INK)],
        [("same 40, new shape", theme.SOFT_INK)],
        [(f"{a + b} \\times {a - b} = {(a + b) * (a - b)}", theme.GREEN)],
    ]

    def ledger(c, upto, only=None):
        for i in (range(upto + 1) if only is None else [only]):
            colored_math(c, 505, 80 + i * 40, rows[i], size=19, anchor="start")

    @wt.setup
    def _(c):
        c.text(505, 46, "counting squares", size=13, color=theme.SOFT_INK, weight="bold", anchor="start")
        return None

    @wt.step("Start with a square of side a", f"Take a = {a}. The square holds {a}² = {a * a} unit squares.",
             math=f"a^2 = {a}^2 = {a * a}")
    def _(c):
        piece(c, 0, 0, a, a, SQ_COL, f"a^2 = {a * a}")
        c.math(OX + a * U / 2, OY - 16, f"a = {a}", size=18, color=SQ_COL)
        c.math(OX - 12, OY + a * U / 2, f"a = {a}", size=18, color=SQ_COL, anchor="end")
        ledger(c, 0)

    @wt.step("Cut out a b-by-b corner", f"Remove a corner square with b = {b}. That takes away "
             f"{b}² = {b * b}, leaving an L-shape.", math=f"a^2 - b^2 = {a * a} - {b * b} = {a * a - b * b}")
    def _(c):
        X0, Y0 = P(a - b, a - b)
        c.rect(X0, Y0, b * U, b * U, color="none", fill=theme.PAPER)
        piece(c, a - b, a - b, b, b, theme.RED, f"b^2 = {b * b}", dashed=True)
        c.math(OX + (a - b / 2) * U, OY + a * U + 18, f"b = {b}", size=16, color=theme.RED)
        ledger(c, 1, only=1)

    @wt.step("Cut the L into two strips", f"The top strip is {a} by {a - b}. The bottom-left piece is "
             f"{a - b} by {b}. Together they still hold {a * a - b * b} squares.",
             math=f"{a} \\cdot {a - b} + {a - b} \\cdot {b} = {a * (a - b)} + {(a - b) * b} = {a * a - b * b}",
             fresh=True)
    def _(c):
        piece(c, 0, 0, a, a - b, SQ_COL, f"{a} \\times {a - b}")
        piece(c, 0, a - b, a - b, b, ONE_COL, f"{a - b} \\times {b}")
        piece(c, a - b, a - b, b, b, theme.RED, "", dashed=True)
        c.text(OX + (a - b / 2) * U, OY + (a - b / 2) * U, "gone", size=14, color=theme.RED)
        ledger(c, 2)

    @wt.step("Turn one strip and slide it to the end", f"Stand the {a - b}-by-{b} piece on its end and "
             f"attach it to the right of the top strip. Its {a - b}-long side matches the strip's height.",
             math=f"{a - b} \\times {b}  \\to  {b} \\times {a - b}", fresh=True)
    def _(c):
        piece(c, 0, 0, a, a - b, SQ_COL, f"{a} \\times {a - b}")
        if c.is_new:
            piece(c, 0, a - b, a - b, b, ONE_COL, "", dashed=True)
        piece(c, a, 0, b, a - b, ONE_COL, f"{b} \\times {a - b}")
        ledger(c, 3)
        if c.is_new:
            x1, y1 = P(a - b, a - b / 2)
            x2, y2 = P(a + b / 2, a - b)
            c.curved_arrow(x1 + 6, y1, x2, y2 + 8, bend=0.35, color=ONE_COL, width=2.2)
            c.text(x2 + 10, y1 + 10, "turn and slide", size=13, color=ONE_COL, anchor="start")

    @wt.step("Read the rectangle", f"The new rectangle is a + b = {a + b} long and a − b = {a - b} tall. "
             f"Its area is {a + b} × {a - b} = {(a + b) * (a - b)}, the same as {a * a} − {b * b}.",
             math=f"a^2 - b^2 = (a + b)(a - b):   {a * a} - {b * b} = {a + b} \\cdot {a - b} = {(a + b) * (a - b)}")
    def _(c):
        L, T = P(0, 0)
        R, Bm = P(a + b, a - b)
        brace(c, L, T - 8, R, T - 8, f"a + b = {a + b}", color=theme.INK, size=17)
        brace(c, R + 8, T, R + 8, Bm, f"a - b = {a - b}", color=theme.INK, size=17)
        c.rect(L, T, R - L, Bm - T, color=theme.INK, width=3)
        ledger(c, 4, only=4)

    return wt


# ---------------------------------------------------------------------------
# Completing the square
# ---------------------------------------------------------------------------


@diagram("completing-the-square", "Completing the Square", "Algebra")
def build_cts() -> Walkthrough:
    wt = Walkthrough(
        "completing-the-square", "Completing the Square", "Algebra",
        concept="x^2 + 6x = 16 \\implies (x + 3)^2 = 25 \\implies x = 2",
        summary="Draw x² + 6x as a square plus a strip, split the strip in half, and wrap it around the square. "
                "One small corner is missing; add it to both sides and you have a perfect square.",
        width=680, height=400, level="201",
    )
    b, rhs = 6, 16
    h = b // 2
    U = 40  # pixels per unit
    xv = 2  # drawn to scale with the positive solution
    XS = xv * U
    OX, OY = 110, 90
    corner = h * h
    total = rhs + corner
    side = int(round(total ** 0.5))
    assert xv * xv + b * xv == rhs and side - h == xv
    LX = 470

    def ledger(c, i, parts):
        colored_math(c, LX, 110 + i * 46, parts, size=19, anchor="start")

    @wt.setup
    def _(c):
        c.text(LX, 70, "the equation so far", size=13, color=theme.SOFT_INK, weight="bold", anchor="start")
        return None

    @wt.step("Draw x² + 6x as area", f"An x-by-x square plus an x-by-{b} strip. Together they cover "
             f"{rhs} square units.", math=f"x^2 + {b}x = {rhs}")
    def _(c):
        tile(c, OX, OY, XS, XS, SQ_COL, "x^2", size=20, label_color=SQ_COL)
        c.rect(OX + XS, OY, b * U, XS, color=X_COL, fill=theme.fill(X_COL, "33"), width=2)
        c.math(OX + XS / 2, OY - 14, "x", size=17, color=SQ_COL)
        c.math(OX - 14, OY + XS / 2, "x", size=17, color=SQ_COL)
        if c.is_new:  # step 2 relabels the strip as two halves
            c.math(OX + XS + b * U / 2, OY + XS / 2, f"{b}x", size=20, color=X_COL)
            c.math(OX + XS + b * U / 2, OY - 14, f"{b}", size=17, color=X_COL)
        ledger(c, 0, [("x^2", SQ_COL), (f" + {b}x", X_COL), (f" = {rhs}", theme.INK)])

    @wt.step("Cut the strip in half", f"Split the {b}x strip into two strips of {h}x each.",
             math=f"{b}x = {h}x + {h}x")
    def _(c):
        c.line(OX + XS + h * U, OY - 4, OX + XS + h * U, OY + XS + 4, color=theme.INK, width=2, dash="6 4")
        for k in range(2):
            c.math(OX + XS + (k + 0.5) * h * U, OY + XS / 2, f"{h}x", size=20, color=X_COL)
        for k in range(2):
            c.math(OX + XS + (k + 0.5) * h * U, OY - 14, f"{h}", size=17, color=X_COL)
        ledger(c, 1, [("x^2", SQ_COL), (f" + {h}x + {h}x", X_COL), (f" = {rhs}", theme.INK)])

    @wt.step("Wrap one half under the square", f"Move the right half below the square and turn it. "
             "Now the square has a strip on its right and a strip underneath.",
             math=f"x^2 + {h}x + {h}x = {rhs}", fresh=True)
    def _(c):
        tile(c, OX, OY, XS, XS, SQ_COL, "x^2", size=20)
        c.rect(OX + XS, OY, h * U, XS, color=X_COL, fill=theme.fill(X_COL, "33"), width=2)
        c.math(OX + XS + h * U / 2, OY + XS / 2, f"{h}x", size=20, color=X_COL)
        c.rect(OX, OY + XS, XS, h * U, color=X_COL, fill=theme.fill(X_COL, "33"), width=2)
        c.math(OX + XS / 2, OY + XS + h * U / 2, f"{h}x", size=20, color=X_COL)
        if c.is_new:
            c.rect(OX + XS + h * U, OY, h * U, XS, color=X_COL, width=1.6, dash="6 4")
            c.text(OX + XS + 1.5 * h * U, OY + XS / 2, "was here", size=13, color=theme.SOFT_INK)
            c.curved_arrow(OX + XS + 1.5 * h * U, OY + XS + 8, OX + XS + 12, OY + XS + h * U / 2, bend=-0.35,
                           color=X_COL, width=2.2)
        c.math(OX - 14, OY + XS + h * U / 2, f"{h}", size=17, color=X_COL)
        c.math(OX + XS + h * U / 2, OY - 14, f"{h}", size=17, color=X_COL)
        c.math(OX + XS / 2, OY - 14, "x", size=17, color=SQ_COL)
        c.math(OX - 14, OY + XS / 2, "x", size=17, color=SQ_COL)
        ledger(c, 0, [("x^2", SQ_COL), (f" + {b}x", X_COL), (f" = {rhs}", theme.INK)])
        ledger(c, 1, [("x^2", SQ_COL), (f" + {h}x + {h}x", X_COL), (f" = {rhs}", theme.INK)])
        c.text(LX, 110 + 2 * 46, "same area, new shape", size=15, color=theme.SOFT_INK, anchor="start")

    @wt.step("Fill in the missing corner", f"The corner is a {h}-by-{h} hole worth {corner}. Add {corner} to "
             f"both sides to keep the equation fair.", math=f"x^2 + {b}x + {corner} = {rhs} + {corner} = {total}")
    def _(c):
        c.rect(OX + XS, OY + XS, h * U, h * U, color=ONE_COL, fill=theme.fill(ONE_COL, "40"), width=2, dash="6 4")
        c.math(OX + XS + h * U / 2, OY + XS + h * U / 2, f"{h}^2 = {corner}", size=18, color=ONE_COL)
        ledger(c, 3, [("x^2", SQ_COL), (f" + {b}x", X_COL), (f" + {corner}", ONE_COL),
                      (f" = {rhs}", theme.INK), (f" + {corner}", ONE_COL)])

    @wt.step("Read the side of the big square", f"The square has side x + {h} and area {total}, so the side is "
             f"{side} and x = {side} − {h} = {xv}. Algebra also allows x + {h} = −{side}, so x = −{side + h}, a "
             "length no drawing can show.",
             math=f"(x + {h})^2 = {total},   x + {h} = {side},   x = {xv}  (or x = {-side - h})")
    def _(c):
        S = (xv + h) * U
        for i in range(1, xv + h):
            c.line(OX + i * U, OY, OX + i * U, OY + S, color=theme.MUTED, width=1, dash="2 3")
            c.line(OX, OY + i * U, OX + S, OY + i * U, color=theme.MUTED, width=1, dash="2 3")
        c.rect(OX, OY, S, S, color=theme.INK, width=3)
        brace(c, OX + S + 10, OY, OX + S + 10, OY + S, f"x + {h} = {side}", color=theme.INK, size=17)
        c.text(OX + S / 2, OY + S + 22, f"{side} × {side} = {total} small squares", size=14,
               color=theme.SOFT_INK)
        ledger(c, 4, [(f"(x + {h})^2 = {total}", theme.INK)])
        ledger(c, 5, [(f"x = {xv}", theme.GREEN)])

    return wt
