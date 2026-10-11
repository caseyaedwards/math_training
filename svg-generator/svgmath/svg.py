"""A small SVG builder with math-aware text.

`Canvas` collects elements into nested groups and serializes them to an
SVG string. All coordinates are SVG pixels with y pointing down. For math
coordinates with y pointing up, wrap a region of the canvas in a
`svgmath.plane.Plane`.
"""

from __future__ import annotations

import math
import numbers
import re
from contextlib import contextmanager
from typing import Iterable, Iterator, Optional, Sequence, Tuple

from . import theme

Point = Tuple[float, float]


def fmt(v: float) -> str:
    """Formats a number compactly for SVG output."""
    if isinstance(v, str):
        return v
    v = float(v)  # accepts Fraction, Decimal, and other real numbers
    if v != v or v in (math.inf, -math.inf):
        raise ValueError(f"cannot write non-finite number {v!r} to SVG")
    r = round(v, 2)
    if r == int(r):
        return str(int(r))
    return f"{r:.2f}".rstrip("0").rstrip(".")


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class Element:
    """One SVG node. Attribute names use underscores for dashes."""

    def __init__(self, tag: str, text: Optional[str] = None, raw: bool = False, **attrs):
        self.tag = tag
        self.text = text
        self.raw = raw  # text is already-escaped markup
        self.attrs = {}
        self.children: list = []
        self.set(**attrs)

    def set(self, **attrs) -> "Element":
        for k, v in attrs.items():
            if v is None:
                continue
            name = k.rstrip("_").replace("_", "-")
            if name in ("class", "klass"):
                name = "class"
            self.attrs[name] = v
        return self

    def add(self, child: "Element") -> "Element":
        self.children.append(child)
        return child

    def render(self, indent: int = 0) -> str:
        pad = "  " * indent
        attrs = "".join(
            f' {k}="{esc(fmt(v) if isinstance(v, numbers.Real) else v)}"'
            for k, v in self.attrs.items()
        )
        if not self.children and self.text is None:
            return f"{pad}<{self.tag}{attrs}/>"
        if not self.children:
            body = self.text if self.raw else esc(self.text)
            return f"{pad}<{self.tag}{attrs}>{body}</{self.tag}>"
        if self.tag in ("text", "tspan"):
            # whitespace between tspans renders as a visible space, so keep them on one line
            inner = "".join(c.render(0) for c in self.children)
            head = (self.text if self.raw else esc(self.text)) if self.text else ""
            return f"{pad}<{self.tag}{attrs}>{head}{inner}</{self.tag}>"
        inner = "\n".join(c.render(indent + 1) for c in self.children)
        head = (self.text if self.raw else esc(self.text)) if self.text else ""
        return f"{pad}<{self.tag}{attrs}>{head}\n{inner}\n{pad}</{self.tag}>"


# ---------------------------------------------------------------------------
# Math text
#
# A tiny markup for inline math, rendered with <tspan> elements:
#   x^2  x^{n+1}   superscript
#   a_1  a_{n-1}   subscript
#   *x*            italic run is automatic for single latin letters
#   sqrt(...)      becomes the radical sign followed by the argument
#   \pi \theta ... Greek letters and common symbols (see SYMBOLS)
# Plain text outside of these markers passes through unchanged.
# ---------------------------------------------------------------------------

