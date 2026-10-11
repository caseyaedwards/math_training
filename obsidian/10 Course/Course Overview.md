---
tags: [course, dashboard]
---
# Course Overview

Six levels and 71 lessons. Each level assumes the ones before it.
Pass the checkpoint at the end of a level before moving on.
Read the course on the [website](https://caseyaedwards.github.io/math_training/course/). The [study plan](https://caseyaedwards.github.io/math_training/docs/STUDY_PLAN/) sets the pace.

| Level | Lessons | Covers |
|---|---|---|
| [[101 Foundations]] | 10 | Place value, the four operations, negatives, fractions, decimals, ratios, exponents, variables |
| [[201 Algebra I and Geometry]] | 12 | Linear equations, inequalities, functions, lines, systems, quadratics intro, Euclidean geometry, area and volume |
| [[301 Algebra II, Trig and Precalculus]] | 12 | Functions in depth, polynomials, exponentials and logarithms, trigonometry, conics, sequences and series, complex numbers |
| [[401 Calculus]] | 12 | Limits, derivatives, integrals, the Fundamental Theorem, series, multivariable intro |
| [[501 Linear Algebra, Probability and Discrete Math]] | 13 | Logic, counting, probability, distributions, graphs, vectors, matrices, eigenvalues |
| [[601 Proof and Higher Math]] | 12 | Proof techniques, cardinality, number theory, real analysis, abstract algebra, topology |

```dataview
TABLE status, confidence, started, finished
FROM "10 Course"
WHERE level
SORT level ASC
```
