# Arithmetic and Number Sense

**Track:** Arithmetic and Number Sense · **Span:** first counting to the real number line · **Main course level:** [101 Foundations](../../course/101/README.md)

## What This Field Studies

Arithmetic studies numbers and the four basic operations on them: add, subtract, multiply, divide. **Number sense** is the feel that sits on top of the rules: knowing that 49 × 21 is close to 1,000, that 0.1% of a million is 1,000, and that a fraction with a big denominator is a small number.

Every other track in this repository runs on arithmetic. Algebra is arithmetic with unknowns. Calculus is arithmetic with limits. Statistics is arithmetic on a pile of measurements.

## Why It Matters

Number sense is what lets you look at a dashboard and know a value is wrong before you can say why. A p99 latency of 40 s on a service that usually answers in 40 ms is a factor of 1,000, which is three orders of magnitude, which is a different failure mode than a factor of two. A disk at 92% of 2 TB has about 160 GB left. Fast, rough, correct estimates come from the ideas in this track.

## Concept Map

<!-- diagram: type=concept-map bands=beginner,intermediate,advanced nodes=place-value,add,multiply,negatives,order-of-operations,factors,fractions,exponents,ratios,decimals,bases,estimation,real-line caption="Arithmetic and number sense concepts with prerequisite arrows" -->
![Concept map of arithmetic in three bands. Beginner: counting and place value leads to add and subtract, which leads to negative numbers and to multiply and divide. Intermediate: multiply and divide leads to order of operations, factors and primes, and fractions. Fractions lead to ratios and to decimals and percents. Order of operations leads to exponents and roots. Advanced: exponents lead to number bases and to estimation and scientific notation, decimals lead to estimation, and both bases and estimation lead to the real number line. Fractions and the real number line are highlighted as milestones.](img/concept-map.svg)

Read the map top to bottom. An arrow from A to B means learn A before B. The two highlighted boxes are the milestones: fractions (where most adults first got lost) and the real number line (where every kind of number finally fits in one picture).

## Signature Diagram

<!-- diagram: type=area-model a=23 b=14 split=20+3,10+4 caption="Area model of 23 x 14 = 200 + 30 + 80 + 12 = 322" -->
![A 23 by 14 rectangle drawn to scale on a unit grid, split by place value into four parts: 20 by 10 equals 200, 3 by 10 equals 30, 20 by 4 equals 80, and 3 by 4 equals 12. The parts add to 322.](img/area-model.svg)

The **area model** is the single most useful picture in arithmetic. A product is the area of a rectangle. Split each side by place value, find the four smaller areas, and add them. Long multiplication on paper is this picture with the rectangles erased. The same picture returns in algebra as $(a + b)(c + d) = ac + ad + bc + bd$.

## The Concept Ladder

### Beginner

#### 1. Counting and Place Value

Our number system uses ten digits, and the position of a digit sets its value. In 3,047, the 3 means three thousands, the 0 means zero hundreds, the 4 means four tens, and the 7 means seven ones. Zero is a placeholder that keeps the other digits in the right column.

**Key idea:** $3047 = 3 \cdot 1000 + 0 \cdot 100 + 4 \cdot 10 + 7 \cdot 1$

<!-- diagram: type=place-value number=3047 columns=thousands,hundreds,tens,ones caption="3,047 split into place-value columns" -->
![Four place-value columns labeled thousands, hundreds, tens and ones, worth 1000, 100, 10 and 1. They hold the digits 3, 0, 4 and 7, with the 0 highlighted as a placeholder. Below each column the products read 3 times 1000 equals 3,000, 0 times 100 equals 0, 4 times 10 equals 40 and 7 times 1 equals 7, and the total reads 3,000 plus 0 plus 40 plus 7 equals 3,047](img/rung-01-place-value-3047.svg)

Read each column top to bottom: the column name sets the worth, and the digit says how many of that worth you have.