SYMBOLS = {
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ",
    r"\Delta": "Δ", r"\epsilon": "ε", r"\theta": "θ", r"\lambda": "λ",
    r"\mu": "μ", r"\pi": "π", r"\sigma": "σ", r"\Sigma": "Σ", r"\phi": "φ",
    r"\omega": "ω", r"\Omega": "Ω", r"\infty": "∞", r"\cdot": "·",
    r"\times": "×", r"\div": "÷", r"\pm": "±", r"\leq": "≤", r"\geq": "≥",
    r"\neq": "≠", r"\approx": "≈", r"\to": "→", r"\implies": "⇒",
    r"\iff": "⇔", r"\in": "∈", r"\notin": "∉", r"\cup": "∪", r"\cap": "∩",
    r"\subset": "⊂", r"\emptyset": "∅", r"\int": "∫", r"\sum": "∑",
    r"\prod": "∏", r"\partial": "∂", r"\nabla": "∇", r"\forall": "∀",
    r"\exists": "∃", r"\neg": "¬", r"\land": "∧", r"\lor": "∨",
    r"\deg": "°", r"\angle": "∠", r"\perp": "⊥", r"\parallel": "∥",
    r"\triangle": "△", r"\sqrt": "√", r"\equiv": "≡", r"\prime": "′",
    r"\mathbb{R}": "ℝ", r"\mathbb{Z}": "ℤ", r"\mathbb{N}": "ℕ",
    r"\mathbb{Q}": "ℚ", r"\mathbb{C}": "ℂ", r"\ldots": "…", r"\cdots": "⋯",
    r"\leftrightarrow": "↔", r"\Rightarrow": "⇒", r"\circ": "∘", r"\varphi": "φ", r"\rho": "ρ",
    r"\tau": "τ", r"\psi": "ψ", r"\chi": "χ", r"\eta": "η", r"\zeta": "ζ", r"\kappa": "κ",
}

_SYMBOL_RE = re.compile("|".join(re.escape(k) for k in sorted(SYMBOLS, key=len, reverse=True)))


def replace_symbols(s: str) -> str:
    s = re.sub(r"\\bar\{(.)\}", "\\1\u0305", s)
    s = re.sub(r"\\hat\{(.)\}", "\\1\u0302", s)
    s = s.replace("\\%", "%")
    s = _SYMBOL_RE.sub(lambda m: SYMBOLS[m.group(0)], s)
    return s.replace("sqrt(", "√(")


def _parse_math(s: str):
    """Splits math markup into (text, mode) runs. mode is '', 'sup', or 'sub'."""
    s = replace_symbols(s)
    # a hyphen between spaces, at the start, or before a digit, letter, or bracket is a minus sign
    s = re.sub(r"(^|[\s(=+\-−,\[{^_])-(?=[\s\dA-Za-z(√.∞\u0370-\u03ff])", lambda m: m.group(1) + "−", s)
    s = re.sub(r"(?<=[A-Za-z0-9)])-(?=[\d(])", "−", s)
    runs = []
    buf = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c in "^_" and i + 1 < len(s):
            if buf:
                runs.append((buf, ""))
                buf = ""
            mode = "sup" if c == "^" else "sub"
            if s[i + 1] == "{":
                depth, j = 1, i + 2
                while j < len(s) and depth:
                    depth += {"{": 1, "}": -1}.get(s[j], 0)
                    j += 1
                runs.append((s[i + 2 : j - 1], mode))
                i = j
            else:
                # a single token: a run of digits, or one character
                m = re.match(r"-?\d+(\.\d+)?|.", s[i + 1 :])
                runs.append((m.group(0), mode))
                i += 1 + len(m.group(0))
            continue
        buf += c
        i += 1
    if buf:
        runs.append((buf, ""))
    return runs


def _italicize(run: str):
    """Splits a run into (text, italic) pieces: lone latin letters are italic."""
    out = []
    for m in re.finditer(r"(?<![A-Za-z])[A-Za-z][\u0300-\u036f]*(?![A-Za-z])|[^A-Za-z]+|[A-Za-z]+", run):
        tok = m.group(0)
        italic = len(tok.rstrip("\u0300\u0301\u0302\u0303\u0304\u0305")) == 1 and tok[0].isalpha()
        out.append((tok, italic))
    return out


def math_tspans(el: Element, s: str, italic_vars: bool = True) -> Element:
    """Fills a <text> element with tspans that render the math markup in s."""
    shift = 0.0
    for text, mode in _parse_math(s):
        target = 0.0
        size = None
        if mode == "sup":
            target, size = -0.42, "70%"
        elif mode == "sub":
            target, size = 0.25, "70%"
        dy = target - shift
        shift = target
        pieces = _italicize(text) if italic_vars else [(text, False)]
        for k, (tok, italic) in enumerate(pieces):
            ts = Element("tspan", tok)
            if k == 0 and abs(dy) > 1e-9:
                ts.set(dy=f"{dy:.2f}em")
            if size:
                ts.set(font_size=size)
            if italic:
                ts.set(font_style="italic")
            el.add(ts)
    return el


