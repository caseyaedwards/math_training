"""Factors and primes: factor trees, the factor ladder, rectangular arrays, and the sieve."""

from __future__ import annotations

import math
from collections import Counter

from .. import theme
from ..annotate import brace
from ..registry import diagram
from ..walkthrough import Walkthrough

# Each prime keeps one color in every factor diagram.
PRIME_COLOR = {2: theme.BLUE, 3: theme.ORANGE, 5: theme.GREEN, 7: theme.PURPLE}


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, int(math.isqrt(n)) + 1))


def prime_factors(n: int) -> list:
    out, d = [], 2
    while n > 1:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    return out


def power_form(n: int) -> str:
    """Returns math markup like 2^3 \\cdot 3^2 \\cdot 5."""
    cnt = Counter(prime_factors(n))
    return " \\cdot ".join(f"{p}^{k}" if k > 1 else f"{p}" for p, k in sorted(cnt.items()))


def node(c, x, y, n, r=22):
    """Draws a tree node: a colored disk for a prime, a white disk for a composite."""
    if is_prime(n):
        col = PRIME_COLOR.get(n, theme.RED)
        c.circle(x, y, r, color=col, fill=theme.fill(col, "40"), width=2.5)
        c.text(x, y, str(n), size=17, weight="bold", color=col)
    else:
        c.circle(x, y, r, color=theme.INK, fill=theme.PAPER, width=2)
        c.text(x, y, str(n), size=17, color=theme.INK)


def edge(c, a, b, r=22):
    (x1, y1), (x2, y2) = a, b
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    c.line(x1 + ux * r, y1 + uy * r, x2 - ux * r, y2 - uy * r, color=theme.SOFT_INK, width=2)


def split(c, pos, parent, kids):
    """Draws the edges and child nodes for parent = kids[0] * kids[1]. pos maps name -> (x, y, value)."""
    px, py, pv = pos[parent]
    vals = [pos[k][2] for k in kids]
    assert vals[0] * vals[1] == pv, (parent, vals)
    for k in kids:
        edge(c, (px, py), pos[k][:2])
    for k in kids:
        node(c, *pos[k])
    # the multiplication sign between the two children
    (x1, y1, _), (x2, y2, _) = pos[kids[0]], pos[kids[1]]
    c.text((x1 + x2) / 2, (y1 + y2) / 2, "×", size=16, color=theme.SOFT_INK)


def prime_row(c, primes, x0, y, gap=56, size=34):
    """Draws the sorted primes in a row of colored boxes. Returns the box centers."""
    xs = []
    for i, p in enumerate(primes):
        x = x0 + i * gap
        col = PRIME_COLOR[p]
        c.rect(x - size / 2, y - size / 2, size, size, color=col, fill=theme.fill(col, "40"), width=2, rx=6)
        c.text(x, y, str(p), size=18, weight="bold", color=col)
        if i:
            c.text(x - gap / 2, y, "×", size=16, color=theme.SOFT_INK)
        xs.append(x)
    return xs


