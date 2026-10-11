"""Statistics diagrams: center, spread, shape, the normal curve, regression, and sampling distributions."""

from __future__ import annotations

import math
import random
from typing import List

from .. import theme
from ..annotate import brace
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough

MEAN_C = theme.BLUE
MEDIAN_C = theme.ORANGE


def num(v: float, nd: int = 2) -> str:
    """Formats a number without trailing zeros, with a real minus sign."""
    if abs(v - round(v)) < 1e-9:
        s = str(int(round(v)))
    else:
        s = f"{v:.{nd}f}".rstrip("0").rstrip(".")
    return s.replace("-", "−")


def median(xs: List[float]) -> float:
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def axis_line(c, X, y, lo, hi, step=1, label_every=1, size=12, color=theme.INK):
    """Draws a plain horizontal axis with ticks and numbers under it."""
    c.line(X(lo) - 8, y, X(hi) + 8, y, color=color, width=1.6)
    k = 0
    v = lo
    while v <= hi + 1e-9:
        c.line(X(v), y, X(v), y + 5, color=color, width=1.2)
        if k % label_every == 0:
            c.text(X(v), y + 17, num(v), size=size, color=theme.SOFT_INK)
        v += step
        k += 1


# ---------------------------------------------------------------------------
# Mean as balance point, median as middle
# ---------------------------------------------------------------------------

BAL_DATA = [2, 3, 3, 4, 5, 6, 12]


@diagram("mean-median-balance", "Mean and Median", "Statistics")
def mean_median() -> Walkthrough:
    data = sorted(BAL_DATA)
    n = len(data)
    mu = sum(data) / n
    med = median(data)
    left = [mu - v for v in data if v < mu]
    right = [v - mu for v in data if v > mu]
    wt = Walkthrough(
        "mean-median-balance", "Mean and Median", "Statistics",
        concept="median = middle value;  mean = balance point = (\\sum x)/n",
        summary="The median is the middle value once the data is sorted. The mean is the point where a "
                "dot plot balances, so a far-out value pulls the mean toward it and leaves the median alone.",
        width=700, height=420, level="301",
    )
    X = lambda v: 50 + v * 46
    BEAM = 320
    ROW0, ROWH = 150, 16

    def dot_y(i):
        v = data[i]
        j = data[:i].count(v)
        return BEAM - 14 - j * 22

    @wt.setup
    def _(c):
        c.line(X(0) - 10, BEAM, X(13) + 10, BEAM, color=theme.INK, width=4)
        for v in range(14):
            c.line(X(v), BEAM + 2, X(v), BEAM + 8, color=theme.INK, width=1.2)
            c.text(X(v), BEAM + 20, str(v), size=12, color=theme.SOFT_INK)
        return None

    def cell_x(i):
        return 350 - (n / 2) * 42 + i * 42

    @wt.step("Sort the data and plot it", f"Seven values, sorted from small to large, sit above the "
             "number line. Each dot is one value, and repeats stack up.",
             math="data: " + ", ".join(map(str, data)))
    def _(c):
        c.text(350, 22, "sorted data", size=12, color=theme.SOFT_INK)
        for i, v in enumerate(data):
            c.rect(cell_x(i), 34, 40, 30, color=theme.MUTED, fill=theme.PANEL, width=1, rx=4)
            c.text(cell_x(i) + 20, 49, str(v), size=16, weight="bold")
            c.dot(X(v), dot_y(i), r=8, color=theme.INK)

    mi = n // 2

    @wt.step("Find the median in the middle", f"Count in from both ends. Three values sit below the middle "
             f"one and three sit above it, so the median is {num(med)}.", math=f"median = {num(med)}")
    def _(c):
        c.rect(cell_x(mi), 34, 40, 30, color=MEDIAN_C, fill=theme.fill(MEDIAN_C, "55"), width=2.5, rx=4)
        c.text(cell_x(mi) + 20, 49, str(data[mi]), size=16, weight="bold", color=theme.INK)
        brace(c, cell_x(mi) - 2, 70, cell_x(0), 70, label="3 below", color=theme.SOFT_INK, size=12,
              math_label=False, depth=8)
        brace(c, cell_x(n), 70, cell_x(mi + 1) + 2, 70, label="3 above", color=theme.SOFT_INK, size=12,
              math_label=False, depth=8)
        c.line(X(med), BEAM - 4, X(med), BEAM - 58, color=MEDIAN_C, width=2.5, dash="5 3")
        c.polygon([(X(med), BEAM + 30), (X(med) - 7, BEAM + 42), (X(med) + 7, BEAM + 42)], color="none",
                  fill=MEDIAN_C)
        c.text(X(med) - 10, BEAM + 56, f"median {num(med)}", size=13, color=MEDIAN_C, weight="bold",
               anchor="end")

    @wt.step("Balance the beam at the mean", f"Add the values and divide by {n}. A fulcrum at "
             f"{num(mu)} holds the beam level, as if every dot weighed the same.",
             math=f"mean = {sum(data)}/{n} = {num(mu)}")
    def _(c):
        c.polygon([(X(mu), BEAM + 3), (X(mu) - 20, BEAM + 40), (X(mu) + 20, BEAM + 40)], color=MEAN_C,
                  fill=theme.fill(MEAN_C, "55"), width=2)
        c.text(X(mu), BEAM + 56, f"mean {num(mu)}", size=13, color=MEAN_C, weight="bold")
        if c.is_new:
            c.math(350, 160, " + ".join(map(str, data)) + f" = {sum(data)}", size=18)
            c.math(350, 196, f"{sum(data)} \\div {n} = {num(mu)}", size=18, color=MEAN_C)
        for i, v in enumerate(data):
            c.dot(X(v), dot_y(i), r=8, color=theme.INK)

    @wt.step("Check that the pulls cancel", "Measure how far each dot sits from the mean. The total "
             "distance on the left equals the total on the right, which is why the beam balances.",
             math=" + ".join(num(d) for d in left) + f" = {num(sum(left))} = "
                  + " + ".join(num(d) for d in right))
    def _(c):
        for i, v in enumerate(data):
            y = ROW0 + i * ROWH
            if v == mu:
                c.dot(X(v), y, r=3, color=theme.SOFT_INK)
                continue
            col = theme.PURPLE if v < mu else theme.GREEN
            c.line(X(mu), y, X(v), y, color=col, width=5)
            c.text(X(v) + (-8 if v < mu else 8), y, num(abs(v - mu)), size=12, color=col, weight="bold",
                   anchor="end" if v < mu else "start")
        c.line(X(mu), ROW0 - 10, X(mu), ROW0 + n * ROWH - 6, color=MEAN_C, width=1.5)
        c.text(X(0), ROW0 + 2 * ROWH, f"left pull: {num(sum(left))}", size=14, color=theme.PURPLE,
               weight="bold", anchor="start")
        c.text(X(13), ROW0 + 2 * ROWH, f"right pull: {num(sum(right))}", size=14, color=theme.GREEN,
               weight="bold", anchor="end")

    @wt.step("See the outlier pull the mean", "The lone 12 sits far out, so it pulls the mean right of "
             "the median. Move it to 100 and the mean jumps; the median does not even blink.",
             math=f"mean = {num(mu)} > median = {num(med)}")
    def _(c):
        c.curved_arrow(X(12), BEAM + 32, X(mu) + 26, BEAM + 36, bend=0.18, color=theme.RED, width=2)
        c.text((X(12) + X(mu)) / 2 + 20, BEAM + 82, "the 12 drags the mean to the right", size=13,
               color=theme.RED, weight="bold", halo=True)

    return wt


