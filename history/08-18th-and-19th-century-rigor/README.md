# 08 The 18th and 19th Centuries: Rigor

**Era:** about 1700 to 1900 · **Reading time:** about 22 minutes · **Previous:** [07 The Scientific Revolution and Calculus](../07-scientific-revolution-and-calculus/README.md) · **Next:** [09 20th-Century Foundations and Computing](../09-20th-century-foundations-and-computing/README.md)

## The Big Idea

The 1700s use calculus like a power tool and ask few questions about how it works. The 1800s stop and check the wiring. Limits get exact definitions, the real numbers get a foundation, geometry learns that Euclid is one option among several, and infinity turns out to come in sizes.

## The World at That Time

Steam engines pump mines and drive mills. Railways and iron bridges need stress calculations. Factories need to know how heat moves through metal and how fast a fluid flows through a pipe. Later in the 1800s electricity and magnetism become an engineering field, and James Clerk Maxwell captures the whole subject in one set of equations in the 1860s. Calculus is the working language of all of it. Joseph Fourier publishes his theory of heat flow in 1822 and breaks functions into sums of waves, a trick that still runs inside audio and image compression.

States want numbers too. Armies and tax offices need accurate maps, which means surveying: measuring triangles of land with telescopes and chains, then correcting the inevitable small errors. Astronomers chase comets and newly found planets across the sky. Insurers sell life policies and annuities, and they price them with mortality tables and probability. The Equitable Society in London starts selling life insurance on mathematical tables in 1762.

Revolution reaches the units of measure. In 1791 the French Academy of Sciences proposes a new length, the **metre**: one ten-millionth of the distance from the North Pole to the equator. Lagrange, Laplace, and Monge serve on the committees. Two astronomers, Delambre and Méchain, survey the meridian from Dunkirk to Barcelona from 1792 to 1798 to fix its length. France also tries decimal time, with ten-hour days, in 1793. The metre survives. Decimal time lasts less than two years.

Data starts to shape policy. Adolphe Quetelet, a Belgian astronomer, applies the bell curve of astronomical errors to human heights and crime rates in the 1830s and invents the average man. His height-to-weight ratio survives as the body mass index. Florence Nightingale nurses soldiers in the Crimean War, then fights the army with statistics. Her polar-area diagrams of 1858 show that most soldiers die of preventable disease in camp hospitals, not of wounds. They change hospital sanitation. She is the first woman elected to the Statistical Society of London, also in 1858. A good chart, it turns out, wins arguments that speeches lose.

```txt
  Need in the 1700s and 1800s           Math that answers it
  -----------------------------------   ------------------------------------
  steam, heat, fluids, electricity      calculus of change, Fourier series
  surveying, maps, the metre            spherical geometry, least squares
  comets and new planets                orbit calculation, least squares
  insurance, census, public health      probability, statistics, charts
  trust in calculus itself              limits, epsilon-delta, real numbers
```

## Key People

| Person | Dates | One-Line Contribution |
| --- | --- | --- |
| Jacob, Johann, and Daniel Bernoulli | 1655 to 1782 (three lives) | Jacob proves the law of large numbers; Johann teaches Euler; Daniel founds fluid dynamics (1738). |
| [Leonhard Euler](../biographies/euler.md) | 1707 to 1783 | Solves Königsberg (1736) and the Basel problem; fixes the notation f(x), e, i, π, Σ. |
| Joseph-Louis Lagrange | 1736 to 1813 | Rewrites mechanics as pure analysis (1788); serves on the metric committee. |
| Pierre-Simon Laplace | 1749 to 1827 | Applies calculus to the solar system and builds the theory of probability (1812). |
| [Carl Friedrich Gauss](../biographies/gauss.md) | 1777 to 1855 | Writes *Disquisitiones Arithmeticae* (1801), finds Ceres, studies curved surfaces. |
| Augustin-Louis Cauchy | 1789 to 1857 | Builds calculus on limits in his *Cours d'analyse* (1821). |
| Nikolai Lobachevsky and János Bolyai | 1792 to 1856; 1802 to 1860 | Publish non-Euclidean geometry (1829 and 1832). |
| Niels Henrik Abel | 1802 to 1829 | Proves that the general fifth-degree equation has no formula in roots (1824). |
| [Évariste Galois](../biographies/galois.md) | 1811 to 1832 | Links equations to groups of symmetries; dies after a duel at 20. |
| Karl Weierstrass | 1815 to 1897 | Gives limits the epsilon-delta form still taught today. |
| George Boole | 1815 to 1864 | Turns logic into algebra in *The Laws of Thought* (1854). |
| Charles Babbage | 1791 to 1871 | Designs the Difference Engine and the programmable Analytical Engine. |
| [Ada Lovelace](../biographies/lovelace.md) | 1815 to 1852 | Writes the 1843 Notes on the Analytical Engine, with the first published program. |
| [Bernhard Riemann](../biographies/riemann.md) | 1826 to 1866 | Redefines geometry (1854) and links primes to the zeta function (1859). |
| Richard Dedekind | 1831 to 1916 | Builds the real numbers from fractions with cuts (1872). |
| [Georg Cantor](../biographies/cantor.md) | 1845 to 1918 | Shows that some infinities are bigger than others (1874, 1891). |
| Sofia Kovalevskaya | 1850 to 1891 | Proves a key theorem on differential equations; becomes a full professor in Stockholm (1889), a first for a woman in northern Europe. |
| Adolphe Quetelet and Florence Nightingale | 1796 to 1874; 1820 to 1910 | Bring statistics to society and public health; Nightingale's diagrams (1858). |

