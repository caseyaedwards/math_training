# 601 Checkpoint

**Level:** 601 · **Time:** 2 to 3 hours · **Covers:** [all twelve lessons](README.md)

Work on paper. Write full sentences for the proofs. A proof that is correct but unreadable counts as half a proof, and the grader in your head knows it.

Score yourself honestly. 12 or more solid answers out of 14 means you are ready for the [Real Analysis](../../tracks/real-analysis/README.md), [Abstract Algebra](../../tracks/abstract-algebra/README.md) and [Topology](../../tracks/topology/README.md) tracks. Fewer than 10 means: revisit the lessons named in the answers, then try again in a week.

## Questions

1. **Negation.** Write the negation of: "For every $\varepsilon > 0$ there exists $N$ such that for all $n > N$, $|a_n| < \varepsilon$." Say in plain words what the negation means.

2. **Four forms.** For the statement "If $n$ is divisible by 6, then $n$ is even", write the contrapositive and the converse. Which of the three statements are true?

3. **Direct proof.** Prove: if $a$ and $b$ are odd integers, then $ab$ is odd.

4. **Contradiction.** Prove that $\sqrt{5}$ is irrational. You can use Euclid's lemma: if a prime $p$ divides $a^2$, then $p$ divides $a$.

5. **Contrapositive.** Prove: if $n^2 - 6n + 5$ is even, then $n$ is odd.

6. **Induction.** Prove for every $n \geq 1$:
   $$1 \cdot 2 + 2 \cdot 3 + \dots + n(n+1) = \frac{n(n+1)(n+2)}{3}.$$

7. **Induction.** Prove that $7 \mid (8^n - 1)$ for every $n \geq 0$. Then give a one-line proof with modular arithmetic.

8. **Cardinality.** (a) Give a bijection from $\mathbb{N} = \{0, 1, 2, \dots\}$ to the set $E$ of all even integers, negative ones included. (b) Explain in four or five sentences why the set of all infinite strings of 0s and 1s is uncountable.

9. **Euclid and Bezout.** Compute $\gcd(391, 299)$ with the Euclidean algorithm, and find integers $x, y$ with $391x + 299y = \gcd(391, 299)$.

10. **Modular arithmetic.** (a) Compute $5^{2026} \bmod 13$. (b) Find the inverse of $9$ mod $31$, and use it to solve $9x \equiv 4 \pmod{31}$.

11. **Epsilon-delta.** Prove $\lim_{x \to -1} x^2 = 1$ with $\varepsilon$ and $\delta$.

12. **Sequences.** Prove $\dfrac{2n + 3}{n + 1} \to 2$ with $\varepsilon$ and $N$. Then say which property of $\mathbb{R}$ guarantees that an increasing sequence bounded above converges, and why $\mathbb{Q}$ lacks it.

13. **Groups.** Use the Cayley table of $D_4$ from [lesson 11](11-groups-rings-and-fields/README.md) to decide whether $H = \{e, r^2, h, v\}$ is a subgroup. Check closure, identity and inverses. Is the size of $H$ consistent with Lagrange's theorem?

14. **Topology.** (a) Is $(0, 1) \cup \{2\}$ an open subset of $\mathbb{R}$? Justify. (b) A pentagonal prism has two pentagon faces joined by five rectangles. Compute $V - E + F$. (c) Explain why a sphere and a torus are not homeomorphic.

## Model Answers

<details>
<summary>1. Negation</summary>

There exists $\varepsilon > 0$ such that for every $N$ there exists $n > N$ with $|a_n| \geq \varepsilon$.

Plain words: some fixed tube around 0 keeps getting escaped. However far out you go, a later term sits outside it. The sequence does not converge to 0. ([Lesson 01](01-reading-and-writing-proofs/README.md), [lesson 10](10-completeness-and-sequences/README.md).)

</details>

<details>
<summary>2. Four forms</summary>

* Original: if $6 \mid n$, then $n$ is even. True: $n = 6k = 2(3k)$.
* Contrapositive: if $n$ is odd, then $6 \nmid n$. True, because it is equivalent to the original.
* Converse: if $n$ is even, then $6 \mid n$. False: $n = 4$.

([Lesson 04](04-contrapositive-and-cases/README.md).)