<!-- diagram: type=base-ten-blocks number=3047 caption="3,047 as cubes, flats, rods and units" -->
![Base-ten blocks for 3,047: three large cubes of 1000 small cubes each, an empty dashed space for zero hundreds, four rods of ten, and seven single unit cubes. The labels read 3 thousands equals 3,000, 0 hundreds equals 0, 4 tens equals 40 and 7 ones equals 7](img/rung-01-place-value-blocks-b.svg)

Compare the sizes: one cube is ten flats, one flat is ten rods, and one rod is ten units.

**In the course:** [101 Foundations](../../course/101/README.md)

#### 2. Add and Subtract

Addition combines two amounts. Subtraction finds the gap between them. On a number line, adding $b$ is a jump of $b$ to the right and subtracting $b$ is a jump of $b$ to the left. Carrying and borrowing are place value in action: ten ones become one ten.

**Key idea:** $a - b$ is the distance you jump from $b$ to reach $a$.

<!-- diagram: type=number-line range=0..15 jumps=5:+8,13:-8 gap=8..13 caption="Adding and subtracting as jumps on a number line" -->
![Three number lines from 0 to 15. On the first, an arrow jumps 8 to the right from 5 and lands on 13, showing 5 plus 8 equals 13. On the second, an arrow jumps 8 to the left from 13 and lands on 5, showing 13 minus 8 equals 5. On the third, a bracket marks the gap from 8 to 13 as 5](img/rung-02-add-subtract-jumps.svg)

Look at the second and third lines: subtraction is both a jump to the left and the size of the gap between two numbers.

<!-- diagram: type=base-ten-blocks sum=27+15 carry=1 caption="Ten ones become one ten when adding 27 and 15" -->
![Rods of ten and unit squares for 27 plus 15. 27 is 2 rods and 7 units, 15 is 1 rod and 5 units, and together they make 3 rods and 12 units. A dashed orange box groups 10 of the units, labeled ten ones make one ten, and the final row shows 4 rods, the last one orange, and 2 units, which is 42](img/rung-02-carry-27-15-b.svg)

Follow the dashed box: ten loose units trade for one orange rod, and that trade is the carry.

**In the course:** [101 Foundations](../../course/101/README.md)

#### 3. Multiply and Divide

Multiplication is repeated addition and also the area of a rectangle. Division asks how many equal groups fit, or how big each group is. Division leaves a remainder when the groups do not come out even, and the remainder is the seed of modular arithmetic (the math behind hash buckets and clock time).

**Key idea:** $17 = 3 \cdot 5 + 2$, so $17 \div 5 = 3$ remainder $2$.

<!-- diagram: type=groups total=17 size=5 groups=3 remainder=2 caption="17 dots in three groups of 5 with 2 left over" -->
![Seventeen dots arranged as three circled rows of 5 dots, labeled group 1, group 2 and group 3, plus a fourth row of 2 orange dots labeled left over. The heading reads 17 divided by 5 equals 3 remainder 2, and the footer reads 17 equals 3 times 5 plus 2](img/rung-03-groups-17.svg)

Count the full groups to get the quotient 3, then count the orange dots to get the remainder 2.

<!-- diagram: type=number-line range=0..17 jumps=5,5,5,2 caption="Three jumps of 5 and a short jump of 2 reach 17" -->
![A number line from 0 to 17 with three dark jumps of plus 5, from 0 to 5, 5 to 10 and 10 to 15, followed by a short orange jump of plus 2 from 15 to 17](img/rung-03-groups-17-b.svg)

The three full jumps are the quotient, and the short orange jump that does not reach another 5 is the remainder.

<!-- diagram: type=modular-clock modulus=5 n=17 buckets=0..4 caption="17 mod 5 as a five-hour clock and as hash buckets" -->
![Left: a clock with five positions 0 to 4, where 17 steps from 0 make 3 full laps plus 2 steps and land on the orange position 2. Right: five buckets labeled 0 to 4 holding the numbers 0 to 17 by remainder, so bucket 2 holds 2, 7, 12 and the orange 17](img/rung-03-groups-17-c.svg)