def text_width(s: str, size: float, font: str = "sans") -> float:
    """Estimates rendered text width in px. Good enough for layout."""
    plain = replace_symbols(re.sub(r"[\^_]\{?|\}", "", s))
    factor = {"sans": 0.55, "serif": 0.56, "mono": 0.6}.get(font, 0.55)
    w = 0.0
    for ch in plain:
        if font == "mono":
            w += 1.0
        elif ch in "il.,:;|!'1 ()[]":
            w += 0.55
        elif ch in "mwMW":
            w += 1.6
        elif ch.isupper():
            w += 1.25
        else:
            w += 1.0
    return w * size * factor


def wrap(s: str, width: float, size: float, font: str = "sans") -> list:
    """Wraps text into lines that fit within width px."""
    lines = []
    for para in s.split("\n"):
        words = para.split()
        line = ""
        for w in words:
            cand = (line + " " + w).strip()
            if line and text_width(cand, size, font) > width:
                lines.append(line)
                line = w
            else:
                line = cand
        lines.append(line)
    return lines


# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------


class Canvas:
    """Collects SVG elements. Drawing methods return the created element."""

    def __init__(self, width: float, height: float, background: Optional[str] = theme.PAPER,
                 id_prefix: str = ""):
        self.width = width
        self.height = height
        self.root = Element("g")
        self._stack = [self.root]
        self.defs = Element("defs")
        self._ids: set = set()
        self._marker_ids: dict = {}
        self.background = background
        self.style = ""
        self.id_prefix = id_prefix  # keeps ids unique when canvases are combined
        self.step_index = 0  # set by Walkthrough while drawing a step
        self.is_new = True  # True while drawing the newest step of a walkthrough

    # -- structure ---------------------------------------------------------

    @property
    def current(self) -> Element:
        return self._stack[-1]

    def add(self, el: Element) -> Element:
        return self.current.add(el)

    @contextmanager
    def group(self, **attrs) -> Iterator[Element]:
        g = self.add(Element("g", **attrs))
        self._stack.append(g)
        try:
            yield g
        finally:
            self._stack.pop()

    def translate(self, dx: float, dy: float, **attrs):
        return self.group(transform=f"translate({fmt(dx)},{fmt(dy)})", **attrs)

    def unique_id(self, base: str) -> str:
        i = 1
        base = self.id_prefix + base
        name = base
        while name in self._ids:
            i += 1
            name = f"{base}-{i}"
        self._ids.add(name)
        return name

    def clip_rect(self, x: float, y: float, w: float, h: float) -> str:
        """Defines a rectangular clip path and returns its url() reference."""
        cid = self.unique_id("clip")
        cp = self.defs.add(Element("clipPath", id=cid))
        cp.add(Element("rect", x=x, y=y, width=w, height=h))
        return f"url(#{cid})"

    def marker(self, color: str, kind: str = "arrow") -> str:
        """Returns a url() for an arrowhead marker in the given color."""
        key = (color, kind)
        if key not in self._marker_ids:
            mid = self.unique_id(f"m-{kind}-{color.strip('#')}")
            m = self.defs.add(
                Element(
                    "marker", id=mid, viewBox="0 0 10 10", refX=8.5, refY=5,
                    markerWidth=11, markerHeight=11, orient="auto-start-reverse",
                    markerUnits="userSpaceOnUse",
                )
            )
            if kind == "arrow":
                m.add(Element("path", d="M0,0.5 L10,5 L0,9.5 L2.5,5 Z", fill=color))
            elif kind == "dot":
                m.set(refX=5)
                m.add(Element("circle", cx=5, cy=5, r=4, fill=color))
            self._marker_ids[key] = mid
        return f"url(#{self._marker_ids[key]})"

    # -- primitives ------------------------------------------------------

    def line(self, x1, y1, x2, y2, color=theme.INK, width=theme.STROKE, dash=None, **kw):
        return self.add(Element(
            "line", x1=x1, y1=y1, x2=x2, y2=y2, stroke=color, stroke_width=width,
            stroke_dasharray=dash, stroke_linecap="round", **kw,
        ))

    def arrow(self, x1, y1, x2, y2, color=theme.INK, width=theme.STROKE, both=False, dash=None, **kw):
        """Draws a straight arrow from (x1, y1) to (x2, y2)."""
        m = self.marker(color)
        return self.line(x1, y1, x2, y2, color=color, width=width, dash=dash,
                         marker_end=m, marker_start=m if both else None, **kw)

    def curved_arrow(self, x1, y1, x2, y2, bend=0.3, color=theme.INK, width=theme.STROKE, dash=None, **kw):
        """Draws an arc-shaped arrow. Positive bend curves to the left of travel."""
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        cx, cy = mx + dy * bend, my - dx * bend
        d = f"M{fmt(x1)},{fmt(y1)} Q{fmt(cx)},{fmt(cy)} {fmt(x2)},{fmt(y2)}"
        return self.path(d, color=color, width=width, dash=dash, marker_end=self.marker(color), **kw)

    def rect(self, x, y, w, h, color=theme.INK, fill="none", width=theme.STROKE, rx=0, dash=None, **kw):
        if w < 0:
            x, w = x + w, -w
        if h < 0:
            y, h = y + h, -h
        return self.add(Element(
            "rect", x=x, y=y, width=w, height=h, rx=rx or None, stroke=color,
            fill=fill, stroke_width=width if color != "none" else None,
            stroke_dasharray=dash, **kw,
        ))

    def circle(self, cx, cy, r, color=theme.INK, fill="none", width=theme.STROKE, dash=None, **kw):
        return self.add(Element(
            "circle", cx=cx, cy=cy, r=r, stroke=color, fill=fill,
            stroke_width=width if color != "none" else None, stroke_dasharray=dash, **kw,
        ))

    def ellipse(self, cx, cy, rx, ry, color=theme.INK, fill="none", width=theme.STROKE, dash=None, **kw):
        return self.add(Element(
            "ellipse", cx=cx, cy=cy, rx=rx, ry=ry, stroke=color, fill=fill,
            stroke_width=width, stroke_dasharray=dash, **kw,
        ))

    def dot(self, x, y, r=4.5, color=theme.INK, hollow=False, **kw):
        """Draws a point. hollow=True draws an open circle (excluded endpoint)."""
        return self.circle(x, y, r, color=color, fill=theme.PAPER if hollow else color,
                           width=2 if hollow else 0.0001, **kw)

    def polyline(self, pts: Sequence[Point], color=theme.INK, width=theme.STROKE, dash=None, fill="none", **kw):
        return self.add(Element(
            "polyline", points=" ".join(f"{fmt(x)},{fmt(y)}" for x, y in pts),
            stroke=color, stroke_width=width, fill=fill, stroke_dasharray=dash,
            stroke_linejoin="round", stroke_linecap="round", **kw,
        ))

    def polygon(self, pts: Sequence[Point], color=theme.INK, fill="none", width=theme.STROKE, dash=None, **kw):
        return self.add(Element(
            "polygon", points=" ".join(f"{fmt(x)},{fmt(y)}" for x, y in pts),
            stroke=color, fill=fill, stroke_width=width if color != "none" else None,
            stroke_dasharray=dash, stroke_linejoin="round", **kw,
        ))

    def path(self, d: str, color=theme.INK, fill="none", width=theme.STROKE, dash=None, **kw):
        return self.add(Element(
            "path", d=d, stroke=color, fill=fill, stroke_width=width if color != "none" else None,
            stroke_dasharray=dash, stroke_linejoin="round", stroke_linecap="round", **kw,
        ))

    def arc(self, cx, cy, r, start_deg, end_deg, color=theme.INK, width=theme.STROKE, fill="none",
            arrow=False, dash=None, sector=False, **kw):
        """Draws a circular arc. Angles are math-style degrees, counterclockwise from +x."""
        a0, a1 = math.radians(start_deg), math.radians(end_deg)
        x0, y0 = cx + r * math.cos(a0), cy - r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy - r * math.sin(a1)
        sweep = end_deg - start_deg
        large = 1 if abs(sweep) > 180 else 0
        flag = 0 if sweep > 0 else 1
        d = f"M{fmt(x0)},{fmt(y0)} A{fmt(r)},{fmt(r)} 0 {large} {flag} {fmt(x1)},{fmt(y1)}"
        if sector:
            d = f"M{fmt(cx)},{fmt(cy)} L{fmt(x0)},{fmt(y0)} " + d[d.index("A"):] + " Z"
        return self.path(d, color=color, width=width, fill=fill, dash=dash,
                         marker_end=self.marker(color) if arrow else None, **kw)

    def text(self, x, y, s, size=theme.LABEL_SIZE, color=theme.INK, anchor="middle", weight=None,
             font="sans", italic=False, math=False, baseline="middle", halo=False, **kw):
        """Draws text. math=True enables x^2 / a_1 / \\pi markup and serif italics.

        anchor: start, middle, end. baseline: middle (centered on y), auto (y is baseline),
        hanging (y is top). halo=True draws a white outline so labels stay legible over lines.
        """
        family = {"sans": theme.SANS, "serif": theme.SERIF, "mono": theme.MONO}[font]
        if math:
            family = theme.SERIF
        el = Element(
            "text", x=x, y=y, font_size=size, fill=color, text_anchor=anchor,
            font_family=family, font_weight=weight,
            font_style="italic" if italic else None,
            dominant_baseline={"middle": "central", "auto": None, "hanging": "hanging"}[baseline],
            **kw,
        )
        if halo:
            el.set(stroke=theme.PAPER, stroke_width=4, stroke_linejoin="round", paint_order="stroke")
        if math:
            math_tspans(el, s)
        else:
            el.text = str(s)
        return self.add(el)

    def math(self, x, y, s, size=theme.MATH_SIZE, **kw):
        """Shorthand for text(..., math=True)."""
        return self.text(x, y, s, size=size, math=True, **kw)

    def paragraph(self, x, y, s, width, size=theme.CAPTION_SIZE, color=theme.INK, line_height=1.35,
                  anchor="start", math=False, **kw) -> float:
        """Draws wrapped text starting at top-left (x, y). Returns the height used."""
        lines = wrap(s, width, size)
        for i, ln in enumerate(lines):
            self.text(x, y + i * size * line_height, ln, size=size, color=color, anchor=anchor,
                      baseline="hanging", math=math, **kw)
        return len(lines) * size * line_height

    def label_box(self, x, y, s, size=theme.LABEL_SIZE, color=theme.INK, fill=theme.PAPER,
                  border=None, math=False, pad=6, anchor="middle"):
        """Draws text inside a rounded box centered at (x, y)."""
        w = text_width(s, size, "serif" if math else "sans") * (1.12 if math else 1.0) + 2 * pad
        h = size + 2 * pad - 2
        left = {"middle": x - w / 2, "start": x, "end": x - w}[anchor]
        self.rect(left, y - h / 2, w, h, color=border or "none", fill=fill, width=1.5, rx=5)
        return self.text(left + w / 2, y, s, size=size, color=color, math=math)

    # -- output ------------------------------------------------------------

    def to_element(self) -> Element:
        svg = Element(
            "svg", xmlns="http://www.w3.org/2000/svg", width=self.width, height=self.height,
            viewBox=f"0 0 {fmt(self.width)} {fmt(self.height)}",
            font_family=theme.SANS,
        )
        if self.style:
            svg.add(Element("style", self.style, raw=True))
        if self.defs.children:
            svg.add(self.defs)
        if self.background:
            svg.add(Element("rect", x=0, y=0, width=self.width, height=self.height, fill=self.background))
        for c in self.root.children:
            svg.add(c)
        return svg

    def to_svg(self) -> str:
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + self.to_element().render() + "\n"

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_svg())
