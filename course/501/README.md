# Course 501: Linear Algebra, Probability and Discrete Math

**Level:** 501 · **Lessons:** 13 · **Time:** about 15 to 20 hours, plus exercises
**Prerequisites:** [Course 201: Algebra I and Geometry](../201/README.md) (functions, coordinate plane, linear equations) and [Course 301: Algebra II, Trig and Precalculus](../301/README.md) (exponentials, a first look at sine and cosine). [Course 401: Calculus](../401/README.md) helps for one idea in lesson 07 and is not required.

## What This Course Is

This course covers the three branches of math that working engineers use most, and that school often skips:

* **Discrete math:** logic, sets, counting and graphs. The math of things you can list: hosts, requests, bit patterns, services.
* **Probability:** how to reason about chance, alerts, failures and averages without fooling yourself.
* **Linear algebra:** vectors and matrices, seen as arrows and as machines that move the plane. The math behind graphics, search and machine learning.

Every lesson starts with a picture, builds the idea one step at a time, works examples line by line with the reason on the right, and ends with exercises (answers hidden in a fold), a short Go program, and a deck of flashcards. Nothing here needs more than patience. The math has waited a few thousand years. It can wait for you to reread a step.

## Outcomes

When you finish, you can:

* Build a truth table, negate a statement correctly, and tell an implication from its converse.
* Work with sets and functions, and say whether a function is one-to-one, onto, or both.
* Count arrangements and selections, and use the pigeonhole principle to prove something must happen.
* Compute probabilities by counting, use the complement and addition rules, and test for independence.
* Turn a conditional probability around with Bayes' rule, using a tree, an area diagram, or odds.
* Compute the mean, variance and standard deviation of a random variable, and use linearity of expectation.
* Pick the right distribution (binomial, Poisson, normal, exponential) from the story behind the data.
* Walk a graph with BFS and DFS, and find a cheapest path with Dijkstra's algorithm.
* Add vectors, measure them, and use the dot product to find angles and projections.
* Read a matrix as a transformation by its columns, and compose transformations by multiplying.
* Solve a linear system by Gaussian elimination, and recognize the no-solution and many-solution cases.
* Explain a determinant as an area scaling factor, and use it to test whether a matrix can be undone.
* Find eigenvalues and eigenvectors of a 2 by 2 matrix, and use them for repeated steps and Markov chains.

## Prerequisite Map

<!-- diagram: type=dependency-map columns="Discrete:01,02,03,08;Probability:04,05,06,07;Linear Algebra:09,10,11,12,13" from=201,301 to=601 caption="course 501 prerequisite map" -->
![Prerequisite map in three columns. Discrete: 01 Logic, 02 Sets and Functions, 03 Counting, 08 Graph Theory, fed by course 201 functions. Probability: 04 Probability Basics, 05 Conditional and Bayes, 06 Expectation and Variance, 07 Distributions, fed by course 301 and by 03 Counting. Linear Algebra: 09 Vectors, 10 Matrices, 11 Gaussian Elimination, 12 Determinants, 13 Eigenvectors, fed by the course 201 coordinate plane. Lessons 08, 07 and 13 lead to course 601 Proof and Higher Math.](img/prereq-map.svg)

The three columns are mostly independent. Two orders work well:

* **Straight through:** 01 to 13 in number order. Graph theory (08) closes the discrete and probability half before linear algebra begins.
* **Linear algebra first:** 09 to 13, then 01 to 08. Choose this if you came for graphics or machine learning.

Inside each column, follow the arrows. Counting (03) feeds probability (04), because most basic probability is counting.

## Lessons

| # | Lesson | Unit | Key Picture |
|---|---|---|---|
| 01 | [Logic and Truth Tables](01-logic-and-truth-tables/README.md) | Discrete | shaded Venn regions for AND, OR, NOT, IF-THEN |
| 02 | [Sets and Functions](02-sets-and-functions/README.md) | Discrete | Venn regions and arrow diagrams |
| 03 | [Counting: Permutations, Combinations and the Pigeonhole Principle](03-counting/README.md) | Discrete | a tree of choices |
| 04 | [Probability Basics](04-probability-basics/README.md) | Probability | the 6 by 6 dice grid |
| 05 | [Conditional Probability and Bayes](05-conditional-probability-and-bayes/README.md) | Probability | tree, area diagram, 100-deploy grid |
| 06 | [Random Variables, Expectation and Variance](06-random-variables-expectation-variance/README.md) | Probability | a bar chart on a fulcrum |
| 07 | [Common Distributions](07-common-distributions/README.md) | Probability | four shapes and the 68-95-99.7 bell |
| 08 | [Graph Theory Basics](08-graph-theory-basics/README.md) | Discrete | BFS rings and a cheapest path |
| 09 | [Vectors and the Dot Product](09-vectors-and-dot-product/README.md) | Linear Algebra | tip-to-tail arrows and a shadow |
| 10 | [Matrices as Transformations](10-matrices-as-transformations/README.md) | Linear Algebra | a grid that slants |
| 11 | [Solving Systems With Gaussian Elimination](11-solving-systems-gaussian-elimination/README.md) | Linear Algebra | crossing lines and a staircase |
| 12 | [Determinants as Area Scaling](12-determinants-as-area-scaling/README.md) | Linear Algebra | the unit square becomes a parallelogram |
| 13 | [Eigenvalues and Eigenvectors](13-eigenvalues-and-eigenvectors/README.md) | Linear Algebra | directions that do not turn |

Then take the [Checkpoint](checkpoint.md): 18 questions with answers, and a rubric for moving on to [Course 601: Proof and Higher Math](../601/README.md).

## How Each Lesson Is Built

Each lesson folder holds:

* `README.md`: the lesson, with The Big Idea, Picture It, Step by Step, Worked Examples, Common Mistakes, Try It, Code Corner and Go Deeper.
* `img/`: the diagrams, one or more for every idea.
* `code/main.go`: a small, self-contained Go program (standard library only). Run it from the `code` folder with `go run .`. Its real output is pasted in the lesson.
* `cards.tsv`: flashcards for Anki. Import with File, Import, and choose Tab as the field separator. Columns are front, back, tags.

## Where This Leads

* [Course 601: Proof and Higher Math](../601/README.md): logic and sets become the language of proof. Linear algebra grows into abstract algebra.
* Tracks for deeper practice: [Logic and Set Theory](../../tracks/logic-and-set-theory/README.md), [Combinatorics](../../tracks/combinatorics/README.md), [Graph Theory](../../tracks/graph-theory/README.md), [Probability](../../tracks/probability/README.md), [Statistics](../../tracks/statistics/README.md), [Linear Algebra](../../tracks/linear-algebra/README.md).
* Workshops that apply this course to real systems: [Probability for On-Call, Error Budgets and SLOs](../../workshops/probability-for-on-call-error-budgets-and-slos/README.md), [Statistics for Monitoring and Anomaly Detection](../../workshops/statistics-for-monitoring-and-anomaly-detection/README.md), [Graph Theory for Networks and Dependencies](../../workshops/graph-theory-for-networks-and-dependencies/README.md), [Linear Algebra for Graphics and ML](../../workshops/linear-algebra-for-graphics-and-ml/README.md).