Both pictures throw away the full laps of 5 and keep only the remainder, which is exactly what a hash table does with a key.

**In the course:** [101 Foundations](../../course/101/README.md)

#### 4. Negative Numbers

Negative numbers extend the number line to the left of zero. They measure debt, temperature below freezing, or a clock offset behind the reference. Subtracting a negative is the same as adding a positive, and a negative times a negative is positive because it reverses a reversal.

**Key idea:** $a - (-b) = a + b$ and $(-a)(-b) = ab$

<!-- diagram: type=number-line range=-6..6 mirror=0 maps=4:-4;-3:-6:6 caption="Multiplying by -1 flips a number across zero" -->
![Two number lines from minus 6 to 6 with a dashed orange mirror line at 0. On the first, an arc flips 4 to minus 4, labeled 4 times minus 1 equals minus 4. On the second, minus 3 scales by 2 to minus 6, and then an orange arc flips minus 6 across zero to 6, showing minus 2 times minus 3 equals 6](img/rung-04-negatives-mirror.svg)

Watch the orange arcs: each factor of minus 1 is one flip across zero, and two flips put you back on the positive side.

<!-- diagram: type=number-line range=-5..6 gap=-3..2 jump=2:+3 caption="2 - (-3) = 5 as a distance and as a jump" -->
![Two number lines from minus 5 to 6 for 2 minus negative 3 equals 5. On the first, an orange bracket spans from minus 3 to 2 and reads 5 steps. On the second, an orange arrow jumps plus 3 from 2 to 5](img/rung-04-subtract-negative-b.svg)

Both lines land on 5: the gap from minus 3 to 2 is 5, and taking away a minus 3 is the same move as adding 3.

**In the course:** [101 Foundations](../../course/101/README.md)

### Intermediate

#### 5. Order of Operations

When an expression mixes operations, everyone agrees to do them in one order: parentheses, then exponents, then multiplication and division from left to right, then addition and subtraction from left to right. Without that agreement, $2 + 3 \times 4$ has two answers. It is the same reason a programming language defines operator precedence.

**Key idea:** $2 + 3 \times 4 = 2 + 12 = 14$, not $20$.

<!-- diagram: type=expression-tree expr="2+3*4" compare="(2+3)*4" caption="Two expression trees: 2 + 3 x 4 = 14 and (2 + 3) x 4 = 20" -->
![Two expression trees side by side. Left: a plus node at the top with children 2 and a times node, and the times node has children 3 and 4. The times node evaluates to 12 and the top to 14. Right, dashed and gray: a times node at the top with children plus and 4, and the plus node has children 2 and 3, giving 5 and then 20, a tree that only parentheses produce](img/rung-05-expression-tree.svg)

Evaluate each tree from the bottom up: the lower node runs first, and the order of operations decides which node sits lower.

<!-- diagram: type=step-list expr="2+3*4" order=P,E,MD,AS caption="The order of operations applied to 2 + 3 x 4" -->
![Left: a ladder of four boxes reading 1 parentheses, 2 exponents, 3 times and divide left to right, and 4 plus and minus left to right, with box 3 highlighted. Right: 2 plus 3 times 4 with 3 times 4 boxed in orange, an arrow to 2 plus 12, and an arrow to the answer 14](img/rung-05-order-steps-b.svg)

Match the orange box on the right to the highlighted rung on the left: multiplication sits higher on the ladder, so it goes first.

**In the course:** [101 Foundations](../../course/101/README.md)

#### 6. Factors and Primes

A **factor** of $n$ divides $n$ with no remainder. A **prime** has exactly two factors, 1 and itself. Every whole number above 1 breaks into primes in exactly one way, the way every chemical compound breaks into elements.

