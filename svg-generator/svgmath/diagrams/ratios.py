"""Percents and ratios: percent grids, tape diagrams, and double number lines."""

from __future__ import annotations

from fractions import Fraction as F

from .. import theme
from ..annotate import brace, hop
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._kit import rich, tag

CAT = "Fractions and Ratios"


def num(v) -> str:
    """Formats a number without a trailing .0."""
    v = float(v)
    return str(int(v)) if v == int(v) else f"{v:g}"


@diagram("percent-grid", "Percent of a Number on a Grid", CAT)
def build_percent() -> Walkthrough:
    pct, whole = 35, 80
    part = F(pct, 100) * whole
    each = F(whole, 100)
    assert part == pct * each == 28

    wt = Walkthrough(
        "percent-grid", "Percent of a Number on a Grid", CAT,
        concept="35% of 80 = 35/100 \\times 80 = 28",
        summary="Percent means out of 100. Shade 35 of 100 squares, let the whole grid stand for 80, "
                "and read off how much 35 squares are worth.",
        width=700, height=364, level="101",
    )
    G, T, CS = 60, 30, 30  # grid left, top, cell size
    B = T + 10 * CS  # grid bottom
    BX, BW = 470, 44  # percent bar left, width
    BLUE, ORANGE, GREEN = theme.BLUE, theme.ORANGE, theme.GREEN
    full_rows, extra = divmod(pct, 10)

    def cell(i):
        r, k = divmod(i, 10)  # rows fill from the bottom
        return G + k * CS, B - (r + 1) * CS

    def Y(p):
        return B - p / 100 * (B - T)

    @wt.setup
    def _(c):
        return None

    @wt.step("One hundred squares make the whole", "The grid has 10 rows of 10, so 100 squares. "
             "Percent means per hundred, so each square is 1%.", math="100 squares = 100%")
    def _(c):
        for k in range(11):
            c.line(G + k * CS, T, G + k * CS, B, color=theme.MUTED, width=1)
            c.line(G, T + k * CS, G + 10 * CS, T + k * CS, color=theme.MUTED, width=1)
        c.rect(G, T, 10 * CS, 10 * CS, color=theme.INK, width=2.2)
        if c.is_new:
            c.text(G + 5 * CS, B + 22, "100 squares = 100%", size=14, color=theme.SOFT_INK)

    @wt.step("Shade 35 squares", "Fill three full rows of ten, then five more. That is 35 squares "
             "out of 100, or 35%.", math="35% = 35/100")
    def _(c):
        for i in range(pct):
            x, y = cell(i)
            c.rect(x, y, CS, CS, color=BLUE, fill=theme.fill(BLUE, "55"), width=1.2)
        for r in range(full_rows + (1 if extra else 0)):
            total = min(pct, (r + 1) * 10)
            c.text(G + 10 * CS + 10, B - (r + 0.5) * CS, str(total), size=13, color=BLUE, anchor="start",
                   weight="bold")

    @wt.step("Let the whole stand for 80", "Draw a bar beside the grid. Its top is 100% on the left "
             "and 80 on the right, so every 10% step is worth 8.", math="10% of 80 = 8")
    def _(c):
        c.rect(BX, T, BW, B - T, color=ORANGE, fill=theme.fill(ORANGE, "25"), width=2)
        for k in range(11):
            y = Y(10 * k)
            c.line(BX - 6, y, BX + BW + 6, y, color=theme.INK, width=1.2)
            c.text(BX - 10, y, f"{10 * k}%", size=12, color=BLUE, anchor="end")
            c.text(BX + BW + 10, y, num(F(whole * k, 10)), size=12, color=ORANGE, anchor="start")
        c.text(BX - 10, T - 16, "percent", size=11, color=BLUE, anchor="end", weight="bold")
        c.text(BX + BW + 10, T - 16, "amount", size=11, color=ORANGE, anchor="start", weight="bold")

    @wt.step("Read 35% across", "The shaded squares reach 35% of the way up. Follow that level to "
             "the bar: it falls halfway between 24 and 32, at 28.", math="35% of 80 = 28")
    def _(c):
        y = Y(pct)
        c.rect(BX, y, BW, B - y, color=GREEN, fill=theme.fill(GREEN, "60"), width=2)
        c.line(G + 10 * CS + 34, y, BX - 44, y, color=GREEN, width=2, dash="6 4")
        c.line(BX + BW + 34, y, 600, y, color=GREEN, width=2, dash="6 4")
        tag(c, 640, y, f"{num(part)}", GREEN, size=20)
        c.text(BX + BW / 2, y, "35%", size=12, color=theme.INK, weight="bold", halo=True)

    @wt.step("Check one square at a time", "One square is 80 ÷ 100 = 0.8, and 35 of them make 28. "
             "Two routes, one answer.", math="35 \\times 0.8 = 28")
    def _(c):
        for i in range(pct):
            x, y = cell(i)
            c.text(x + CS / 2, y + CS / 2, num(each), size=11, color=theme.INK)
        tag(c, 640, Y(80), f"1 square = {num(each)}", ORANGE, size=14)
        rich(c, 640, Y(65), f"35 \\times {num(each)} = {num(part)}", size=17, color=GREEN)

    return wt


