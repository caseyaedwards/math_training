"""Place value: adding with base-ten blocks and regrouping."""

from __future__ import annotations

from .. import theme
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._kit import fade

U = 8  # side of one unit cube in px
COLS = {"h": (110, 290), "t": (410, 140), "o": (560, 130)}  # left, width of each place column
ROWS = [48, 148, 262]  # top of the first addend, second addend, and sum rows
H = 80  # block height


def flat(c, x, y, color):
    c.rect(x, y, 10 * U, 10 * U, color=color, fill=theme.fill(color, "40"), width=1.6)
    for k in range(1, 10):
        c.line(x + k * U, y, x + k * U, y + 10 * U, color=theme.fill(color, "80"), width=0.6)
        c.line(x, y + k * U, x + 10 * U, y + k * U, color=theme.fill(color, "80"), width=0.6)


def rod(c, x, y, color):
    c.rect(x, y, U, 10 * U, color=color, fill=theme.fill(color, "40"), width=1.6)
    for k in range(1, 10):
        c.line(x, y + k * U, x + U, y + k * U, color=theme.fill(color, "80"), width=0.6)


def unit(c, x, y, color):
    c.rect(x, y, U, U, color=color, fill=theme.fill(color, "40"), width=1.4)


def flat_x(i):
    return COLS["h"][0] + 4 + i * (10 * U + 12)


def rod_x(i):
    return COLS["t"][0] + 10 + i * (U + 7)


