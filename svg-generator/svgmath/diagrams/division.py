"""Whole-number division: long division and partial quotients."""

from __future__ import annotations

from .. import theme
from ..annotate import brace
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._kit import rich, tag

DIVIDE, MULTIPLY, SUBTRACT, BRING = theme.GREEN, theme.RED, theme.BLUE, theme.PURPLE


@diagram("long-division", "Long Division", "Arithmetic")
def build_long() -> Walkthrough:
    n, d = 156, 12
    digits = str(n)
    q1, r1 = divmod(int(digits[:2]), d)  # 15 / 12 = 1 r 3
    p1 = q1 * d
    nxt = r1 * 10 + int(digits[2])  # 36
    q2, r2 = divmod(nxt, d)
    p2 = q2 * d
    q = q1 * 10 + q2
    assert q * d + r2 == n

    wt = Walkthrough(
        "long-division", "Long Division", "Arithmetic",
        concept=f"{n} \\div {d} = {q}",
        summary="Long division repeats four moves: divide, multiply, subtract, bring down. Each lap "
                "of the loop finds one digit of the quotient.",
        width=700, height=330, level="101",
    )
    X0, CW, SZ = 190, 28, 30  # x of the first dividend digit, column width, digit size
    QY, DY, P1Y, R1Y, P2Y, R2Y = 64, 118, 160, 206, 248, 294

    def col(k):
        return X0 + k * CW

    def digit(c, k, y, s, color=theme.INK):
        c.text(col(k), y, s, size=SZ, font="mono", color=color, weight="bold")

    def rule(c, k0, k1, y, color):
        c.line(col(k0) - CW / 2 - 4, y, col(k1) + CW / 2 + 4, y, color=color, width=2.4)

    boxes = {  # name: (center x, center y, color)
        "Divide": (480, 92, DIVIDE),
        "Multiply": (620, 92, MULTIPLY),
        "Subtract": (620, 178, SUBTRACT),
        "Bring down": (480, 178, BRING),
    }

    def active(c, *names, note=None, note_color=theme.INK):
        if not c.is_new:
            return
        for name in names:
            x, y, color = boxes[name]
            c.rect(x - 58, y - 20, 116, 40, color=color, fill=color, rx=8, width=2)
            c.text(x, y, name, size=15, color=theme.PAPER, weight="bold")
        if note:
            rich(c, 550, 252, note, size=19, color=note_color)

    @wt.setup
    def _(c):
        c.text(550, 46, "the loop", size=13, color=theme.SOFT_INK, weight="bold")
        for name, (x, y, color) in boxes.items():
            c.rect(x - 58, y - 20, 116, 40, color=color, fill=theme.PAPER, rx=8, width=2)
            c.text(x, y, name, size=15, color=color, weight="bold")
        c.arrow(538, 92, 558, 92, color=theme.SOFT_INK, width=1.8)
        c.arrow(620, 113, 620, 155, color=theme.SOFT_INK, width=1.8)
        c.arrow(560, 178, 542, 178, color=theme.SOFT_INK, width=1.8)
        c.arrow(480, 157, 480, 115, color=theme.SOFT_INK, width=1.8)
        return None

    @wt.step("Set up the division", "Write 156 under the bracket and the divisor 12 outside it. "
             "The answer, the quotient, grows on top, one digit at a time.",
             math=f"{n} \\div {d} = ?")
    def _(c):
        for k, ch in enumerate(digits):
            digit(c, k, DY, ch)
        left = col(0) - CW / 2 - 8
        c.path(f"M{left},{DY - 24} Q{left + 9},{DY} {left},{DY + 24}", color=theme.INK, width=2.4)
        c.line(left, DY - 24, col(2) + CW / 2 + 10, DY - 24, color=theme.INK, width=2.4)
        c.text(left - 10, DY, str(d), size=SZ, font="mono", color=theme.INK, weight="bold", anchor="end")
        if c.is_new:
            c.text(col(1), DY + 44, "dividend", size=12, color=theme.SOFT_INK)
            c.text(left - 30, DY + 44, "divisor", size=12, color=theme.SOFT_INK)

    @wt.step("Divide: how many 12s fit in 15", "Twelve does not fit in 1, so look at 15. One 12 fits "
             "in 15. Write the 1 above the 5.", math=f"15 \\div {d} \\to {q1}")
    def _(c):
        if c.is_new:
            c.rect(col(0) - CW / 2 + 3, DY - 20, 2 * CW - 6, 40, color=DIVIDE, width=2, rx=5, dash="5 3")
        digit(c, 1, QY, str(q1), DIVIDE)
        active(c, "Divide", note=f"15 \\div 12 \\to {q1}", note_color=DIVIDE)

    @wt.step("Multiply the digit by 12", "One times 12 is 12. Write it under the 15 so the places "
             "line up.", math=f"{q1} \\times {d} = {p1}")
    def _(c):
        for k, ch in enumerate(str(p1)):
            digit(c, k, P1Y, ch, MULTIPLY)
        c.text(col(-1), P1Y, "−", size=SZ, color=MULTIPLY)
        active(c, "Multiply", note=f"{q1} \\times 12 = {p1}", note_color=MULTIPLY)

    @wt.step("Subtract to find what is left", "Fifteen minus 12 leaves 3. The 3 is smaller than 12, "
             "which means the digit 1 was right.", math=f"15 - {p1} = {r1}")
    def _(c):
        rule(c, 0, 1, P1Y + 22, MULTIPLY)
        digit(c, 1, R1Y, str(r1), SUBTRACT)
        active(c, "Subtract", note=f"15 - {p1} = {r1}", note_color=SUBTRACT)

    @wt.step("Bring down the next digit", "Pull the 6 straight down next to the 3. The 3 tens and "
             "6 ones now read as 36.", math=f"{r1} and 6 \\to {nxt}")
    def _(c):
        if c.is_new:
            c.arrow(col(2), DY + 20, col(2), R1Y - 20, color=BRING, width=2.2, dash="5 4")
        digit(c, 2, R1Y, digits[2], BRING)
        active(c, "Bring down", note=f"{r1} and 6 \\to {nxt}", note_color=BRING)

    @wt.step("Divide again: 12s in 36", "Back to the top of the loop. Three 12s fit in 36 exactly. "
             "Write 3 above the 6.", math=f"{nxt} \\div {d} \\to {q2}")
    def _(c):
        if c.is_new:
            c.rect(col(1) - CW / 2 + 3, R1Y - 20, 2 * CW - 6, 40, color=DIVIDE, width=2, rx=5, dash="5 3")
        digit(c, 2, QY, str(q2), DIVIDE)
        active(c, "Divide", note=f"{nxt} \\div 12 \\to {q2}", note_color=DIVIDE)

    @wt.step("Multiply and subtract", "Three times 12 is 36, and 36 minus 36 is 0. No digits are "
             "left to bring down, so the loop stops.",
             math=f"{q2} \\times {d} = {p2},  {nxt} - {p2} = {r2}")
    def _(c):
        for k, ch in enumerate(str(p2)):
            digit(c, 1 + k, P2Y, ch, MULTIPLY)
        c.text(col(0), P2Y, "−", size=SZ, color=MULTIPLY)
        rule(c, 1, 2, P2Y + 22, MULTIPLY)
        digit(c, 2, R2Y, str(r2), SUBTRACT)
        active(c, "Multiply", "Subtract", note=f"{nxt} - {p2} = {r2}", note_color=SUBTRACT)

    @wt.step("Check the answer", "The quotient is 13 with remainder 0. Multiply back to check: "
             "13 groups of 12 rebuild 156.", math=f"{q} \\times {d} = {q * d}")
    def _(c):
        c.rect(col(1) - CW / 2 - 6, QY - 22, 2 * CW + 12, 44, color=DIVIDE, width=2.4, rx=6)
        tag(c, 550, 252, f"{q} \\times {d} = {q * d}", DIVIDE, size=19)
        c.text(550, 286, f"quotient {q}, remainder {r2}", size=14, color=theme.SOFT_INK)

    return wt


