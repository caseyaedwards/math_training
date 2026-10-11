"""Binary numbers: place value with powers of two, and conversion by repeated halving."""

from __future__ import annotations

from .. import theme
from ..annotate import brace
from ..registry import diagram
from ..walkthrough import Walkthrough

N = 13
BITS = 4
POW_COL = {8: theme.BLUE, 4: theme.ORANGE, 2: theme.MUTED, 1: theme.GREEN}
ON_COL = {8: theme.BLUE, 4: theme.ORANGE, 2: theme.PURPLE, 1: theme.GREEN}


def answer_box(c, x, y, s, w=170, color=theme.INK):
    c.rect(x - w / 2, y - 20, w, 40, color=color, fill=theme.PAPER, width=2, rx=8)
    c.math(x, y, s, size=24, color=color)


def digits(n: int, k: int = BITS) -> list:
    return [(n >> i) & 1 for i in range(k - 1, -1, -1)]


@diagram("binary-place-value", "Binary Place Value", "Number Theory")
def build() -> Walkthrough:
    bits = digits(N)
    binary = "".join(map(str, bits))
    assert int(binary, 2) == N
    powers = [2 ** i for i in range(BITS - 1, -1, -1)]
    wt = Walkthrough(
        "binary-place-value", "Binary Place Value", "Number Theory",
        concept=f"{N} = 8 + 4 + 0 + 1 = {binary}_2",
        summary="In base 2 each place is worth twice the place to its right: 1, 2, 4, 8, and so on. "
                "Fill places from the left with the biggest power that fits.",
        width=680, height=400, level="101",
    )
    BW, GAP, BX0, BY = 120, 18, 70, 36
    UNIT, UX0, UY = 36, 106, 270

    def box_x(i):
        return BX0 + i * (BW + GAP)

    @wt.setup
    def _(c):
        for i, p in enumerate(powers):
            x = box_x(i)
            c.rect(x, BY, BW, 40, color=theme.INK, fill=theme.PANEL, width=1.5)
            c.math(x + BW / 2, BY + 20, f"2^{BITS - 1 - i} = {p}", size=18)
            c.rect(x, BY + 40, BW, 90, color=theme.INK, fill=theme.PAPER, width=1.5)
        for i in range(BITS - 1):
            c.text(box_x(i) + BW + GAP / 2, BY - 13, "×2 ←", size=12, color=theme.SOFT_INK)
        c.text(BX0 - 12, BY + 20, "worth", size=12, color=theme.SOFT_INK, anchor="end")
        c.text(BX0 - 12, BY + 85, "digit", size=12, color=theme.SOFT_INK, anchor="end")
        # 13 unit squares, the amount to share out
        for k in range(N):
            c.rect(UX0 + k * UNIT, UY, UNIT, UNIT, color=theme.MUTED, fill=theme.PAPER, width=1.5)
        c.text(UX0 - 12, UY + UNIT / 2, str(N), size=18, weight="bold", anchor="end")
        return None

    state = []
    left = N
    for i, p in enumerate(powers):
        take = p if p <= left else 0
        state.append((i, p, take, left))
        left -= take

    def fill_box(c, i, p, bit):
        x = box_x(i)
        col = ON_COL[p] if bit else theme.MUTED
        c.rect(x + 2, BY + 42, BW - 4, 86, color="none", fill=theme.fill(col, "30" if bit else "14"))
        c.text(x + BW / 2, BY + 85, str(bit), size=52, weight="bold", color=col)

    def draw(i):
        _, p, take, before = state[i]
        start = N - before  # units already used

        def fn(c):
            fill_box(c, i, p, 1 if take else 0)
            if take:
                col = ON_COL[p]
                for k in range(start, start + take):
                    c.rect(UX0 + k * UNIT, UY, UNIT, UNIT, color=col, fill=theme.fill(col, "55"), width=2)
                a, b = UX0 + start * UNIT, UX0 + (start + take) * UNIT
                brace(c, b - 2, UY + UNIT + 4, a + 2, UY + UNIT + 4, str(take), color=col, depth=10)
                # link the chunk to its box
                c.line((a + b) / 2, UY - 4, box_x(i) + BW / 2, BY + 132, color=col, width=1.5, dash="4 3")
            if c.is_new:
                rest = before - take
                msg = f"{rest} left" if rest else "0 left"
                c.label_box(632, UY + UNIT / 2, msg, color=theme.RED if rest else theme.GREEN,
                            border=theme.RED if rest else theme.GREEN, size=14)
                if not take:
                    c.text(box_x(i) + BW / 2, BY + 150, f"{p} > {before}: too big", size=13, color=theme.SOFT_INK)
        return fn

    @wt.step("Places are powers of two", "In base 10 the places are 1, 10, 100. In base 2 they are 1, 2, 4, 8, "
             "each one double the last. Each place holds a digit 0 or 1, never more.",
             math="places: 2^3, 2^2, 2^1, 2^0 = 8, 4, 2, 1")
    def _(c):
        if c.is_new:
            c.text(UX0 + N * UNIT / 2, UY + UNIT + 24, f"{N} units to share out among the places", size=14,
                   color=theme.SOFT_INK)

    texts = [
        ("Does 8 fit? Yes", f"8 fits into {N}, so the 8s place gets a 1. That uses 8 units and leaves 5.",
         f"{N} - 8 = 5"),
        ("Does 4 fit? Yes", "4 fits into 5, so the 4s place gets a 1. One unit is left.", "5 - 4 = 1"),
        ("Does 2 fit? No", "2 is bigger than the 1 unit left, so the 2s place gets a 0. A zero is a placeholder, "
         "not nothing.", "2 > 1  \\implies  digit 0"),
        ("Does 1 fit? Yes", "The last unit fills the 1s place. Nothing is left, so the digits are done.",
         "1 - 1 = 0"),
    ]
    for i, (t, x, m) in enumerate(texts):
        wt.step(t, x, math=m)(draw(i))

    @wt.step("Read the digits left to right", f"The digits spell {binary}. Add up the places that hold a 1 to "
             f"check: 8 + 4 + 1 = {N}. There are 10 kinds of people: those who read binary and those who do not.",
             math=f"{binary}_2 = 1 \\cdot 8 + 1 \\cdot 4 + 0 \\cdot 2 + 1 \\cdot 1 = {N}")
    def _(c):
        answer_box(c, UX0 + N * UNIT / 2, 372, f"{N} = {binary}_2")

    return wt


