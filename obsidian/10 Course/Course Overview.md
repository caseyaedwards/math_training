---
tags: [course, dashboard]
---
# 📘 Course Overview

Levels are provisional and will be aligned with the course content in the repo.

| Level | Scope |
|---|---|
| [[101 Foundations]] | Arithmetic, fractions, decimals, ratios, negative numbers, order of operations, intro to variables |
| [[201 Algebra I and Geometry]] | Linear equations, inequalities, functions, Euclidean geometry, area and volume, coordinate plane |
| [[301 Algebra II, Trig and Precalculus]] | Polynomials, exponentials and logs, trigonometry, conic sections, sequences and series |
| [[401 Calculus]] | Limits, derivatives, integrals, the fundamental theorem, series, multivariable intro |
| [[501 Linear Algebra, Probability and Discrete Math]] | Vectors, matrices, eigenvalues, probability, combinatorics, graph theory, logic |
| [[601 Proof and Higher Math]] | Proof techniques, real analysis, abstract algebra, number theory, topology taster |

```dataview
TABLE status, confidence, started, finished
FROM "10 Course"
WHERE level
SORT level ASC
```