## Key Ideas

### Euler: Graphs, Notation, and the Basel Problem

Leonhard Euler is the most productive mathematician in history. His collected works fill more than 80 volumes. He goes blind in one eye in 1738 and almost fully blind by 1771. His output rises anyway: he dictates to assistants and does the arithmetic in his head. Much of the notation in any calculus book is his. He writes f(x) for a function in 1734. He uses e for the base of natural logarithms, Σ for a sum (1755), and i for the square root of -1 (1777). The symbol π comes from William Jones in 1706, and Euler makes it standard.

In 1735 he solves the **Basel problem**, open for about 90 years: what is 1 + 1/4 + 1/9 + 1/16 + ..., the sum of one over every square? His answer is π²/6, about 1.6449. Nobody expects π in a sum of squares. Euler finds it with a bold step that only later gets a rigorous proof. That pattern, brilliant first and rigorous later, sums up the 1700s.

The city of Königsberg in Prussia sits on the river Pregel. The river surrounds an island and splits the city into four land masses joined by seven bridges. Residents ask whether a walk can cross every bridge exactly once. In 1736 Euler proves that it cannot. More important is how he proves it.

<!-- diagram: type=graph-theory ref=konigsberg nodes=A,B,C,D edges=7 degrees=A5,B3,C3,D3 caption="Euler (1736): the seven bridges of Königsberg as a graph" -->
![Left: a schematic map with banks C (top) and B (bottom), island A in the middle, land D on the right, and seven orange bridges: two from A to C, two from A to B, one from A to D, one from D to C, one from D to B. An arrow leads to the right panel: a graph with dots A, B, C, D and seven lines, with degrees A 5, B 3, C 3, D 3 in orange](img/konigsberg.svg)

Euler throws away everything that does not matter: the shape of the land, the length of the bridges, the street plan. Each land mass becomes a dot, and each bridge becomes a line between two dots. This is a **graph** in the modern sense: dots (called nodes or vertices) joined by lines (called edges). The **degree** of a dot is the number of lines that touch it. In the picture A has degree 5 and B, C, D each have degree 3.

Now the argument. A walker who passes through a land mass arrives on one bridge and leaves on another. Every visit uses up two bridges. A land mass in the middle of the walk needs an even degree. Only the start and the end can have odd degree. A walk that crosses each bridge once therefore needs zero or two odd dots. Königsberg has four. No walk exists, and no amount of walking changes it.

```txt
  Euler's test on Königsberg
  degrees: A 5, B 3, C 3, D 3          count the lines at each dot
  odd dots: A, B, C, D = 4             all four are odd
  a walk needs 0 or 2 odd dots         every middle visit uses 2 bridges
  4 is neither                         no such walk exists
  add a bridge B-C: B 4, C 4           now only A and D are odd
  2 odd dots                           a walk exists, from A to D
```

Euler proves the rule in one direction. The other direction, that a connected graph with zero or two odd dots always has such a walk, gets a full proof from Carl Hierholzer in 1873. Graph theory starts here. It now routes packets, schedules jobs, and draws the dependency graphs of your microservices.