</details>

<details>
<summary>3. Direct proof</summary>

```txt
  a = 2k + 1, b = 2m + 1                     a and b are odd, two letters
  ab = (2k + 1)(2m + 1)                      multiply
     = 4km + 2k + 2m + 1                     expand
     = 2(2km + k + m) + 1                    factor 2 from the first three terms
  2km + k + m is an integer                  sums and products of integers
  ab is odd                                  definition of odd
```

$\blacksquare$ ([Lesson 02](02-direct-proof/README.md).)

</details>

<details>
<summary>4. Contradiction</summary>

```txt
  suppose sqrt(5) = a/b in lowest terms        assume the opposite
  a^2 = 5 b^2                                  square, multiply by b^2
  5 divides a^2, hence 5 divides a             Euclid's lemma, 5 is prime
  a = 5k                                       definition of divides
  25 k^2 = 5 b^2                               substitute
  b^2 = 5 k^2                                  divide by 5
  5 divides b^2, hence 5 divides b             Euclid's lemma
  5 divides a and b                            contradicts lowest terms
```

$\blacksquare$ ([Lesson 03](03-proof-by-contradiction/README.md).)

</details>

<details>
<summary>5. Contrapositive</summary>

Contrapositive: if $n$ is even, then $n^2 - 6n + 5$ is odd.

```txt
  n = 2k                                     n is even
  n^2 - 6n + 5 = 4k^2 - 12k + 5              substitute
               = 2(2k^2 - 6k + 2) + 1        split 5 = 4 + 1, factor 2
  odd                                        definition of odd
```

$\blacksquare$ ([Lesson 04](04-contrapositive-and-cases/README.md).)

</details>

<details>
<summary>6. Induction: a sum</summary>

```txt
  base n = 1:  left 1*2 = 2,  right 1*2*3/3 = 2           equal
  step: assume sum up to k is k(k+1)(k+2)/3               hypothesis
    sum up to k+1 = k(k+1)(k+2)/3 + (k+1)(k+2)            peel off the last term
                  = (k+1)(k+2) [k/3 + 1]                  factor (k+1)(k+2)
                  = (k+1)(k+2)(k+3)/3                     k/3 + 1 = (k+3)/3
  this is the formula with n = k + 1                      done
```

$\blacksquare$ ([Lesson 05](05-induction/README.md).)

</details>

<details>
<summary>7. Induction: divisibility</summary>

```txt
  base n = 0:  8^0 - 1 = 0 = 7*0                          divisible by 7
  step: assume 8^k - 1 = 7m                               hypothesis
    8^(k+1) - 1 = 8 * 8^k - 1                             split off one 8
                = 8(7m + 1) - 1                           hypothesis
                = 56m + 7 = 7(8m + 1)                     factor 7
```

$\blacksquare$ One line with [lesson 08](08-modular-arithmetic-and-fermat/README.md): $8 \equiv 1 \pmod 7$, hence $8^n \equiv 1^n = 1$, hence $7 \mid 8^n - 1$.

</details>

<details>
<summary>8. Cardinality</summary>

(a) Take the bijection $f: \mathbb{N} \to \mathbb{Z}$ from [lesson 06](06-sets-and-cardinality/README.md) and double it: $g(n) = 2f(n)$. Concretely $0, 1, 2, 3, 4, \dots \mapsto 0, -2, 2, -4, 4, \dots$. It is injective because $f$ is and doubling is. It is onto $E$ because each even $2z$ is $g$ of the $n$ with $f(n) = z$.

(b) Suppose the strings can be listed $s_1, s_2, s_3, \dots$. Build a new string whose $n$-th digit is the opposite of the $n$-th digit of $s_n$. The new string differs from $s_n$ at place $n$, for every $n$. Hence it is not in the list, which contradicts the list being complete. No list works, hence the set is uncountable.

</details>

<details>
<summary>9. Euclid and Bezout</summary>

```txt
  391 = 1 * 299 + 92
  299 = 3 *  92 + 23
   92 = 4 *  23 + 0              gcd = 23
  23 = 299 - 3 * 92              second line
     = 299 - 3 * (391 - 299)     first line
     = 4 * 299 - 3 * 391         collect
  check: 1196 - 1173 = 23
```