@diagram("mean-fair-share", "The Mean as a Fair Share", "Statistics")
def mean_fair_share() -> Walkthrough:
    """Alternate view of the mean: level the bars by moving extra height to short bars."""
    data = list(BAL_DATA)
    n = len(data)
    total = sum(data)
    mu = total / n
    wt = Walkthrough(
        "mean-fair-share", "The Mean as a Fair Share", "Statistics",
        concept="mean = (\\sum x)/n",
        summary="The mean is what each value gets if you pool the total and share it out evenly. Cut the "
                "extra off the tall bars and use it to fill the short ones.",
        width=680, height=380, level="301",
    )
    U, BASE, BW, GAP, X0 = 24, 330, 56, 30, 60

    def bx(i):
        return X0 + i * (BW + GAP)

    @wt.setup
    def _(c):
        c.line(X0 - 14, BASE, bx(n - 1) + BW + 14, BASE, color=theme.INK, width=1.6)
        for k in range(0, 13, 2):
            c.text(X0 - 22, BASE - k * U, str(k), size=12, color=theme.SOFT_INK, anchor="end")
            c.line(X0 - 16, BASE - k * U, X0 - 12, BASE - k * U, color=theme.INK, width=1)
        return None

    @wt.step("Draw each value as a bar", f"Seven bars with heights {', '.join(map(str, data))}. They "
             "are far from even.", math=f"total = {' + '.join(map(str, data))} = {total}")
    def _(c):
        for i, v in enumerate(data):
            for k in range(v):
                c.rect(bx(i), BASE - (k + 1) * U, BW, U - 2, color="none", fill=theme.fill(theme.BLUE, "77"))
            c.text(bx(i) + BW / 2, BASE + 16, str(v), size=14, weight="bold")

    @wt.step("Draw the fair share line", f"Share {total} blocks among {n} bars and each gets {num(mu)}. "
             "Draw that level across all bars.", math=f"{total}/{n} = {num(mu)}")
    def _(c):
        y = BASE - mu * U
        c.line(X0 - 10, y, bx(n - 1) + BW + 10, y, color=MEAN_C, width=2.5, dash="8 5")
        c.text(bx(4) + BW / 2, y - 14, f"mean {num(mu)}", size=13, color=MEAN_C, weight="bold", halo=True)

    @wt.step("Mark extra and missing blocks", "Blocks above the line are extra (red). Gaps below it are "
             "missing (dashed). The counts match, which is the whole trick.",
             math=f"extra = {num(sum(v - mu for v in data if v > mu))} = missing")
    def _(c):
        for i, v in enumerate(data):
            if v > mu:
                for k in range(int(mu), v):
                    c.rect(bx(i), BASE - (k + 1) * U, BW, U - 2, color="none", fill=theme.RED)
                c.text(bx(i) + BW / 2, BASE - v * U - 12, f"+{num(v - mu)}", size=13, color=theme.RED,
                       weight="bold")
            elif v < mu:
                for k in range(v, int(mu)):
                    c.rect(bx(i) + 1, BASE - (k + 1) * U + 1, BW - 2, U - 4, color=theme.GREEN, width=1.5,
                           dash="4 3")
                c.text(bx(i) + BW / 2, BASE - mu * U - 12, f"−{num(mu - v)}", size=13, color=theme.GREEN,
                       weight="bold", halo=True)

    @wt.step("Move the blocks to level the bars", f"Cut the extra blocks (now dashed) and drop them into the gaps. Every bar ends at "
             f"{num(mu)}, and the total stays {total}.", math=f"{n} \\times {num(mu)} = {total}", fresh=True)
    def _(c):
        for i, v in enumerate(data):
            for k in range(int(mu)):
                moved = k >= v
                c.rect(bx(i), BASE - (k + 1) * U, BW, U - 2, color="none",
                       fill=theme.RED if moved else theme.fill(theme.BLUE, "77"))
            for k in range(int(mu), v):
                c.rect(bx(i) + 1, BASE - (k + 1) * U + 1, BW - 2, U - 4, color=theme.RED, width=1.2, dash="4 3")
            c.text(bx(i) + BW / 2, BASE + 16, f"{v}→{num(mu)}", size=13, weight="bold")
        y = BASE - mu * U
        c.line(X0 - 10, y, bx(n - 1) + BW + 10, y, color=MEAN_C, width=2.5, dash="8 5")
        c.label_box(340, 60, f"every bar = mean = {num(mu)}", color=MEAN_C, border=MEAN_C, size=15)

    return wt


# ---------------------------------------------------------------------------
# Box plot
# ---------------------------------------------------------------------------

BOX_DATA = [14, 3, 10, 18, 7, 31, 11, 9, 15, 5, 13, 10, 16, 8, 12]


