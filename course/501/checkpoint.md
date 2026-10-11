# Course 501 Checkpoint

**Level:** 501 · **Time:** 60 to 90 minutes · **Covers:** [lessons 01 to 13](README.md#lessons)

Work each question on paper first. Then open the answer. Each answer names the lesson to revisit if you missed it. No calculator is needed except for question 11, and even there a rough answer is fine.

## Questions

### Discrete Math

1. Write the truth table for $P \to Q$. Then state the contrapositive of `if the cache is cold, then latency is high`.
2. Negate the statement `every replica acknowledged the write`.
3. $A = \{1, 2, 3, 4, 5\}$ and $B = \{4, 5, 6\}$. Find $A \cap B$, $A \cup B$ and $A \setminus B$.
4. Is $f(x) = 3x - 2$, from the real numbers to the real numbers, a bijection? If so, find $f^{-1}$.
5. A deploy picks 3 of 8 canary hosts. How many choices are there if the order does not matter? If the hosts are ranked first, second, third?
6. 30 alerts fired in one week. Show that some day had at least 5 alerts.
7. In a graph, every vertex has degree 3 and there are 12 edges. How many vertices are there?
8. Edges: A-B weight 2, A-C weight 5, B-C weight 1, B-D weight 7, C-D weight 2. Find the cheapest path from A to D and its cost.

### Probability

9. Roll two dice. What is $P(\text{sum} \le 4)$? What is $P(\text{at least one 1})$?
10. 2% of requests hit a slow path. A latency alert fires for 90% of slow requests and for 5% of normal requests. Given the alert fired, what is the chance the request hit the slow path?
11. A job succeeds with probability 0.9, independently, each of 5 runs. Find the probability of exactly 4 successes, and the expected number of successes.
12. $X$ is 0, 10 or 20 with probabilities 0.5, 0.3, 0.2. Find $E[X]$ and $\operatorname{Var}(X)$.
13. A service averages 2 incidents per month (Poisson). What is the chance of a month with no incidents? What is the mean time between incidents?

### Linear Algebra

14. $a = (2, 1)$ and $b = (-1, 2)$. Find $a + b$, $|a|$ and $a \cdot b$. What does $a \cdot b$ tell you about the angle?
15. Write the matrix that sends $(1, 0)$ to $(1, 2)$ and $(0, 1)$ to $(3, 1)$. Apply it to $(2, 1)$.
16. Solve with elimination: $x + y + z = 4$, $x + 2y + 3z = 9$, $2x + 3y + z = 7$.
17. Find $\det \begin{pmatrix} 4 & 2 \\ 3 & 1 \end{pmatrix}$. What does the sign mean? By what factor does the matrix scale areas?
18. Find the eigenvalues and eigenvectors of $\begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix}$.

## Answers

<details>
<summary>1. Implication and contrapositive</summary>

Rows (P, Q, $P \to Q$): T T T, T F F, F T T, F F T. Contrapositive: `if latency is not high, then the cache is not cold`. Revisit [Logic and Truth Tables](01-logic-and-truth-tables/README.md).

</details>

<details>
<summary>2. Negation</summary>

`At least one replica did not acknowledge the write.` Revisit [Logic and Truth Tables](01-logic-and-truth-tables/README.md), step 6.

</details>

<details>
<summary>3. Set operations</summary>

$A \cap B = \{4, 5\}$, $A \cup B = \{1, 2, 3, 4, 5, 6\}$, $A \setminus B = \{1, 2, 3\}$. Revisit [Sets and Functions](02-sets-and-functions/README.md).

</details>

<details>
<summary>4. Bijection</summary>

Yes. Different inputs give different outputs ($3a - 2 = 3b - 2$ forces $a = b$), and every $y$ is hit by $x = (y + 2)/3$. That gives $f^{-1}(y) = (y + 2)/3$. Revisit [Sets and Functions](02-sets-and-functions/README.md).

</details>

<details>
<summary>5. Choices of canaries</summary>

Unordered: $\binom{8}{3} = 56$. Ranked: $P(8, 3) = 8 \cdot 7 \cdot 6 = 336$. Revisit [Counting](03-counting/README.md).

</details>

<details>
<summary>6. Pigeonhole</summary>

Seven days are the boxes. $\lceil 30 / 7 \rceil = 5$. If every day had at most 4 alerts, the week holds at most 28, which is less than 30. Revisit [Counting](03-counting/README.md).

</details>

<details>
<summary>7. Handshake lemma</summary>

Degree sum $= 2 \times 12 = 24$. With degree 3 each: $24 / 3 = 8$ vertices. Revisit [Graph Theory Basics](08-graph-theory-basics/README.md).

</details>

<details>
<summary>8. Cheapest path</summary>

A, B, C, D with cost $2 + 1 + 2 = 5$. The other routes cost more: A, C, D is 7 and A, B, D is 9. Revisit [Graph Theory Basics](08-graph-theory-basics/README.md), Dijkstra.

</details>

<details>
<summary>9. Two dice</summary>

Sum at most 4: sums 2, 3, 4 have $1 + 2 + 3 = 6$ cells, giving $6/36 = 1/6$. At least one 1: $1 - (5/6)^2 = 11/36$. Revisit [Probability Basics](04-probability-basics/README.md).

