"""Number line diagrams: adding and subtracting integers as hops."""

from __future__ import annotations

from .. import theme
from ..annotate import hop, number_line
from ..registry import diagram
from ..walkthrough import Walkthrough


@diagram("number-line-integers", "Adding Integers on a Number Line", "Arithmetic")
def build() -> Walkthrough:
    wt = Walkthrough(
        "number-line-integers", "Adding Integers on a Number Line", "Arithmetic",
        concept="-3 + 5 - 4 = -2",
        summary="Every number is a position. Adding a positive number moves right; adding a negative number "
                "(subtracting) moves left.",
        width=680, height=230, level="101",
    )
    Y = 150

    @wt.setup
    def _(c):
        return number_line(c, 50, Y, 630, -6, 6)

    @wt.step("Start at the first number", "Every integer has a place on the line. Zero is in the middle, "
             "positive numbers go right, and negative numbers go left. Start at −3.", math="start: -3")
    def _(c, X):
        c.dot(X(-3), Y, r=8, color=theme.BLUE)
        c.text(X(-3), Y - 26, "start", size=13, color=theme.BLUE)

    @wt.step("Add 5: move right 5", "Adding a positive number moves you to the right. Five hops right "
             "from −3 lands on 2.", math="-3 + 5 = 2")
    def _(c, X):
        hop(c, X(-3), X(2), Y, "+5", color=theme.BLUE, height=64)
        c.dot(X(2), Y, r=7, color=theme.BLUE)

    @wt.step("Subtract 4: move left 4", "Subtracting moves you to the left. Four hops left from 2 lands "
             "on −2.", math="2 - 4 = -2")
    def _(c, X):
        hop(c, X(2), X(-2), Y, "−4", color=theme.ORANGE, height=28)
        c.dot(X(-2), Y, r=8, color=theme.ORANGE)

    @wt.step("Read the answer", "The final position is the answer. The order of the hops does not "
             "matter: −3 − 4 + 5 lands in the same place.", math="-3 + 5 - 4 = -2")
    def _(c, X):
        c.circle(X(-2), Y, 15, color=theme.GREEN, width=3)
        c.label_box(X(-2), Y + 56, "answer: −2", color=theme.GREEN, border=theme.GREEN, size=15)

    return wt