@diagram("box-plot", "Box Plots", "Statistics")
def box_plot() -> Walkthrough:
    data = sorted(BOX_DATA)
    n = len(data)
    mid = n // 2
    q2 = median(data)
    lower, upper = data[:mid], data[mid + 1:]
    q1, q3 = median(lower), median(upper)
    iqr = q3 - q1
    lo_f, hi_f = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    inside = [v for v in data if lo_f <= v <= hi_f]
    outl = [v for v in data if v < lo_f or v > hi_f]
    wmin, wmax = min(inside), max(inside)
    wt = Walkthrough(
        "box-plot", "Box Plots", "Statistics",
        concept="IQR = Q_3 - Q_1;  outlier if beyond Q_3 + 1.5 IQR  or  Q_1 - 1.5 IQR",
        summary="Sort the data, split it at the median, and split each half again to get the quartiles. "
                "The box spans the middle half, whiskers reach the furthest ordinary values, and anything "
                "past 1.5 IQR from the box is flagged.",
        width=700, height=380, level="301",
    )
    CW, CX0, CY = 40, 50, 40
    X = lambda v: 50 + (v + 5) * 15
    AX, BT, BB = 330, 222, 276
    BMID = (BT + BB) / 2

    def cx(i):
        return CX0 + i * CW + CW / 2

    def cell(c, i, color=None, fill=None):
        c.rect(CX0 + i * CW + 1, CY, CW - 2, 28, color=color or theme.MUTED, fill=fill or theme.PANEL,
               width=2 if color else 1, rx=4)
        c.text(cx(i), CY + 14, str(data[i]), size=15, weight="bold")

    i_q1 = (len(lower) - 1) // 2
    i_q3 = mid + 1 + (len(upper) - 1) // 2

    @wt.setup
    def _(c):
        axis_line(c, X, AX, -5, 35, step=5)
        return None

    @wt.step("Sort the data", f"Write the {n} values from smallest to largest. Number the positions so "
             "the middle is easy to find.", math=f"n = {n}")
    def _(c):
        for i in range(n):
            c.text(cx(i), CY - 12, str(i + 1), size=10, color=theme.SOFT_INK)
            cell(c, i)

    @wt.step("Find the median", f"Position {mid + 1} sits in the middle, with {mid} values on each side. "
             f"Its value is the median, Q2.", math=f"Q_2 = {num(q2)}")
    def _(c):
        cell(c, mid, MEDIAN_C, theme.fill(MEDIAN_C, "55"))
        c.text(cx(mid), CY + 46, f"Q2 = {num(q2)}", size=13, color=MEDIAN_C, weight="bold")
        c.dot(X(q2), AX, r=6, color=MEDIAN_C)

    @wt.step("Find the quartiles", "Take the median of each half, leaving Q2 out. These are Q1 and Q3: a "
             "quarter of the data sits below Q1 and a quarter above Q3.",
             math=f"Q_1 = {num(q1)},  Q_3 = {num(q3)}")
    def _(c):
        cell(c, i_q1, MEAN_C, theme.fill(MEAN_C, "44"))
        cell(c, i_q3, MEAN_C, theme.fill(MEAN_C, "44"))
        brace(c, CX0 + mid * CW - 2, CY + 34, CX0 + 2, CY + 34, color=theme.SOFT_INK, depth=10)
        brace(c, CX0 + n * CW - 2, CY + 34, CX0 + (mid + 1) * CW + 2, CY + 34, color=theme.SOFT_INK, depth=10)
        c.text(cx(i_q1), CY + 64, f"Q1 = {num(q1)}", size=13, color=MEAN_C, weight="bold")
        for v in (q1, q3):
            c.dot(X(v), AX, r=6, color=MEAN_C)
        c.text(cx(i_q3), CY + 64, f"Q3 = {num(q3)}", size=13, color=MEAN_C, weight="bold")
        c.text(cx(1), CY + 82, "lower half", size=11, color=theme.SOFT_INK)
        c.text(cx(n - 2), CY + 82, "upper half", size=11, color=theme.SOFT_INK)

    @wt.step("Draw the box", "On a number line, draw a box from Q1 to Q3 with a line at the median. The "
             "box holds the middle half of the data; its width is the IQR.",
             math=f"IQR = {num(q3)} - {num(q1)} = {num(iqr)}")
    def _(c):
        c.rect(X(q1), BT, X(q3) - X(q1), BB - BT, color=MEAN_C, fill=theme.fill(MEAN_C, "33"), width=2.5)
        c.line(X(q2), BT, X(q2), BB, color=MEDIAN_C, width=3.5)
        brace(c, X(q1), BT - 6, X(q3), BT - 6, label=f"IQR = {num(iqr)}", color=MEAN_C, depth=9, size=13,
              math_label=False)
        for v, lab in ((q1, "Q1"), (q2, "Q2"), (q3, "Q3")):
            c.text(X(v), BB + 12, lab, size=11, color=MEDIAN_C if v == q2 else MEAN_C, weight="bold")

    @wt.step("Set the outlier fences", "Step 1.5 IQR out from each end of the box. Values past these "
             "fences count as outliers.",
             math=f"{num(q1)} - 1.5 \\times {num(iqr)} = {num(lo_f)};  {num(q3)} + 1.5 \\times {num(iqr)} = "
                  f"{num(hi_f)}")
    def _(c):
        for f in (lo_f, hi_f):
            c.line(X(f), 150, X(f), AX, color=theme.RED, width=2, dash="6 4")
            c.text(X(f), 140, f"fence {num(f)}", size=12, color=theme.RED, weight="bold")
        y = 176
        c.arrow(X(q3), y, X(hi_f), y, color=theme.RED, width=1.4, both=True)
        c.text((X(q3) + X(hi_f)) / 2, y - 11, f"1.5 × {num(iqr)} = {num(1.5 * iqr)}", size=12, color=theme.RED,
               halo=True)
        c.arrow(X(lo_f), y, X(q1), y, color=theme.RED, width=1.4, both=True)
        c.text((X(lo_f) + X(q1)) / 2, y - 11, num(1.5 * iqr), size=12, color=theme.RED, halo=True)

    @wt.step("Draw whiskers and flag the outlier", f"Whiskers run to the smallest and largest values "
             f"inside the fences, {wmin} and {wmax}. The {outl[0]} sits past the fence, so it gets its own "
             "dot. Somebody either aced it or typed it wrong.",
             math=f"whiskers {wmin} to {wmax};  outlier {', '.join(map(str, outl))}")
    def _(c):
        for a, b in ((wmin, q1), (q3, wmax)):
            c.line(X(a), BMID, X(b), BMID, color=theme.INK, width=2)
        for v in (wmin, wmax):
            c.line(X(v), BMID - 12, X(v), BMID + 12, color=theme.INK, width=2)
            c.text(X(v), BMID + 24, str(v), size=12, color=theme.INK, weight="bold")
        for v in outl:
            c.circle(X(v), BMID, 7, color=theme.RED, fill=theme.fill(theme.RED, "55"), width=2.5)
            c.text(X(v), BMID - 22, f"outlier {v}", size=12, color=theme.RED, weight="bold", halo=True)
            cell(c, data.index(v), theme.RED, theme.fill(theme.RED, "44"))

    return wt


# ---------------------------------------------------------------------------
# Histogram
# ---------------------------------------------------------------------------

SCORES = [55, 58, 62, 64, 67, 69, 71, 72, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 88, 88, 89, 92, 95, 97]


def _tally(c, x, y, k, color, h=16):
    """Draws k tally marks with every fifth one crossing the four before it."""
    gx = 0
    i = 0
    while i < k:
        grp = min(5, k - i)
        for j in range(min(grp, 4)):
            c.line(x + gx + j * 6, y - h / 2, x + gx + j * 6, y + h / 2, color=color, width=2)
        if grp == 5:
            c.line(x + gx - 3, y + h / 2 - 2, x + gx + 21, y - h / 2 + 2, color=color, width=2)
        gx += 32
        i += grp