</details>

<details>
<summary>10. Bayes</summary>

$\frac{0.02 \times 0.9}{0.02 \times 0.9 + 0.98 \times 0.05} = \frac{0.018}{0.018 + 0.049} = \frac{0.018}{0.067} \approx 0.269$. About 27%. Revisit [Conditional Probability and Bayes](05-conditional-probability-and-bayes/README.md).

</details>

<details>
<summary>11. Binomial</summary>

$\binom{5}{4} (0.9)^4 (0.1) = 5 \times 0.6561 \times 0.1 = 0.32805$. Expected successes: $5 \times 0.9 = 4.5$. Revisit [Common Distributions](07-common-distributions/README.md).

</details>

<details>
<summary>12. Mean and variance</summary>

$E[X] = 0 + 3 + 4 = 7$. $E[X^2] = 0 + 0.3 \times 100 + 0.2 \times 400 = 110$. $\operatorname{Var}(X) = 110 - 49 = 61$. Revisit [Random Variables, Expectation and Variance](06-random-variables-expectation-variance/README.md).

</details>

<details>
<summary>13. Poisson and exponential</summary>

$P(0) = e^{-2} \approx 0.135$. Gaps are exponential with rate 2 per month, which gives a mean gap of $1/2$ month. Revisit [Common Distributions](07-common-distributions/README.md).

</details>

<details>
<summary>14. Vectors</summary>

$a + b = (1, 3)$. $|a| = \sqrt{5}$. $a \cdot b = -2 + 2 = 0$: the vectors are perpendicular. Revisit [Vectors and the Dot Product](09-vectors-and-dot-product/README.md).

</details>

<details>
<summary>15. Matrix from columns</summary>

$\begin{pmatrix} 1 & 3 \\ 2 & 1 \end{pmatrix}$. Applied to $(2, 1)$: $2(1, 2) + 1(3, 1) = (5, 5)$. Revisit [Matrices as Transformations](10-matrices-as-transformations/README.md).

</details>

<details>
<summary>16. Elimination</summary>

```txt
[1 1 1 | 4]
[1 2 3 | 9]
[2 3 1 | 7]

[1 1  1 | 4]
[0 1  2 | 5]        R2 <- R2 - R1
[0 1 -1 | -1]       R3 <- R3 - 2 R1

[1 1  1 | 4]
[0 1  2 | 5]
[0 0 -3 | -6]       R3 <- R3 - R2

z = 2, y = 5 - 4 = 1, x = 4 - 1 - 2 = 1
```

Solution $(1, 1, 2)$. Check row 3: $2 + 3 + 2 = 7$. Revisit [Solving Systems With Gaussian Elimination](11-solving-systems-gaussian-elimination/README.md).

</details>

<details>
<summary>17. Determinant</summary>

$4 \cdot 1 - 2 \cdot 3 = -2$. The negative sign means the plane is flipped (mirrored). Areas scale by $|-2| = 2$. Revisit [Determinants as Area Scaling](12-determinants-as-area-scaling/README.md).

</details>

<details>
<summary>18. Eigenvalues</summary>

Trace 5, det 6: $\lambda^2 - 5\lambda + 6 = 0$, giving $\lambda = 3$ and $\lambda = 2$. For 3: $A - 3I = \begin{pmatrix} 0 & 1 \\ 0 & -1 \end{pmatrix}$, which gives $y = 0$ and $v = (1, 0)$. For 2: $A - 2I = \begin{pmatrix} 1 & 1 \\ 0 & 0 \end{pmatrix}$, which gives $x + y = 0$ and $v = (1, -1)$. Check: $A(1, -1) = (2, -2)$. Revisit [Eigenvalues and Eigenvectors](13-eigenvalues-and-eigenvectors/README.md).

</details>

## Ready for 601 If

Score one point per question answered fully and correctly. Then read the rubric honestly. Nobody else is grading.

| Area | Questions | You Are Ready When |
|---|---|---|
| Logic and sets | 1 to 4 | 4 of 4. Course 601 is written in this language, which leaves no room for gaps. |
| Counting and graphs | 5 to 8 | 3 of 4, and you can explain why the pigeonhole bound works. |
| Probability | 9 to 13 | 4 of 5, including question 10 (Bayes). |
| Linear algebra | 14 to 18 | 4 of 5, including question 16 (elimination) done without notes. |

You are **ready for [Course 601: Proof and Higher Math](../601/README.md)** if:

* You meet the bar in every row of the table (at least 15 of 18 overall).
* You can explain, in plain words and without symbols, why a truth table proves an equivalence, why $\binom{n}{k}$ divides by $k!$, why a zero determinant means no inverse, and why an eigenvector does not turn.
* You can draw from memory: the Bayes area diagram, a BFS level picture, and the unit square under a 2 by 2 matrix.

If a row falls short, reread the lessons named in the missed answers, redo their Try It sections, and review their flashcards for a few days. Then take this checkpoint again. Logic and sets carry the most weight. Course 601 is mostly proofs, and proofs are made of `if`, `and`, `not`, `for all` and `there exists`.
