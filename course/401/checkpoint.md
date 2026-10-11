# 401 Checkpoint

Twenty questions covering every 401 lesson. Work on paper, without notes or a calculator except where a question says otherwise. Show the steps, then check against the hidden answers. Allow about 90 minutes.

Use it two ways:

* **Placement:** take it cold before starting 401. A score of 16 or better means you can skim 401 and move on.
* **Exit check:** take it after lesson 12. The rubric at the end says whether you are ready for [501](../501/README.md).

## Questions

### Limits and Continuity

1. Find $\lim_{x \to 4} \dfrac{x^2 - 16}{x - 4}$.
2. Let $f(x) = \dfrac{x^2 - 1}{x - 1}$ for $x \ne 1$ and $f(1) = 3$. Is $f$ continuous at $x = 1$? If not, what kind of discontinuity is it?

### Derivatives

3. Use the limit definition to find the derivative of $f(x) = x^2 - 3x$.
4. Differentiate $x^3 \ln x$.
5. Differentiate $e^{\sin x}$.
6. Differentiate $\dfrac{x^2 + 1}{x - 1}$.
7. A counter reads $N(t) = 3t^2 + 40t$ requests after $t$ seconds. Find the average rate over $[0, 10]$ and the instantaneous rate at $t = 10$.

### Applications of Derivatives

8. The cost per record of a batch of size $b$ is $C(b) = \dfrac{800}{b} + 2b$. Find the best batch size and its cost.
9. Use a tangent line to estimate $\sqrt{25.5}$.
10. A circle's radius grows at 0.5 cm/s. How fast does its area grow when $r = 4$ cm?

### Integrals

11. Compute the left Riemann sum for $f(x) = x^2 + 1$ on $[0, 2]$ with $n = 4$ strips. Is it above or below the true area?
12. Evaluate $\displaystyle\int_1^2 (3x^2 + 2x)\,dx$.
13. Find $\dfrac{d}{dx}\displaystyle\int_0^x e^{-t^2}\,dt$.
14. Find $\displaystyle\int x\cos(x^2)\,dx$.
15. Find $\displaystyle\int x e^{2x}\,dx$.
16. Find the area between $y = 3x$ and $y = x^2$.
17. Requests arrive at $r(t) = 50 + 10t$ req/s for $0 \le t \le 6$. Find the total number of requests and the average rate a 6-second window reports.

### Series and Multivariable

18. Sum $\displaystyle\sum_{n=0}^{\infty} 3(0.4)^n$. Then say whether $\sum \dfrac{1}{n^{1.5}}$ and $\sum \dfrac{1}{\sqrt{n}}$ converge.
19. Write the degree 2 Taylor polynomial of $e^x$ about 0 and use it to estimate $e^{0.05}$.
20. Find both partial derivatives of $f(x, y) = x^2 y^3$ and the gradient at $(1, 1)$.

## Answers

<details>
<summary>Answers 1 to 7</summary>

1. **8.** Factor: $\dfrac{(x-4)(x+4)}{x-4} = x + 4 \to 8$. ([Lesson 01](01-limits-and-continuity/README.md))
2. **No.** The limit is 2 but $f(1) = 3$. A removable discontinuity (a hole with a misplaced dot). ([Lesson 01](01-limits-and-continuity/README.md))
3. **$2x - 3$.**

   ```txt
     ((x+h)^2 - 3(x+h) - x^2 + 3x)/h
   = (2xh + h^2 - 3h)/h                 x^2 and 3x cancel
   = 2x + h - 3  ->  2x - 3             let h -> 0
   ```

   ([Lesson 02](02-the-derivative/README.md))
4. **$3x^2 \ln x + x^2$.** Product rule: $3x^2 \cdot \ln x + x^3 \cdot \tfrac{1}{x}$. ([Lesson 03](03-derivative-rules/README.md))
5. **$\cos x \, e^{\sin x}$.** Chain rule. ([Lesson 03](03-derivative-rules/README.md))
6. **$\dfrac{x^2 - 2x - 1}{(x - 1)^2}$.** Quotient rule: $\dfrac{2x(x - 1) - (x^2 + 1)}{(x-1)^2}$. ([Lesson 03](03-derivative-rules/README.md))
7. **Average 70 req/s, instantaneous 100 req/s.** $N(10) = 700$, and $700/10 = 70$. $N'(t) = 6t + 40$, and $N'(10) = 100$. ([Lesson 02](02-the-derivative/README.md))