@diagram("histogram", "Histograms", "Statistics")
def histogram() -> Walkthrough:
    raw = list(SCORES)
    random.Random(7).shuffle(raw)
    bins = [(50, 60), (60, 70), (70, 80), (80, 90), (90, 100)]
    cols = [theme.PURPLE, theme.SKY, theme.GREEN, theme.BLUE, theme.ORANGE]
    counts = [sum(1 for v in raw if a <= v < b) for a, b in bins]
    peak = max(range(len(bins)), key=lambda k: counts[k])

    def bin_of(v):
        return next(k for k, (a, b) in enumerate(bins) if a <= v < b)

    wt = Walkthrough(
        "histogram", "Histograms", "Statistics",
        concept="bar height = how many values land in each bin",
        summary="Group raw numbers into equal bins, count each bin, and draw touching bars. The outline of "
                "the bars shows the shape of the data.",
        width=700, height=450, level="301",
    )
    RC, RR, CWID, RH, RX0, RY0 = 4, 6, 52, 30, 22, 52

    def raw_cells(c, colored):
        for i, v in enumerate(raw):
            r, k = divmod(i, RC)
            x, y = RX0 + k * CWID, RY0 + r * RH
            col = cols[bin_of(v)] if colored else theme.MUTED
            c.rect(x + 2, y + 2, CWID - 4, RH - 4, color=col, fill=theme.fill(col, "33") if colored else "none",
                   width=1.5 if colored else 1, rx=4)
            c.text(x + CWID / 2, y + RH / 2, str(v), size=15, weight="bold")

    TY0, TRH = 274, 32

    def bin_label(a, b):
        return f"{a}–{b - 1}"

    p = Plane(None, box=(340, 50, 330, 320), x=(50, 100), y=(0, 9))

    def axes(c):
        p.c = c
        for k in range(0, 10):
            c.line(p.X(50), p.Y(k), p.X(100), p.Y(k), color=theme.GRID, width=1)
            if k % 2 == 0:
                c.text(p.X(50) - 8, p.Y(k), str(k), size=12, color=theme.SOFT_INK, anchor="end")
        c.line(p.X(50), p.Y(0), p.X(100), p.Y(0), color=theme.INK, width=1.6)
        c.line(p.X(50), p.Y(0), p.X(50), p.Y(9), color=theme.INK, width=1.6)
        for v in range(50, 101, 10):
            c.text(p.X(v), p.Y(0) + 16, str(v), size=12, color=theme.SOFT_INK)
        c.text(p.X(75), p.Y(0) + 38, "score", size=13, color=theme.SOFT_INK)
        c.text(p.X(50) - 32, p.Y(4.5), "count", size=13, color=theme.SOFT_INK,
               transform=f"rotate(-90 {p.X(50) - 32} {p.Y(4.5)})")

    @wt.setup
    def _(c):
        axes(c)
        return None

    @wt.step("Start with the raw data", f"Here are {len(raw)} quiz scores in the order they came in. As a "
             "pile of numbers they say very little.", math=f"n = {len(raw)} scores")
    def _(c):
        c.text(RX0, 30, f"{len(raw)} quiz scores", size=13, color=theme.SOFT_INK, anchor="start", weight="bold")
        raw_cells(c, False)

    @wt.step("Choose equal bins", "Split the range into bins of width 10: the 50s, 60s, 70s, 80s, and "
             "90s. Color each score by its bin.", math="bin width = 10")
    def _(c):
        raw_cells(c, True)
        c.text(RX0, TY0 - 18, "bin", size=12, color=theme.SOFT_INK, anchor="start", weight="bold")
        for k, (a, b) in enumerate(bins):
            y = TY0 + k * TRH
            c.rect(RX0, y, 70, TRH - 4, color="none", fill=theme.fill(cols[k], "44"), rx=4)
            c.text(RX0 + 35, y + (TRH - 4) / 2, bin_label(a, b), size=14, weight="bold", color=theme.INK)

    @wt.step("Tally each bin", "Go through the scores once and make a mark in the matching bin. Every "
             "fifth mark crosses the four before it, which keeps counting easy.",
             math="counts: " + ", ".join(map(str, counts)) + f"  (total {sum(counts)})")
    def _(c):
        c.text(RX0 + 84, TY0 - 18, "tally", size=12, color=theme.SOFT_INK, anchor="start", weight="bold")
        c.text(RX0 + 222, TY0 - 18, "count", size=12, color=theme.SOFT_INK, anchor="middle", weight="bold")
        for k in range(len(bins)):
            y = TY0 + k * TRH + (TRH - 4) / 2
            _tally(c, RX0 + 90, y, counts[k], cols[k])
            c.text(RX0 + 222, y, str(counts[k]), size=15, weight="bold", color=cols[k])

    @wt.step("Draw the bars", "Each bar covers its bin and rises to its count. The bars touch because "
             "the bins have no gaps between them.", math="bar height = count")
    def _(c):
        for k, (a, b) in enumerate(bins):
            p.rect(a, 0, b, counts[k], color=cols[k], fill=theme.fill(cols[k], "77"), width=2)
            c.text(p.X((a + b) / 2), p.Y(counts[k]) - 12, str(counts[k]), size=14, weight="bold",
                   color=cols[k])

    @wt.step("Read the shape", f"One peak sits in the {bins[peak][0]}s. The bars trail off more slowly "
             "to the left, so the data is skewed left: a few low scores, most students doing well.",
             math=f"peak in {bin_label(*bins[peak])},  tail to the left")
    def _(c):
        a, b = bins[peak]
        c.text(p.X(a + 5), p.Y(counts[peak]) - 32, "peak", size=13, color=theme.INK, weight="bold")
        c.arrow(p.X(72), p.Y(8.4), p.X(53), p.Y(8.4), color=theme.RED, width=2)
        c.text(p.X(62.5), p.Y(8.4) - 14, "long tail: skewed left", size=13, color=theme.RED, weight="bold",
               halo=True)

    return wt


# ---------------------------------------------------------------------------
# Standard deviation
# ---------------------------------------------------------------------------

SD_DATA = [2, 4, 4, 4, 5, 5, 7, 9]