@diagram("partial-quotients", "Division by Partial Quotients", "Arithmetic")
def build_partial() -> Walkthrough:
    n, d = 156, 12
    big = 10
    take1 = big * d  # 120
    left1 = n - take1  # 36
    small = left1 // d  # 3
    take2 = small * d
    left2 = left1 - take2
    q = big + small
    assert left2 == 0 and q * d == n

    wt = Walkthrough(
        "partial-quotients", "Division by Partial Quotients", "Arithmetic",
        concept=f"{n} \\div {d} = {big} + {small} = {q}",
        summary="Division asks how many groups of 12 fit in 156. Take out big, easy groups first, "
                "then smaller ones, and add up the group counts.",
        width=700, height=330, level="101",
    )
    L, R = 40, 660
    TOP, BH = 92, 54

    def X(v):
        return L + v / n * (R - L)

    @wt.setup
    def _(c):
        return None

    @wt.step("Draw 156 as one long bar", "Think of 156 as a strip of tape. The question is how many "
             "pieces of length 12 it cuts into.", math=f"{n} \\div {d} = ?")
    def _(c):
        c.rect(L, TOP, R - L, BH, color=theme.INK, fill=theme.PANEL, width=2)
        if c.is_new:
            c.text((L + R) / 2, TOP + BH / 2, str(n), size=22, weight="bold")
        brace(c, L, TOP - 6, R, TOP - 6, label=f"{n}", color=theme.INK, size=17)
        if not c.is_new:
            return
        c.rect(L, TOP + BH + 46, X(d) - L, 26, color=theme.ORANGE, fill=theme.fill(theme.ORANGE, "55"), width=2)
        c.text(X(d) + 10, TOP + BH + 59, "one piece = 12", size=13, color=theme.ORANGE, anchor="start")

    @wt.step("Take out ten 12s at once", "Ten 12s are 120, an easy product. Cut that much off the "
             "front and 36 is left.", math=f"{big} \\times {d} = {take1},  {n} - {take1} = {left1}")
    def _(c):
        c.rect(L, TOP, X(take1) - L, BH, color=theme.BLUE, fill=theme.fill(theme.BLUE, "40"), width=2)
        for k in range(1, big):
            c.line(X(k * d), TOP, X(k * d), TOP + BH, color=theme.BLUE, width=1, dash="3 3")
        c.text((L + X(take1)) / 2, TOP + BH / 2, f"{big} \\times {d} = {take1}".replace("\\times", "×"),
               size=18, color=theme.BLUE, weight="bold", halo=True)
        if c.is_new:
            c.text((X(take1) + R) / 2, TOP + BH / 2, f"{left1} left", size=16, color=theme.SOFT_INK)
        rich(c, L, 262, f"{n} - {take1} = {left1} left", size=18, color=theme.BLUE, anchor="start")

    @wt.step("Take out three more 12s", "Three 12s are 36, which uses up the rest of the tape "
             "exactly.", math=f"{small} \\times {d} = {take2},  {left1} - {take2} = {left2}")
    def _(c):
        c.rect(X(take1), TOP, R - X(take1), BH, color=theme.GREEN, fill=theme.fill(theme.GREEN, "40"), width=2)
        for k in range(1, small):
            c.line(X(take1 + k * d), TOP, X(take1 + k * d), TOP + BH, color=theme.GREEN, width=1, dash="3 3")
        c.text((X(take1) + R) / 2, TOP + BH / 2, f"{small} × {d} = {take2}", size=16, color=theme.GREEN, weight="bold",
               halo=True)
        rich(c, L, 296, f"{left1} - {take2} = {left2} left", size=18, color=theme.GREEN, anchor="start")

    @wt.step("Add up the groups", "The tape holds 10 groups plus 3 groups, which is 13 groups of 12. "
             "Any split into easy chunks gives the same total.", math=f"{n} \\div {d} = {big} + {small} = {q}")
    def _(c):
        y = TOP + BH + 6
        brace(c, X(take1), y, L, y, label=f"{big} groups", color=theme.BLUE, size=16)
        brace(c, R, y, X(take1), y, label=f"{small} groups", color=theme.GREEN, size=16)
        rich(c, R, 262,
             [(f"{big}", theme.BLUE), (" + ", theme.INK), (f"{small}", theme.GREEN),
              (f" = {q} groups of {d}", theme.INK)], size=22, anchor="end")
        rich(c, R, 296, f"{q} \\times {d} = {take1} + {take2} = {n}", size=17, color=theme.SOFT_INK,
             anchor="end")

    return wt