@diagram("tape-diagram-ratio", "Sharing in a Ratio with a Tape Diagram", CAT)
def build_tape() -> Walkthrough:
    total, ra, rb = 64, 3, 5
    parts = ra + rb
    unit = total // parts
    assert unit * parts == total
    sa, sb = ra * unit, rb * unit

    wt = Walkthrough(
        "tape-diagram-ratio", "Sharing in a Ratio with a Tape Diagram", CAT,
        concept=f"{ra} : {rb} of {total} \\to {total} \\div {parts} = {unit},  {sa} : {sb}",
        summary="A ratio of 3 to 5 means 3 equal boxes for one person and 5 for the other. Split the "
                "total over all 8 boxes, then count each person's boxes.",
        width=680, height=330, level="101",
    )
    L, U, H = 130, 56, 46
    YA, YB = 104, 200
    BLUE, ORANGE, GREEN = theme.BLUE, theme.ORANGE, theme.GREEN

    def boxes(c, y, n, color, value=None):
        for i in range(n):
            c.rect(L + i * U, y, U, H, color=color, fill=theme.fill(color, "40"), width=2)
            if value is not None:
                c.text(L + i * U + U / 2, y + H / 2, str(value), size=20, weight="bold", color=theme.INK)

    @wt.setup
    def _(c):
        return None

    @wt.step("Draw the ratio as equal boxes", "Maya and Leo share 64 stickers in the ratio 3 : 5. "
             "Give Maya 3 boxes and Leo 5 boxes, all the same size.", math=f"{ra} : {rb}")
    def _(c):
        boxes(c, YA, ra, BLUE)
        boxes(c, YB, rb, ORANGE)
        c.text(L - 14, YA + H / 2, "Maya", size=17, color=BLUE, anchor="end", weight="bold")
        c.text(L - 14, YB + H / 2, "Leo", size=17, color=ORANGE, anchor="end", weight="bold")
        c.text(L - 14, YA + H / 2 + 20, f"{ra} boxes", size=12, color=BLUE, anchor="end")
        c.text(L - 14, YB + H / 2 + 20, f"{rb} boxes", size=12, color=ORANGE, anchor="end")

    @wt.step("Mark the total", "All 64 stickers fill all the boxes. Three boxes plus 5 boxes is "
             "8 boxes in all.", math=f"{ra} + {rb} = {parts} boxes = {total}")
    def _(c):
        x = L + rb * U + 16
        brace(c, x, YA, x, YB + H, label=None, color=GREEN)
        c.text(x + 26, (YA + YB + H) / 2 - 12, f"{total} stickers", size=17, color=GREEN, anchor="start",
               weight="bold")
        c.text(x + 26, (YA + YB + H) / 2 + 12, f"in {parts} boxes", size=15, color=GREEN, anchor="start")

    @wt.step("Find one box", "Share 64 evenly over 8 boxes. Each box holds 8 stickers.",
             math=f"{total} \\div {parts} = {unit}")
    def _(c):
        boxes(c, YA, ra, BLUE, unit)
        boxes(c, YB, rb, ORANGE, unit)
        x = L + rb * U + 16
        rich(c, x + 26, (YA + YB + H) / 2 + 40, f"{total} \\div {parts} = {unit} each", size=17, color=GREEN,
             anchor="start")

    @wt.step("Find each share", "Count the boxes. Maya gets 3 × 8 = 24 and Leo gets 5 × 8 = 40. "
             "The shares add back to 64, so nobody got shortchanged.",
             math=f"{ra} \\times {unit} = {sa},  {rb} \\times {unit} = {sb},  {sa} + {sb} = {total}")
    def _(c):
        brace(c, L, YA - 6, L + ra * U, YA - 6, label=f"{ra} \\times {unit} = {sa}", color=BLUE, size=17)
        brace(c, L + rb * U, YB + H + 6, L, YB + H + 6, label=f"{rb} \\times {unit} = {sb}", color=ORANGE,
              size=17)

    return wt