@diagram("standard-deviation", "Standard Deviation", "Statistics")
def standard_deviation() -> Walkthrough:
    data = sorted(SD_DATA)
    n = len(data)
    mu = sum(data) / n
    dev = [v - mu for v in data]
    sq = [d * d for d in dev]
    var = sum(sq) / n
    sd = math.sqrt(var)
    wt = Walkthrough(
        "standard-deviation", "Standard Deviation", "Statistics",
        concept="\\sigma = sqrt(\\sum (x - \\mu)^2 / n)",
        summary="Standard deviation is the typical distance from the mean. Find each distance, square it, "
                "average the squares, and take the square root to get back to the original units.",
        width=720, height=450, level="301",
    )
    X = lambda v: 40 + v * 34
    ROW0, RH = 56, 30
    AXY = ROW0 + n * RH + 4
    TX = [440, 520, 620]
    NEG, POS, SQ, SD_C = theme.PURPLE, theme.GREEN, theme.ORANGE, theme.RED

    def ry(i):
        return ROW0 + i * RH

    @wt.setup
    def _(c):
        for v in range(11):
            c.line(X(v), ROW0 - 14, X(v), AXY, color=theme.GRID, width=1)
        axis_line(c, X, AXY, 0, 10)
        c.text(TX[0], 24, "x", size=15, weight="bold", math=True)
        for i, v in enumerate(data):
            c.text(TX[0], ry(i), str(v), size=15)
        return None

    @wt.step("Put each value on its own row", f"Give each of the {n} values a row so none hide behind "
             f"another. The mean, {num(mu)}, is the blue line.",
             math=f"\\mu = {sum(data)}/{n} = {num(mu)}")
    def _(c):
        c.line(X(mu), ROW0 - 18, X(mu), AXY, color=MEAN_C, width=2.5)
        c.text(X(mu), ROW0 - 30, f"μ = {num(mu)}", size=14, color=MEAN_C, weight="bold")
        for i, v in enumerate(data):
            c.dot(X(v), ry(i), r=7, color=theme.INK)

    @wt.step("Measure each deviation", "Draw a bar from the mean to each value. Bars to the left are "
             "negative and bars to the right are positive. They always add to zero, so their plain "
             "average is useless.", math="x - \\mu: " + ", ".join(num(d) for d in dev) + ";  sum = 0")
    def _(c):
        c.text(TX[1], 24, "x - \\mu", size=15, weight="bold", math=True)
        for i, d in enumerate(dev):
            col = NEG if d < 0 else POS
            if d != 0:
                c.line(X(mu), ry(i), X(data[i]), ry(i), color=col, width=5)
            c.dot(X(data[i]), ry(i), r=7, color=theme.INK)
            c.text(TX[1], ry(i), num(d), size=15, color=col if d else theme.SOFT_INK, weight="bold")

    SQX, SQB, U = 40, 420, 13

    @wt.step("Square the deviations", "Squaring makes every distance positive and gives far values extra "
             "weight. Each orange square has side |x − μ| and area (x − μ)².",
             math=" + ".join(num(s) for s in sq) + f" = {num(sum(sq))}")
    def _(c):
        c.text(TX[2], 24, "(x - \\mu)^2", size=15, weight="bold", math=True)
        for i, s in enumerate(sq):
            c.text(TX[2], ry(i), num(s), size=15, color=SQ if s else theme.SOFT_INK, weight="bold")
        c.text(TX[2], ry(n) + 4, f"sum {num(sum(sq))}", size=14, color=SQ, weight="bold")
        c.line(TX[2] - 30, ry(n) - 13, TX[2] + 30, ry(n) - 13, color=theme.INK, width=1)
        x = SQX
        c.text(SQX, SQB - 62, "squares, side = |x − μ|", size=12, color=theme.SOFT_INK, anchor="start")
        for d in dev:
            a = abs(d) * U
            if a:
                c.rect(x, SQB - a, a, a, color=SQ, fill=theme.fill(SQ, "55"), width=1.5)
                c.text(x + a / 2, SQB - a - 9, num(d * d), size=11, color=SQ, weight="bold")
                x += a + 8
            else:
                c.dot(x + 3, SQB - 2, r=2.5, color=theme.SOFT_INK)
                x += 14

    AVX = 330

    @wt.step("Average the squares", f"Pool the total area, {num(sum(sq))}, and share it among {n} values. "
             f"The average square has area {num(var)}. This is the variance.",
             math=f"\\sigma^2 = {num(sum(sq))}/{n} = {num(var)}")
    def _(c):
        c.text(AVX - 40, SQB - 20, f"÷ {n} →", size=15, color=theme.INK, weight="bold")
        c.text(TX[2], ry(n) + 30, f"÷ {n} = {num(var)} = σ²", size=14, color=SD_C, weight="bold")
        a = sd * U
        c.rect(AVX, SQB - a, a, a, color=SD_C, fill=theme.fill(SD_C, "55"), width=2)
        c.text(AVX + a + 8, SQB - a / 2, f"area {num(var)}", size=13, color=SD_C, weight="bold",
               anchor="start")

    @wt.step("Take the square root", f"The side of the average square is {num(sd)}, back in the units of "
             f"the data. Most values sit within one standard deviation of the mean, between "
             f"{num(mu - sd)} and {num(mu + sd)}.", math=f"\\sigma = sqrt({num(var)}) = {num(sd)}")
    def _(c):
        a = sd * U
        c.line(AVX, SQB + 6, AVX + a, SQB + 6, color=SD_C, width=3)
        c.text(AVX + a / 2, SQB + 20, f"side σ = {num(sd)}", size=13, color=SD_C, weight="bold")
        c.text(TX[2], ry(n) + 56, f"√{num(var)} = {num(sd)} = σ", size=15, color=SD_C, weight="bold")
        c.rect(X(mu - sd), ROW0 - 14, X(mu + sd) - X(mu - sd), AXY - ROW0 + 14, color="none",
               fill=theme.fill(SD_C, "1a"))
        y = AXY + 34
        c.arrow(X(mu - sd), y, X(mu + sd), y, color=SD_C, width=1.5, both=True)
        c.text(X(mu - sd) - 6, y, f"μ − σ = {num(mu - sd)}", size=12, color=SD_C, weight="bold", anchor="end")
        c.text(X(mu + sd) + 6, y, f"μ + σ = {num(mu + sd)}", size=12, color=SD_C, weight="bold", anchor="start")

    return wt


# ---------------------------------------------------------------------------
# Normal distribution
# ---------------------------------------------------------------------------

def phi(z: float) -> float:
    return math.exp(-z * z / 2) / math.sqrt(2 * math.pi)


