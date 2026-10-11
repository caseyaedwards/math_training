"""Order of operations: an expression as a tree, evaluated from the bottom up."""

from __future__ import annotations

import math

from .. import theme
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._kit import rich, tag

PAREN, EXP, MUL, ADD = theme.BLUE, theme.ORANGE, theme.GREEN, theme.PURPLE

# node: (x, y, label, children)
NODES = {
    "plus": (250, 112, "+", ["n3", "times"]),
    "n3": (120, 190, "3", []),
    "times": (380, 190, "×", ["n4", "pow"]),
    "n4": (290, 270, "4", []),
    "pow": (470, 270, "^", ["minus", "e2"]),
    "minus": (400, 350, "−", ["n6", "n2"]),
    "e2": (560, 350, "2", []),
    "n6": (330, 428, "6", []),
    "n2": (470, 428, "2", []),
}


def node(c, key, color=theme.INK, fill=theme.PAPER):
    x, y, s, kids = NODES[key]
    if kids:
        c.circle(x, y, 21, color=color, fill=fill, width=2.4)
        c.text(x, y + (7 if s == "^" else 0), s, size=28 if s == "^" else 22, color=theme.PAPER if fill != theme.PAPER else color,
               weight="bold")
    else:
        c.rect(x - 19, y - 16, 38, 32, color=color, fill=fill, width=2, rx=6)
        c.text(x, y, s, size=19, color=color, weight="bold", font="serif")


def edges(c, key, color=theme.MUTED, width=2):
    x, y, _s, kids = NODES[key]
    for k in kids:
        kx, ky, _t, kk = NODES[k]
        L = math.hypot(kx - x, ky - y)
        ux, uy = (kx - x) / L, (ky - y) / L
        r1, r2 = 22, (22 if kk else 18)
        c.line(x + ux * r1, y + uy * r1, kx - ux * r2, ky - uy * r2, color=color, width=width)


def evaluate(key):
    x, y, s, kids = NODES[key]
    if not kids:
        return int(s)
    a, b = (evaluate(k) for k in kids)
    return {"+": a + b, "×": a * b, "^": a ** b, "−": a - b}[s]


@diagram("order-of-operations-tree", "Order of Operations as a Tree", "Arithmetic")
def build() -> Walkthrough:
    v_minus, v_pow, v_times, v_plus = (evaluate(k) for k in ("minus", "pow", "times", "plus"))
    assert v_plus == 3 + 4 * (6 - 2) ** 2

    wt = Walkthrough(
        "order-of-operations-tree", "Order of Operations as a Tree", "Arithmetic",
        concept=f"3 + 4 \\times (6 - 2)^2 = 3 + 4 \\times 16 = {v_plus}",
        summary="Draw the expression as a tree: each operation sits above the two things it works on. "
                "Evaluate from the leaves up, and the order of operations takes care of itself.",
        width=700, height=456, level="101",
    )
    chain = [
        [("3 + 4 \\times (6 - 2)^2", theme.INK)],
        [("3 + 4 \\times ", theme.INK), (str(v_minus), PAREN), ("^2", theme.INK)],
        [("3 + 4 \\times ", theme.INK), (str(v_pow), EXP)],
        [("3 + ", theme.INK), (str(v_times), MUL)],
        [(str(v_plus), ADD)],
    ]

    def show_chain(c):
        seq = []
        for i, p in enumerate(chain[: c.step_index + 1]):
            if i:
                seq.append((" = ", theme.SOFT_INK))
            seq.extend(p)
        if c.is_new:
            rich(c, 24, 36, seq, size=21, anchor="start")

    rules = [("1", "( ) parentheses", PAREN), ("2", "exponents", EXP), ("3", "× and ÷", MUL), ("4", "+ and −", ADD)]

    def rule_box(c, i, on):
        n, s, color = rules[i]
        y = 108 + i * 34
        c.rect(546, y - 14, 140, 28, color=color, fill=color if on else theme.PAPER, rx=6, width=1.6)
        c.text(558, y, f"{n}. {s}", size=14, color=theme.PAPER if on else color, anchor="start", weight="bold")

    def mark(c, key, color, value, dx, dy):
        x, y, _s, kids = NODES[key]
        edges(c, key, color=color, width=3)
        for k in kids:
            if not NODES[k][3]:
                node(c, k, color=color)
        node(c, key, color=color, fill=color)
        tag(c, x + dx, y + dy, f"= {value}", color, size=17)

    @wt.setup
    def _(c):
        c.text(616, 80, "who goes first", size=13, color=theme.SOFT_INK, weight="bold")
        c.arrow(40, 424, 40, 142, color=theme.MUTED, width=2)
        c.text(58, 285, "work from the bottom up", size=13, color=theme.SOFT_INK, transform="rotate(-90 58 285)")
        c.text(40, 438, "first", size=12, color=theme.SOFT_INK)
        c.text(40, 128, "last", size=12, color=theme.SOFT_INK)
        return None

    @wt.step("Turn the expression into a tree", "Each operation sits above the two numbers it "
             "combines. Lower in the tree means sooner, so work from the bottom up.",
             math="3 + 4 \\times (6 - 2)^2 = ?")
    def _(c):
        for key in NODES:
            edges(c, key)
        for key in NODES:
            node(c, key)
        for i in range(4):
            rule_box(c, i, False)
        show_chain(c)

    @wt.step("Parentheses first", "The subtraction sits at the bottom, inside the parentheses. "
             "Six minus 2 is 4, and that 4 travels up the tree.", math=f"6 - 2 = {v_minus}")
    def _(c):
        mark(c, "minus", PAREN, v_minus, 54, 0)
        if c.is_new:
            rule_box(c, 0, True)
        show_chain(c)

    @wt.step("Exponent next", "The power node squares the 4 it received. Four squared is 16, not 8: "
             "an exponent is repeated multiplication.", math=f"{v_minus}^2 = {v_minus} \\times {v_minus} = {v_pow}")
    def _(c):
        mark(c, "pow", EXP, v_pow, 30, -36)
        if c.is_new:
            rule_box(c, 1, True)
        show_chain(c)

    @wt.step("Then multiply", "The times node gets 4 from the left and 16 from the right. "
             "Four times 16 is 64.", math=f"4 \\times {v_pow} = {v_times}")
    def _(c):
        mark(c, "times", MUL, v_times, 36, -34)
        if c.is_new:
            rule_box(c, 2, True)
        show_chain(c)

    @wt.step("Add last, at the top", "The root waits for everything below it. Three plus 64 is 67. "
             "Adding first gives 7 × 16 = 112, a wrong answer said with great confidence.", math=f"3 + {v_times} = {v_plus}")
    def _(c):
        mark(c, "plus", ADD, v_plus, 36, -34)
        if c.is_new:
            rule_box(c, 3, True)
        show_chain(c)

    return wt
