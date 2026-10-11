# 301 Algebra II, Trig and Precalculus

**Level:** 301 · **Lessons:** 12 · **Time:** about 15 to 20 hours of focused work
**Comes after:** [201 Algebra I and Geometry](../201/README.md) · **Leads to:** [401 Calculus](../401/README.md)

## Overview

This level builds the toolkit that calculus assumes you already own. It has two halves that meet at the end.

The algebra half studies whole families of functions: what inputs they accept, how to chain and undo them, and how their graphs behave. Polynomials, rational functions, exponentials and logarithms each get a lesson. Logarithms get extra care, since base 2 and log scales run through all of computing.

The trigonometry half starts from a single right triangle and ends with waves. The unit circle extends sine and cosine to every angle, radians replace degrees, and the laws of sines and cosines solve any triangle.

Conic sections and sequences and series round out the level. The last lesson gathers every "approaches but never arrives" idea from the earlier lessons into one concept, the limit, which is the door into 401.

Every lesson follows the same shape: a picture first, then the idea built step by step, worked examples with a reason on every line, common mistakes, exercises with hidden answers, and a small Go program in a `code` folder with its real output. Each lesson also has a `cards.tsv` file of flashcards you can import into Anki.

## Outcomes

After 301 you can:

* Find the domain and range of a function, compose functions, find inverses, and sketch graphs by shifting and stretching a parent graph.
* Sketch a polynomial from its factors and do arithmetic with complex numbers.
* Find the asymptotes, holes and zeros of a rational function.
* Model growth and decay with exponentials, and solve exponential equations with logarithms.
* Reason in orders of magnitude and base 2: read log scales, count bits, and explain why binary search is $O(\log n)$.
* Solve right triangles with sine, cosine and tangent, and any triangle with the laws of sines and cosines.
* Use radians and the unit circle to evaluate trig functions at any angle.
* Graph $y = A\sin(B(x - C)) + D$ and use the core trig identities.
* Recognize the four conic sections from their equations and their focus definitions.
* Sum arithmetic and geometric series, including infinite geometric series.
* Explain what a limit is, and compute simple limits by substitution, factoring, tables and comparison of leading terms.

## Prerequisite Map

<!-- diagram: type=prerequisite-map nodes=201,01..12,401 columns=algebra,middle,trig caption="How the 301 lessons depend on each other" -->
![A flow chart. The dashed box 201 Algebra I and Geometry at the top points to two columns. The left column runs 01 Functions in Depth, 02 Polynomials and Complex Numbers, 03 Rational Functions, 04 Exponential Functions, 05 Logarithms. The right column runs 06 Right-Triangle Trig, 07 Unit Circle and Radians, 08 Trig Graphs and Identities, 09 Laws of Sines and Cosines. In the middle, 01 points to 10 Conic Sections and 04 points to 11 Sequences and Series. Lessons 05, 11 and 09 all point to the highlighted 12 Limits Preview, which points to the dashed box 401 Calculus.](img/prerequisite-map.svg)

The two columns are independent. Work them in order, or alternate between them if a change of scenery helps. Lessons 10 and 11 need only the lesson that points to them. Lesson 12 draws on everything.

## Lessons

| # | Lesson | Core ideas | Time |
|---|---|---|---|
| 1 | [Functions in Depth](01-functions-in-depth/README.md) | domain and range, composition, inverses, transformations | 60 to 90 min |
| 2 | [Polynomials and Complex Numbers](02-polynomials-and-complex-numbers/README.md) | end behavior, zeros and multiplicity, synthetic division, $i$, the complex plane | 75 to 100 min |
| 3 | [Rational Functions](03-rational-functions/README.md) | asymptotes, holes, work rates | 60 to 90 min |
| 4 | [Exponential Functions](04-exponential-functions/README.md) | exponent rules, growth and decay, half-life, $e$ | 60 to 90 min |
| 5 | [Logarithms](05-logarithms/README.md) | log as exponent, log scales, base 2 and bits, log laws | 75 to 100 min |
| 6 | [Right-Triangle Trigonometry](06-right-triangle-trigonometry/README.md) | SOH CAH TOA, special triangles, inverse trig | 60 to 90 min |
| 7 | [The Unit Circle and Radians](07-unit-circle-and-radians/README.md) | radians, arc length, $(\cos\theta, \sin\theta)$, reference angles | 75 to 100 min |
| 8 | [Trig Graphs and Identities](08-trig-graphs-and-identities/README.md) | amplitude, period, phase, Pythagorean and sum identities | 90 to 120 min |
| 9 | [Laws of Sines and Cosines](09-laws-of-sines-and-cosines/README.md) | solving any triangle, the ambiguous case, area | 60 to 90 min |
| 10 | [Conic Sections](10-conic-sections/README.md) | circle, parabola, ellipse, hyperbola, completing the square | 75 to 100 min |
| 11 | [Sequences and Series](11-sequences-and-series/README.md) | arithmetic and geometric sums, sigma notation, infinite series | 75 to 100 min |
| 12 | [Limits Preview](12-limits-preview/README.md) | limits, continuity, tangent slopes, area by rectangles | 60 to 90 min |

Then take the [301 Checkpoint](checkpoint.md).

## How to Use This Level

* Read the picture before the prose. If the picture makes sense, the prose confirms it.
* Do the worked examples yourself on paper before reading the reasons column.
* Attempt every exercise before opening the answers. Wrong answers you discover yourself teach more than right answers you read.
* Run each lesson's Go program, then change one number and predict the new output before you run it again.
* Import each lesson's `cards.tsv` into Anki (tab-separated, three fields: front, back, tags) and review a few minutes a day.

## Related Material

* Tracks: [Algebra](../../tracks/algebra/README.md), [Trigonometry](../../tracks/trigonometry/README.md), [Geometry](../../tracks/geometry/README.md), [Complex Analysis](../../tracks/complex-analysis/README.md), [Calculus](../../tracks/calculus/README.md).
* Workshops: [Exponential Growth in Interest, Epidemics and Load](../../workshops/exponential-growth-in-interest-epidemics-and-load/README.md), [Statistics for Monitoring and Anomaly Detection](../../workshops/statistics-for-monitoring-and-anomaly-detection/README.md), [Calculus of Rates in Physics and Queues](../../workshops/calculus-of-rates-in-physics-and-queues/README.md).
* Free textbook: [OpenStax Precalculus 2e](https://openstax.org/details/books/precalculus-2e) covers this whole level with many more exercises.