@diagram("factor-tree", "Factor Tree", "Number Theory")
def build_tree() -> Walkthrough:
    N = 360
    primes = prime_factors(N)
    wt = Walkthrough(
        "factor-tree", "Factor Tree", "Number Theory",
        concept=f"{N} = {power_form(N)}",
        summary="Split a number into two factors, then split those, until only primes are left. "
                "Any way you split it, the same primes come out.",
        width=680, height=440, level="101",
    )
    Y = [48, 128, 208, 288]
    tree1 = {
        "r": (340, Y[0], 360),
        "a": (220, Y[1], 36), "b": (480, Y[1], 10),
        "a1": (140, Y[2], 6), "a2": (300, Y[2], 6), "b1": (430, Y[2], 2), "b2": (530, Y[2], 5),
        "c1": (100, Y[3], 2), "c2": (180, Y[3], 3), "c3": (260, Y[3], 2), "c4": (340, Y[3], 3),
    }
    leaves1 = ["c1", "c2", "c3", "c4", "b1", "b2"]
    tree2 = {
        "r": (340, Y[0], 360),
        "a": (190, Y[1], 4), "b": (480, Y[1], 90),
        "a1": (130, Y[2], 2), "a2": (250, Y[2], 2), "b1": (400, Y[2], 9), "b2": (560, Y[2], 10),
        "c1": (360, Y[3], 3), "c2": (440, Y[3], 3), "c3": (520, Y[3], 2), "c4": (600, Y[3], 5),
    }
    ROW_Y = 370
    row_x0 = 340 - (len(primes) - 1) * 28

    def ring_leaves(c, pos, names):
        for k in names:
            x, y, v = pos[k]
            c.circle(x, y, 28, color=PRIME_COLOR[v], width=1.5, dash="4 3")

    def row_with_braces(c):
        xs = prime_row(c, primes, row_x0, ROW_Y)
        cnt = Counter(primes)
        i = 0
        for p in sorted(cnt):
            k = cnt[p]
            a, b = xs[i] - 17, xs[i + k - 1] + 17
            lab = f"{p}^{k}" if k > 1 else f"{p}^1"
            brace(c, b, ROW_Y + 22, a, ROW_Y + 22, lab, color=PRIME_COLOR[p], depth=10)
            i += k
        return xs

    @wt.step("Split 360 into two factors", "Pick any two numbers that multiply to 360. Here 36 × 10 works. "
             "Neither one is prime yet, so both stay white.", math="360 = 36 \\times 10")
    def _(c):
        node(c, *tree1["r"])
        split(c, tree1, "r", ["a", "b"])
        c.text(600, Y[0], "white = not prime yet", size=13, color=theme.SOFT_INK)
        c.text(600, Y[0] + 20, "color = prime, done", size=13, color=theme.SOFT_INK)

    @wt.step("Split again", "36 = 6 × 6 and 10 = 2 × 5. The 2 and the 5 are prime, so they get a color "
             "and stop growing. Primes are the dead ends of the tree.",
             math="36 = 6 \\times 6,  10 = 2 \\times 5")
    def _(c):
        split(c, tree1, "a", ["a1", "a2"])
        split(c, tree1, "b", ["b1", "b2"])

    @wt.step("Split until every branch ends in a prime", "Each 6 splits into 2 × 3. Now every branch ends "
             "in a colored circle, so the tree is finished.", math="6 = 2 \\times 3")
    def _(c):
        split(c, tree1, "a1", ["c1", "c2"])
        split(c, tree1, "a2", ["c3", "c4"])

    @wt.step("Collect the leaves", "Gather the prime leaves and sort them. Their product is the number at "
             "the top of the tree.", math="360 = 2 \\times 2 \\times 2 \\times 3 \\times 3 \\times 5")
    def _(c):
        ring_leaves(c, tree1, leaves1)
        c.text(row_x0 - 26, ROW_Y, "360 =", size=18, anchor="end")
        prime_row(c, primes, row_x0, ROW_Y)

    @wt.step("Group repeats with exponents", "Three 2s make 2³ and two 3s make 3². "
             "This short form is the prime factorization.",
             math=f"360 = {power_form(N)} = " + " \\cdot ".join(
                 str(p ** k) for p, k in sorted(Counter(primes).items())) + f" = {N}")
    def _(c):
        row_with_braces(c)

    @wt.step("A different tree gives the same primes", "Start with 360 = 4 × 90 instead. The tree looks "
             "different, but the leaves are the same six primes. This is the Fundamental Theorem of "
             "Arithmetic, and it never makes exceptions.", math=f"360 = 4 \\times 90 = {power_form(N)}",
             fresh=True)
    def _(c):
        node(c, *tree2["r"])
        split(c, tree2, "r", ["a", "b"])
        split(c, tree2, "a", ["a1", "a2"])
        split(c, tree2, "b", ["b1", "b2"])
        split(c, tree2, "b1", ["c1", "c2"])
        split(c, tree2, "b2", ["c3", "c4"])
        ring_leaves(c, tree2, ["a1", "a2", "c1", "c2", "c3", "c4"])
        c.text(row_x0 - 26, ROW_Y, "360 =", size=18, anchor="end")
        row_with_braces(c)

    return wt