@diagram("double-number-line", "Double Number Line for Proportions", CAT)
def build_dnl() -> Walkthrough:
    eggs0, flour0 = 2, 3
    rate = F(flour0, eggs0)
    wt = Walkthrough(
        "double-number-line", "Double Number Line for Proportions", CAT,
        concept="3 cups flour : 2 eggs = 6 : 4 = 9 : 6 = 12 : 8 = 1.5 : 1",
        summary="Two number lines share a zero. Every pair of marks that line up is the same recipe at a "
                "different size, so scaling one line scales the other by the same factor.",
        width=700, height=330, level="101",
    )
    L, R = 146, 650
    YT, YB = 132, 214  # eggs line, flour line
    EMAX = 8
    BLUE, ORANGE, GREEN, PURPLE = theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE

    def X(e):
        return L + float(e) / EMAX * (R - L)

    def pair(c, e, strong=True):
        f = rate * e
        c.line(X(e), YT, X(e), YB, color=GREEN if strong else theme.MUTED, width=1.8, dash="5 4")
        c.line(X(e), YT - 8, X(e), YT + 8, color=ORANGE, width=2.2)
        c.line(X(e), YB - 8, X(e), YB + 8, color=BLUE, width=2.2)
        c.text(X(e), YT - 22, num(e), size=16, color=ORANGE, weight="bold")
        c.text(X(e), YB + 24, num(f), size=16, color=BLUE, weight="bold")
        c.dot(X(e), YT, r=4.5, color=ORANGE)
        c.dot(X(e), YB, r=4.5, color=BLUE)

    @wt.setup
    def _(c):
        c.arrow(L - 10, YT, R + 26, YT, color=theme.INK, width=2)
        c.arrow(L - 10, YB, R + 26, YB, color=theme.INK, width=2)
        c.text(L - 24, YT, "eggs", size=15, color=ORANGE, anchor="end", weight="bold")
        c.text(L - 24, YB, "cups of flour", size=15, color=BLUE, anchor="end", weight="bold")
        return None

    @wt.step("Line up two number lines at zero", "The top line counts eggs and the bottom line "
             "counts cups of flour. Zero eggs needs zero flour, so the zeros line up.",
             math="0 eggs : 0 cups")
    def _(c):
        pair(c, 0, strong=False)

    @wt.step("Mark the recipe", "The recipe uses 3 cups of flour for every 2 eggs. Put 2 on the egg "
             "line right above 3 on the flour line.", math="2 eggs : 3 cups")
    def _(c):
        pair(c, eggs0)

    @wt.step("Double the recipe", "Twice the eggs needs twice the flour. Both lines scale by 2 "
             "at the same time.", math="2 \\times 2 = 4 eggs,  3 \\times 2 = 6 cups")
    def _(c):
        pair(c, 2 * eggs0)
        if c.is_new:
            hop(c, X(eggs0), X(2 * eggs0), YT - 40, "\\times 2", color=PURPLE, height=26, size=16)
            hop(c, X(eggs0), X(2 * eggs0), YB + 44, "\\times 2", color=PURPLE, height=26, size=16, below=True)

    @wt.step("Keep adding the recipe", "Each extra batch adds 2 eggs on top and 3 cups below. The "
             "marks stay lined up all the way out.", math="6 : 9,  8 : 12")
    def _(c):
        for k in (3, 4):
            pair(c, k * eggs0)
            if c.is_new:
                hop(c, X((k - 1) * eggs0), X(k * eggs0), YT - 40, "+2", color=GREEN, height=22, size=15)
                hop(c, X((k - 1) * eggs0), X(k * eggs0), YB + 44, "+3", color=GREEN, height=22, size=15,
                    below=True)

    @wt.step("Halve to find the unit rate", "Halve the recipe to reach 1 egg. Half of 3 cups is "
             "1.5 cups, so the recipe uses 1.5 cups of flour per egg.",
             math="2 \\div 2 = 1 egg,  3 \\div 2 = 1.5 cups")
    def _(c):
        pair(c, 1)
        hop(c, X(eggs0), X(1), YT - 40, "\\div 2", color=PURPLE, height=22, size=16)
        hop(c, X(eggs0), X(1), YB + 44, "\\div 2", color=PURPLE, height=22, size=16, below=True)
        tag(c, X(6), 34, f"{num(rate)} cups per egg", GREEN, size=16, math=False)

    return wt