### Gauss: Patterns, Orbits, and Curved Surfaces

Carl Friedrich Gauss is the son of a laborer in Brunswick. A famous story says that at about age nine, around 1786, his teacher sets the class to add the numbers from 1 to 100, expecting an hour of quiet. Gauss writes the answer almost at once. The story comes from a memoir written by a friend after his death in 1855, and the details have likely grown in the retelling. The math is solid either way.

<!-- diagram: type=historical-method ref=gauss-pairing n=100 staircase=6x7 caption="Young Gauss (story, c. 1786): 1 + 2 + ... + 100 by pairing" -->
![Top: the numbers 1 to 50 paired with 100 down to 51, each pair summing to 101 in orange, with the total 50 x 101 = 5,050. Bottom: two staircases of 1 + 2 + ... + 6 squares, one orange and one gray, fit together into a 6 by 7 rectangle of 42 squares, one staircase is 21, and in general 1 + 2 + ... + n = n(n + 1)/2. Footnote: the classroom story comes from a later biography](img/gauss-pairing.svg)

The top half pairs the first number with the last, the second with the second-to-last, and onward: 1 + 100, 2 + 99, 3 + 98, down to 50 + 51. Each pair sums to 101, and there are 50 pairs. The bottom half shows why this always works. Draw 1 + 2 + ... + 6 as a staircase of squares. A second copy, turned upside down, fits against it to make a 6 by 7 rectangle. The rectangle holds 42 squares. One staircase holds half: 21.

```txt
  1 + 2 + ... + 100
  pairs: 1+100, 2+99, ..., 50+51    pair the ends, work inward
  each pair = 101                   one side up by 1, other down by 1
  number of pairs = 100 / 2 = 50    100 numbers, two per pair
  total = 50 x 101 = 5,050          multiply
  formula: n(n + 1) / 2             the rectangle picture, n = 100
         = 100 x 101 / 2 = 5,050    same answer
```

The adult Gauss does far more. In 1796 he shows how to construct a regular 17-sided polygon with compass and straightedge, a construction the Greeks never find. In 1801 he publishes *Disquisitiones Arithmeticae*, the founding book of modern number theory. It introduces **modular arithmetic**, clock arithmetic in which only the remainder counts: 14 ≡ 2 (mod 12). Every hash ring and every RSA key uses it.

Also in 1801, the astronomer Giuseppe Piazzi spots a new object, the dwarf planet Ceres. He tracks it for a few weeks before it vanishes into the glare of the sun. Nobody can predict where it reappears from such a short arc. Gauss, at 24, computes an orbit. On the last night of 1801 astronomers find Ceres close to where he says. He later explains his method of **least squares**: when measurements disagree, choose the answer that makes the sum of the squared errors as small as possible. Adrien-Marie Legendre publishes least squares first, in 1805. Gauss says he has used it since 1795. Another priority dispute. Least squares now fits every trend line in every capacity plan.

Gauss also surveys the kingdom of Hanover. This work leads him to study curved surfaces, and in 1827 he proves that a surface has a **curvature** that its inhabitants can measure without leaving it. An ant on a sphere can tell that its world is curved by measuring triangles. That idea leads straight to the next section.

### Geometry Without the Parallel Postulate

Euclid builds geometry on five assumptions. The fifth, the **parallel postulate**, says in its common modern form: through a point not on a line, exactly one line runs parallel to the given line. For 2,000 years mathematicians try to prove it from the other four. All fail.

In the 1820s three people try the opposite. What if more than one parallel exists? Nikolai Lobachevsky in Kazan publishes the result in 1829. János Bolyai, a Hungarian army officer, publishes in 1832. Gauss explores the same idea privately for years and publishes nothing. Each finds a geometry with no contradictions in which the parallel postulate fails. In this **hyperbolic geometry** the angles of every triangle add to less than 180 degrees.

The opposite case is easier to picture, because we live on it.

