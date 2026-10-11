"""Colors, fonts, and sizes shared by every diagram.

The palette is Okabe-Ito, which stays distinguishable for the common
forms of color blindness. Use the named roles (INK, MUTED, ACCENT, ...)
rather than raw hex values so every diagram reads as one system.
"""

from __future__ import annotations

# Okabe-Ito palette
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
RED = "#D55E00"
PURPLE = "#CC79A7"
SKY = "#56B4E9"
YELLOW = "#F0E442"  # fills only; too light for text or thin lines

# Neutrals
INK = "#1f2933"  # main text and outlines
SOFT_INK = "#52606d"  # secondary text
MUTED = "#9aa5b1"  # de-emphasized lines
GRID = "#e4e7eb"  # grid lines
PAPER = "#ffffff"  # background
PANEL = "#f5f7fa"  # caption and header panels
HIGHLIGHT = "#fff3c4"  # soft yellow highlight behind text or regions

# Ordered series colors for multiple curves, bars, or sets
SERIES = [BLUE, ORANGE, GREEN, RED, PURPLE, SKY]

# Translucent fills that pair with the series colors
FILL = {
    BLUE: "#0072B233",
    ORANGE: "#E69F0033",
    GREEN: "#009E7333",
    RED: "#D55E0033",
    PURPLE: "#CC79A733",
    SKY: "#56B4E933",
    YELLOW: "#F0E44266",
}


def fill(color: str, alpha: str = "33") -> str:
    """Returns a translucent version of a hex color, for region fills."""
    if color.startswith("#") and len(color) == 7:
        return color + alpha
    return color


SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
SERIF = "'STIX Two Text', 'Cambria Math', Cambria, 'Times New Roman', serif"
MONO = "Menlo, Consolas, 'Courier New', monospace"

# Font sizes in px
TITLE_SIZE = 22
STEP_TITLE_SIZE = 17
CAPTION_SIZE = 15
LABEL_SIZE = 15
SMALL_SIZE = 12
MATH_SIZE = 18

STROKE = 2  # default line width
THIN = 1
THICK = 3.5
