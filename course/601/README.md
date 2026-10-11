# 601 Proof and Higher Math

**Level:** 601 · **Lessons:** 12 · **Time:** 12 to 18 hours of study, plus exercises

Earlier levels teach you how to compute. This level teaches you how to be certain. A **proof** is an argument that leaves no case unchecked, much like a code review that traces every branch instead of running a few test inputs. You learn the four main proof patterns first. You then use them on the big ideas of higher math: infinity, whole numbers, the real line, symmetry and shape.

Every lesson follows the same rule: a picture first, then the full proof. The picture tells you why the statement ought to be true. The proof shows that it is true.

## What You Can Do After This Level

* Read a proof line by line and say which definition, fact or rule justifies each line.
* Write a clean direct proof, proof by contradiction, proof by contrapositive and proof by induction.
* Negate statements with "for every" and "there exists" without getting tangled.
* Explain why the integers and the rationals are countable but the real numbers are not.
* Run the Euclidean algorithm by hand, use it to solve $ax + by = \gcd(a, b)$, and prove why it works.
* Compute powers in modular arithmetic and prove Fermat's little theorem.
* Prove limits of functions and sequences with $\varepsilon$ and $\delta$, and explain what completeness of $\mathbb{R}$ buys you.
* Build the Cayley table of the symmetries of a square and check the group axioms.
* Explain open sets, continuity and homeomorphism, and compute the Euler characteristic of a solid.

## Before You Start

You need comfort with algebra, basic logic and the idea of a limit:

* [501 Linear Algebra, Probability and Discrete Math](../501/README.md): logic, sets, functions and counting.
* [401 Calculus](../401/README.md): the informal idea of a limit and of a series.
* [301 Algebra II, Trig and Precalculus](../301/README.md): sequences, exponents, factoring.

## Prerequisite Map

<!-- diagram: type=dag nodes=501,401,01..12 edges="501>01,401>09,01>02,02>03,02>04,03>05,04>05,05>06,05>07,07>08,04>09,09>10,06>11,08>11,10>12,06>12" caption="Prerequisite map for course 601" -->
![Prerequisite map. Course 501 leads to lesson 01, which leads to 02. Lesson 02 splits into 03 contradiction and 04 contrapositive, which both feed 05 induction. Induction feeds 06 sets and 07 divisibility. Lesson 07 feeds 08 modular arithmetic. Lessons 06 and 08 feed 11 groups. Lesson 04 and course 401 feed 09 epsilon-delta limits, which feeds 10 completeness, which feeds 12 topology together with 06.](img/prerequisite-map.svg)

Read the map from the top. The left and middle columns are the algebra and number theory path. The right column is the analysis path. Both paths start from the same four proof techniques in lessons 01 to 05.

## Lessons

| # | Lesson | Big Idea |
|---|--------|----------|
| 01 | [Reading and Writing Proofs](01-reading-and-writing-proofs/README.md) | Implication, quantifiers, negation, and what counts as a proof |
| 02 | [Direct Proof](02-direct-proof/README.md) | Unpack the definitions, push the algebra, repack |
| 03 | [Proof by Contradiction](03-proof-by-contradiction/README.md) | $\sqrt{2}$ is irrational and there are infinitely many primes |
| 04 | [Contrapositive and Cases](04-contrapositive-and-cases/README.md) | Prove "not Q implies not P", split into cases, prove "if and only if" |
| 05 | [Induction](05-induction/README.md) | Dominoes, staircases, and strong induction |
| 06 | [Sets and Cardinality](06-sets-and-cardinality/README.md) | Bijections, countable sets and Cantor's diagonal argument |
| 07 | [Divisibility, GCD and Euclid](07-divisibility-gcd-and-euclid/README.md) | The division algorithm, the Euclidean algorithm, Bezout and Euclid's lemma |
| 08 | [Modular Arithmetic and Fermat](08-modular-arithmetic-and-fermat/README.md) | Clock arithmetic, inverses and Fermat's little theorem |
| 09 | [Epsilon-Delta Limits](09-epsilon-delta-limits/README.md) | The rigorous definition of a limit and of continuity |
| 10 | [Completeness and Sequences](10-completeness-and-sequences/README.md) | Convergent sequences, least upper bounds and the monotone convergence theorem |
| 11 | [Groups, Rings and Fields](11-groups-rings-and-fields/README.md) | The symmetries of a square, Cayley tables, and a taste of rings and fields |
| 12 | [Topology Taster](12-topology-taster/README.md) | Open sets, continuity, the coffee mug and the donut, Euler characteristic |

Finish with the [Checkpoint](checkpoint.md): 14 questions, including short proofs, with model answers.

## How to Study This Level

* Read each proof twice. The first time, follow the picture and the plot. The second time, cover the reasons column and say each reason out loud.
* Write proofs by hand. Typing hides sloppy steps. A pen exposes them.
* When stuck, test small cases with the Code Corner snippets. A computer check is evidence, not a proof. It often shows you the pattern that the proof needs.
* After each lesson, import its `cards.tsv` into Anki (fields: front, back, tags) and write a concept card in your vault for the main theorem with its picture.
* Each lesson has a `code/main.go`. Run it with `go run main.go` inside that folder. The output in the lesson is the real output.

## Where This Leads

* [Real Analysis Track](../../tracks/real-analysis/README.md): continuity, derivatives and integrals done rigorously.
* [Abstract Algebra Track](../../tracks/abstract-algebra/README.md): groups, rings, fields and Galois theory.
* [Number Theory Track](../../tracks/number-theory/README.md) and the [Number Theory for Cryptography Workshop](../../workshops/number-theory-for-cryptography/README.md): RSA, Diffie-Hellman and elliptic curves.
* [Topology Track](../../tracks/topology/README.md): metric spaces, compactness and connectedness.
* [Logic and Set Theory Track](../../tracks/logic-and-set-theory/README.md): axioms, infinity and the limits of proof.
