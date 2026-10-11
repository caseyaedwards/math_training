# 101 Foundations

Level 101 rebuilds arithmetic from the ground up. It starts at place value and ends at the door of algebra: variables and expressions. It assumes nothing. Every later level uses all of it.

The approach is plain and visual. Every idea gets at least one picture, and two when it can be drawn two ways. Numbers are points on a line and counts of bundles. Multiplication is the area of a rectangle. Fractions are bars cut into equal pieces. Each lesson builds a picture, then uses it to explain a rule you were once asked to memorize without a reason.

## What You Can Do After This Level

* Read any whole number or decimal as place values, place it on a number line, and round it.
* Explain the four operations with pictures: moves on a number line for addition and subtraction, rectangles for multiplication and division.
* Compute with negative numbers and explain why a negative times a negative is positive.
* Find factors, multiples, prime factorizations, the GCD and the LCM, and use them to schedule recurring jobs.
* Add, subtract, multiply and divide fractions, and explain why flip-and-multiply works.
* Move freely between fractions, decimals and percents, compute percent change, and turn an availability target into an error budget.
* Split amounts by a ratio, solve proportions, compute unit rates, and convert units.
* Evaluate exponents and square roots, and apply the order of operations as an expression tree.
* Evaluate, simplify and expand expressions with variables.

## Prerequisite Map

<!-- diagram: type=dag layout=left-to-right nodes=01..10 edges=01-02,02-03,02-04,04-05,05-06,06-07,07-08,03-09,04-09,09-10,06-10 caption="Lesson dependencies for 101" -->
![Prerequisite map of the ten lessons. 01 Place Value leads to 02 Four Operations. 02 leads to 03 Negatives and 04 Factors and Primes. 04 leads to 05 Fractions, then 06 Fraction Ops, then 07 Decimals and Percents, then 08 Ratios and Rates. 03 and 04 both lead to 09 Powers and Order of Operations. 06 and 09 both lead to 10 Variables](img/prerequisite-map.svg)

An arrow from one lesson to another means the second lesson uses ideas from the first. The top row is the fractions chain. The bottom row is the path to algebra. Lesson 10 needs both rows.

## Lessons

| # | Lesson | One-Line Description |
|---|---|---|
| 01 | [Place Value and the Number Line](01-place-value-and-the-number-line/README.md) | Digits as counts of bundles, numbers as points on a ruler, rounding and binary. |
| 02 | [The Four Operations](02-the-four-operations/README.md) | Addition as moves, multiplication as area, division as a missing side, remainders. |
| 03 | [Negative Numbers](03-negative-numbers/README.md) | The line left of zero, opposites, absolute value, and every sign rule from one picture. |
| 04 | [Factors, Multiples and Primes](04-factors-multiples-and-primes/README.md) | Factor rectangles, factor trees, GCD, LCM and Euclid on primes. |
| 05 | [Fractions: Meaning and Equivalence](05-fractions-meaning-and-equivalence/README.md) | Fractions as pieces, points and divisions; equivalent fractions and comparison. |
| 06 | [Fraction Operations](06-fraction-operations/README.md) | Common denominators, multiplication as area, and why flip-and-multiply works. |
| 07 | [Decimals and Percents](07-decimals-and-percents/README.md) | Place value past the point, percent change, and error budgets. |
| 08 | [Ratios, Proportions and Rates](08-ratios-proportions-and-rates/README.md) | Tape diagrams, double number lines, unit rates and capacity planning. |
| 09 | [Exponents, Roots and Order of Operations](09-exponents-roots-and-order-of-operations/README.md) | Repeated multiplication, square roots as sides, and precedence as a syntax tree. |
| 10 | [Variables and Expressions](10-variables-and-expressions/README.md) | Letters for numbers, substitution, like terms and the distributive property. |

Finish with the [Level 101 Checkpoint](checkpoint.md): a 20-question self-test with a ready-for-201 rubric.

## How to Use This Level

1. **Go in order the first time.** The lessons follow the prerequisite map. If a lesson feels easy, skim the pictures, do the Try It exercises, and move on when you get them all right.
2. **Look before you read.** Each idea comes with a diagram. Spend a minute on the picture before the text. Say what it shows in your own words.
3. **Redo the worked examples on paper.** Cover the reason column, write each line, and name the reason yourself. Then compare.
4. **Do every Try It exercise before opening the answers.** A wrong answer you catch yourself teaches more than a right answer you peeked at.
5. **Run the Code Corner.** Each lesson has a `code/` folder with one Go program, standard library only. Run `go run .` in that folder. The lesson shows the real output. Change the numbers and predict the output before you run it.
6. **Review with flashcards.** Each lesson has a `cards.tsv` file. Import it into Anki (File, Import, tab-separated, three fields: front, back, tags). Review a little every day. Spaced review beats one long cram.
7. **Plan 30 to 60 minutes per lesson.** Two or three lessons a week finishes the level in about a month.
8. **Take the checkpoint.** Use its rubric to decide whether to move on to [201 Algebra I and Geometry](../201/README.md) or revisit a unit.
9. **Track progress in Obsidian.** Tick off each unit in the 101 Foundations note in the vault and add a confidence score.

## Where This Leads

* [201 Algebra I and Geometry](../201/README.md) starts by solving the equations whose expressions you build in lesson 10.
* The [Arithmetic and Number Sense track](../../tracks/arithmetic-and-number-sense/README.md) offers extra practice at this level.
* The [Number Theory track](../../tracks/number-theory/README.md) goes much further with primes, GCD and remainders from lesson 4.
