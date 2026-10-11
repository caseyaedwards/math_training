# Authoring Diagram Types

This guide describes how to add a diagram type to `svgmath`. Each diagram type is a worked example that builds up one idea per step.

## What a Good Diagram Looks Like

A good diagram teaches a visual learner the idea without the text, and the text confirms what the picture shows:

- One new idea per step. Each step adds a few marks to the previous picture.
- Three to six steps. Simple ideas need three. Proofs and multi-stage methods need up to eight.
- The last step shows the result, labeled, with the answer in the caption math line.
- Color carries meaning. A quantity keeps its color in every step and in the caption.
- Labels sit next to what they name. Use `halo=True` on labels that cross lines.
- Real numbers. Pick an example with clean values, and compute values in code rather than typing them.

## Files

Each diagram family lives in one module in `svgmath/diagrams/`. A module can register several diagram types. The registry imports every module in that folder, so a new file needs no other changes.

```python
"""Pythagorean theorem diagrams."""

from __future__ import annotations

from .. import theme
from ..annotate import right_angle, segment_label
from ..plane import Plane
from ..registry import diagram
from ..walkthrough import Walkthrough


@diagram("pythagorean-theorem", "Pythagorean Theorem", "Geometry")
def build() -> Walkthrough:
    wt = Walkthrough(
        "pythagorean-theorem", "Pythagorean Theorem", "Geometry",
        concept="a^2 + b^2 = c^2",
        summary="The squares on the two legs of a right triangle together have the same area "
                "as the square on the hypotenuse.",
        width=640, height=420, level="201",
    )

    @wt.setup
    def _(c):
        return Plane(c, box=(40, 20, 560, 380), x=(-5, 9), y=(-4, 9), equal=True)

    @wt.step("Draw a right triangle", "The legs a = 3 and b = 4 meet at a right angle.", math="a = 3, b = 4")
    def _(c, p):
        p.polygon([(0, 0), (4, 0), (0, 3)], color=theme.INK)

    return wt
```

Rules for the code:

- Python 3.9 or later, standard library only. Start each module with `from __future__ import annotations`.
- The `@diagram` slug, title, and category must match the `Walkthrough` arguments. The tests check this.
- Use a category from `CATEGORIES` in `svgmath/registry.py`.
- Use colors from `svgmath/theme.py`. Do not type hex values.
- The setup function draws what every step shares, such as axes, and returns an object passed to each step. Return a `Plane`, a dict, or any value.
- A step with `fresh=True` drops the drawings of earlier steps. Use it when a step replaces a picture, for example a finer set of rectangles.
- Inside a step, `c.is_new` is `True` while the newest step draws. Use it to highlight what changed.

## API Summary

`Canvas` in `svgmath/svg.py`, pixel coordinates with y pointing down:

- `line`, `arrow`, `curved_arrow`, `rect`, `circle`, `ellipse`, `dot`, `polyline`, `polygon`, `path`, `arc`
- `text(x, y, s, size, color, anchor, weight, math, halo)` and `math(x, y, s)` for math markup
- `paragraph` for wrapped text, `label_box` for text in a rounded box
- `group(**attrs)` and `translate(dx, dy)` as context managers, `clip_rect` for a clip path

`Plane` in `svgmath/plane.py`, world coordinates with y pointing up:

- `grid`, `axes`, `plot`, `parametric`, `polar`
- `shade_between`, `shade_under`, `region`, `polygon`, `rect`, `circle`
- `point`, `segment`, `vector`, `line_through`, `vline`, `hline`, `label`
- `px(x, y)` converts world to pixels, `length(d)` converts a distance
- `equal=True` keeps one unit the same length on both axes, so circles stay round

Annotations in `svgmath/annotate.py`, pixel coordinates:

- `brace`, `angle_mark`, `right_angle`, `tick_marks`, `segment_label`, `dimension`, `callout`
- `number_line` returns a function from value to x, and `hop` draws a jump arc
- `table` draws a grid of cells with optional highlights

Math markup for any text drawn with `math=True` and for `concept` and step `math`:

| Markup | Result |
| --- | --- |
| `x^2`, `x^{n+1}` | superscript |
| `a_1`, `a_{n-1}` | subscript |
| `\pi`, `\theta`, `\Delta`, `\int`, `\sum`, `\infty` | Greek letters and symbols, see `SYMBOLS` in `svgmath/svg.py` |
| `\cdot`, `\times`, `\leq`, `\neq`, `\approx`, `\to` | operators |
| `sqrt(2)` | √(2) |

Single latin letters render in italics, and a hyphen before a number becomes a minus sign.

## Writing Rules

Captions follow the [Axibase technical writing guide](https://axibase.com/use-cases/workshop/technical-writing.html):

- Present tense, active voice. Describe what happens, or use the imperative: "Draw the radius", "The sum approaches the area."
- No "will", "should", "please", "in order to", "make sure", "e.g.", or "i.e.". Write "for example" instead.
- No contractions.
- Step titles use sentence case and have no terminal period.
- Write out numbers one through ten in prose, except next to units or in math.
- Keep each step text to one to three sentences.

The tests in `tests/test_diagrams.py` flag the banned words.

## Check Your Work

```sh
cd svg-generator
python3 -m unittest discover -s tests
python3 -m svgmath render pythagorean-theorem --out /tmp/svg
tools/snapshot.sh /tmp/svg/pythagorean-theorem/step-03.svg /tmp/step3.png
```

The snapshot script renders an SVG to PNG with headless Chrome, so you can inspect every step for overlapping labels, clipped text, and wrong values.