<!-- diagram: type=geometry ref=sphere-triangle angles=90,90,90 caption="A triangle on a sphere with three right angles: 270 degrees" -->
![A sphere with the North Pole at the top and the equator drawn as a dashed ellipse. An orange triangle runs from the North Pole down to a point on the equator, a quarter of the way around the equator, and back up to the pole. Text: walk from the North Pole down to the equator, turn 90°, walk a quarter of the way round, turn 90°, walk back up to the pole; angles 90° + 90° + 90° = 270°. Euclid's parallel postulate fails on a sphere. Gauss, Bolyai and Lobachevsky (1820s) show other consistent geometries exist](img/sphere-triangle.svg)

On a sphere the straightest paths are **great circles**, such as the equator and the lines of longitude. Walk from the North Pole straight down a line of longitude to the equator. Turn 90 degrees. Walk a quarter of the way around the equator. Turn 90 degrees again and walk straight back to the pole. You arrive at an angle of 90 degrees. The triangle has three right angles: 270 degrees. On a sphere no parallels exist at all: any two great circles cross. Triangle angles add to more than 180. This is the **elliptic** case. Riemann develops it, and much more, in a lecture of 1854.

```txt
  Three geometries, one question: angle sum of a triangle
  flat (Euclid)         exactly 180°       one parallel through a point
  sphere (elliptic)     more than 180°     no parallels
  saddle (hyperbolic)   less than 180°     many parallels
  sphere example        90 + 90 + 90 = 270 the triangle in the picture
  the excess, 90°,      grows with area    small triangles look flat
```

The last line explains why Euclid works fine for a field or a bridge. The Earth curves, but a small triangle on it has an angle sum very close to 180. Riemann's 1854 lecture describes spaces whose curvature changes from point to point. Einstein uses exactly that geometry for gravity in 1915. A question about a 2,000-year-old axiom ends up inside GPS satellite corrections.

### Rigor: Limits, Real Numbers, and Algebra as Structure

Calculus works, but nobody can say what an infinitely small quantity is. The philosopher George Berkeley mocks them in 1734 as the ghosts of departed quantities. The 1800s answer him.

Augustin-Louis Cauchy, in his *Cours d'analyse* of 1821, builds calculus on the **limit**: a value that a quantity gets as close to as you like. Karl Weierstrass, teaching in Berlin from the late 1850s, sharpens it into the **epsilon-delta** definition. It works like a contract. The skeptic names a tolerance ε (epsilon) for the output. You must answer with a tolerance δ (delta) for the input that guarantees it. If you can always answer, whatever ε is named, the limit holds. It is a service level objective for functions.

```txt
  Claim: as x approaches 1, 2x + 1 approaches 3
  distance of output from 3: |2x + 1 - 3| = 2|x - 1|    simplify
  want: 2|x - 1| < ε                                     the skeptic's tolerance
  works if |x - 1| < ε / 2                               divide by 2
  answer: δ = ε / 2                                      valid for every ε
  example: ε = 0.01 gives δ = 0.005                      keep x within 0.005 of 1
```

Weierstrass also produces, in 1872, a function that is continuous everywhere but has no slope anywhere: a curve with no breaks that is all corners. Intuition clearly needs supervision. Bernhard Riemann gives the integral its exact definition in 1854, as the limit of strip sums. In 1859 he writes a short paper on prime numbers that contains the **Riemann hypothesis**, still unproved and worth a million dollars.

Limits rest on the real numbers, and in the 1860s nobody can define those either. Richard Dedekind publishes an answer in 1872. He builds each real number from fractions alone, as a **cut**: a split of all fractions into a lower set and an upper set.

```txt
  The number √2 as a Dedekind cut
  lower set: fractions q with q < 0 or q^2 < 2    1.4 is here: 1.96 < 2
  upper set: every other fraction                 1.5 is here: 2.25 > 2
  the lower set has no largest member             always a closer fraction below
  the upper set has no smallest member            always a closer fraction above
  the gap between them is √2                      no fraction fills it
```

Algebra changes too. For centuries mathematicians search for a formula, like the quadratic formula, for equations of degree five. Niels Henrik Abel proves in 1824 that no such general formula in roots exists. Évariste Galois finds the deeper reason. He attaches to each equation a **group**: the set of ways to shuffle its roots that keep every algebraic relation among them intact. The shape of the group decides whether a root formula exists. Galois dies after a duel in 1832, at 20. Joseph Liouville publishes his papers in 1846. Groups now describe symmetry everywhere, from crystals to particle physics to error-correcting codes.

George Boole publishes *The Laws of Thought* in 1854. He writes logic as algebra over two values, 1 for true and 0 for false. AND becomes multiplication. His key law is x · x = x, true only for 0 and 1. About 80 years later Claude Shannon shows that Boole's algebra describes switching circuits. Every `if` in your code is Boolean algebra.

Charles Babbage designs mechanical calculators: the Difference Engine from 1822 and, from 1834, the Analytical Engine, a general machine with a store, a mill, and punched cards. Neither is finished in his lifetime. Ada Lovelace translates an Italian engineer's article on the Analytical Engine in 1843 and adds Notes about three times longer than the article. Note G lays out step by step how the engine computes the Bernoulli numbers: the first published computer program. She also sees that the engine manipulates symbols, not only numbers.

Sofia Kovalevskaya, barred from Russian universities as a woman, studies privately with Weierstrass in Berlin. Göttingen awards her a doctorate in 1874 for work that includes the Cauchy-Kovalevskaya theorem on differential equations. In 1888 she wins the Prix Bordin of the Paris Academy, and in 1889 she becomes a full professor in Stockholm.

### Cantor: Infinity Comes in Sizes

Georg Cantor asks a question that looks childish. Are there as many even numbers as whole numbers? As many fractions as whole numbers? He answers with a precise rule: two sets have the same size if you can pair their members one to one with nothing left over. A set that can be paired with 1, 2, 3, ... is **countable**: you can list it, one item per line, and every member eventually appears.

<!-- diagram: type=set-theory ref=cantor-rationals grid=5x5 caption="The positive fractions in one list by a zigzag path" -->
![A 5 by 5 grid of fractions, tops 1 to 5 across and bottoms 1 to 5 down. A dashed orange zigzag path runs along the diagonals. Repeats such as 2/2, 3/3, 4/2, 2/4, 4/4, and 5/5 are gray and skipped. Orange numbers give each fraction its place: 1/1, 1/2, 2/1, 3/1, 1/3, 1/4, 2/3, 3/2, 4/1, 5/1, 1/5. Text: every fraction gets a place, the fractions are countable; the real numbers are not](img/cantor-rationals.svg)

Lay out every positive fraction in a grid: the top number across, the bottom number down. Now walk the diagonals in a zigzag, skipping any fraction that repeats an earlier one, such as 2/2 = 1/1. Every fraction sits on some diagonal, and every diagonal is finite. Every fraction gets a place in the list. The fractions are countable, the same size as the whole numbers, even though they pack densely along the number line. Cantor proves a stronger result in 1874: even the algebraic numbers, the roots of all polynomial equations with whole-number coefficients, form a countable set. The zigzag picture is the later classroom version.

The real numbers are different. In 1874 Cantor proves they are not countable. In 1891 he gives a second proof, the **diagonal argument**, short enough to fit on a napkin.

<!-- diagram: type=set-theory ref=cantor-diagonal rows=6 diagonal=010100 flipped=101011 caption="Cantor (1891): the diagonal argument" -->
![Six rows of binary digits, s1 = 010110..., s2 = 110010..., s3 = 000101..., s4 = 101100..., s5 = 011001..., s6 = 111010..., with the diagonal digits highlighted: 0, 1, 0, 1, 0, 0. The new row flips each one: 101011. Text: new differs from s1 in place 1, from s2 in place 2, from sn in place n. No list catches every infinite sequence](img/cantor-diagonal.svg)

Suppose someone claims a complete list of every infinite sequence of 0s and 1s. Write the list as rows. Read down the diagonal: the first digit of row 1, the second digit of row 2, and onward. In the picture the diagonal reads 010100. Flip every digit: 101011. The new sequence differs from row 1 in place 1, from row 2 in place 2, from row n in place n. It differs from every row, and it is missing from the list. Every list misses something. Infinite binary sequences, and with them the real numbers, are **uncountable**: a strictly bigger infinity.

```txt
  Diagonal argument on the six rows in the picture
  s1 = 0 1 0 1 1 0    digit 1 is 0        flip to 1
  s2 = 1 1 0 0 1 0    digit 2 is 1        flip to 0
  s3 = 0 0 0 1 0 1    digit 3 is 0        flip to 1
  s4 = 1 0 1 1 0 0    digit 4 is 1        flip to 0
  s5 = 0 1 1 0 0 1    digit 5 is 0        flip to 1
  s6 = 1 1 1 0 1 0    digit 6 is 0        flip to 1
  new = 1 0 1 0 1 1   differs from each row on the diagonal
```

Many leading mathematicians reject Cantor's ideas. Leopold Kronecker opposes him in public. Cantor suffers repeated bouts of depression. David Hilbert later declares that nobody can expel mathematicians from the paradise Cantor has created. The diagonal trick lives on. Turing uses it in 1936 to prove that no program can decide whether every program halts.

## What It Unlocked Next

* Cantor's sets become the proposed foundation of all mathematics, and its paradoxes start the crisis of [chapter 09](../09-20th-century-foundations-and-computing/README.md).
* The diagonal argument powers Gödel's incompleteness theorems (1931) and Turing's halting problem (1936): see [chapter 09](../09-20th-century-foundations-and-computing/README.md).
* Boole's algebra and the Babbage-Lovelace engine meet in the electronic computers of [chapter 09](../09-20th-century-foundations-and-computing/README.md).
* Riemann's geometry becomes Einstein's general relativity (1915), and the Riemann hypothesis appears on Hilbert's list of problems in 1900 (number 8) and remains open in [chapter 10](../10-modern-mathematics/README.md).
* Euler's graphs grow into network science, the four color theorem, and routing algorithms in [chapter 10](../10-modern-mathematics/README.md).
* Galois groups become abstract algebra, the language Emmy Noether builds in the 1920s.

## Connects To

* [Course 401](../../course/401/README.md): limits and the epsilon-delta definition at the start of serious calculus.
* [Course 501](../../course/501/README.md): proofs, sets, and countability.
* [Graph theory track](../../tracks/graph-theory/README.md): Euler paths, degrees, and everything that grows from Königsberg.
* [Real analysis track](../../tracks/real-analysis/README.md): Cauchy, Weierstrass, and Dedekind in full.
* [Logic and set theory track](../../tracks/logic-and-set-theory/README.md): Boole, Cantor, countable and uncountable sets.
* [Abstract algebra track](../../tracks/abstract-algebra/README.md): groups, from Galois onward.
* [Number theory track](../../tracks/number-theory/README.md): modular arithmetic from the *Disquisitiones*.
* [Geometry track](../../tracks/geometry/README.md): the parallel postulate and curved geometries.
* [Statistics track](../../tracks/statistics/README.md): least squares, Quetelet, and Nightingale.
* [Story of an idea: infinity](../story-of-an-idea/infinity.md): from the ghosts of departed quantities to the diagonal argument.
* [Story of an idea: proof](../story-of-an-idea/proof.md): why the 1800s demand rigor.
* [Story of an idea: notation](../story-of-an-idea/notation.md): how Euler fixes f(x), e, i, π, and Σ.
* Biographies of [Euler](../biographies/euler.md), [Gauss](../biographies/gauss.md), [Galois](../biographies/galois.md), [Lovelace](../biographies/lovelace.md), [Riemann](../biographies/riemann.md), and [Cantor](../biographies/cantor.md): the people behind the ideas.

## Try It

1. Add 1 + 2 + ... + 50 by the pairing method. Then find 1 + 2 + ... + 1,000 with the formula n(n + 1)/2.
2. A graph is a square ABCD with one diagonal from A to C. Give the degree of each dot. Can you draw it in one stroke without lifting the pen or repeating a line? If yes, where must you start?
3. The city of Königsberg removes the single bridge from A to D. Recompute the degrees. Does a walk over every remaining bridge exactly once now exist? Where does it start and end?
4. Continue the zigzag listing of fractions past 1/5. Which fractions get places 12 and 13?
5. A list holds four rows: 0000, 1111, 0101, 1010. Build the diagonal row and flip it. Check that the result is missing from the list.
6. A triangle on a sphere has its top corner at the North Pole and the other two corners on the equator, an eighth of the way around the equator apart. What is the angle sum?
7. For f(x) = 3x near x = 2, the limit is 6. The skeptic names ε = 0.03. Find a δ that works.
8. Add the first four terms of the Basel sum, 1 + 1/4 + 1/9 + 1/16. How far is it from π²/6 ≈ 1.6449?

<details>
<summary>Answers</summary>

1. 25 pairs of 51 give 1,275, and 1,000 x 1,001 / 2 = 500,500.
2. A 3, B 2, C 3, D 2: two odd dots. The stroke exists and must start at A or C and end at the other.
3. A drops to 4 and D to 2, B and C stay at 3. Two odd dots: a walk exists from B to C or from C to B.
4. The next diagonal (top + bottom = 7) runs 1/6, 2/5, 3/4, and onward. Place 12 is 1/6 and place 13 is 2/5.
5. Diagonal 0, 1, 0, 0 reads 0100, flipped to 1011, which differs from each row in its own place.
6. 90 + 90 + 45 = 225 degrees, because an eighth of the way around makes a 45-degree angle at the pole.
7. |3x - 6| = 3|x - 2| < 0.03 when |x - 2| < 0.01. Take δ = 0.01 (any smaller δ also works).
8. 1 + 0.25 + 0.1111 + 0.0625 = 1.4236, short by about 0.221: the series creeps up slowly.

</details>

## Code Corner

The program in [code/main.go](code/main.go) runs four checks from the chapter. It counts degrees on any list of bridges (a **multigraph**, a graph that allows several lines between the same two dots), tests connectivity with a breadth-first walk, and applies Euler's rule. It verifies the Gauss sum three ways. It lists fractions along Cantor's zigzag with a greatest-common-divisor test to skip repeats. It builds the diagonal row from the six rows of the picture. The core of the Euler test:

```go
	odd := 0
	for _, d := range deg {
		if d%2 == 1 {
			odd++
		}
	}
	ok := len(seen) == len(deg) && (odd == 0 || odd == 2)
```

And the zigzag. Each diagonal holds the fractions whose top and bottom add to s. Odd diagonals start at the small top number and even diagonals at the large one, which makes the path turn back and forth:

```go
	for s := 2; len(out) < count; s++ {
		for i := 1; i < s && len(out) < count; i++ {
			top := i
			if s%2 == 0 {
				top = s - i
			}
			bottom := s - top
			if gcd(top, bottom) == 1 {
				out = append(out, fmt.Sprintf("%d/%d", top, bottom))
			}
		}
	}
```

Run it:

```txt
cd code && go run main.go
```

Output:

```txt
1. Euler and the bridges
   Konigsberg, 7 bridges: degrees A=5 B=3 C=3 D=3, odd nodes 4, walk exists: false
   with an 8th bridge B-C: degrees A=5 B=4 C=4 D=3, odd nodes 2, walk exists: true

2. Gauss: 1 + 2 + ... + 100
   loop: 5050   pairing: 50 x 101 = 5050   formula n(n+1)/2 = 5050

3. Cantor: the fractions in one list
   1/1, 1/2, 2/1, 3/1, 1/3, 1/4, 2/3, 3/2, 4/1, 5/1, 1/5

4. Cantor: the diagonal
   s1 = 010110  differs from new in place 1
   s2 = 110010  differs from new in place 2
   s3 = 000101  differs from new in place 3
   s4 = 101100  differs from new in place 4
   s5 = 011001  differs from new in place 5
   s6 = 111010  differs from new in place 6
   diagonal 010100, flipped (new) 101011
```

The fraction list matches the orange numbers in the zigzag diagram. The diagonal matches the picture digit for digit. Try your own bridge lists in `main`: Euler's rule answers in microseconds a question the people of Königsberg walked for years.

## Flashcards

Anki deck in [cards.tsv](cards.tsv) (tab-separated: front, back, tags).

## Go Deeper

* [MacTutor biography of Leonhard Euler](https://mathshistory.st-andrews.ac.uk/Biographies/Euler/): the life, the blindness, and the 80 volumes.
* [MacTutor: Non-Euclidean geometry](https://mathshistory.st-andrews.ac.uk/HistTopics/Non-Euclidean_geometry/): the 2,000-year fight with the parallel postulate.
* [MacTutor: The real numbers, part 2](https://mathshistory.st-andrews.ac.uk/HistTopics/Real_numbers_2/): Cauchy, Weierstrass, Dedekind, and Cantor build the reals.
* [MacTutor: Beginnings of set theory](https://mathshistory.st-andrews.ac.uk/HistTopics/Beginnings_of_set_theory/): Cantor and the sizes of infinity.
* [MacTutor: The development of group theory](https://mathshistory.st-andrews.ac.uk/HistTopics/Development_group_theory/): from Lagrange and Galois to abstract groups.
* [MacTutor biography of Ada Lovelace](https://mathshistory.st-andrews.ac.uk/Biographies/Lovelace/): the Notes of 1843 and the Analytical Engine.
