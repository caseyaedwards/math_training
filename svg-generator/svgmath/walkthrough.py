"""Step-by-step walkthroughs: the unit every diagram type produces.

A walkthrough is an optional setup function plus an ordered list of steps.
Step k renders the setup, then steps 1..k on top of each other, so each
picture adds one idea to the previous one. Every step carries a title, a
plain-language explanation, and an optional line of math shown in the
caption panel under the drawing.

    wt = Walkthrough("pythagoras", "Pythagorean Theorem", category="Geometry",
                     concept="a^2 + b^2 = c^2", width=640, height=400)

    @wt.setup
    def _(c):
        return Plane(c, box=(40, 20, 560, 360), x=(0, 8), y=(0, 6), equal=True)

    @wt.step("Draw a right triangle", "Legs a and b meet at a right angle.", math="a = 3, b = 4")
    def _(c, p):
        p.polygon([(0, 0), (3, 0), (0, 4)])

One walkthrough renders to:
  * one SVG per step (header, drawing, caption)
  * a storyboard SVG with every step in a grid
  * an animated SVG that plays the steps in a loop
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional

from . import theme
from .svg import Canvas, Element, fmt, text_width, wrap

HEADER_H = 52
PAD = 22


@dataclass
class Step:
    title: str
    text: str
    draw: Callable[..., Any]
    math: Optional[str] = None
    fresh: bool = False  # drop earlier steps (setup still draws)


@dataclass
class Walkthrough:
    slug: str
    title: str
    category: str
    concept: str = ""  # one-line statement of the idea, may use math markup
    summary: str = ""  # one or two sentences for the showcase index
    width: float = 640  # drawing area size in px, without header and caption
    height: float = 400
    level: str = ""  # optional course level, for example 101
    tags: List[str] = field(default_factory=list)
    steps: List[Step] = field(default_factory=list)
    _setup: Optional[Callable[[Canvas], Any]] = None

    # -- authoring -----------------------------------------------------------

    def setup(self, fn: Callable[[Canvas], Any]):
        """Registers a function drawn under every step. Its return value is passed to each step."""
        self._setup = fn
        return fn

    def step(self, title: str, text: str, math: Optional[str] = None, fresh: bool = False):
        """Decorator that appends a step. The function receives (canvas, setup_result)."""
        def deco(fn):
            self.steps.append(Step(title, text, fn, math, fresh))
            return fn
        return deco

    # -- layout ------------------------------------------------------------

    @property
    def frame_width(self) -> float:
        return self.width

    def _caption_lines(self, st: Step):
        w = self.width - 2 * PAD
        return wrap(st.text, w, theme.CAPTION_SIZE)

    @property
    def caption_height(self) -> float:
        h = 0.0
        for st in self.steps:
            lines = len(self._caption_lines(st))
            hh = 16 + theme.STEP_TITLE_SIZE * 1.4 + lines * theme.CAPTION_SIZE * 1.4
            if st.math:
                hh += theme.MATH_SIZE * 1.9
            h = max(h, hh + 14)
        return h

    @property
    def frame_height(self) -> float:
        return HEADER_H + self.height + self.caption_height

    # -- rendering ---------------------------------------------------------

    def _draw_steps(self, c: Canvas, k: int):
        """Draws the setup and the steps visible at step k (0-based) into c."""
        start = 0
        for i in range(k + 1):
            if self.steps[i].fresh:
                start = i
        ctx = None
        if self._setup:
            with c.group(class_="setup"):
                ctx = self._setup(c)
        for i in range(start, k + 1):
            c.step_index = i
            c.is_new = i == k
            with c.group(class_=f"step step-{i + 1}" + (" new" if i == k else "")):
                if ctx is None:
                    _call(self.steps[i].draw, c, None)
                else:
                    _call(self.steps[i].draw, c, ctx)

    def drawing(self, k: int, id_prefix: str = "") -> Canvas:
        """Renders only the drawing area for step k (0-based), with no header or caption."""
        c = Canvas(self.width, self.height, id_prefix=id_prefix)
        self._draw_steps(c, k)
        return c

    def render_step(self, k: int, id_prefix: str = "") -> Canvas:
        """Renders step k (0-based) with header, drawing, and caption."""
        n = len(self.steps)
        st = self.steps[k]
        W, H = self.frame_width, self.frame_height
        c = Canvas(W, H, id_prefix=id_prefix)

        # header
        c.rect(0, 0, W, HEADER_H, color="none", fill=theme.PANEL)
        c.line(0, HEADER_H, W, HEADER_H, color=theme.GRID, width=1)
        c.text(PAD, HEADER_H / 2, self.title, size=theme.TITLE_SIZE - 2, weight="bold", anchor="start",
               color=theme.INK)
        label = f"Step {k + 1} of {n}"
        c.text(W - PAD, HEADER_H / 2 - 7, label, size=13, anchor="end", color=theme.SOFT_INK)
        dot_gap = min(14, (W / 3) / max(n, 1))
        for i in range(n):
            x = W - PAD - (n - 1 - i) * dot_gap - 4
            c.circle(x, HEADER_H / 2 + 11, 4, color=theme.BLUE if i <= k else theme.MUTED,
                     fill=theme.BLUE if i <= k else theme.PAPER, width=1.4)

        # drawing
        with c.translate(0, HEADER_H, class_="drawing"):
            self._draw_steps(c, k)

        # caption
        top = HEADER_H + self.height
        c.rect(0, top, W, self.caption_height, color="none", fill=theme.PANEL)
        c.line(0, top, W, top, color=theme.GRID, width=1)
        y = top + 16
        num = f"{k + 1}"
        c.circle(PAD + 11, y + 10, 12, color="none", fill=theme.BLUE)
        c.text(PAD + 11, y + 10, num, size=13, weight="bold", color=theme.PAPER)
        c.text(PAD + 32, y + 10, st.title, size=theme.STEP_TITLE_SIZE, weight="bold", anchor="start")
        y += theme.STEP_TITLE_SIZE * 1.4 + 6
        for ln in self._caption_lines(st):
            c.text(PAD, y, ln, size=theme.CAPTION_SIZE, anchor="start", baseline="hanging", color=theme.INK)
            y += theme.CAPTION_SIZE * 1.4
        if st.math:
            y += 6
            mw = text_width(st.math, theme.MATH_SIZE, "serif") + 24
            c.rect(PAD - 2, y - 4, mw, theme.MATH_SIZE + 12, color=theme.GRID, fill=theme.PAPER, rx=5, width=1)
            c.math(PAD + 10, y + theme.MATH_SIZE / 2 + 2, st.math, anchor="start", size=theme.MATH_SIZE)
        return c

    def render_all(self) -> List[Canvas]:
        return [self.render_step(k) for k in range(len(self.steps))]

    def final(self) -> Canvas:
        """Renders the last step's drawing alone, for thumbnails."""
        return self.drawing(len(self.steps) - 1)

    def storyboard(self, cols: Optional[int] = None, scale: float = 0.5, gap: float = 16) -> Canvas:
        """Renders every step side by side in a grid, scaled down."""
        n = len(self.steps)
        cols = cols or (n if n <= 3 else (2 if n == 4 else 3))
        rows = math.ceil(n / cols)
        fw, fh = self.frame_width * scale, self.frame_height * scale
        top = 74 if self.concept else 50
        W = cols * fw + (cols + 1) * gap
        H = top + rows * fh + (rows + 1) * gap
        c = Canvas(W, H)
        c.text(gap, 28, f"{self.title}: all steps", size=20, weight="bold", anchor="start")
        if self.concept:
            c.math(gap, 56, self.concept, size=17, anchor="start", color=theme.SOFT_INK)
        for k in range(n):
            r, col = divmod(k, cols)
            x = gap + col * (fw + gap)
            y = top + gap + r * (fh + gap)
            frame = self.render_step(k, id_prefix=f"s{k + 1}-")
            g = c.add(Element("g", transform=f"translate({fmt(x)},{fmt(y)}) scale({scale})"))
            _inline(frame, g)
            c.rect(x, y, fw, fh, color=theme.GRID, width=1)
        return c

    def animated(self, seconds: float = 4.0, hold_last: float = 2.5) -> Canvas:
        """Renders a looping animation that shows each step for `seconds`.

        Uses SMIL, which plays in browsers when the SVG is opened directly or
        embedded with <img>. Viewers without SMIL show step 1.
        """
        n = len(self.steps)
        durations = [seconds] * n
        durations[-1] += hold_last
        total = sum(durations)
        c = Canvas(self.frame_width, self.frame_height, background=None)
        t = 0.0
        for k in range(n):
            frame = self.render_step(k, id_prefix=f"a{k + 1}-")
            g = c.add(Element("g", opacity=1 if k == 0 else 0))
            _inline(frame, g)
            a, b = t / total, (t + durations[k]) / total
            if k == 0:
                key_times, values = f"0;{b:.4f};1", "1;0;0"
            elif k == n - 1:
                key_times, values = f"0;{a:.4f};1", "0;1;1"
            else:
                key_times, values = f"0;{a:.4f};{b:.4f};1", "0;1;0;0"
            g.add(Element("animate", attributeName="opacity", dur=f"{total:g}s", repeatCount="indefinite",
                          calcMode="discrete", keyTimes=key_times, values=values))
            t += durations[k]
        return c


def _call(fn, c, ctx):
    try:
        import inspect

        nparams = len(inspect.signature(fn).parameters)
    except (TypeError, ValueError):
        nparams = 2
    return fn(c) if nparams == 1 else fn(c, ctx)


def _inline(frame: Canvas, g: Element):
    """Copies a rendered canvas (defs, background, content) into group g."""
    svg = frame.to_element()
    for child in svg.children:
        if child.tag == "style":
            continue
        g.add(child)