**Key idea:** $360 = 2^3 \cdot 3^2 \cdot 5$

<!-- diagram: type=factor-tree n=360 split=36x10 caption="Factor tree of 360 starting from 36 x 10" -->
![A factor tree for 360. 360 splits into 36 and 10. 36 splits into 6 and 6, and each 6 splits into 2 and 3. 10 splits into 2 and 5. The prime leaves 2, 3, 2, 3, 2 and 5 are orange circles, and the footer reads 360 equals 2 times 2 times 2 times 3 times 3 times 5, which is 2 cubed times 3 squared times 5](img/rung-06-factor-tree-360.svg)

Collect only the orange circles at the ends of the branches: those primes multiply back to 360.

<!-- diagram: type=factor-tree n=360 split=2x180 caption="Factor tree of 360 peeling off one prime at a time" -->
![A staircase factor tree for 360 that peels off one prime at a time: 360 is 2 times 180, 180 is 2 times 90, 90 is 2 times 45, 45 is 3 times 15, and 15 is 3 times 5. The orange prime leaves are 2, 2, 2, 3, 3 and 5, and the footer reads 360 equals 2 cubed times 3 squared times 5 again](img/rung-06-factor-tree-360-b.svg)

Compare the orange leaves with the first tree: the route differs, but the list of primes is identical, which is the uniqueness of prime factorization.

**In the course:** [101 Foundations](../../course/101/README.md) · **Go further:** [Number Theory track](../number-theory/README.md)

#### 7. Fractions

A fraction $\frac{a}{b}$ means cut a whole into $b$ equal parts and take $a$ of them. Two fractions are equal when they name the same point on the number line, which is why you can multiply top and bottom by the same number. To add fractions, first cut both into the same size of piece (a common denominator).

**Key idea:** $\frac{a}{b} + \frac{c}{d} = \frac{ad + bc}{bd}$ and $\frac{a}{b} \cdot \frac{c}{d} = \frac{ac}{bd}$

<!-- diagram: type=fraction-bars sum=3/4+5/6 common=12 caption="Adding 3/4 and 5/6 by recutting both bars into twelfths" -->
![Fraction bars of equal length. A bar cut into 4 parts with 3 shaded is the same length as a bar cut into 12 parts with 9 shaded. A bar cut into 6 parts with 5 shaded matches a bar of 12 parts with 10 shaded. The sum, 19 twelfths, fills one whole bar of 12 twelfths and 7 twelfths of a second bar. The footer reads 3/4 plus 5/6 equals 9/12 plus 10/12 equals 19/12 equals 1 and 7/12, and checks (3 times 6 plus 4 times 5) over (4 times 6) equals 38/24 equals 19/12](img/rung-07-fraction-bars.svg)

Compare each bar with the twelfths bar under it: the shaded length stays the same, only the cuts get finer, and then the pieces can be counted together.

<!-- diagram: type=number-line-stack range=0..1 denominators=2,3,4,6,8 marks=1/2,2/3 caption="Equivalent fractions line up at the same point" -->
![Five number lines from 0 to 1, cut into halves, thirds, fourths, sixths and eighths. An orange dashed vertical line passes through 1/2, 2/4, 3/6 and 4/8, and a gray dashed line passes through 2/3 and 4/6](img/rung-07-equivalent-fractions-b.svg)

Follow each dashed line straight down: every fraction it touches is the same number with a different size of piece.

<!-- diagram: type=area-model a=2/3 b=3/4 grid=3x4 caption="2/3 x 3/4 as 6 of 12 cells in a unit square" -->
![A unit square cut into 3 columns and 4 rows, 12 cells in all. The first 2 columns are shaded to show 2/3 of the width, and the bottom 3 rows mark 3/4 of the height. Their overlap, outlined in orange, holds 6 of the 12 cells, so 2/3 times 3/4 equals 6/12 equals 1/2](img/rung-07-multiply-area-c.svg)

