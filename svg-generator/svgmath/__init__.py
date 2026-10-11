"""svgmath: step-by-step SVG diagrams for learning math.

Standard library only. See README.md in the parent folder for usage.
"""

from . import theme
from .annotate import angle_mark, brace, callout, dimension, hop, number_line, right_angle, segment_label, table, tick_marks
from .plane import Plane, nice_step, pi_label, tick_label
from .registry import all_diagrams, diagram, get
from .svg import Canvas, Element, text_width, wrap
from .walkthrough import Step, Walkthrough

__all__ = [
    "theme", "Canvas", "Element", "Plane", "Walkthrough", "Step", "diagram", "all_diagrams", "get",
    "angle_mark", "brace", "callout", "dimension", "hop", "number_line", "right_angle", "segment_label",
    "table", "tick_marks", "nice_step", "pi_label", "tick_label", "text_width", "wrap",
]
