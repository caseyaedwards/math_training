# Course 201: Algebra I and Geometry

**Level:** 201 · **Lessons:** 12 · **Time:** about 15 hours, or three to four weeks at three sessions a week
**Prerequisites:** [Course 101 Foundations](../101/README.md): arithmetic, fractions, negatives, order of operations, and the idea of a variable

## What This Level Is

Course 101 taught the rules of numbers. Course 201 puts them to work in two directions.

* **Algebra** treats an unknown number as a box with a label and finds what is inside by keeping a balance level. It then draws equations as lines and curves on a grid.
* **Geometry** starts from points, lines, and angles, and builds up to triangles, the Pythagorean theorem, areas, and volumes, with a reason for every formula.

The two strands meet often: slope uses similar triangles, distance uses the Pythagorean theorem, and the area model explains factoring.
No step assumes more than the lessons before it. Every idea has at least one picture.

## Outcomes

After this level you can:

1. Solve any linear equation or inequality in one variable, and check the answer.
2. Plot points, read and write function notation, and decide whether a relation is a function.
3. Find the slope and equation of a line from two points, a graph, or a word problem, and read the slope as a rate.
4. Solve a system of two linear equations by graphing, substitution, and elimination, and recognize the no-solution and infinite cases.
5. Simplify expressions with the exponent rules, including zero and negative exponents, and compute in scientific notation.
6. Expand and factor quadratics, and solve them by factoring or by the quadratic formula.
7. Use angle facts: complementary, supplementary, vertical, and the angle pairs at parallel lines.
8. Prove the triangle angle sum, apply the congruence shortcuts, and solve problems with similar triangles.
9. State, prove, and use the Pythagorean theorem and the distance formula.
10. Find perimeter, area, circumference, volume, and surface area of the standard shapes and solids, and explain where each formula comes from.

## Prerequisite Map

<!-- diagram: type=dag nodes="101,01..12,301" strands="algebra: 01-07, geometry: 08-12" -->
![Prerequisite map. Course 101 leads to Lesson 01 Linear Equations and Lesson 08 Lines and Angles. On the algebra strand, 01 leads to 02 Inequalities, 03 Plane and Functions, and 06 Exponents. 03 leads to 04 Slope and Lines, which leads to 05 Systems. 03 and 06 lead to 07 Quadratics. On the geometry strand, drawn in orange, 08 leads to 09 Triangles, which leads to 10 Pythagoras and 11 Area and Circles. 06 also feeds 10. 11 leads to 12 Volume and Surface. Lessons 05, 07, 10, and 12 lead to Course 301.](img/unit-map.svg)

The two strands are independent until Lesson 10. Alternate between them if one gets heavy. A change of scenery is cheaper than a burnout.

## Lessons

| # | Lesson | What it covers |
|---|---|---|
| 01 | [Solving Linear Equations](01-solving-linear-equations/README.md) | The balance model: do the same thing to both sides, undo in reverse order, always check |
| 02 | [Inequalities](02-inequalities/README.md) | Solution sets on the number line, interval notation, and why negatives flip the sign |
| 03 | [The Coordinate Plane and Functions](03-coordinate-plane-and-functions/README.md) | Points as addresses, functions as machines, mapping diagrams, and the vertical line test |
| 04 | [Slope and Lines](04-slope-and-lines/README.md) | Rise over run, $y = mx + b$, the three forms of a line, parallel and perpendicular slopes |
| 05 | [Systems of Linear Equations](05-systems-of-equations/README.md) | Two lines, one crossing: graphing, substitution, elimination, and the special cases |
| 06 | [Exponents and Scientific Notation](06-exponents-and-scientific-notation/README.md) | Exponent rules from counting factors, zero and negative powers, and powers of ten for scale |
| 07 | [Factoring and Quadratics](07-factoring-and-quadratics/README.md) | The area model, sum-product factoring, the zero product property, and the quadratic formula |
| 08 | [Points, Lines, and Angles](08-points-lines-and-angles/README.md) | Euclid's building blocks, angle types, vertical angles, and parallel lines cut by a transversal |
| 09 | [Triangles, Congruence, and Similarity](09-triangles-congruence-and-similarity/README.md) | The 180° proof, SSS SAS ASA AAS, why SSA fails, and similar triangles with shadows |
| 10 | [The Pythagorean Theorem](10-pythagorean-theorem/README.md) | A visual rearrangement proof, the converse, triples, and distance in two and three dimensions |
| 11 | [Area, Perimeter, and Circles](11-area-perimeter-and-circles/README.md) | Cut-and-rearrange area formulas, pi, circumference, circle area by slices, sectors |
| 12 | [Volume and Surface Area](12-volume-and-surface-area/README.md) | Volume as layers, nets, the one-third rule for cones, spheres, and how scaling works |

Then take the [201 checkpoint](checkpoint.md).

## How to Use a Lesson

1. Look at the first picture before reading a word. Guess what it shows.
2. Read the Step by Step section one idea at a time. Each idea has its own diagram.
3. Cover the right-hand reasons in each worked example and say them yourself.
4. Do the Try It exercises on paper before opening the answers.
5. Run the Go program in the lesson `code/` folder with `go run main.go`. Change a number and predict the new output before you run it again.
6. Import the lesson `cards.tsv` into Anki (File, Import, tab-separated, fields: Front, Back, Tags) and review daily.

## Where This Leads

* [Course 301](../301/README.md) extends lines and parabolas to polynomials, exponentials, logarithms, and trigonometry, which grows straight out of similar right triangles.
* [Algebra track](../../tracks/algebra/README.md) and [Geometry track](../../tracks/geometry/README.md) collect these topics with links forward and backward.
* [History of Math](../../history/README.md) tells the story of Euclid, al-Khwarizmi, and Descartes, whose ideas fill this level.