Count the cells inside the orange box and the cells in the whole square: 6 over 12 is the product.

**In the course:** [101 Foundations](../../course/101/README.md)

#### 8. Decimals and Percents

A decimal is a fraction whose denominator is a power of ten: $0.375 = \frac{375}{1000}$. A percent is a fraction out of 100. Every fraction becomes a decimal that either stops or repeats forever, because long division only has finitely many possible remainders.

**Key idea:** $\frac{1}{8} = 0.125 = 12.5\%$ and $\frac{1}{3} = 0.333\ldots$

<!-- diagram: type=hundred-grid shaded=12.5 caption="1/8 shown as 12.5 squares of a 10 by 10 grid" -->
![A 10 by 10 grid of 100 squares with 12 full squares shaded and one more square half filled in orange, 12.5 squares in all. The notes read 1/8 of 100 equals 12.5 squares, which is 12.5 out of 100, equals 12.5 percent, equals 0.125](img/rung-08-percent-grid.svg)

Count the shaded squares: percent means out of 100, and 1/8 of the grid is 12 and a half squares.

<!-- diagram: type=number-line-zoom target=0.125 levels=0..1,0.1..0.2,0.12..0.13 caption="Zooming into 0.125 one decimal place at a time" -->
![Three number lines stacked as a zoom. The first runs from 0 to 1 in tenths with the interval 0.1 to 0.2 highlighted. Dashed lines expand it into the second line, 0.10 to 0.20 in hundredths, with 0.12 to 0.13 highlighted. That expands into the third line, 0.120 to 0.130 in thousandths, where an orange dot marks 0.125 equals 125/1000](img/rung-08-decimal-zoom-b.svg)

Each decimal digit picks one of ten slots on the line above, so the digits 1, 2 and 5 are three zoom steps.

<!-- diagram: type=cycle n=1/7 remainders=1,3,2,6,4,5 digits=1,4,2,8,5,7 caption="Long division remainders of 1/7 run in a cycle" -->
![A ring of six circles holding the long-division remainders of 1 divided by 7 in order: 1, 3, 2, 6, 4, 5, and back to 1. Orange arrows between them carry the digits written at each step: 1, 4, 2, 8, 5, 7. The notes read 1/7 equals 0.142857 repeating, only remainders 1 to 6 exist so one must come back, and for 1/3 the remainder is 1 every time, so 1/3 equals 0.333 repeating](img/rung-08-remainder-cycle-c.svg)

Walk around the ring once and read the orange digits: after six steps the remainder returns to 1, so the same six digits start over.

**In the course:** [101 Foundations](../../course/101/README.md)

#### 9. Ratios and Proportion

A ratio compares two amounts: 3 errors per 1,000 requests. A proportion says two ratios are equal, which lets you scale: if 3 errors happen per 1,000 requests, then 30 happen per 10,000. Unit rates (per second, per request, per GB) are ratios with a denominator of 1.

**Key idea:** $\frac{a}{b} = \frac{c}{d} \iff ad = bc$

<!-- diagram: type=double-number-line top=errors:0..30:3 bottom=requests:0..10000:1000 marks=1,10 caption="Errors and requests stay in step on a double number line" -->
![A double number line. The top line counts errors 0, 3, 6 and so on up to 30. The bottom line counts requests 0, 1,000, 2,000 and so on up to 10,000, with each tick aligned. Orange dashed links join 3 errors to 1,000 requests and 30 errors to 10,000 requests, and an arc labeled times 10 on both lines spans from the first link to the second](img/rung-09-double-number-line.svg)

Read straight down from any tick: the pair above and below always has the same ratio of 3 to 1,000.

<!-- diagram: type=cross-multiply a=3 b=1000 c=30 d=10000 caption="Cross products of 3/1000 and 30/10000 are both 30,000" -->
![The fractions 3 over 1,000 and 30 over 10,000 side by side with two crossing arrows. The orange arrow links 3 with 10,000 and reads 3 times 10,000 equals 30,000. The gray dashed arrow links 1,000 with 30 and reads 1,000 times 30 equals 30,000. The footer reads a/b equals c/d exactly when ad equals bc](img/rung-09-cross-multiply-b.svg)

