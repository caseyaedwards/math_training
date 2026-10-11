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

The `showcase` command builds the showcase site in `showcase/` in about five seconds. Open it in a browser to see every diagram with its animation, a step viewer, every step with its caption, and a storyboard:

```sh
python3 -m svgmath showcase && open showcase/index.html
```

The generated files are not committed. The course site builds the showcase in CI and serves it under `/diagrams/`. The `showcase/manifest.json` file lists every diagram with its step files, titles, captions, and math, for embedding in lessons.

## Catalog

The generator has 165 diagram types across 17 categories:

| Category | Examples |
| --- | --- |
| Arithmetic | base-ten blocks, area model, long division, order of operations tree, decimal zoom |
| Fractions and Ratios | fraction strips, equivalent fractions, fraction area and division, percent grid, tape diagram |
| Number Theory | factor trees, sieve of Eratosthenes, GCD and LCM, Euclidean algorithm, modular clock, binary |
| Algebra | balance scale, algebra tiles, completing the square, slope, systems, parabolas, exponents |
| Functions | function machine, mapping diagram, transformations, inverses, composition, asymptotes |
| Geometry | angle sums, Pythagorean proof, constructions, transformations, circle area, nets, volume |
| Trigonometry | SOH-CAH-TOA, unit circle, radians, sine from the circle, law of cosines |
| Complex Numbers | complex plane, multiplication as rotation, roots of unity |
| Calculus | secant to tangent, epsilon-delta, derivative graph, Riemann sums, FTC, Taylor, Newton |
| Differential Equations | slope fields, Euler's method, exponential decay |
| Linear Algebra | vectors, span, dot product, matrix transformations, determinants, eigenvectors, elimination |
| Probability | probability trees, Bayes with counts and areas, dice grid, binomial, law of large numbers |
| Statistics | mean and median, box plot, histogram, standard deviation, normal curve, regression, CLT |
| Discrete Math | Pascal's triangle, permutations and combinations, pigeonhole, Euler paths |
| Logic and Proof | truth tables, logic gates, set operations, induction, contradiction, flowchart proofs |
| Sequences and Series | geometric series, Gauss sum, Fibonacci, Sierpinski, harmonic series |
| Concept Maps | number systems, branches of mathematics |

Run `python3 -m svgmath list` for the full list.

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