def unit_xy(i, top):
    return COLS["o"][0] + 14 + (i % 5) * (U + 5), top + 14 + (i // 5) * (U + 5)


def blocks(c, top, h, t, o, color, start=(0, 0, 0)):
    for i in range(h):
        flat(c, flat_x(start[0] + i), top, color)
    for i in range(t):
        rod(c, rod_x(start[1] + i), top, color)
    for i in range(o):
        unit(c, *unit_xy(start[2] + i, top), color)


def note(c, col, top, s, color=theme.SOFT_INK):
    left, w = COLS[col]
    c.text(left + w / 2, top + H + 12, s, size=12, color=color)


@diagram("place-value-blocks", "Adding with Base-Ten Blocks", "Arithmetic")
def build() -> Walkthrough:
    a, b = 247, 135
    da = [a // 100, a // 10 % 10, a % 10]
    db = [b // 100, b // 10 % 10, b % 10]
    ones = da[2] + db[2]
    carry, ones_left = divmod(ones, 10)
    tens = da[1] + db[1] + carry
    hundreds = da[0] + db[0]
    total = a + b
    assert total == hundreds * 100 + tens * 10 + ones_left

    wt = Walkthrough(
        "place-value-blocks", "Adding with Base-Ten Blocks", "Arithmetic",
        concept=f"{a} + {b} = {total}",
        summary="Build each number from hundreds, tens, and ones, then combine one place at a time. "
                "Ten ones trade for one ten, so no column ever holds more than nine.",
        width=700, height=380, level="101",
    )
    BLUE, ORANGE, GREEN = theme.BLUE, theme.ORANGE, theme.GREEN

    @wt.setup
    def _(c):
        for key, name, val in (("h", "hundreds", "100"), ("t", "tens", "10"), ("o", "ones", "1")):
            left, w = COLS[key]
            c.text(left + w / 2, 20, f"{name} (each = {val})", size=13, color=theme.SOFT_INK, weight="bold")
            c.line(left - 6, 34, left - 6, 352, color=theme.GRID, width=1)
        c.line(20, 252, 690, 252, color=theme.INK, width=2)
        return None

    @wt.step("Build 247 with blocks", "A flat is 100, a rod is 10, and a small cube is 1. "
             "Two flats, four rods, and seven cubes make 247.", math="247 = 200 + 40 + 7")
    def _(c):
        top = ROWS[0]
        blocks(c, top, *da, BLUE)
        c.text(92, top + H / 2, str(a), size=28, color=BLUE, anchor="end", weight="bold")
        note(c, "h", top, f"{da[0]} hundreds = {da[0] * 100}", BLUE)
        note(c, "t", top, f"{da[1]} tens = {da[1] * 10}", BLUE)
        note(c, "o", top, f"{da[2]} ones = {da[2]}", BLUE)

    @wt.step("Build 135 below it", "Line the second number up by place: hundreds under hundreds, "
             "tens under tens, ones under ones.", math="135 = 100 + 30 + 5")
    def _(c):
        top = ROWS[1]
        blocks(c, top, *db, ORANGE)
        c.text(92, top + H / 2, f"+ {b}", size=28, color=ORANGE, anchor="end", weight="bold")
        note(c, "h", top, f"{db[0]} hundred = {db[0] * 100}", ORANGE)
        note(c, "t", top, f"{db[1]} tens = {db[1] * 10}", ORANGE)
        note(c, "o", top, f"{db[2]} ones = {db[2]}", ORANGE)

    @wt.step("Add the ones", "Start on the right. Slide the seven blue cubes and the five orange "
             "cubes into the answer row. That is twelve ones, and a column holds at most nine.",
             math=f"{da[2]} + {db[2]} = {ones} ones")
    def _(c):
        fade(c, COLS["o"][0] - 4, ROWS[0] - 4, COLS["o"][1], 2 * 100 + 2)
        top = ROWS[2]
        blocks(c, top, 0, 0, da[2], BLUE)
        blocks(c, top, 0, 0, db[2], ORANGE, start=(0, 0, da[2]))
        if c.is_new:
            note(c, "o", top, f"{ones} ones: more than 9!", theme.RED)

    @wt.step("Trade ten ones for one ten", "Ten loose cubes make a crowd. Stack them into one rod "
             "and move it to the tens column. Two ones stay behind.",
             math=f"{ones} ones = {carry} ten + {ones_left} ones")
    def _(c):
        top = ROWS[2]
        x0, y0 = unit_xy(0, top)
        x1, y1 = unit_xy(9, top)
        fade(c, x0 - 2, y0 - 2, x1 + U - x0 + 4, y1 + U - y0 + 4, opacity=0.65)
        c.rect(x0 - 5, y0 - 5, x1 + U - x0 + 10, y1 + U - y0 + 10, color=GREEN, width=2, rx=4,
               dash=None if c.is_new else "4 3")
        rx = rod_x(da[1] + db[1])
        rod(c, rx, top, GREEN)
        if c.is_new:
            c.curved_arrow(x0 - 8, y0 + 8, rx + U + 4, top + 30, bend=0.35, color=GREEN, width=2.2)
            c.text(COLS["o"][0] + COLS["o"][1] / 2, top + H - 6, "10 ones = 1 ten", size=13, color=GREEN,
                   weight="bold")
        note(c, "o", top, f"{ones_left} ones", GREEN)

    @wt.step("Add the tens", "Four blue rods, three orange rods, and the traded green rod make "
             "eight tens. Eight fits, so no trade this time.",
             math=f"{da[1]} + {db[1]} + {carry} = {tens} tens")
    def _(c):
        fade(c, COLS["t"][0] - 4, ROWS[0] - 4, COLS["t"][1], 2 * 100 + 2)
        top = ROWS[2]
        blocks(c, top, 0, da[1], 0, BLUE)
        blocks(c, top, 0, db[1], 0, ORANGE, start=(0, da[1], 0))
        note(c, "t", top, f"{tens} tens = {tens * 10}", GREEN)

    @wt.step("Add the hundreds and read the answer", "Two flats and one flat make three hundreds. "
             "Read the answer row from left to right: three hundreds, eight tens, two ones.",
             math=f"{a} + {b} = {hundreds * 100} + {tens * 10} + {ones_left} = {total}")
    def _(c):
        fade(c, COLS["h"][0] - 4, ROWS[0] - 4, COLS["h"][1], 2 * 100 + 2)
        top = ROWS[2]
        blocks(c, top, da[0], 0, 0, BLUE)
        blocks(c, top, db[0], 0, 0, ORANGE, start=(da[0], 0, 0))
        note(c, "h", top, f"{hundreds} hundreds = {hundreds * 100}", GREEN)
        c.text(92, top + H / 2, str(total), size=28, color=GREEN, anchor="end", weight="bold")

    return wt
