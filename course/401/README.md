# 401: Calculus

Calculus is the mathematics of change and accumulation. It answers two questions about anything that moves:

* **How fast is it changing right now?** That is the derivative.
* **How much has piled up so far?** That is the integral.

The surprise at the heart of the subject is that these two questions undo each other. An SRE already lives this every day: a request counter is the integral of the request rate, and the rate is the derivative of the counter. This level turns that working instinct into tools you can reason with.

## What You Learn

By the end of 401 you can:

1. Explain a limit with the epsilon band picture and compute limits that start as $0/0$.
2. Find a derivative from the definition, then quickly with the power, product, quotient, and chain rules.
3. Use derivatives to find optimal values, estimate with tangent lines, and solve related rates problems.
4. Build an integral as a Riemann sum and evaluate it with the Fundamental Theorem of Calculus.
5. Integrate with substitution and by parts, and check every answer by differentiating.
6. Compute areas between curves, volumes of round solids, and average values.
7. Decide whether a series converges, and sum geometric series.
8. Build Taylor polynomials and know when small-$x$ shortcuts are safe.
9. Compute partial derivatives and gradients, and read a double integral as a sum of columns.
10. Translate between counters, rates, windows, and totals in monitoring systems, and say which calculus idea each one is.

## Before You Start

You need comfort with functions and graphs, factoring, exponent laws, logarithms, the unit circle, and sigma notation. All of it is in [301 Algebra II, Trig and Precalculus](../301/README.md). If any of it feels rusty, take the 301 checkpoint (linked from the [301 overview](../301/README.md)) first. Calculus is mostly algebra with one new idea, and most calculus mistakes are algebra mistakes in disguise.

## Prerequisite Map

<!-- diagram: type=dag nodes="301 prerequisites, 01..12" edges="301 seq->10, 301 functions->01, 301 exp/log/trig->01, 01->02, 02->03, 03->04, 03->05, 03->11, 10->11, 03->12, 01->06, 06->07, 02->07, 07->08, 08->09, 07->12, 01->10" caption="Prerequisite map for 401" -->
![A flow diagram. Three dashed boxes on the left are 301 prerequisites: sequences and series, functions and graphs, and exponentials, logs and trig. Functions and exp-log-trig feed lesson 01 Limits and Continuity; 301 sequences feeds lesson 10. From 01, arrows lead to 02 The Derivative, 06 Riemann Sums, and 10 Sequences and Series. 02 leads to 03 Derivative Rules and 07 Fundamental Theorem. 03 leads to 04 Optimization, 05 Related Rates, 11 Taylor Series, and 12 Multivariable Intro. 06 leads to 07, 07 leads to 08 Integration Techniques and 12, and 08 leads to 09 Applications of Integrals. 10 leads to 11.](img/prerequisite-map.svg)

The top row is the derivative track, the bottom row the integral track, and the upper branch is series. They meet at the Fundamental Theorem (07) and again in multivariable calculus (12). Work in number order unless you have a reason not to.

## Lessons

| # | Lesson | The one-line idea |
|---|---|---|
| 01 | [Limits and Continuity](01-limits-and-continuity/README.md) | What a function heads toward, drawn as an epsilon band |
| 02 | [The Derivative](02-the-derivative/README.md) | Secant slopes shrink into a tangent slope: the instantaneous rate |
| 03 | [Derivative Rules](03-derivative-rules/README.md) | Power, product, quotient, and chain rules, each with a picture |
| 04 | [Optimization and Linear Approximation](04-optimization-and-linear-approximation/README.md) | Best values live where the slope is zero. Tangent lines make good estimates |
| 05 | [Related Rates](05-related-rates/README.md) | Linked quantities have linked rates: ladders, cones, queues, meshes |
| 06 | [Riemann Sums and Area](06-riemann-sums-and-area/README.md) | Area as a sum of thin rectangles, and rate buckets as totals |
| 07 | [The Fundamental Theorem of Calculus](07-fundamental-theorem/README.md) | Integration and differentiation undo each other |
| 08 | [Integration Techniques](08-integration-techniques/README.md) | Substitution and integration by parts |
| 09 | [Applications of Integrals](09-applications-of-integrals/README.md) | Area between curves, volume by disks, average value |
| 10 | [Sequences and Series](10-sequences-and-series/README.md) | When an infinite sum is finite, and why backoff needs a cap |
| 11 | [Taylor Series](11-taylor-series/README.md) | Hard functions as long polynomials, and small-x shortcuts |
| 12 | [Multivariable Calculus Intro](12-multivariable-intro/README.md) | Partial derivatives, gradients, and double integrals |
| ✓ | [Checkpoint](checkpoint.md) | Eighteen questions and a "ready for 501" rubric |

## How Each Lesson Is Built

Every lesson follows the [lesson template](../../docs/LESSON_TEMPLATE.md) and contains:

* Diagrams for every idea, in the lesson `img/` folder. Read the picture before the paragraph under it.
* Worked examples with every step and its reason.
* A **The SRE Connection** section tying the idea to counters, rates, queues, and capacity.
* Eight to ten exercises with answers hidden in a fold.
* A Go program in `code/main.go` that checks the lesson numerically. Run it with `go run main.go` inside the `code/` folder. Each lesson shows the real output.
* A `cards.tsv` flashcard deck for Anki (front, back, tags, separated by tabs).

## Pace

Plan on one lesson per sitting of 60 to 90 minutes, and twelve to fifteen sittings for the level. Lessons 07 and 10 reward a second pass a few days later. If a lesson feels like a wall, step back to the lesson its arrows come from in the map above. The wall is usually one lesson earlier.

## Pairs Well With

* The [Calculus track](../../tracks/calculus/README.md) goes further: more techniques, more applications, more proofs.
* The [Calculus of Rates in Physics and Queues workshop](../../workshops/calculus-of-rates-in-physics-and-queues/README.md) applies lessons 02, 05, and 07 to real queue models.
* The [Exponential Growth workshop](../../workshops/exponential-growth-in-interest-epidemics-and-load/README.md) applies lessons 03, 10, and 11 to load growth.
* The [Differential Equations track](../../tracks/differential-equations/README.md) and [Real Analysis track](../../tracks/real-analysis/README.md) are the natural follow-ups after [501](../501/README.md).

**Previous level:** [301 Algebra II, Trig and Precalculus](../301/README.md) · **Next level:** [501 Linear Algebra, Probability and Discrete Math](../501/README.md)
