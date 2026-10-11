# 07 The Scientific Revolution and Calculus

**Era:** about 1600 to 1700 · **Reading time:** about 20 minutes · **Previous:** [06 Medieval and Renaissance Europe](../06-medieval-and-renaissance-europe/README.md) · **Next:** [08 The 18th and 19th Centuries: Rigor](../08-18th-and-19th-century-rigor/README.md)

## The Big Idea

In one century Europe builds the tools that still run physics and engineering. Logarithms turn hard multiplication into easy addition. Coordinates turn curves into equations. Probability turns a gambling quarrel into arithmetic. Calculus measures things that change, one tiny step at a time.

## The World at That Time

Ships cross oceans for trade and empire. A navigator finds latitude from the height of the sun or the Pole Star. Longitude is the hard part. It needs either an accurate clock at sea or a sky event visible from everywhere, and neither exists yet. Spain offers a prize for a solution in 1598. Galileo proposes the moons of Jupiter as a sky clock in the 1610s. The problem stays open until the marine clocks of the 1700s. A wrong longitude puts a ship on the rocks. Navigation tables are life-or-death data, and every entry costs hours of hand multiplication.

Astronomy changes at the same time. Johannes Kepler publishes his first two laws of planetary motion in 1609 and his third in 1619. Planets move in ellipses, not circles, and they speed up near the sun. Galileo Galilei rolls balls down ramps and finds that a falling body covers distance in proportion to the square of the time: after twice the time, four times the distance. Nature turns out to follow equations, and the equations involve change: speed, acceleration, curved paths.

The tools are thin. A scholar has pen, paper, tables, and letters. There are few journals. Mathematicians mail results to each other, often through Marin Mersenne in Paris, a friar who acts as a one-man message queue for European science. The Royal Society in London starts in 1660 and the Paris Academy in 1666. Publication is slow, and credit is a matter of who wrote to whom and when.

```txt
  Need in the 1600s                    Math that answers it
  ----------------------------------   ------------------------------
  navigation tables, astronomy         logarithms (1614), slide rules
  orbits, cannon fire, optics          coordinates (1637), calculus
  gambling disputes, annuities         probability (1654)
  motion, falling bodies, planets      calculus, Principia (1687)
```

## Key People

| Person | Dates | One-Line Contribution |
| --- | --- | --- |
| John Napier | 1550 to 1617 | Publishes the first table of logarithms in 1614. |
| Henry Briggs | 1561 to 1630 | Recasts logarithms in base 10, the version used for 350 years. |
| Johannes Kepler | 1571 to 1630 | Finds the laws of planetary motion (1609 to 1619) from data, not theory. |
| Galileo Galilei | 1564 to 1642 | Measures falling bodies and writes the law of fall as a math rule. |
| Bonaventura Cavalieri | 1598 to 1647 | Finds areas and volumes by slicing shapes into thin pieces (1635). |
| [René Descartes](../biographies/descartes.md) | 1596 to 1650 | Turns curves into equations in *La Géométrie* (1637). |
| [Pierre de Fermat](../biographies/fermat.md) | c. 1607 to 1665 | Invents coordinates on his own, finds tangents and maxima, cofounds probability. |
| [Blaise Pascal](../biographies/pascal.md) | 1623 to 1662 | Writes up the arithmetic triangle and solves the problem of points with Fermat (1654). |
| John Wallis | 1616 to 1703 | Pushes infinite sums and products; introduces the symbol ∞. |
| Isaac Barrow | 1630 to 1677 | Teaches Newton; states a geometric form of the link between tangents and areas. |
| Christiaan Huygens | 1629 to 1695 | Writes the first printed book on probability (1657) and builds the pendulum clock. |
| [Isaac Newton](../biographies/newton.md) | 1643 to 1727 | Invents fluxions (1665 to 1666) and writes the *Principia* (1687). |
| [Gottfried Wilhelm Leibniz](../biographies/leibniz.md) | 1646 to 1716 | Invents calculus on his own, with the notation still in use (published 1684). |

## Key Ideas

### Logarithms: Multiply by Adding

A **logarithm** answers the question: what power of a base gives this number? In base 10, the logarithm of 100 is 2, because 10 x 10 = 100. The logarithm of 1,000 is 3. The logarithm of 2 sits between 0 and 1, at about 0.30103.

The useful fact is simple. Multiplying two numbers adds their powers:

$$10^a \times 10^b = 10^{a+b} \quad\Longrightarrow\quad \log(xy) = \log x + \log y$$

A clerk who needs 4,729 x 3,816 looks up two logarithms, adds them, and looks up the answer in reverse. Addition is fast and hard to get wrong. Multiplying seven-digit numbers by hand is slow and easy to get wrong. Logarithms are a lookup table that converts expensive work into cheap work, the same trade an SRE makes with a cache.

John Napier, a Scottish landowner, publishes his table in 1614 after about 20 years of computing. His version uses an awkward base. Henry Briggs travels to Scotland to meet him in 1615, and the two agree that base 10 is better. Briggs publishes base-10 tables in 1617 and a large set in 1624. Kepler uses logarithms for his planetary tables of 1627. The astronomer Laplace later says that logarithms double the life of an astronomer by cutting the work in half.

<!-- diagram: type=historical-method ref=slide-rule-logs caption="Slide rule: log scales multiply 2 x 3 = 6" -->
![Two logarithmic scales, C on top and D below. The 1 of scale C sits over the 2 of scale D. Under the 3 of scale C, scale D reads 6. Caption: distance from 1 to n is log(n), and adding lengths log 2 + log 3 = log 6 multiplies 2 x 3 = 6. Napier publishes tables in 1614; Gunter, Oughtred and others turn them into scales and slide rules](img/slide-rule-logs.svg)

The picture turns the table into a ruler. On each scale, the distance from 1 to a number n is proportional to log n. Slide the top scale until its 1 sits over the 2 on the bottom scale. That shifts everything by the length log 2. Now read under the 3 on the top scale: the bottom scale says 6, because the two lengths add to log 2 + log 3 = log 6. Edmund Gunter draws a single log scale in 1620. William Oughtred puts two of them side by side about 1622. Engineers carry slide rules until pocket calculators replace them in the 1970s.

```txt
  2 x 3 with base-10 logarithms
  log 2  = 0.30103               look up in the table
  log 3  = 0.47712               look up in the table
  sum    = 0.77815               add: the only real work
  10^0.77815 = 6.000             look up the sum in reverse
  check: log 6 = 0.77815         same entry, the method holds
```

### Coordinates: A Curve Becomes an Equation

Greek geometry studies curves with drawings and proportions. Algebra studies unknown numbers with symbols. In the 1630s two Frenchmen join the two. René Descartes publishes *La Géométrie* in 1637 as an appendix to his *Discourse on Method*. Pierre de Fermat, a lawyer in Toulouse, has the same idea in a manuscript that circulates about 1636 but is printed only after his death.

The idea: pick a fixed starting point and measure every other point by two numbers, how far across and how far up. These two numbers are the **coordinates** of the point. Now a curve is the set of all points whose coordinates pass some test, and the test is an equation. Geometry questions become algebra questions, and algebra has rules that grind through without inspiration.