def Phi(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


@diagram("normal-distribution", "The Normal Distribution", "Statistics")
def normal() -> Walkthrough:
    MU, SIG = 100, 15
    within = {k: Phi(k) - Phi(-k) for k in (1, 2, 3)}
    band = {1: within[1] / 2, 2: (within[2] - within[1]) / 2, 3: (within[3] - within[2]) / 2}
    tail2 = 1 - Phi(2)
    wt = Walkthrough(
        "normal-distribution", "The Normal Distribution", "Statistics",
        concept="z = (x - \\mu)/\\sigma;  68%, 95%, 99.7% within 1, 2, 3 \\sigma",
        summary="In a bell curve, about 68% of values fall within one standard deviation of the mean, 95% "
                "within two, and 99.7% within three. A z-score counts how many standard deviations a value "
                "sits from the mean.",
        width=700, height=430, level="301",
    )
    COL = {1: theme.BLUE, 2: theme.GREEN, 3: theme.ORANGE}
    BR = {1: 352, 2: 378, 3: 404}

    @wt.setup
    def _(c):
        p = Plane(c, box=(70, 22, 560, 260), x=(-3.6, 3.6), y=(0, 0.44))
        y0 = p.Y(0)
        c.line(p.X(-3.6), y0, p.X(3.6), y0, color=theme.INK, width=1.6)
        c.text(36, y0 + 16, "z", size=13, color=theme.SOFT_INK, math=True)
        c.text(36, y0 + 34, "IQ", size=12, color=theme.SOFT_INK)
        for z in range(-3, 4):
            c.line(p.X(z), y0, p.X(z), y0 + 5, color=theme.INK, width=1.2)
            c.text(p.X(z), y0 + 16, num(z), size=12, color=theme.SOFT_INK)
            c.text(p.X(z), y0 + 34, str(MU + z * SIG), size=12, color=theme.INK)
        return p

    def curve(p):
        p.plot(phi, color=theme.INK, width=2.5)

    def bracket(c, p, k):
        y = BR[k]
        col = COL[k]
        c.line(p.X(-k), y, p.X(k), y, color=col, width=2)
        for z in (-k, k):
            c.line(p.X(z), y - 6, p.X(z), y + 6, color=col, width=2)
        pct = {1: "68%", 2: "95%", 3: "99.7%"}[k]
        c.label_box(p.X(0), y, f"{pct} within ±{k}σ", color=col, border=col, size=12)

    @wt.step("Draw the bell curve", f"IQ scores follow a bell curve centered at μ = {MU} with standard "
             f"deviation σ = {SIG}. The curve bends from cap to cup exactly one σ from the center.",
             math=f"\\mu = {MU},  \\sigma = {SIG}")
    def _(c, p):
        curve(p)
        p.vline(0, color=MEAN_C, dash="6 4", width=1.8, y1=phi(0))
        p.label(0, 0.425, f"μ = {MU}", color=MEAN_C, size=14, math=False, weight="bold")
        y = phi(1)
        c.arrow(p.X(0), p.Y(y), p.X(1), p.Y(y), color=theme.RED, width=1.8)
        c.text(p.X(0.5), p.Y(y) + 14, f"σ = {SIG}", size=13, color=theme.RED, weight="bold", halo=True)
        p.point(1, y, color=theme.RED, r=4)

    def shade(p, k):
        col = COL[k]
        for a, b in ((-k, -(k - 1)), (k - 1, k)):
            if a == b:
                continue
            p.shade_under(phi, min(a, b), max(a, b), color=col, opacity=0.35)

    @wt.step("Shade one standard deviation", "Between 85 and 115, one σ either side of the mean, lies "
             f"about 68% of all people: {band[1]:.1%} on each side.",
             math=f"P(-1 < z < 1) \\approx {within[1]:.1%}")
    def _(c, p):
        shade(p, 1)
        curve(p)
        for s in (-1, 1):
            p.label(0.5 * s, 0.15, f"{band[1]:.1%}", color=COL[1], size=13, math=False, weight="bold")
        bracket(c, p, 1)

    @wt.step("Add the second standard deviation", f"Each band from one to two σ adds {band[2]:.1%}. Within "
             "two σ, from 70 to 130, lies about 95%.", math=f"P(-2 < z < 2) \\approx {within[2]:.1%}")
    def _(c, p):
        shade(p, 2)
        curve(p)
        for s in (-1, 1):
            p.label(1.45 * s, 0.05, f"{band[2]:.1%}", color=COL[2], size=12, math=False, weight="bold")
        bracket(c, p, 2)

    @wt.step("Add the third standard deviation", f"The thin bands from two to three σ add only "
             f"{band[3]:.1%} each. Within three σ lies 99.7%, nearly everyone.",
             math=f"P(-3 < z < 3) \\approx {within[3]:.1%}")
    def _(c, p):
        shade(p, 3)
        curve(p)
        for s in (-1, 1):
            p.label(2.5 * s, 0.05, f"{band[3]:.1%}", color=COL[3], size=12, math=False, weight="bold")
        bracket(c, p, 3)

    x0 = 130
    z0 = (x0 - MU) / SIG

    @wt.step("Turn a score into a z-score", f"A score of {x0} sits {num(z0)} standard deviations above "
             f"the mean. The rule says about 2.5% score higher; the exact tail is {tail2:.1%}.",
             math=f"z = ({x0} - {MU})/{SIG} = {num(z0)};   P(z > {num(z0)}) \\approx {tail2:.1%}", fresh=True)
    def _(c, p):
        p.shade_under(phi, z0, 3.6, color=theme.RED, opacity=0.45)
        p.shade_under(phi, -3.6, z0, color=theme.MUTED, opacity=0.15)
        curve(p)
        p.vline(z0, color=theme.RED, dash="6 4", width=2, y1=0.2)
        p.label(z0, 0.225, f"x = {x0}", color=theme.RED, size=14, math=False, weight="bold")
        c.arrow(p.X(0), p.Y(0.17), p.X(z0), p.Y(0.17), color=theme.RED, width=1.8)
        c.text(p.X(z0 / 2), p.Y(0.17) - 12, f"{num(z0)} σ = {num(z0 * SIG)} points", size=12, color=theme.RED,
               weight="bold", halo=True)
        c.text(p.X(2.75), p.Y(0.1), f"{tail2:.1%}", size=14, color=theme.RED, weight="bold")
        c.text(p.X(2.75), p.Y(0.1) + 16, f"above {x0}", size=12, color=theme.RED)
        c.line(p.X(2.6), p.Y(0.1) + 26, p.X(2.25), p.Y(0.012), color=theme.RED, width=1.2)
        c.label_box(p.X(-1.6), p.Y(0.33), "z = (x − μ)/σ", color=theme.INK, border=theme.MUTED, size=14)
        y = BR[2]
        for a, b, col, txt in ((-3.5, z0, theme.SOFT_INK, f"{1 - tail2:.1%} score below {x0}"),
                               (z0, 3.5, theme.RED, f"{tail2:.1%} above")):
            c.line(p.X(a), y, p.X(b) - 3, y, color=col, width=2)
            for z in (a, b):
                c.line(p.X(z) - (3 if z == b else 0), y - 6, p.X(z) - (3 if z == b else 0), y + 6, color=col,
                       width=2)
            c.label_box((p.X(a) + p.X(b)) / 2, y, txt, color=col, border=col, size=12)

    return wt


# ---------------------------------------------------------------------------
# Linear regression
# ---------------------------------------------------------------------------

REG_X = [1, 2, 3, 4, 5, 6, 7, 8]
REG_Y = [48, 57, 57, 65, 61, 74, 70, 80]


def least_squares(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sxy / sxx
    return mx, my, sxy, sxx, b, my - b * mx


@diagram("linear-regression", "Least Squares Regression", "Statistics")
def regression() -> Walkthrough:
    xs, ys = REG_X, REG_Y
    n = len(xs)
    mx, my, sxy, sxx, b, a = least_squares(xs, ys)
    yhat = lambda x: a + b * x
    res = [y - yhat(x) for x, y in zip(xs, ys)]
    sse = sum(r * r for r in res)
    b2 = b + 1
    sse2 = sum((y - (my + b2 * (x - mx))) ** 2 for x, y in zip(xs, ys))
    xp = 9
    wt = Walkthrough(
        "linear-regression", "Least Squares Regression", "Statistics",
        concept=f"ŷ = a + bx;   b = S_{{xy}} / S_{{xx}} = {num(sxy, 1)}/{num(sxx, 1)} = {num(b, 3)}",
        summary="The least squares line passes through the center of the data and makes the total of the "
                "squared vertical misses, the residuals, as small as possible.",
        width=720, height=420, level="301",
    )
    PX = 548

    @wt.setup
    def _(c):
        p = Plane(c, box=(64, 30, 440, 320), x=(0, 9.6), y=(45, 90))
        for v in range(0, 10):
            c.line(p.X(v), p.Y(45), p.X(v), p.Y(90), color=theme.GRID, width=1)
            c.text(p.X(v), p.Y(45) + 16, str(v), size=12, color=theme.SOFT_INK)
        for v in range(45, 91, 5):
            c.line(p.X(0), p.Y(v), p.X(9.6), p.Y(v), color=theme.GRID, width=1)
            c.text(p.X(0) - 8, p.Y(v), str(v), size=12, color=theme.SOFT_INK, anchor="end")
        c.line(p.X(0), p.Y(45), p.X(9.6), p.Y(45), color=theme.INK, width=1.6)
        c.line(p.X(0), p.Y(45), p.X(0), p.Y(90), color=theme.INK, width=1.6)
        c.text(p.X(4.8), p.Y(45) + 38, "hours studied, x", size=13, color=theme.SOFT_INK)
        c.text(22, p.Y(67.5), "test score, y", size=13, color=theme.SOFT_INK,
               transform=f"rotate(-90 22 {p.Y(67.5)})")
        return p

    def pts(p):
        for x, y in zip(xs, ys):
            p.point(x, y, color=theme.INK, r=5.5)

    def line(p):
        with p.c.group(clip_path=p.clip):
            p.c.line(*p.px(0, yhat(0)), *p.px(9.6, yhat(9.6)), color=MEAN_C, width=3)

    def panel(c, rows, y0=40):
        for i, (s, col) in enumerate(rows):
            c.text(PX, y0 + i * 24, s, size=14 if "_" in s else 13, color=col, anchor="start", math="_" in s,
                   weight="bold")

    @wt.step("Plot the data", f"Each dot is one student: hours studied across, test score up. The dots "
             "drift upward, so more study goes with higher scores, on average.", math=f"n = {n} students")
    def _(c, p):
        pts(p)
        c.text(PX + 20, 30, "x", size=14, math=True, weight="bold")
        c.text(PX + 80, 30, "y", size=14, math=True, weight="bold")
        c.line(PX - 6, 42, PX + 110, 42, color=theme.MUTED, width=1)
        for i, (x, y) in enumerate(zip(xs, ys)):
            c.text(PX + 20, 58 + i * 22, str(x), size=14)
            c.text(PX + 80, 58 + i * 22, str(y), size=14)

    @wt.step("Mark the center of the data", "Average the x values and the y values. The best line always "
             "passes through this center point.",
             math=f"mean of x = {num(mx)};  mean of y = {num(my, 3)}", fresh=True)
    def _(c, p):
        p.vline(mx, color=theme.PURPLE, dash="5 4", width=1.5)
        p.hline(my, color=theme.PURPLE, dash="5 4", width=1.5)
        pts(p)
        p.point(mx, my, color=theme.PURPLE, r=7, label=f"center ({num(mx)}, {num(my, 3)})", offset=(-12, -18), anchor="end", math=False,
                size=13)
        panel(c, [(f"mean of x = {num(mx)}", theme.PURPLE), (f"mean of y = {num(my, 3)}", theme.PURPLE)])

    @wt.step("Draw the least squares line", "The slope compares how x and y move together with how x "
             "moves alone. Then the line goes through the center.",
             math=f"b = {num(sxy, 1)}/{num(sxx, 1)} = {num(b, 3)},   a = {num(my, 3)} - {num(b, 3)} \\cdot "
                  f"{num(mx)} = {num(a, 2)}", fresh=True)
    def _(c, p):
        line(p)
        pts(p)
        p.point(mx, my, color=theme.PURPLE, r=6)
        panel(c, [(f"S_{{xy}} = {num(sxy, 1)}", theme.INK), (f"S_{{xx}} = {num(sxx, 1)}", theme.INK),
                  (f"b = {num(b, 3)}", MEAN_C), (f"a = {num(a, 2)}", MEAN_C)])
        p.label(7.6, yhat(7.6) + 5.2, f"ŷ = {num(a, 1)} + {num(b, 2)}x", color=MEAN_C, size=15, math=False,
                weight="bold")

    def residuals(c, p, labels=True):
        for x, y, r in zip(xs, ys, res):
            col = theme.GREEN if r > 0 else theme.RED
            p.segment(x, yhat(x), x, y, color=col, width=2.5)
            if labels:
                c.text(p.X(x) - 9, p.Y(y) + (8 if r > 0 else -8), num(r, 1), size=11, color=col, weight="bold",
                       anchor="end", halo=True)

    @wt.step("Measure the residuals", "A residual is the vertical miss: actual minus predicted. Dots "
             "above the line miss high (green), dots below miss low (red), and they add to zero.",
             math=f"residual = y - ŷ;   \\sum residuals = {num(abs(sum(res)), 6)}", fresh=True)
    def _(c, p):
        line(p)
        residuals(c, p)
        pts(p)
        panel(c, [(f"ŷ = {num(a, 2)} + {num(b, 3)}x", MEAN_C),
                  ("above line: green", theme.GREEN), ("below line: red", theme.RED)])

    @wt.step("Square the residuals and add", f"Draw each residual as a square. Least squares makes the "
             f"total area as small as it can be. Tilt the line steeper through the center and the total "
             f"jumps from {num(sse, 1)} to {num(sse2, 1)}.",
             math=f"SSE = \\sum (y - ŷ)^2 = {num(sse, 2)}", fresh=True)
    def _(c, p):
        with p.c.group(clip_path=p.clip):
            p.c.line(*p.px(0, my + b2 * (0 - mx)), *p.px(9.6, my + b2 * (9.6 - mx)), color=theme.MUTED,
                     width=1.8, dash="6 5")
        line(p)
        for x, y, r in zip(xs, ys, res):
            col = theme.GREEN if r > 0 else theme.RED
            s = abs(p.Y(y) - p.Y(yhat(x)))
            top = min(p.Y(y), p.Y(yhat(x)))
            c.rect(p.X(x), top, s, s, color=col, fill=theme.fill(col, "44"), width=1.2)
        residuals(c, p, labels=False)
        pts(p)
        c.text(PX, 40, "total squared area", size=12, color=theme.SOFT_INK, anchor="start")
        panel(c, [(f"blue line: {num(sse, 1)}", MEAN_C), (f"dashed line: {num(sse2, 1)}", theme.SOFT_INK)],
              y0=64)
        sq = [num(r * r) for r in res]
        c.text(PX, 130, " + ".join(sq[:4]) + " +", size=12, color=theme.INK, anchor="start")
        c.text(PX, 148, " + ".join(sq[4:]) + f" = {num(sse)}", size=12, color=theme.INK, anchor="start")

    @wt.step("Predict with the line", f"For a student who studies {xp} hours, read the line at x = {xp}. "
             "Predictions past the data are guesses, so trust them less the farther you go.",
             math=f"ŷ = {num(a, 2)} + {num(b, 3)} \\times {xp} = {num(yhat(xp), 1)}", fresh=True)
    def _(c, p):
        line(p)
        pts(p)
        p.segment(xp, 45, xp, yhat(xp), color=theme.ORANGE, width=2, dash="5 4")
        p.segment(0, yhat(xp), xp, yhat(xp), color=theme.ORANGE, width=2, dash="5 4")
        p.point(xp, yhat(xp), color=theme.ORANGE, r=7)
        c.text(p.X(xp) - 10, p.Y(yhat(xp)) - 16, f"({xp}, {num(yhat(xp), 1)})", size=13, color=theme.ORANGE,
               weight="bold", anchor="end", halo=True)
        panel(c, [(f"ŷ = {num(a, 2)} + {num(b, 3)}x", MEAN_C), (f"x = {xp}: ŷ = {num(yhat(xp), 1)}",
                                                                   theme.ORANGE)])

    return wt


# ---------------------------------------------------------------------------
# Central limit theorem
# ---------------------------------------------------------------------------

def dice_mean_dist(n: int):
    """Exact distribution of the mean of n fair dice: list of (mean, probability)."""
    counts = {0: 1}
    for _ in range(n):
        nxt = {}
        for s, k in counts.items():
            for f in range(1, 7):
                nxt[s + f] = nxt.get(s + f, 0) + k
        counts = nxt
    tot = 6 ** n
    return [(s / n, k / tot) for s, k in sorted(counts.items())]


@diagram("central-limit-theorem", "The Central Limit Theorem", "Statistics")
def clt() -> Walkthrough:
    mu = 3.5
    sig1 = math.sqrt(35 / 12)
    NS = [1, 2, 3, 5]
    COLS = {1: theme.BLUE, 2: theme.ORANGE, 3: theme.GREEN, 5: theme.PURPLE}
    wt = Walkthrough(
        "central-limit-theorem", "The Central Limit Theorem", "Statistics",
        concept="average of n dice: center 3.5, spread \\sigma/sqrt(n), shape \\to normal",
        summary="Average more dice and the distribution of the average changes from flat to bell-shaped, "
                "and it narrows like sigma over root n. These are the exact distributions, not simulations.",
        width=700, height=420, level="301",
    )

    @wt.setup
    def _(c):
        p = Plane(c, box=(70, 40, 560, 290), x=(0.5, 6.5), y=(0, 0.6))
        for k in range(1, 7):
            c.line(p.X(0.5), p.Y(k / 10), p.X(6.5), p.Y(k / 10), color=theme.GRID, width=1)
            c.text(p.X(0.5) - 8, p.Y(k / 10), f"{k / 10:g}", size=12, color=theme.SOFT_INK, anchor="end")
        c.line(p.X(0.5), p.Y(0), p.X(6.5), p.Y(0), color=theme.INK, width=1.6)
        c.line(p.X(0.5), p.Y(0), p.X(0.5), p.Y(0.6), color=theme.INK, width=1.6)
        for v in range(1, 7):
            c.line(p.X(v), p.Y(0), p.X(v), p.Y(0) + 5, color=theme.INK, width=1.2)
            c.text(p.X(v), p.Y(0) + 17, str(v), size=12, color=theme.SOFT_INK)
        c.text(p.X(3.5), p.Y(0) + 40, "average of the dice", size=13, color=theme.SOFT_INK)
        c.text(24, p.Y(0.3), "probability per unit", size=13, color=theme.SOFT_INK,
               transform=f"rotate(-90 24 {p.Y(0.3)})")
        p.vline(mu, color=theme.INK, dash="4 4", width=1.2)
        return p

    def bars(p, n, ghost=False):
        col = COLS[n]
        w = 1 / n
        pts = []
        dist = dice_mean_dist(n)
        for m, pr in dist:
            h = pr / w
            if ghost:
                pts += [p.px(m - w / 2, h), p.px(m + w / 2, h)]
            else:
                p.rect(m - w / 2, 0, m + w / 2, h, color=col, fill=theme.fill(col, "55"), width=1.2)
        if ghost:
            pts = [p.px(dist[0][0] - w / 2, 0)] + pts + [p.px(dist[-1][0] + w / 2, 0)]
            p.c.polyline(pts, color=COLS[n], width=1.6, dash="5 4")

    def info(c, p, n, prev=None):
        sig = sig1 / math.sqrt(n)
        dice = "die" if n == 1 else "dice"
        c.label_box(560, 64, f"n = {n} {dice}", color=COLS[n], border=COLS[n], size=15)
        c.text(560, 96, f"spread σ = {sig:.2f}", size=13, color=COLS[n], weight="bold")
        c.text(560, 116, f"outcomes: {6 ** n}", size=12, color=theme.SOFT_INK)
        if prev:
            c.text(140, 64, f"dashed: n = {prev}", size=12, color=COLS[prev], weight="bold", anchor="start")
        y = p.Y(0) - 14
        c.arrow(p.X(mu - sig), y, p.X(mu + sig), y, color=theme.INK, width=1.3, both=True)
        c.text(p.X(mu + sig) + 6, y, "±σ", size=12, color=theme.INK, anchor="start", halo=True)

    caps = {
        1: ("Roll one die", "One die is flat: each face has chance 1/6. Average 3.5, spread "
            f"{sig1:.2f}. No bell in sight."),
        2: ("Average two dice", "Averages of two dice pile up in the middle, because many pairs average "
            "3.5 and only one pair averages 1. The shape is a triangle."),
        3: ("Average three dice", "With three dice the triangle rounds off. Extreme averages need every "
            "die to cooperate, which they rarely do."),
        5: ("Average five dice", "Five dice already look like a bell. The center stays at 3.5 while the "
            "spread shrinks."),
    }
    for idx, n in enumerate(NS):
        prev = NS[idx - 1] if idx else None
        t, txt = caps[n]

        def draw(c, p, n=n, prev=prev):
            if prev:
                bars(p, prev, ghost=True)
            bars(p, n)
            info(c, p, n, prev)

        wt.step(t, txt, math=f"\\sigma/sqrt({n}) = {sig1:.2f}/{math.sqrt(n):.2f} = {sig1 / math.sqrt(n):.2f}",
                fresh=True)(draw)

    s5 = sig1 / math.sqrt(5)

    @wt.step("Lay a normal curve on top", "A normal curve with mean 3.5 and σ = 0.76 hugs the bars. This "
             "is the central limit theorem: averages of many independent values come out close to normal, "
             "whatever the shape you started with.",
             math=f"average of 5 dice \\approx Normal(3.5, {s5:.2f})", fresh=True)
    def _(c, p):
        bars(p, 5)
        p.plot(lambda x: math.exp(-((x - mu) / s5) ** 2 / 2) / (s5 * math.sqrt(2 * math.pi)), color=theme.RED,
               width=2.8)
        info(c, p, 5)
        c.text(p.X(4.75), p.Y(0.36), "normal curve", size=13, color=theme.RED, weight="bold", anchor="start",
               halo=True)

    return wt