Follow each arrow and multiply its two ends: when both products match, the two ratios are equal.

**In the course:** [101 Foundations](../../course/101/README.md)

#### 10. Exponents and Roots

An exponent counts repeated multiplication: $2^{10} = 1024$. A root undoes it: $\sqrt{49} = 7$ because $7^2 = 49$. Exponents explain why doubling grows so fast and why $2^{10} \approx 10^3$ makes KiB and KB almost the same.

**Key idea:** $a^m \cdot a^n = a^{m+n}$ and $\sqrt[n]{a} = a^{1/n}$

<!-- diagram: type=square-numbers n=1..7 highlight=49 caption="Square numbers as areas and the square root as the side" -->
![A row of squares built from unit cells with sides 1 to 6, labeled 1 squared equals 1, 2 squared equals 4, up to 6 squared equals 36. A larger orange-outlined square of 7 by 7 cells is labeled side 7, area 7 squared equals 49, and square root of 49 equals 7. Notes read squaring takes side to area and square root takes area to side](img/rung-10-squares-roots.svg)

Look at the big square from both ends: squaring counts its cells, and the square root reads off its side.

<!-- diagram: type=bar-chart values=2^0..2^10 ref=1000 caption="Powers of two from 1 to 1024 against a line at 1000" -->
![A bar chart of the powers of two from 2 to the 0, which is 1, up to 2 to the 10, which is 1024, each bar twice the height of the one before. The 1024 bar is orange and rises just above a dashed reference line at 1000, which is 10 cubed. The note reads 2 to the 10 equals 1024, about 10 cubed, so 1 KiB is about 1 KB](img/rung-10-doubling-b.svg)

Notice how the first bars barely leave the floor and the last one towers over them: that is what repeated doubling looks like.

<!-- diagram: type=factor-boxes a=2 m=3 n=2 caption="2^3 x 2^2 = 2^5 shown as boxes of factors" -->
![Three boxes each holding a 2, labeled 2 cubed equals 8, times two boxes of 2, labeled 2 squared equals 4, equal five orange boxes of 2, labeled 2 to the 5 equals 32. The notes read 3 factors plus 2 factors equals 5 factors, so a to the m times a to the n equals a to the m plus n, and roots run it backward: 49 to the one half equals 7 and 8 to the one third equals 2](img/rung-10-exponent-factors-c.svg)

Count the boxes on each side of the equals sign: multiplying powers just joins two rows of factors into one longer row.

**In the course:** [101 Foundations](../../course/101/README.md) and [301 Algebra II, Trig and Precalculus](../../course/301/README.md)

### Advanced

#### 11. Estimation and Scientific Notation

Scientific notation writes a number as a value between 1 and 10 times a power of ten: $86{,}400 = 8.64 \times 10^4$. Multiply the front parts, add the exponents, and you can estimate almost anything in your head. This is **Fermi estimation**, and it is the core of capacity planning.

**Key idea:** $(a \times 10^m)(b \times 10^n) = ab \times 10^{m+n}$

<!-- diagram: type=log-axis range=10^0..10^8 marks=1,60,3600,86400,604800,3.16e7 caption="Common time spans placed on a log scale of seconds" -->
![A logarithmic axis of seconds from 10 to the 0 up to 10 to the 8, with equal spacing for each factor of 10. Marked points: 1 second, 1 minute at 60 seconds, 1 hour at 3,600 seconds, 1 day at 8.64 times 10 to the 4 seconds in orange, 1 week at 604,800 seconds, and 1 year at about 3.16 times 10 to the 7 seconds](img/rung-11-log-scale-time.svg)

