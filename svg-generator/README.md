# SVG Math Diagram Generator

`svgmath` draws math concepts as step-by-step SVG diagrams. Each diagram type is a worked example that adds one idea per step, with a caption that explains the step and a line of math that records it.

Every diagram type produces:

- one SVG per step, with a header, the drawing, and a caption
- a storyboard with all steps in a grid
- an animated SVG that plays the steps in a loop
- the final drawing alone, for thumbnails

## Requirements

Python 3.9 or later. The generator uses the standard library only, so there is nothing to install.

## Usage

Run the commands from the `svg-generator` folder:

```sh
python3 -m svgmath list
python3 -m svgmath render riemann-sum --out /tmp/svg
python3 -m svgmath showcase
```

The `showcase` command rebuilds the [showcase site](showcase/README.md) in `showcase/`. Open `showcase/index.html` in a browser to see every diagram with its animation, steps, and storyboard.

## Write Your Own Diagram

Use the building blocks directly from Python:

```python
from svgmath import Canvas, Plane, theme

c = Canvas(480, 320)
p = Plane(c, box=(40, 20, 400, 280), x=(-3, 3), y=(-1, 9))
p.grid()
p.axes()
p.plot(lambda x: x * x, color=theme.BLUE, label="y = x^2")
c.save("parabola.svg")
```

To add a diagram type to the showcase, follow the [authoring guide](AUTHORING.md).

## Layout

| Path | Contents |
| --- | --- |
| `svgmath/svg.py` | `Canvas`, SVG elements, math text markup |
| `svgmath/plane.py` | `Plane`: axes, grids, plots, shading in math coordinates |
| `svgmath/annotate.py` | braces, angle marks, callouts, number lines, tables |
| `svgmath/walkthrough.py` | `Walkthrough`: steps, captions, storyboard, animation |
| `svgmath/diagrams/` | one module per diagram family |
| `svgmath/showcase.py` | builds the HTML showcase |
| `tests/` | render checks and writing-rule checks for every diagram |
| `tools/snapshot.sh` | renders an SVG to PNG with headless Chrome |