@diagram("binary-by-halving", "Binary by Repeated Halving", "Number Theory")
def build_halving() -> Walkthrough:
    rows = []  # (n, quotient, remainder)
    n = N
    while n:
        rows.append((n, n // 2, n % 2))
        n //= 2
    binary = "".join(str(r) for _, _, r in reversed(rows))
    assert int(binary, 2) == N
    wt = Walkthrough(
        "binary-by-halving", "Binary by Repeated Halving", "Number Theory",
        concept=f"{N} \\to {binary}_2: divide by 2, keep remainders, read bottom to top",
        summary="Divide by 2 again and again and write down each remainder. The remainders, read from the bottom "
                "up, are the binary digits.",
        width=640, height=380, level="101",
    )
    X_N, X_Q, X_R = 120, 300, 430
    TOP, ROW = 70, 56

    @wt.setup
    def _(c):
        c.text(X_N, 28, "number ÷ 2", size=14, color=theme.SOFT_INK, weight="bold")
        c.text(X_Q, 28, "quotient", size=14, color=theme.SOFT_INK, weight="bold")
        c.text(X_R, 28, "remainder", size=14, color=theme.SOFT_INK, weight="bold")
        c.line(40, 46, 520, 46, color=theme.GRID, width=1.5)
        return None

    def row(c, i):
        n, q, r = rows[i]
        y = TOP + i * ROW
        p = 2 ** i
        col = ON_COL[p] if r else theme.MUTED
        c.text(X_N, y, f"{n} ÷ 2", size=20)
        c.text(X_Q - 50, y, "=", size=20, color=theme.SOFT_INK)
        c.text(X_Q, y, str(q), size=20)
        c.text(X_R - 60, y, "R", size=16, color=theme.SOFT_INK)
        c.circle(X_R, y, 19, color=col, fill=theme.fill(col, "30"), width=2)
        c.text(X_R, y, str(r), size=20, weight="bold", color=col)
        c.text(X_R + 34, y, f"{p}s place", size=13, color=col, anchor="start")
        if i:
            c.arrow(X_Q - 8, y - ROW + 14, X_N + 30, y - 14, color=theme.MUTED, width=1.3, dash="4 3")

    @wt.step("Divide by 2, keep the remainder", f"{N} ÷ 2 = 6 remainder 1. An odd number always leaves "
             "remainder 1, and that 1 is the last binary digit.", math=f"{N} = 2 \\times 6 + 1")
    def _(c):
        row(c, 0)
        if c.is_new:
            c.text(280, 250, "even number ÷ 2: remainder 0", size=15, color=theme.SOFT_INK)
            c.text(280, 280, "odd number ÷ 2: remainder 1", size=15, color=theme.GREEN)

    @wt.step("Pass the quotient down", "Divide the quotient again: 6 ÷ 2 = 3 remainder 0. Each new remainder "
             "is the next place to the left.", math="6 = 2 \\times 3 + 0")
    def _(c):
        row(c, 1)

    @wt.step("Repeat until the quotient is 0", "3 ÷ 2 = 1 R 1, then 1 ÷ 2 = 0 R 1. A quotient of 0 means stop.",
             math="3 = 2 \\times 1 + 1,  1 = 2 \\times 0 + 1")
    def _(c):
        row(c, 2)
        row(c, 3)
        c.text(X_Q, TOP + 3 * ROW + 28, "0: stop", size=13, color=theme.GREEN)

    @wt.step("Read the remainders bottom to top", f"The last remainder is the biggest place. Read up the "
             f"column to get {binary}. Same answer as filling places with 8, 4, 2, 1.",
             math=f"{N} = {binary}_2")
    def _(c):
        x = X_R + 120
        y0, y1 = TOP + (len(rows) - 1) * ROW + 10, TOP - 10
        c.arrow(x, y0, x, y1, color=theme.INK, width=2.5)
        c.text(x + 14, (y0 + y1) / 2, "read up", size=13, anchor="start", color=theme.INK)
        answer_box(c, 260, TOP + len(rows) * ROW + 40, f"{N} = {binary}_2")

    return wt