Read the exponent under each point: the exponent is the order of magnitude, and a day sits between 10 to the 4 and 10 to the 5.

<!-- diagram: type=flow inputs="5e2,8.64e4" result=4.32e7 caption="500 requests per second times 86,400 seconds per day" -->
![A flow diagram for 500 requests per second times 86,400 seconds per day. 500 is written as 5 times 10 squared and 86,400 as 8.64 times 10 to the 4. Arrows send the front parts to a box reading 5 times 8.64 equals 43.2 and the exponents to an orange box reading 2 plus 4 equals 6. The result reads 43.2 times 10 to the 6 equals 4.32 times 10 to the 7, about 43 million requests per day](img/rung-11-fermi-estimate-b.svg)

Split the work in two: multiply the front numbers, add the exponents, then tidy the front back to between 1 and 10.

**In the course:** [101 Foundations](../../course/101/README.md)

#### 12. Number Bases

Base ten is a choice, not a law. Base 2 (binary) uses only 0 and 1, and each place is worth a power of 2. Base 16 (hex) packs four binary digits into one symbol, which is why a byte is two hex digits and why IPv6 addresses and memory dumps look the way they do.

**Key idea:** $101101_2 = 32 + 8 + 4 + 1 = 45$ and $\text{FF}_{16} = 255$

<!-- diagram: type=place-value base=2 digits=101101 value=45 caption="Binary place values for 101101 = 45" -->
![Six binary place-value boxes worth 32, 16, 8, 4, 2 and 1, which are 2 to the 5 down to 2 to the 0. They hold the bits 1, 0, 1, 1, 0, 1, and the boxes with a 1 are orange. Under them the values 32, 8, 4 and 1 add to 45](img/rung-12-binary-45.svg)

Add only the place values under the orange boxes: a 1 bit switches its place on and a 0 bit switches it off.

<!-- diagram: type=bit-groups values=45,255 groups=4 caption="Bytes split into two nibbles that become two hex digits" -->
![Two bytes split into groups of four bits. 45 is 0010 1101, where 0010 is the hex digit 2 and 1101 is D, which is 13, so 45 is 0x2D because 2 times 16 plus 13 equals 45. 255 is 1111 1111, where each group is F, which is 15, so 255 is 0xFF because 15 times 16 plus 15 equals 255](img/rung-12-hex-nibbles-b.svg)

Cover one group of four bits with your hand: each group becomes one orange hex digit worth 0 to 15.

**In the course:** [101 Foundations](../../course/101/README.md)

#### 13. The Real Number Line

The **rational numbers** are all fractions. They are dense (between any two there is another), yet they still leave holes: $\sqrt{2}$ and $\pi$ are not fractions. Filling every hole gives the **real numbers**, one point for every possible length. This is the stage where arithmetic hands off to algebra and analysis.

**Key idea:** $\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$

<!-- diagram: type=nested-sets sets=N,Z,Q,R caption="Natural numbers inside integers inside rationals inside reals" -->
![Four nested rounded boxes. The innermost, natural numbers, holds 1, 2, 3 and 47. The integers box around it adds 0, minus 1 and minus 7. The rational numbers box adds 1/2, minus 3/4, 0.125 and 0.333 repeating. The outer real numbers box adds the square root of 2, pi and minus the square root of 5](img/rung-13-nested-sets.svg)

Move outward one box at a time: each larger set keeps every number from the box inside and adds new kinds.

<!-- diagram: type=number-line range=-0.4..2.3 construct=unit-square-diagonal mark=sqrt2 caption="The diagonal of a unit square swung onto the number line" -->
![A unit square with sides of length 1 sits on a number line between 0 and 1. Its orange diagonal has length square root of 2. A dashed orange arc centered at 0 swings the diagonal down onto the number line, landing at about 1.41421, between the ticks 1.4 and 1.5](img/rung-13-sqrt2-diagonal-b.svg)

Follow the dashed arc: it carries a length you can draw onto a point that no fraction names.