$x = -3$, $y = 4$. ([Lesson 07](07-divisibility-gcd-and-euclid/README.md).)

</details>

<details>
<summary>10. Modular arithmetic</summary>

(a)

```txt
  5^12 = 1 mod 13                Fermat, 13 is prime, 13 does not divide 5
  2026 = 12 * 168 + 10           reduce the exponent mod 12
  5^2026 = 5^10 mod 13           Fermat
  5^2 = 25 = -1 mod 13           25 = 26 - 1
  5^10 = (5^2)^5 = (-1)^5 = -1   exponent rules
  -1 = 12 mod 13                 add 13
```

Answer: $12$.

(b) $9 \cdot 7 = 63 = 2 \cdot 31 + 1$, hence $9^{-1} \equiv 7$. Then $x \equiv 7 \cdot 4 = 28 \pmod{31}$. Check: $9 \cdot 28 = 252 = 8 \cdot 31 + 4$. ([Lesson 08](08-modular-arithmetic-and-fermat/README.md).)

</details>

<details>
<summary>11. Epsilon-delta</summary>

Scratch: $|x^2 - 1| = |x + 1| \cdot |x - 1|$. If $|x + 1| < 1$, then $-2 < x < 0$ and $|x - 1| < 3$.

```txt
  let eps > 0                                 challenger's move
  choose delta = min(1, eps/3)                both caps
  suppose 0 < |x + 1| < delta                 x near -1
  -2 < x < 0, hence |x - 1| < 3               delta <= 1
  |x^2 - 1| = |x + 1| |x - 1|                 factor
            < (eps/3) * 3 = eps               delta <= eps/3
```

$\blacksquare$ ([Lesson 09](09-epsilon-delta-limits/README.md).)

</details>

<details>
<summary>12. Sequences and completeness</summary>

```txt
  |(2n + 3)/(n + 1) - 2| = |(2n + 3 - 2n - 2)/(n + 1)|     common denominator
                         = 1/(n + 1) < 1/n                 simplify
  let eps > 0, choose an integer N > 1/eps                 Archimedean property
  for n > N: 1/n < 1/N < eps                               done
```

The **completeness axiom** (every nonempty set bounded above has a least upper bound in $\mathbb{R}$) drives the monotone convergence theorem. $\mathbb{Q}$ lacks it: the rationals with $x^2 < 2$ have no least rational upper bound, because the natural candidate $\sqrt{2}$ is irrational. ([Lesson 10](10-completeness-and-sequences/README.md).)

</details>

<details>
<summary>13. Groups</summary>

Read from the table:

```txt
  h h = e,  v v = e,  r2 r2 = e         each element is its own inverse
  h v = r2,  v h = r2                   stays in H
  h r2 = v,  r2 h = v                   stays in H
  v r2 = h,  r2 v = h                   stays in H
  e is in H                             identity
```

Closed, contains $e$, contains inverses. Associativity comes for free from $D_4$. Hence $H$ is a subgroup. Its size 4 divides 8, as Lagrange's theorem demands. Bonus: every product in $H$ commutes, unlike $D_4$ as a whole. ([Lesson 11](11-groups-rings-and-fields/README.md).)

</details>

<details>
<summary>14. Topology</summary>

(a) No. The point $2$ is in the set, and every interval $(2 - r, 2 + r)$ contains points such as $2 + r/2$ that are not in the set. One point without breathing room is enough to fail.

(b) $V = 10$ (five on each pentagon), $E = 15$ (five on each pentagon plus five vertical edges), $F = 7$ (two pentagons plus five rectangles). $V - E + F = 10 - 15 + 7 = 2$.

(c) The Euler characteristic is a topological invariant. The sphere has $\chi = 2$ and the torus has $\chi = 0$. Homeomorphic surfaces share $\chi$, hence these two are not homeomorphic. Plain version: the torus has a hole, and no amount of stretching without cutting removes it. ([Lesson 12](12-topology-taster/README.md).)

</details>

## Next

* Mark the units done in your vault note for 601 and add a confidence score from 0 to 5 per lesson.
* Turn every question you missed into a new card in the matching lesson `cards.tsv`.
* Review this checkpoint again in seven days, cold.
