"""Decimals: zooming in on a number line, and the hundredths grid."""

from __future__ import annotations

from fractions import Fraction as F

from .. import theme
from ..annotate import brace, hop
from ..registry import diagram
from ..walkthrough import Walkthrough
from ._kit import tag

BLUE, ORANGE, GREEN = theme.BLUE, theme.ORANGE, theme.GREEN


@diagram("decimal-zoom", "Zooming In on a Decimal", "Arithmetic")
def build_zoom() -> Walkthrough:
    target = F(37, 100)
    tenths = int(target * 10)  # 3
    hund = int(target * 100) - 10 * tenths  # 7
    lo, hi = F(tenths, 10), F(tenths + 1, 10)

    wt = Walkthrough(
        "decimal-zoom", "Zooming In on a Decimal", "Arithmetic",
        concept="0.37 = 3 tenths + 7 hundredths = 0.3 + 0.07",
        summary="Find 0.37 by zooming. The first digit picks a tenth of the line, and inside that tenth "
                "the second digit picks a hundredth.",
        width=700, height=360, level="101",
    )
    L, R = 60, 640
    Y1, Y2 = 70, 252

    def X1(v):
        return L + float(v) * (R - L)

    def X2(v):
        return L + float((v - lo) / (hi - lo)) * (R - L)

    def f2(v):
        return f"{float(v):.2f}"

    @wt.setup
    def _(c):
        c.line(L, Y1, R, Y1, color=theme.INK, width=2)
        for k in range(11):
            big = k in (0, 10)
            c.line(X1(F(k, 10)), Y1 - (10 if big else 7), X1(F(k, 10)), Y1 + (10 if big else 7),
                   color=theme.INK, width=2 if big else 1.5)
            c.text(X1(F(k, 10)), Y1 + 22, str(k // 10) if big else f"0.{k}", size=13)
        c.text(R, Y1 - 26, "tenths", size=12, color=theme.SOFT_INK, anchor="end")
        return None

    @wt.step("Start with tenths from 0 to 1", "Cut the line from 0 to 1 into 10 equal steps. "
             "Each step is one tenth, 0.1.", math="1 = 10 tenths")
    def _(c):
        if c.is_new:
            brace(c, X1(0), Y1 - 12, X1(F(1, 10)), Y1 - 12, label="0.1", color=theme.SOFT_INK, size=14)

    @wt.step("The first digit picks a tenth", "The 3 in 0.37 means 3 tenths, and the 7 adds a bit "
             "more. So 0.37 sits somewhere between 0.3 and 0.4.", math="0.3 < 0.37 < 0.4")
    def _(c):
        c.line(X1(lo), Y1, X1(hi), Y1, color=BLUE, width=7)
        c.line(X1(0), Y1, X1(lo), Y1, color=theme.fill(BLUE, "60"), width=4)
        brace(c, X1(0), Y1 - 12, X1(lo), Y1 - 12, label="3 tenths", color=BLUE, size=14)

    @wt.step("Zoom into that tenth", "Stretch the piece from 0.3 to 0.4 across the page and cut it "
             "into 10 smaller steps. Each small step is one hundredth, 0.01.",
             math="0.1 = 10 hundredths")
    def _(c):
        c.polygon([(X1(lo), Y1 + 34), (X1(hi), Y1 + 34), (R, Y2 - 46), (L, Y2 - 46)], color="none",
                  fill=theme.fill(BLUE, "18"))
        c.line(X1(lo), Y1 + 34, L, Y2 - 46, color=BLUE, width=1.4, dash="5 4")
        c.line(X1(hi), Y1 + 34, R, Y2 - 46, color=BLUE, width=1.4, dash="5 4")
        c.text((L + R) / 2, (Y1 + Y2) / 2 + 6, "zoom × 10", size=14, color=BLUE, weight="bold")
        c.line(L, Y2, R, Y2, color=BLUE, width=2.4)
        for k in range(11):
            v = lo + F(k, 100)
            big = k in (0, 10)
            c.line(X2(v), Y2 - (10 if big else 7), X2(v), Y2 + (10 if big else 7),
                   color=BLUE if big else theme.INK, width=2 if big else 1.5)
            c.text(X2(v), Y2 + 22, f2(v), size=13, color=BLUE if big else theme.INK,
                   weight="bold" if big else None)
        c.text(R, Y2 + 46, "hundredths", size=12, color=theme.SOFT_INK, anchor="end")

    @wt.step("Count 7 hundredths", "Starting at 0.30, take 7 small steps. They land on 0.37.",
             math="0.30 + 7 \\times 0.01 = 0.37")
    def _(c):
        for k in range(hund):
            a, b = lo + F(k, 100), lo + F(k + 1, 100)
            hop(c, X2(a), X2(b), Y2, str(k + 1) if c.is_new else None, color=ORANGE, height=18, size=12)
        c.dot(X2(target), Y2, r=7, color=ORANGE)
        brace(c, X2(target), Y2 + 34, X2(lo), Y2 + 34, label="7 hundredths", color=ORANGE, size=14)

    @wt.step("Mark 0.37 on both lines", "The same point sits on the first line, seven tenths of the "
             "way from 0.3 to 0.4. Zoom does not move numbers, it only spreads them out.",
             math="0.37 = 0.3 + 0.07")
    def _(c):
        c.dot(X1(target), Y1, r=6, color=ORANGE)
        c.line(X1(target), Y1 + 8, X2(target), Y2 - 10, color=ORANGE, width=1.8, dash="3 3")
        tag(c, X2(target), Y2 - 48, "0.37", ORANGE, size=18)
        tag(c, X1(target) + 2, Y1 - 46, "0.37", ORANGE, size=15)

    return wt


@diagram("decimal-hundredths-grid", "Decimals on a Hundredths Grid", "Arithmetic")
def build_grid() -> Walkthrough:
    target = F(37, 100)
    t = int(target * 10)
    h = int(target * 100) - 10 * t
    wt = Walkthrough(
        "decimal-hundredths-grid", "Decimals on a Hundredths Grid", "Arithmetic",
        concept="0.37 = 3 tenths + 7 hundredths = 37/100",
        summary="A square split into 100 small squares is one whole. A column is a tenth and a small square "
                "is a hundredth, so 0.37 is three columns and seven squares.",
        width=700, height=370, level="101",
    )
    G, T, CS = 50, 26, 30
    PX = 392  # place-value chart left

    def place_chart(c, digits, colors):
        heads = ["ones", "", "tenths", "hundredths"]
        widths = [64, 20, 80, 110]
        x = PX
        for head, w, d, col in zip(heads, widths, digits, colors):
            if head:
                c.rect(x, 80, w, 34, color=theme.MUTED, fill=theme.PANEL, width=1)
                c.text(x + w / 2, 97, head, size=13, weight="bold", color=col)
                c.rect(x, 114, w, 54, color=theme.MUTED, width=1)
            c.text(x + w / 2, 141, d, size=32, color=col, weight="bold", font="serif")
            x += w

    @wt.setup
    def _(c):
        for k in range(11):
            c.line(G + k * CS, T, G + k * CS, T + 10 * CS, color=theme.MUTED, width=1)
            c.line(G, T + k * CS, G + 10 * CS, T + k * CS, color=theme.MUTED, width=1)
        c.rect(G, T, 10 * CS, 10 * CS, color=theme.INK, width=2.2)
        return None

    @wt.step("The whole square is 1", "The big square is one whole, cut into 10 columns of 10 "
             "small squares. That makes 100 small squares.", math="1 = 100 hundredths")
    def _(c):
        place_chart(c, ["0", ".", "", ""], [theme.INK, theme.INK, BLUE, ORANGE])

    @wt.step("Shade three tenths", "One column is a tenth of the square. Shade 3 columns for the 3 in "
             "the tenths place.", math="3 tenths = 0.3 = 30 hundredths")
    def _(c):
        c.rect(G, T, t * CS, 10 * CS, color=BLUE, fill=theme.fill(BLUE, "50"), width=2.4)
        for k in range(1, t):
            c.line(G + k * CS, T, G + k * CS, T + 10 * CS, color=BLUE, width=2)
        for k in range(t):
            c.text(G + (k + 0.5) * CS, T + 10 * CS + 16, "0.1", size=12, color=BLUE)
        if c.is_new:
            place_chart(c, ["0", ".", str(t), ""], [theme.INK, theme.INK, BLUE, ORANGE])

    @wt.step("Add seven hundredths", "One small square is a hundredth. Shade 7 more in the next "
             "column for the 7 in the hundredths place.", math="7 hundredths = 0.07")
    def _(c):
        for k in range(h):
            c.rect(G + t * CS, T + k * CS, CS, CS, color=ORANGE, fill=theme.fill(ORANGE, "60"), width=1.6)
            c.text(G + (t + 0.5) * CS, T + (k + 0.5) * CS, str(k + 1), size=12, weight="bold")
        place_chart(c, ["0", ".", str(t), str(h)], [theme.INK, theme.INK, BLUE, ORANGE])

    @wt.step("Read it three ways", "Three columns and seven squares cover 37 of the 100 small "
             "squares. That is 0.37, or 37 hundredths, or 37%.", math="0.37 = 37/100 = 37%")
    def _(c):
        c.text(PX + 130, 214, "= 3 tenths + 7 hundredths", size=15, color=theme.INK)
        c.text(PX + 130, 246, "= 37 hundredths = 37/100", size=15, color=GREEN, weight="bold")
        c.text(PX + 130, 278, "= 37% (37 out of 100)", size=15, color=GREEN, weight="bold")

    return wt