**In the course:** [101 Foundations](../../course/101/README.md) · **Go further:** [Real Analysis track](../real-analysis/README.md)

## Big Theorems You Should Know

* **Commutative, associative and distributive laws:** $a + b = b + a$, $(ab)c = a(bc)$, and $a(b + c) = ab + ac$. The area model is a picture of the distributive law.
* **Division algorithm:** for whole numbers $a$ and $b > 0$, there is exactly one pair $q, r$ with $a = qb + r$ and $0 \le r < b$.
* **Fundamental theorem of arithmetic:** every whole number above 1 is a product of primes in exactly one way, up to order.
* **Decimal expansions:** a number is rational exactly when its decimal expansion stops or repeats.
* **$\sqrt{2}$ is irrational:** no fraction squares to 2. The Pythagoreans knew this about 2,500 years ago.
* **Density:** between any two different real numbers there is a rational number.

## Open Problems and Fun Facts

* **$0.999\ldots = 1$:** the two strings name the same point on the number line. If they were different, some number would fit between them, and none does.
* **Cyclic numbers:** $\frac{1}{7} = 0.\overline{142857}$, and $2 \times 142857 = 285714$ uses the same digits rotated.
* **A year is about $\pi \times 10^7$ seconds:** $365 \times 86{,}400 = 31{,}536{,}000 \approx 3.15 \times 10^7$. A handy rule for uptime math.
* **Benford's law:** in many real data sets (populations, invoice totals, file sizes) the leading digit is 1 about 30% of the time, not 11%. Auditors use this to spot invented numbers.
* **Open problem:** nobody knows whether $\pi$ is **normal**, that is, whether every digit (and every block of digits) appears equally often in its decimal expansion. Trillions of digits look normal, but no proof exists.

## Starter Problem Set

1. Compute $3 + 4 \times (6 - 2)^2 \div 8$.
2. Add $\frac{3}{4} + \frac{5}{6}$ and write the result as a mixed number.
3. A volume of 250 GB holds 80 GB of data. What percent is used?
4. Write 45 in binary.
5. Estimate the number of seconds in a year using scientific notation, then compare with the exact value.

<details>
<summary>Answers</summary>

1. $11$. Parentheses: $4$. Exponent: $16$. Then $4 \times 16 = 64$, $64 \div 8 = 8$, and $3 + 8 = 11$.
2. $\frac{19}{12} = 1\frac{7}{12}$. Common denominator 12: $\frac{9}{12} + \frac{10}{12} = \frac{19}{12}$.
3. $32\%$, because $\frac{80}{250} = 0.32$.
4. $101101_2$, because $45 = 32 + 8 + 4 + 1$.
5. $(8.64 \times 10^4)(3.65 \times 10^2) \approx 31.5 \times 10^6 \approx 3.2 \times 10^7$. The exact value for 365 days is $31{,}536{,}000$.

</details>

## Go Deeper

* [Math Is Fun: Numbers](https://www.mathsisfun.com/numbers/index.html): short, friendly pages with pictures for every topic on this ladder.
* [Khan Academy: Arithmetic](https://www.khanacademy.org/math/arithmetic): videos and practice for whole numbers, fractions and decimals.
* [OpenStax Prealgebra 2e](https://openstax.org/details/books/prealgebra-2e): a free, complete textbook with worked examples.
* [Better Explained](https://betterexplained.com/): intuition-first articles on exponents, percentages and number systems.
* [MacTutor: Fibonacci](https://mathshistory.st-andrews.ac.uk/Biographies/Fibonacci/): the merchant who brought place-value numerals to Europe.

## Related Tracks and Workshops

* Next: [Algebra track](../algebra/README.md) and [Number Theory track](../number-theory/README.md).
* Applied: [Exponential Growth in Interest, Epidemics and Load](../../workshops/exponential-growth-in-interest-epidemics-and-load/README.md).
