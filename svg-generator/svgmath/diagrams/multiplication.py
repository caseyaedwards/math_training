"""Multiplication of whole numbers: the area model and partial products."""

from __future__ import annotations

from .. import theme
from ..annotate import dimension
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._kit import rich


@diagram("area-model-multiplication", "Area Model for Multiplication", "Arithmetic")
def build() -> Walkthrough:
    a, b = 23, 14
    a1, a2 = a // 10 * 10, a % 10  # 20, 3
    b1, b2 = b // 10 * 10, b % 10  # 10, 4
    S = 17  # px per unit
    L, T = 110, 90
    R, B = L + a * S, T + b * S
    XS, YS = L + a1 * S, T + b1 * S
    cells = [  # (x0, y0, x1, y1, width factor, height factor, color)
        (L, T, XS, YS, a1, b1, theme.BLUE),
        (XS, T, R, YS, a2, b1, theme.ORANGE),
        (L, YS, XS, B, a1, b2, theme.GREEN),
        (XS, YS, R, B, a2, b2, theme.PURPLE),
    ]
    total = sum(w * h for *_, w, h, _c in cells)
    assert total == a * b

    wt = Walkthrough(
        "area-model-multiplication", "Area Model for Multiplication", "Arithmetic",
        concept=f"{a} \\times {b} = ({a1} + {a2})({b1} + {b2}) = {a1 * b1} + {a2 * b1} + {a1 * b2} + {a2 * b2} = {total}",
        summary="A product is the area of a rectangle. Split each side by place value, find the four easy "
                "areas, and add them.",
        width=700, height=356, level="101",
    )
    PX, PY, GAP = 682, 118, 34  # right panel: right edge, first row, row gap

    def panel_row(c, i, w, h, color):
        rich(c, PX, PY + i * GAP, f"{w} \\times {h} = {w * h}", size=17, anchor="end", color=color)
        if i:
            c.text(PX - 128, PY + i * GAP, "+", size=18, color=theme.SOFT_INK)

    @wt.setup
    def _(c):
        return None

    @wt.step("Draw a 23 by 14 rectangle", "Multiplying 23 by 14 asks how many unit squares fit in a "
             "rectangle 23 wide and 14 tall. Counting all of them one by one is a long afternoon.",
             math=f"{a} \\times {b} = area = ?")
    def _(c):
        for i in range(1, a):
            c.line(L + i * S, T, L + i * S, B, color=theme.GRID, width=1)
        for j in range(1, b):
            c.line(L, T + j * S, R, T + j * S, color=theme.GRID, width=1)
        c.rect(L, T, R - L, B - T, color=theme.INK, width=2.2)
        dimension(c, (L, T), (R, T), str(a), offset=56, color=theme.INK, size=17)
        dimension(c, (L, B), (L, T), str(b), offset=62, color=theme.INK, size=17)

    @wt.step("Split each side by place value", "Cut 23 into 20 and 3, and cut 14 into 10 and 4. "
             "The dashed lines chop the big rectangle into four smaller ones.",
             math=f"{a} = {a1} + {a2},  {b} = {b1} + {b2}")
    def _(c):
        c.line(XS, T - 6, XS, B + 6, color=theme.INK, width=2, dash="7 5")
        c.line(L - 6, YS, R + 6, YS, color=theme.INK, width=2, dash="7 5")
        dimension(c, (L, T), (XS, T), str(a1), offset=20, size=15)
        dimension(c, (XS, T), (R, T), str(a2), offset=20, size=15)
        dimension(c, (L, YS), (L, T), str(b1), offset=22, size=15)
        dimension(c, (L, B), (L, YS), str(b2), offset=22, size=15)

    def fill_cell(c, k, i):
        x0, y0, x1, y1, w, h, color = cells[k]
        c.rect(x0, y0, x1 - x0, y1 - y0, color=color, fill=theme.fill(color, "38"), width=2.4)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if x1 - x0 > 120:
            if y1 - y0 > 80:
                rich(c, cx, cy - 13, f"{w} \\times {h}", size=20, color=color, halo=True)
                rich(c, cx, cy + 15, f"= {w * h}", size=24, color=color, halo=True, weight="bold")
            else:
                rich(c, cx, cy, f"{w} \\times {h} = {w * h}", size=20, color=color, halo=True)
        else:
            rich(c, cx, cy - 12, f"{w}\\times{h}", size=15, color=color, halo=True)
            rich(c, cx, cy + 12, f"={w * h}", size=17, color=color, halo=True, weight="bold")
        panel_row(c, i, w, h, color)

    @wt.step("Multiply the tens row", "The top strip is 10 tall. Its big piece is 20 × 10 and its thin "
             "piece is 3 × 10. Multiplying by tens is easy: tack on a zero.",
             math=f"{a1} \\times {b1} = {a1 * b1},  {a2} \\times {b1} = {a2 * b1}")
    def _(c):
        c.text(PX - 60, PY - 34, "partial products", size=13, color=theme.SOFT_INK, weight="bold")
        fill_cell(c, 0, 0)
        fill_cell(c, 1, 1)

    @wt.step("Multiply the ones row", "The bottom strip is 4 tall. Its pieces are 20 × 4 and 3 × 4, "
             "two facts from the times table.",
             math=f"{a1} \\times {b2} = {a1 * b2},  {a2} \\times {b2} = {a2 * b2}")
    def _(c):
        fill_cell(c, 2, 2)
        fill_cell(c, 3, 3)

    @wt.step("Add the four pieces", "The four areas fill the whole rectangle with no gaps and no "
             "overlaps, so their sum is the product.",
             math=f"{a1 * b1} + {a2 * b1} + {a1 * b2} + {a2 * b2} = {total}")
    def _(c):
        y = PY + 3 * GAP + 20
        c.line(PX - 140, y, PX, y, color=theme.INK, width=2)
        rich(c, PX, y + 24, f"{a} \\times {b} = {total}", size=21, anchor="end", weight="bold")

    return wt