@diagram("factor-ladder", "Factor Ladder", "Number Theory")
def build_ladder() -> Walkthrough:
    N = 360
    wt = Walkthrough(
        "factor-ladder", "Factor Ladder", "Number Theory",
        concept=f"{N} = {power_form(N)}",
        summary="Divide by the smallest prime that fits, write the quotient underneath, and repeat until you reach 1. "
                "The divisors down the left side are the prime factorization.",
        width=640, height=400, level="101",
    )
    rungs = []  # (prime, number before dividing)
    n = N
    for p in prime_factors(N):
        rungs.append((p, n))
        n //= p
    X_DIV, X_NUM = 290, 360
    ROW = 50
    TOP = 52

    def rung(c, i):
        p, v = rungs[i]
        y = TOP + i * ROW
        col = PRIME_COLOR[p]
        c.text(X_DIV, y, str(p), size=20, weight="bold", color=col)
        # the ladder bracket: a line on the left of the number and under it
        c.line(X_DIV + 22, y - 18, X_DIV + 22, y + 22, color=theme.INK, width=2)
        c.line(X_DIV + 22, y + 22, X_NUM + 70, y + 22, color=theme.INK, width=2)
        c.text(X_NUM, y, str(v), size=20, anchor="start")
        c.text(X_NUM + 110, y + ROW / 2, f"{v} ÷ {p} = {v // p}", size=13, color=theme.SOFT_INK, anchor="start")

    def quotient(c, i):
        p, v = rungs[i]
        y = TOP + (i + 1) * ROW
        c.text(X_NUM, y, str(v // p), size=20, anchor="start", color=theme.GREEN if v // p == 1 else theme.INK)

    @wt.step("Divide by the smallest prime", "360 is even, so 2 goes into it. Write 2 on the left and the "
             "quotient 180 underneath.", math="360 \\div 2 = 180")
    def _(c):
        rung(c, 0)
        quotient(c, 0)
        if c.is_new:
            c.text(X_DIV - 24, TOP, "prime divisor →", size=13, color=theme.BLUE, anchor="end")
            c.text(X_NUM + 50, TOP + ROW, "← quotient goes below", size=13, color=theme.SOFT_INK, anchor="start")
            c.text(X_NUM + 30, TOP - 28, "number to split", size=13, color=theme.SOFT_INK)
    @wt.step("Keep dividing by 2 while you can", "180 and 90 are still even. After three 2s you reach 45, "
             "which is odd, so 2 is out of moves.", math="180 \\div 2 = 90,  90 \\div 2 = 45")
    def _(c):
        for i in (1, 2):
            rung(c, i)
            quotient(c, i)

    @wt.step("Move up to 3, then 5", "45 = 3 × 15 and 15 = 3 × 5. Then 5 ÷ 5 = 1. "
             "Reaching 1 means the ladder is done.", math="45 \\div 3 = 15,  15 \\div 3 = 5,  5 \\div 5 = 1")
    def _(c):
        for i in range(3, len(rungs)):
            rung(c, i)
            quotient(c, i)
        y = TOP + len(rungs) * ROW
        c.text(X_NUM + 40, y, "← stop at 1", size=14, color=theme.GREEN, anchor="start")

    @wt.step("Read down the left side", "The divisors on the left are the primes. Group the repeats with "
             "exponents. Same answer as the factor tree, with less climbing.",
             math=f"360 = 2 \\cdot 2 \\cdot 2 \\cdot 3 \\cdot 3 \\cdot 5 = {power_form(N)}")
    def _(c):
        y0, y1 = TOP - 22, TOP + (len(rungs) - 1) * ROW + 22
        c.rect(X_DIV - 20, y0, 40, y1 - y0, color=theme.INK, width=1.5, rx=8, dash="5 4")
        cnt = Counter(prime_factors(N))
        i = 0
        for p in sorted(cnt):
            k = cnt[p]
            ya, yb = TOP + i * ROW - 18, TOP + (i + k - 1) * ROW + 18
            lab = f"{p}^{k}" if k > 1 else f"{p}^1"
            brace(c, X_DIV - 28, yb, X_DIV - 28, ya, lab, color=PRIME_COLOR[p], depth=12)
            i += k
        c.label_box(120, TOP + len(rungs) * ROW, f"360 = {power_form(N)}", math=True,
                    color=theme.INK, border=theme.INK, size=18)

    return wt


@diagram("factor-arrays", "Factors as Rectangles", "Number Theory")
def build_arrays() -> Walkthrough:
    N, P = 12, 7
    pairs = [(a, N // a) for a in range(1, N + 1) if N % a == 0 and a <= N // a]
    factors = [a for a in range(1, N + 1) if N % a == 0]
    wt = Walkthrough(
        "factor-arrays", "Factors as Rectangles", "Number Theory",
        concept="12 = 1 \\times 12 = 2 \\times 6 = 3 \\times 4,  7 = 1 \\times 7 only",
        summary="Arrange tiles into a full rectangle. Every rectangle you can build gives a factor pair. "
                "A prime number only fits in a single row.",
        width=680, height=440, level="101",
    )
    S = 22  # tile size
    ROWC, COLC = theme.ORANGE, theme.BLUE

    def array(c, x, y, rows, cols, fill=theme.BLUE, extra=0, label=True):
        """Draws rows x cols tiles at top-left (x, y), plus `extra` leftover tiles in red."""
        for r in range(rows):
            for k in range(cols):
                c.rect(x + k * S, y + r * S, S, S, color=theme.PAPER, fill=theme.fill(fill, "80"), width=2)
        for e in range(extra):
            c.rect(x + (cols + 0) * S if rows == 0 else x + cols * S, y + e * S, S, S, color=theme.RED,
                   fill=theme.fill(theme.RED, "33"), width=2, dash="3 2")
        if label:
            c.text(x - 10, y + rows * S / 2, str(rows), size=15, color=ROWC, anchor="end", weight="bold")
            c.text(x + cols * S / 2, y - 12, str(cols), size=15, color=COLC, weight="bold")

    tops = {1: (64, 50), 2: (64, 130), 3: (250, 120)}

    @wt.step("One long row", "Twelve tiles fit in one row of 12. That gives the factor pair 1 × 12. "
             "Every number has this boring rectangle.", math="1 \\times 12 = 12")
    def _(c):
        x, y = tops[1]
        array(c, x, y, 1, 12)
        c.text(x + 12 * S + 16, y + S / 2, "1 × 12", size=16, anchor="start", math=True)
        c.text(x - 16, y - 30, "rows ↓", size=12, color=ROWC)
        c.text(x + 12 * S / 2 + 40, y - 12, "← columns", size=12, color=COLC, anchor="start")

    @wt.step("Two rows", "Fold the row in half: 2 rows of 6, with no tile left over. So 2 and 6 are factors.",
             math="2 \\times 6 = 12")
    def _(c):
        x, y = tops[2]
        array(c, x, y, 2, 6)
        c.text(x + 6 * S / 2, y + 2 * S + 18, "2 × 6", size=16, math=True)

    @wt.step("Three rows", "Three rows of 4 also fill a rectangle. Four rows of 3 is the same rectangle "
             "turned on its side, so it adds no new pair.", math="3 \\times 4 = 12")
    def _(c):
        x, y = tops[3]
        array(c, x, y, 3, 4)
        c.text(x + 4 * S / 2, y + 3 * S + 18, "3 × 4", size=16, math=True)

    @wt.step("List the factors of 12", "Each rectangle gives two factors. Twelve has six factors, more than "
             "two, so 12 is composite.",
             math=f"factors of 12: {', '.join(map(str, factors))}")
    def _(c):
        x, y = 400, 110
        c.rect(x, y, 260, 104, color=theme.BLUE, fill=theme.PAPER, width=1.5, rx=8)
        c.text(x + 130, y + 18, "factor pairs of 12", size=13, color=theme.SOFT_INK)
        c.text(x + 130, y + 42, ", ".join(f"{a} × {b}" for a, b in pairs), size=16, color=theme.BLUE,
               weight="bold")
        c.text(x + 130, y + 66, "factors: " + ", ".join(map(str, factors)), size=14, color=theme.INK)
        c.text(x + 130, y + 88, f"{len(factors)} factors, so 12 is composite", size=14, color=theme.BLUE)

    LY = 260

    @wt.step("Now try 7", "Seven tiles fit in one row of 7. So far 7 looks like any other number.",
             math="1 \\times 7 = 7")
    def _(c):
        c.line(20, LY - 30, 660, LY - 30, color=theme.GRID, width=1.5)
        array(c, 64, LY + 20, 1, 7, fill=theme.GREEN)
        c.text(64 + 7 * S / 2, LY + 20 + S + 18, "1 × 7", size=16, math=True)

    @wt.step("Other rows leave leftovers", "Two rows of 3 leave 1 tile over. Three rows of 2 also leave "
             "1 over. Rows of 4, 5, or 6 fail too. The odd tile out refuses to join any rectangle.",
             math="7 = 2 \\times 3 + 1 = 3 \\times 2 + 1")
    def _(c):
        for x, rows in ((270, 2), (470, 3)):
            cols = P // rows
            left = P - rows * cols
            y = LY + 20
            array(c, x, y, rows, cols, fill=theme.GREEN)
            for e in range(left):
                c.rect(x + cols * S + 4, y + e * S, S, S, color=theme.RED, fill=theme.fill(theme.RED, "33"),
                       width=2, dash="3 2")
            c.text(x + cols * S + 40, y + S / 2, f"{left} left over", size=13, color=theme.RED, anchor="start")
            c.text(x + cols * S / 2, y + rows * S + 18, f"{rows} × {cols} + {left}", size=15, math=True,
                   color=theme.RED)

    @wt.step("A prime has one rectangle", "The only rectangle for 7 is 1 × 7. A number whose only factors "
             "are 1 and itself is prime.", math="factors of 7: 1, 7  \\implies  7 is prime")
    def _(c):
        c.label_box(150, LY + 120, "only 1 × 7 works: 7 is prime", color=theme.GREEN, border=theme.GREEN,
                    size=15)
        c.label_box(520, 420 - 14 - 0, "12 has 6 factors, 7 has 2", color=theme.SOFT_INK, border=theme.MUTED,
                    size=13)

    return wt


@diagram("sieve-of-eratosthenes", "Sieve of Eratosthenes", "Number Theory")
def build_sieve() -> Walkthrough:
    N = 100
    sieve_primes = [p for p in range(2, int(math.isqrt(N)) + 1) if is_prime(p)]
    crossed = {}  # number -> prime that crossed it out first
    counts = {}
    for p in sieve_primes:
        counts[p] = 0
        for m in range(p * p, N + 1, p):
            if m not in crossed:
                crossed[m] = p
                counts[p] += 1
    primes = [n for n in range(2, N + 1) if n not in crossed]
    assert primes == [n for n in range(2, N + 1) if is_prime(n)]
    COL = {2: theme.BLUE, 3: theme.ORANGE, 5: theme.PURPLE, 7: theme.RED}
    nxt = next(p for p in range(max(sieve_primes) + 1, N) if is_prime(p))

    wt = Walkthrough(
        "sieve-of-eratosthenes", "Sieve of Eratosthenes", "Number Theory",
        concept=f"cross out multiples of 2, 3, 5, 7  \\implies  {len(primes)} primes below 100",
        summary="Circle the next number that is not crossed out, then cross out its multiples. "
                "Whatever survives is prime.",
        width=700, height=420, level="101",
    )
    X0, Y0, S = 24, 24, 37
    LX = 420

    def cell(n):
        r, k = divmod(n - 1, 10)
        return X0 + k * S, Y0 + r * S

    @wt.setup
    def _(c):
        for n in range(1, N + 1):
            x, y = cell(n)
            c.rect(x, y, S, S, color=theme.GRID, fill=theme.PAPER, width=1)
            c.text(x + S / 2, y + S / 2, str(n), size=14)
        return None

    def strike(c, n, col, strong):
        x, y = cell(n)
        c.rect(x + 1, y + 1, S - 2, S - 2, color="none", fill=theme.fill(col, "40" if strong else "22"))
        c.line(x + 6, y + S - 6, x + S - 6, y + 6, color=col, width=2 if strong else 1.4)

    def ring(c, n, col):
        x, y = cell(n)
        c.circle(x + S / 2, y + S / 2, S / 2 - 3, color=col, width=2.5)

    def legend(c, i, col, text, sub=None):
        y = 40 + i * 52
        c.rect(LX, y - 10, 20, 20, color=col, fill=theme.fill(col, "40"), width=1.5, rx=3)
        c.text(LX + 32, y, text, size=15, anchor="start", color=col, weight="bold")
        if sub:
            c.text(LX + 32, y + 20, sub, size=13, anchor="start", color=theme.SOFT_INK)

    @wt.step("Cross out 1", "Write 1 to 100 in a grid. The number 1 is not prime, since a prime needs "
             "exactly two factors and 1 has only one.", math="1 is not prime")
    def _(c):
        strike(c, 1, theme.SOFT_INK, True)
        legend(c, 0, theme.SOFT_INK, "1: not prime", "only one factor")

    def prime_step(p, i):
        first = p * p

        def draw(c):
            ring(c, p, COL[p])
            for m, q in crossed.items():
                if q == p:
                    strike(c, m, COL[p], c.is_new)
            legend(c, i, COL[p], f"{p}: crosses out {counts[p]}",
                   f"start at {p}² = {first}, step by {p}")
        return draw

    texts = {
        2: ("Circle 2, cross out its multiples", "Two is prime. Every other even number is a multiple of 2, "
            "so cross out 4, 6, 8, and so on. Half the grid goes in one move."),
        3: ("Circle 3, cross out its multiples", "Three is the next survivor, so it is prime. Start crossing "
            "at 9, since 6 is already gone. Many multiples of 3 were crossed by 2 already."),
        5: ("Circle 5, cross out its multiples", "Start at 25. Smaller multiples of 5, like 10, 15, and 20, "
            "already fell to 2 or 3."),
        7: ("Circle 7, cross out its multiples", "Start at 49. Only three new numbers fall: 49, 77, and 91. "
            "The sieve is running out of work."),
    }
    for i, p in enumerate(sieve_primes, 1):
        title, text = texts[p]
        new = sorted(m for m, q in crossed.items() if q == p)
        shown = ", ".join(map(str, new[:3])) + (", \\ldots" if len(new) > 3 else "")
        wt.step(title, text, math=f"new crossings: {shown}  ({counts[p]} in all)")(prime_step(p, i))

    @wt.step("Stop at the square root", f"The next prime is {nxt}, but {nxt}² = {nxt * nxt} is past 100. Any "
             "composite number up to 100 has a factor of 10 or less, so it is already crossed out. "
             "Every survivor is prime.", math=f"{len(primes)} primes from 2 to 97")
    def _(c):
        for n in primes:
            if n not in COL:
                ring(c, n, theme.GREEN)
        legend(c, len(sieve_primes) + 1, theme.GREEN, f"{len(primes)} primes survive",
               f"{nxt}² = {nxt * nxt} > 100: stop")

    return wt