<!-- diagram: type=coordinate-plane ref=descartes-coordinates range=-5..5 curve="x^2+y^2=25" point=3,4 caption="Descartes (1637): a curve becomes an equation" -->
![A grid with x and y axes from -5 to 5. An orange circle of radius 5 is centered at the origin. The point (3, 4) is marked on the circle, with a radius line of length 5 and a right triangle with legs 3 and 4. Text: every point is a pair of numbers; the circle is every pair that satisfies x² + y² = 25; check (3, 4): 9 + 16 = 25. Footnote: modern perpendicular axes came after Descartes, but the idea is his and Fermat's](img/descartes-coordinates.svg)

The circle in the picture has radius 5 and its center at the origin, the point (0, 0). The point (3, 4) sits 3 across and 4 up. Drop a line straight down from it and you get a right triangle with legs 3 and 4. The radius is the long side. The theorem of Pythagoras says 3² + 4² = 5². That holds for every point on the circle. The whole circle is the equation x² + y² = 25. One honest footnote: Descartes does not draw the familiar pair of perpendicular axes. He uses one reference line and measures at an angle that suits the problem. The full grid comes later. The idea is his and Fermat's.

```txt
  Is (4, 3) on the circle x^2 + y^2 = 25?
  x^2 + y^2 = 4^2 + 3^2          substitute x = 4, y = 3
            = 16 + 9             square each coordinate
            = 25                 add: matches, the point is on it
  Is (4, 4) on it?
  16 + 16   = 32                 32 is not 25: the point lies outside
```

### Chance Becomes Arithmetic: Pascal and Fermat

In 1654 a gambler, the Chevalier de Méré, asks Blaise Pascal a question known as the **problem of points**. Two players stake equal money on a game of several rounds. The first to win a set number of rounds takes everything. The game stops early. How do you split the money fairly?

Pascal writes to Fermat. Over a summer of letters they solve it. The key move: do not look back at the rounds already played. Look forward. List every way the remaining rounds can go, each equally likely, and count how many end in a win for each player. Split the stakes in that ratio. This is the start of **probability**: the share of equally likely outcomes in which an event happens.

Counting outcomes leads straight to a triangle of numbers. Pascal writes a treatise on it in 1654. It is now called Pascal's triangle, though it is much older.

<!-- diagram: type=number-triangle ref=pascal-triangle rows=0..7 highlight=row4 caption="Pascal's triangle with the coin-flip reading of row 4" -->
![Pascal's triangle, rows 0 to 7, from 1 at the top to 1 7 21 35 35 21 7 1 at the bottom. Row 4 (1 4 6 4 1) is matched to four coin flips: 0 heads 1 way, 1 head 4 ways, 2 heads 6 ways, 3 heads 4 ways, 4 heads 1 way, total 16, and P(exactly 2 heads) = 6/16. Footnote: known centuries earlier in India (Pingala), Persia (al-Karaji), and China (Yang Hui, 1261)](img/pascal-triangle.svg)

Each entry is the sum of the two entries above it. Row n lists the number of ways to get 0, 1, 2, ..., n heads in n coin flips. Row 4 reads 1, 4, 6, 4, 1. Exactly two heads in four flips happens 6 ways out of 16, a probability of 6/16. The footnote matters. Pingala in India, al-Karaji in Persia, and Yang Hui in China (1261) all know the triangle centuries earlier. Pascal does not discover it. He works out its theory and puts it to a new use.

```txt
  Problem of points: first to 3 wins. A has 2, B has 1. Stakes: 64 coins.
  A needs 1 more, B needs 2 more    at most 2 more rounds settle it
  outcomes: AA, AB, BA, BB          4 equally likely futures
  A wins in AA, AB, BA              any future with at least one A
  B wins only in BB                 B needs both rounds
  split 3 : 1                       A gets 48 coins, B gets 16
```

Pascal gives this exact case in a letter to Fermat: 48 coins to the leader. Huygens hears of the problem on a visit to Paris and writes the first printed book on probability in 1657. Insurance, annuities, and every error budget you have ever set descend from that summer of letters.

### Calculus: Slopes and Areas

Two questions dominate the century. First: how steep is a curve at one point? That gives speed from a distance record and the direction of a light ray off a curved mirror. Second: how much area lies under a curve? That gives distance from a speed record, volumes of barrels, and the pull of a planet. Kepler writes a whole book on the volume of wine barrels in 1615, after he watches a merchant measure the barrels for his wedding wine with a single dipstick. The questions are everywhere.

Many people chip away at them. Fermat finds tangents and maxima for polynomial curves. Cavalieri, in 1635, slices areas into thin lines he calls indivisibles and compares the slices. Wallis, in 1656, finds areas with infinite sums. Isaac Barrow, Newton's teacher at Cambridge, proves a geometric theorem that links tangents and areas. Each has a piece of the method. None has a general machine.

Isaac Newton builds the machine in 1665 and 1666. Cambridge closes for the plague, and Newton, about 23 years old, goes home to Woolsthorpe. There he develops what he calls **fluxions**: rates at which quantities flow. He tells few people. His 1669 tract *De analysi* circulates in manuscript. His *Method of Fluxions*, written in 1671, appears only in 1736, after his death. His great book, the *Principia* of 1687, explains the motions of planets and tides from one law of gravity. Its proofs are written mostly in classical geometry.

Gottfried Wilhelm Leibniz, a German lawyer and diplomat, reaches the same machine about ten years later, mainly in Paris. On 29 October 1675 he first writes the integral sign ∫ in his notes. It is a stretched letter S for *summa*, sum. He publishes his differential calculus in 1684 and the integral calculus in 1686. His notation is the one everyone still uses: dx for a tiny change in x, dy/dx for a slope, ∫ for a sum of tiny pieces. Good notation does half the thinking. Leibniz knows it and designs his symbols with care.

The two core words, in plain language:

* The **derivative** is the slope of a curve at a single point. It is the rate of change right now: speed, not average speed.
* The **integral** is the total accumulated under a curve. It adds up a rate over time to get an amount: distance from speed, bytes from a throughput graph.

<!-- diagram: type=calculus ref=tangent-and-area f="x^2" point=1,1 secants=3,2.5 strips=8 interval=0..2 caption="Derivative as limit of secant slopes; integral as limit of strip sums" -->
![Left panel: the curve y = x² with the point P = (1, 1). Two gray dashed secant lines through P, with slopes 3 and 2.5, close in on the orange tangent line of slope 2. A small orange triangle on the tangent is labeled dx and dy. Right panel: the same curve from 0 to 2 with 8 orange strips under it, total area 2.188; thinner strips push the area toward 8/3 ≈ 2.667. Caption: Leibniz writes the limit of the sum as ∫ x² dx](img/tangent-and-area.svg)

The left panel finds a slope. A **secant** is a straight line through two points of the curve. From P = (1, 1) to (2, 4) the secant rises 3 for a run of 1: slope 3. Move the second point closer, to (1.5, 2.25), and the slope drops to 2.5. Keep moving it closer. The slopes close in on 2, the slope of the **tangent**, the line that just touches the curve at P. The small triangle shows the Leibniz view: a tiny step dx across and the matching tiny step dy up. Their ratio dy/dx is the slope.

The right panel finds an area. Cut the region under y = x² from 0 to 2 into eight strips of width 0.25. Make each strip as tall as the curve at its left edge. The strips total 2.1875, shown rounded as 2.188. They miss the thin slivers between strip tops and the curve. Use thinner strips and the slivers shrink. The total closes in on 8/3, about 2.667. Leibniz writes that limit as ∫ x² dx.

```txt
  Slope of y = x^2 at x = 1, by shrinking the step h
  h = 1      (4 - 1) / 1                  = 3      secant to (2, 4)
  h = 0.5    (2.25 - 1) / 0.5             = 2.5    secant to (1.5, 2.25)
  h = 0.1    (1.21 - 1) / 0.1             = 2.1    closer
  h = 0.01   (1.0201 - 1) / 0.01          = 2.01   closer still
  algebra:   ((1+h)^2 - 1) / h = 2 + h    expand and cancel the h
  h -> 0:    slope = 2                    the tangent slope at (1, 1)
```

The algebra line is the real trick. For any step h the secant slope is exactly 2 + h. As h shrinks to nothing, the slope settles at 2. Nobody in the 1600s can say precisely what "shrinks to nothing" means. Newton talks of ultimate ratios. Leibniz talks of infinitely small quantities. Both work in practice. The precise definition takes about another 150 years and fills much of the [next chapter](../08-18th-and-19th-century-rigor/README.md).

### The Fundamental Theorem and the Priority Dispute

The central discovery of Newton and Leibniz is that the two questions are one question run in opposite directions. Slope and area undo each other. This is the **Fundamental Theorem of Calculus**. In plain words: if you know the rate at which something grows, you find the total by working the rate backwards. To find the area under x², ask which function has slope x². The answer is x³/3, since its slope is x². The area from 0 to 2 is then 2³/3 - 0 = 8/3. No strips needed.

```txt
  Area under y = x^2 from 0 to 2, with the Fundamental Theorem
  want: a function whose slope is x^2     reverse the slope question
  try x^3 / 3: its slope is x^2           the power rule run backwards
  value at 2:  8 / 3                      plug in the right end
  value at 0:  0                          plug in the left end
  area = 8/3 - 0 = 8/3 ≈ 2.667            matches the strips' limit
```

Think of an odometer and a speedometer. The speedometer is the derivative of the odometer. The odometer is the integral of the speedometer. A monitoring dashboard does the same thing: a counter of total requests and a graph of requests per second hold the same information. Take the rate of one to get the other, and add up the other to get back the first.

Two inventors means a fight. Leibniz publishes first, in 1684. Newton has the method first, from 1665 to 1666, but keeps it mostly private. Leibniz saw some of Newton's work in manuscript and exchanged letters with him in 1676. Newton's supporters accuse Leibniz of copying. In 1712 the Royal Society, with Newton as its president, appoints a committee. Its report, issued in 1713, finds for Newton. Newton drafts much of it himself. That is not how a code review is supposed to work. Historians now agree that the two men find calculus independently, by different routes. The cost of the fight falls on Britain. British mathematicians keep Newton's dot notation out of loyalty and fall behind the continent, where Leibniz's d and ∫ make the work easier, for about a century.

## What It Unlocked Next

* Calculus becomes the language of physics. The Bernoullis and Euler extend it to the motion of fluids, strings, and planets: see [08 The 18th and 19th Centuries: Rigor](../08-18th-and-19th-century-rigor/README.md).
* The vague infinitely small quantities of Newton and Leibniz force the long search for rigor that ends with limits and epsilon-delta definitions in [chapter 08](../08-18th-and-19th-century-rigor/README.md).
* Coordinates lead to vectors, to functions of several variables, and much later to the geometry of data in [chapter 09](../09-20th-century-foundations-and-computing/README.md).
* Probability grows into statistics, insurance math, and the modern theory of [chapter 09](../09-20th-century-foundations-and-computing/README.md).
* Leibniz writes on binary numbers in 1703 and dreams of a calculus of reasoning. Boole, Turing, and every computer follow that thread.

## Connects To

* [Course 201](../../course/201/README.md): the coordinate plane and lines that Descartes and Fermat start.
* [Course 301](../../course/301/README.md): logarithms, conic sections, and a first look at limits.
* [Course 401](../../course/401/README.md): limits, derivatives, and integrals as a working toolkit.
* [Calculus track](../../tracks/calculus/README.md): the full modern treatment of slopes, areas, and the Fundamental Theorem.
* [Algebra track](../../tracks/algebra/README.md): logarithms and exponents, with the rule log(xy) = log x + log y.
* [Geometry track](../../tracks/geometry/README.md): circles and lines written as equations.
* [Probability track](../../tracks/probability/README.md): counting equally likely outcomes, from the problem of points onward.
* [Combinatorics track](../../tracks/combinatorics/README.md): Pascal's triangle and binomial coefficients.
* [Story of an idea: notation](../story-of-an-idea/notation.md): why dx, dy/dx, and ∫ outlive the dots of Newton.
* [Story of an idea: infinity](../story-of-an-idea/infinity.md): the infinitely small quantities that nobody can yet define.
* Biographies of [Descartes](../biographies/descartes.md), [Fermat](../biographies/fermat.md), [Pascal](../biographies/pascal.md), [Newton](../biographies/newton.md), and [Leibniz](../biographies/leibniz.md): the people behind each idea.

## Try It

1. Use the base-10 values log 2 = 0.30103 and log 3 = 0.47712. Find log 12 by adding logarithms only. (Hint: 12 = 2 x 2 x 3.)
2. On a slide rule, you set the 1 of scale C over the 3 of scale D. What does scale D show under the 2 of scale C?
3. Is the point (5, 0) on the circle x² + y² = 25? Is (2, 4)?
4. Find the slope of the secant of y = x² from (1, 1) to (1.2, 1.44). Compare it with the tangent slope 2.
5. Find the slope of the tangent to y = x² at x = 3 using the shrinking-step method: compute ((3 + h)² - 9) / h for h = 0.1 and h = 0.01, then guess the limit.
6. Cut the area under y = x² from 0 to 2 into four strips of width 0.5, each as tall as the curve at its left edge. Find the total. Is it above or below 8/3?
7. Read row 5 of Pascal's triangle. In five coin flips, how many ways give exactly three heads? What is the probability?
8. Problem of points: first to 3 wins, A has 1 win, B has 2 wins, stakes 64 coins. How do Pascal and Fermat split the money?

<details>
<summary>Answers</summary>

1. 0.30103 + 0.30103 + 0.47712 = 1.07918, which matches log 12 because 12 = 2 x 2 x 3.
2. 6, because the lengths log 3 + log 2 add to log 6.
3. (5, 0) is on it since 25 + 0 = 25; (2, 4) is not since 4 + 16 = 20.
4. (1.44 - 1) / 0.2 = 2.2, a bit steeper than the tangent slope 2, and the gap equals the step 0.2.
5. h = 0.1 gives 6.1, h = 0.01 gives 6.01, and the limit is 6 because the secant slope is exactly 6 + h.
6. 0.5 x (0 + 0.25 + 1 + 2.25) = 1.75, below 8/3 because left-edge strips sit under a rising curve.
7. Row 5 is 1, 5, 10, 10, 5, 1: ten ways out of 32, a probability of 10/32 = 5/16.
8. A needs 2 and B needs 1. The futures are AA, AB, BA, BB and A wins only in AA: A gets 16 coins and B gets 48.

</details>

## Code Corner

The program in [code/main.go](code/main.go) runs the four methods of the chapter. It shrinks the step h to find the slope of x² at 1, adds thinner and thinner strips under x² on the interval from 0 to 2, checks that log 2 + log 3 = log 6, and builds Pascal's triangle to split stakes in the problem of points. The heart of it is three small functions:

```go
// slope returns the slope of the secant from (x, f(x)) to (x+h, f(x+h)).
func slope(x, h float64) float64 {
	return (f(x+h) - f(x)) / h
}

// leftSum adds n strips under f on [a, b], each strip as tall as
// the curve at its left edge.
func leftSum(a, b float64, n int) float64 {
	w := (b - a) / float64(n)
	total := 0.0
	for i := 0; i < n; i++ {
		total += f(a+float64(i)*w) * w
	}
	return total
}

// points splits the stakes when player A needs a more wins and
// player B needs b more. Play at most a+b-1 more fair rounds and
// count the outcomes in which A gets at least a wins.
func points(a, b int) (aWays, total int) {
	n := a + b - 1
	row := pascal(n)[n]
	for k := a; k <= n; k++ {
		aWays += row[k]
	}
	return aWays, 1 << n
}
```

Run it:

```txt
cd code && go run main.go
```

Output:

```txt
1. Slope of y = x^2 at x = 1 (secant slopes)
   h = 1      slope = 3.0000
   h = 0.5    slope = 2.5000
   h = 0.1    slope = 2.1000
   h = 0.01   slope = 2.0100
   h = 0.001  slope = 2.0010

2. Area under y = x^2 from 0 to 2 (left strips)
   n = 8       area = 2.187500
   n = 100     area = 2.626800
   n = 1000    area = 2.662668
   n = 100000  area = 2.666627
   exact 8/3   area = 2.666667

3. Logarithms (base 10, as in Briggs)
   log 2 + log 3 = 0.30103 + 0.47712 = 0.77815
   log 6         = 0.77815
   10^(log 2 + log 3) = 6.0000

4. Pascal's triangle and the problem of points
   row 0: [1]
   row 1: [1 1]
   row 2: [1 2 1]
   row 3: [1 3 3 1]
   row 4: [1 4 6 4 1]
   row 5: [1 5 10 10 5 1]
   row 6: [1 6 15 20 15 6 1]
   row 7: [1 7 21 35 35 21 7 1]
   A needs 1, B needs 2: A gets 3/4 of the stakes
   A needs 1, B needs 3: A gets 7/8 of the stakes
   A needs 2, B needs 3: A gets 11/16 of the stakes
```

The slopes match the gray secants of the diagram, then close in on 2. The strip sums start at the 2.1875 of the diagram and creep toward 8/3. Note how slowly: 100,000 strips still miss by about 0.00004. The Fundamental Theorem gets the exact answer in one line. That is the whole case for calculus.

## Flashcards

Anki deck in [cards.tsv](cards.tsv) (tab-separated: front, back, tags).

## Go Deeper

* [MacTutor: The rise of calculus](https://mathshistory.st-andrews.ac.uk/HistTopics/The_rise_of_calculus/): the path from Archimedes through Cavalieri and Barrow to Newton and Leibniz.
* [MacTutor biography of John Napier](https://mathshistory.st-andrews.ac.uk/Biographies/Napier/): the inventor of logarithms and his 20 years of tables.
* [MacTutor biography of Isaac Newton](https://mathshistory.st-andrews.ac.uk/Biographies/Newton/): fluxions, the *Principia*, and the priority dispute.
* [MacTutor biography of Gottfried Leibniz](https://mathshistory.st-andrews.ac.uk/Biographies/Leibniz/): the notation, the 1675 notes, and the calculating machine.
* [MacTutor biography of Blaise Pascal](https://mathshistory.st-andrews.ac.uk/Biographies/Pascal/): the triangle, the Pascaline, and the letters with Fermat.
* [MacTutor: the longitude problem](https://mathshistory.st-andrews.ac.uk/HistTopics/Longitude1/): why finding longitude at sea drives much of 17th-century math.