</details>

<details>
<summary>Answers 8 to 13</summary>

8. **$b = 20$, $C = 80$.** $C'(b) = -800/b^2 + 2 = 0$ gives $b^2 = 400$. Then $C(20) = 40 + 40$. ([Lesson 04](04-optimization-and-linear-approximation/README.md))
9. **About 5.05.** $L(x) = 5 + \tfrac{1}{10}(x - 25)$, and $L(25.5) = 5.05$. The true value is $5.04975$. ([Lesson 04](04-optimization-and-linear-approximation/README.md))
10. **$4\pi \approx 12.57$ cm²/s.** $dA/dt = 2\pi r\,dr/dt = 2\pi(4)(0.5)$. ([Lesson 05](05-related-rates/README.md))
11. **3.75, below the true area.**

    ```txt
      dx = 0.5, left points 0, 0.5, 1, 1.5
      heights 1, 1.25, 2, 3.25              f(x) = x^2 + 1
      sum = 0.5 * 7.5 = 3.75
    ```

    The function increases, and left sums of an increasing function undershoot. The true area is $14/3 \approx 4.667$. ([Lesson 06](06-riemann-sums-and-area/README.md))
12. **10.** $[x^3 + x^2]_1^2 = 12 - 2$. ([Lesson 07](07-fundamental-theorem/README.md))
13. **$e^{-x^2}$.** Fundamental Theorem, Part 1. ([Lesson 07](07-fundamental-theorem/README.md))

</details>

<details>
<summary>Answers 14 to 20</summary>

14. **$\tfrac{1}{2}\sin(x^2) + C$.** Substitute $u = x^2$, $du = 2x\,dx$. ([Lesson 08](08-integration-techniques/README.md))
15. **$\tfrac{1}{2}x e^{2x} - \tfrac{1}{4}e^{2x} + C$.** Parts with $u = x$, $dv = e^{2x}\,dx$, $v = \tfrac{1}{2}e^{2x}$. ([Lesson 08](08-integration-techniques/README.md))
16. **$9/2 = 4.5$.**

    ```txt
      3x = x^2  ->  x = 0, 3                crossings
      integral from 0 to 3 of (3x - x^2) dx
      = [3x^2/2 - x^3/3] from 0 to 3 = 27/2 - 9 = 9/2
    ```

    ([Lesson 09](09-applications-of-integrals/README.md))
17. **480 requests, average 80 req/s.** $[50t + 5t^2]_0^6 = 300 + 180$, and $480/6 = 80$. ([Lesson 09](09-applications-of-integrals/README.md))
18. **5. The first converges, the second diverges.** $3/(1 - 0.4) = 5$. The p-series test: $p = 1.5 > 1$ converges, $p = 0.5 \le 1$ diverges. ([Lesson 10](10-sequences-and-series/README.md))
19. **$1 + x + \tfrac{x^2}{2}$, giving $1.05125$.** The true value is $1.051271$. ([Lesson 11](11-taylor-series/README.md))
20. **$f_x = 2xy^3$, $f_y = 3x^2y^2$, $\nabla f(1, 1) = (2, 3)$.** ([Lesson 12](12-multivariable-intro/README.md))

</details>

## Ready for 501 If

Score one point per fully correct answer. Half a point for the right method with an arithmetic slip.

| Check | Standard |
|---|---|
| Total score | 16 or more out of 20 (80%) |
| Derivative core (questions 3 to 6) | All four correct. These skills appear everywhere later |
| Fundamental Theorem (questions 12 and 13) | Both correct |
| Rates and totals (questions 7 and 17) | Both correct, with units |
| Explain in words | You can say, without notes, why `rate()` over a window is a secant slope and `increase()` is an integral of the rate |
| Code | You ran at least three lesson `code/main.go` programs and can read their output |

**If you meet every standard:** move on to [501 Linear Algebra, Probability and Discrete Math](../501/README.md). Probability in 501 uses integrals as areas under density curves, and linear algebra picks up where the gradient left off.

**If you score 12 to 15:** redo the lessons behind your misses (each answer names its lesson), then retake only those questions a few days later.

**If you score below 12:** work through 401 again at a slower pace, one lesson per sitting, and do every Try It exercise. Check algebra first: most calculus errors are [301](../301/README.md) errors wearing a disguise.

Flashcard decks (`cards.tsv`) in every lesson folder are the cheapest way to keep these skills from fading between levels.
