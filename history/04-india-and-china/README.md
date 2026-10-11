# 04 India and China

**Era:** about 800 BCE to 1400s CE · **Reading time:** about 22 minutes · **Previous:** [03 Ancient Greece](../03-ancient-greece/README.md) · **Next:** [05 The Islamic Golden Age](../05-islamic-golden-age/README.md)

## The Big Idea

India and China build mathematics around computation that works. China solves systems of equations on a counting board with negative numbers. India gives the world the place-value digits and zero that every computer still uses. Kerala astronomers find infinite series for pi and sine about 250 years before Europe.

## The World at That Time

India and China are large agricultural states with kings, tax offices, and armies. Officials need to measure fields, divide grain, share out labor on dikes and canals, convert currencies, and collect taxes. Both civilizations also need calendars. A calendar decides when to plant, when to hold a festival, and when a ruler looks competent. Calendars need astronomy, and astronomy needs heavy arithmetic and tables of angles.

In India, the oldest mathematics serves religion. Vedic priests build fire altars of exact shapes and areas. A wrong area makes the ritual fail. Rules for laying out altars with stakes and ropes fill the **Sulba Sutras** (rule books of the cord), about 800 to 500 BCE. Later Indian mathematics lives inside astronomy books written in Sanskrit verse, meant to be memorized.

In China, the classic texts are handbooks for officials. The *Nine Chapters on the Mathematical Art* collects 246 problems with answers and recipes, compiled roughly 200 BCE to 100 CE. Calculation happens on a **counting board**: a grid on a table where small bamboo or bone **rods** stand for digits. The board is the CPU. The text is the program listing.

```txt
  c. 800-500 BCE  Sulba Sutras: altar geometry and a value for root 2
  c. 100 BCE      Zhoubi Suanjing; Nine Chapters compiled (c. 200 BCE to 100 CE)
       263        Liu Hui writes his commentary on the Nine Chapters
  c. 400          Sunzi Suanjing: the remainder problem (dates uncertain)
  c. 480          Zu Chongzhi: pi between 3.1415926 and 3.1415927
       499        Aryabhata writes the Aryabhatiya
       628        Brahmagupta: rules for zero and negative numbers
       876        Gwalior inscription: a round zero, carved in stone
       1150       Bhaskara II: Lilavati and Bijaganita
  c. 1400         Madhava (Kerala): infinite series for pi and sine
```

## Key People

| Person | Dates | One-Line Contribution |
| --- | --- | --- |
| Baudhayana and other Sulba authors | about 800 BCE to 500 BCE | Write altar rules that state the right-triangle rule and approximate root 2. |
| Authors of the *Nine Chapters* | about 200 BCE to 100 CE | Solve linear systems on a counting board and use negative numbers. |
| [Liu Hui](../biographies/liu-hui.md) | c. 225 to c. 295 | Proves the recipes of the *Nine Chapters* in 263 and gets pi = 3.1416. |
| Sunzi | about 300s to 400s | Poses the remainder problem: the root of the Chinese remainder theorem. |
| Zu Chongzhi | 429 to 500 | Finds 355/113 for pi, correct to six decimals. |
| [Aryabhata](../biographies/aryabhata.md) | 476 to 550 | Writes the *Aryabhatiya* (499): place value, pi = 3.1416, sine tables. |
| [Brahmagupta](../biographies/brahmagupta.md) | 598 to c. 668 | States rules for zero and negative numbers (628). |
| Bhaskara II | 1114 to c. 1185 | Writes *Lilavati* and *Bijaganita*; solves hard whole-number equations. |
| Madhava of Sangamagrama | c. 1340 to c. 1425 | Founds the Kerala school; finds infinite series for pi, sine, and cosine. |

## Key Ideas

### Right Triangles and Square Roots: Cords and the Gougu

Both traditions know the right-triangle rule early, and both use it to build things.

The Sulba author Baudhayana states it in words: the diagonal rope of a rectangle makes as much area as the two sides make separately. That is $a^2 + b^2 = c^2$. Priests use it to double a square altar: the square on the diagonal of a square has twice its area. That makes the **square root of 2** (the side of a square of area 2) a practical question. The Sulba rule gives:

$$\sqrt{2} \approx 1 + \frac{1}{3} + \frac{1}{3 \cdot 4} - \frac{1}{3 \cdot 4 \cdot 34}$$

```txt
  1                      start with the side of the small square
  + 1/3       = 1.33333  add a third
  + 1/12      = 1.41667  add a fourth of that third
  - 1/408     = 1.41422  take away a 34th of that last piece
  total = 577/408        as one fraction
  577^2 = 332,929        check by squaring
  2 x 408^2 = 332,928    off by exactly 1
  error about 0.0000021  five correct decimals, from rope and stakes
```

The same fraction 577/408 appears in [Chapter 03](../03-ancient-greece/README.md) as one of the near misses for root 2. Nobody knows how the priests find it. It is too good to be luck.

In China, the *Zhoubi Suanjing* (Arithmetical Classic of the Gnomon, compiled about 100 BCE) calls the short side **gou** (base), the long side **gu** (upright), and the hypotenuse **xian** (string). It shows the rule with a picture.

<!-- diagram: type=historical-method ref=gougu caption="The Zhoubi Suanjing hypotenuse diagram: a 3-4-5 triangle on a 7 by 7 grid" -->
![A 7 by 7 grid. A tilted square touches each side, cutting off four right triangles with legs 3 and 4. Text: outer square 49, four triangles 24, inner square 49 minus 24 = 25, side 5. In general (a + b) squared minus 2ab = a squared + b squared = c squared.](img/gougu-diagram.svg)

The outer square is 7 by 7. A tilted square sits inside it and cuts off four right triangles, each with legs 3 and 4. Count grid cells instead of using algebra. The tilted square has area 25. Its side, the xian, is 5. Compare this with the Greek rearrangement in [Chapter 03](../03-ancient-greece/README.md): same figure, different culture, no contact. Good ideas get found more than once.

```txt
  outer square:      7 x 7 = 49                  (3 + 4) on each side
  one triangle:      3 x 4 / 2 = 6               half of a 3 by 4 rectangle
  four triangles:    4 x 6 = 24
  inner square:      49 - 24 = 25                what is left
  xian:              5                           5 x 5 = 25
  in general:        (a + b)^2 - 2ab = a^2 + b^2 = c^2
```

### The Counting Board: Rods, Negatives, and Elimination

Chinese digits are not written symbols at first. They are rods laid on a board.

<!-- diagram: type=numeral-system ref=counting-rods caption="Counting rod numerals 1 to 9 in vertical and horizontal forms, and 4,705 on a board with an empty square for zero" -->
![Rod numerals 1 to 9 in vertical form (upright rods, with a crossbar for 5) and horizontal form. Below, the number 4,705 on a board: thousands 4 horizontal, hundreds 7 vertical, tens an empty square, ones 5 vertical. Note: a written circle for zero appears by the 1200s.](img/counting-rods.svg)

One to five are that many rods. Six to nine use a crossbar worth five plus single rods. Each digit has two forms, vertical and horizontal. Places alternate between them: ones vertical, tens horizontal, hundreds vertical, and the pattern repeats. Two neighbors never blur into one long row of sticks. The board is **place value**: the same rods mean 7 or 700 depending on the column. An empty square is zero. Writers draw a small circle for it by the 1200s.

The board also holds **negative numbers**, values below zero, such as debts. Liu Hui writes in 263 that red rods count as positive and black rods as negative. The *Nine Chapters* gives rules to add and subtract them. Europe resists negative numbers into the 1600s and beyond. The Chinese clerk shrugs and picks up a black rod.

The best use of the board is chapter 8, **fangcheng** (rectangular arrays). Today this method is called **Gaussian elimination** after Carl Friedrich Gauss, who uses it about 1,800 years later. Problem 8.1, in modern words:

```txt
  3 bundles of top grain + 2 of medium + 1 of low = 39 dou
  2 bundles of top grain + 3 of medium + 1 of low = 34 dou
  1 bundle  of top grain + 2 of medium + 3 of low = 26 dou
  how much grain (in dou, a dry measure) is in one bundle of each grade?
```

The clerk lays the numbers on the board in columns. (Here they appear as rows.) To clear the first number of a lower row, multiply that row by the top-left number and subtract the top row as many times as needed. Every entry stays a whole number. Fractions appear only at the last step.

```txt
  3x + 2y +  z = 39          row 1
  2x + 3y +  z = 34          row 2
   x + 2y + 3z = 26          row 3

  0x + 5y +  z = 24          3 x row 2 - 2 x row 1
  0x + 4y + 8z = 39          3 x row 3 - 1 x row 1
  0x + 0y + 36z = 99         5 x (new row 3) - 4 x (new row 2)

  z = 99/36 = 11/4 = 2 3/4   divide
  5y = 24 - 11/4 = 85/4      put z into new row 2
  y = 17/4 = 4 1/4           divide by 5
  3x = 39 - 17/2 - 11/4      put y and z into row 1
  x = 37/4 = 9 1/4           divide by 3
```

Answer: top grade 9 1/4 dou, medium 4 1/4 dou, low 2 3/4 dou. Plug them back in to check: $3 \cdot 9.25 + 2 \cdot 4.25 + 2.75 = 39$.

A short book called the *Sunzi Suanjing* (Master Sun's Mathematical Manual, about 400 CE, dates uncertain) adds a different puzzle. A number leaves remainder 2 when counted by threes, 3 by fives, and 2 by sevens. What is it? Think of three cron jobs that run every 3, 5, and 7 minutes. Find the minute when they line up in a given way.

```txt
  70 leaves 1 by 3, 0 by 5, 0 by 7           70 = 2 x 5 x 7, and 69 = 23 x 3
  21 leaves 0 by 3, 1 by 5, 0 by 7           21 = 3 x 7, and 20 = 4 x 5
  15 leaves 0 by 3, 0 by 5, 1 by 7           15 = 3 x 5, and 14 = 2 x 7
  2 x 70 + 3 x 21 + 2 x 15 = 233             weight each by its wanted remainder
  233 - 2 x 105 = 23                         remove multiples of 3 x 5 x 7 = 105
  check: 23 = 7 x 3 + 2 = 4 x 5 + 3 = 3 x 7 + 2
```

Sunzi gives exactly this recipe and the answer 23. Qin Jiushao gives a general method in 1247. Today the result is the **Chinese remainder theorem**, and RSA decryption uses it to run about four times faster.

### Chasing Pi: Liu Hui, Zu Chongzhi, Aryabhata

Liu Hui, in his 263 commentary, uses the same idea as Archimedes: polygons inside a circle, doubling the sides. As far as anyone knows, he has never heard of Archimedes.

<!-- diagram: type=historical-method ref=archimedes-pi caption="Polygons inside and outside a circle of radius 1; Liu Hui uses the inside polygons, doubling the sides" -->
![A circle of radius 1 with inscribed and circumscribed hexagons and a dashed inscribed 12-gon, with a table of half-perimeters for 6 to 96 sides.](../03-ancient-greece/img/archimedes-pi.svg)

Liu Hui starts with the inside hexagon, like the picture, and works with areas instead of perimeters. A polygon with 192 sides gives him 3.14. He pushes on to 3,072 sides and gets 3.1416. All this is done with rods on a board, square root by square root.

About 480, **Zu Chongzhi** goes further. His book is lost. Later records say he proves $3.1415926 < \pi < 3.1415927$ and gives two fractions: 22/7 (the rough ratio) and 355/113 (the close ratio).

```txt
  22/7    = 3.1428571    error about 0.0013
  355/113 = 3.1415929    error about 0.00000027
  pi      = 3.1415927
  355/113: a 3-digit over 3-digit fraction, right to 6 decimals
```

No closer value of pi appears anywhere for about 900 years. Memory trick: write 113355, split it, and put the second half over the first.

In 499, in India, **Aryabhata** writes the *Aryabhatiya*, a short astronomy book in verse, at age 23. One verse reads, in plain words: add 4 to 100, multiply by 8, add 62,000. The result is the approximate circumference of a circle with diameter 20,000.

```txt
  (100 + 4) x 8 + 62,000 = 62,832      circumference
  62,832 / 20,000 = 3.1416             circumference divided by diameter
```

He calls it approximate, and he is right to. Aryabhata also tabulates **sines**. Draw an arc of a circle and its chord. The sine is half the chord of twice the arc: the height of one end of the arc above the radius through the other end. He calls it **jya**, the bowstring. Arab scholars write it as jiba. A Latin translator misreads it as jaib (a fold or pocket) and translates that as sinus. That is the word sine. A mistranslation in production, never rolled back.

### Zero and Place Value: Aryabhata to Bhaskara II

**Place value** means the position of a digit sets its worth: in 2,075 the 2 means two thousand. Place value needs a symbol for an empty position.

<!-- diagram: type=place-value ref=place-value-zero caption="2,075 versus 275: zero holds the hundreds place" -->
![Two rows of boxes labeled thousands, hundreds, tens, ones. Top row 2, 0, 7, 5 equals 2,075 (2 x 1,000 + 0 x 100 + 7 x 10 + 5 x 1). Bottom row empty, 2, 7, 5 equals 275. Without a mark for an empty place, the two look alike.](img/place-value-zero.svg)

Without a mark in the hundreds box, 2,075 and 275 look the same. A gap on a counting board is easy to see. A gap in handwriting is not. Indian astronomers write numbers with nine digit symbols and, by the 600s, a dot or small circle for an empty place. Aryabhata already computes square roots and cube roots by place-value steps. A stone inscription at Gwalior, dated 876, shows the number 270 with a round zero. It is one of the oldest zeros that can be dated beyond doubt.

```txt
  2 0 7 5     2 x 1,000 + 0 x 100 + 7 x 10 + 5 x 1 = 2,075
    2 7 5                 2 x 100 + 7 x 10 + 5 x 1 =   275
  the 0 changes nothing in the sum and everything in the meaning
```

In 628 **Brahmagupta** goes further. He treats zero as a number you compute with, not just a gap. He calls positive numbers **fortunes** and negative numbers **debts**, and gives rules.

<!-- diagram: type=number-line ref=brahmagupta-zero range=-5..5 caption="Brahmagupta's fortunes, debts, and rules for zero" -->
![A number line from -5 to 5, debts on the left, fortunes on the right, zero marked. An arrow jumps from -3 to 3: zero minus a debt is a fortune. Rules listed: a debt minus zero is a debt, a fortune minus zero is a fortune, zero times anything is zero, a debt times a debt is a fortune, and his slip: zero divided by zero is zero.](img/brahmagupta-zero.svg)

Most of his rules are exactly the modern ones. Zero minus a debt of 3 is a fortune of 3. A debt times a debt is a fortune. Zero times anything is zero. One rule is wrong: he says 0/0 = 0. Modern mathematics says 0/0 has no value at all. Any number c satisfies $c \times 0 = 0$. No single answer exists, and the operation is left undefined. On division of a nonzero number by zero he stays vague. Five centuries later Bhaskara II says the result is infinite. That is also not the modern view, but it is an honest attempt at a hard edge case. Programming languages still handle it case by case. Go, at run time, panics on integer division by zero, gives +Inf for a positive float divided by zero, and gives NaN (not a number) for float 0/0.

```txt
  (-4) - (-7) = 3       removing a debt of 7 from a debt of 4 leaves a fortune of 3
  (-3) x 0    = 0       zero times anything is zero
  0 - 5       = -5      zero minus a fortune is a debt
  (-2) x (-5) = 10      a debt times a debt is a fortune
  0 / 0                 Brahmagupta says 0; today: undefined
```

Brahmagupta also finds an identity that builds new whole-number solutions from old ones. Write $x^2 - N y^2 = 1$ for the equation. If $(a, b)$ and $(c, d)$ are solutions, then $(ac + Nbd,\ ad + bc)$ is another. Start with N = 2 and $3^2 - 2 \cdot 2^2 = 1$:

```txt
  (3, 2):    9 - 2 x 4 = 1                    a known solution
  combine (3, 2) with (3, 2):
  (3x3 + 2x2x2, 3x2 + 2x3) = (17, 12)         Brahmagupta's rule with N = 2
  check: 289 - 2 x 144 = 289 - 288 = 1
  combine (17, 12) with itself: (577, 408)    the Sulba fraction for root 2 again
```

**Bhaskara II** (1114 to c. 1185) heads the observatory at Ujjain. His *Lilavati* teaches arithmetic through word problems. By legend it is named for his daughter. His *Bijaganita* (seed arithmetic, that is algebra) uses the **chakravala** (cyclic) method to solve $x^2 - 61y^2 = 1$. The smallest answer is x = 1,766,319,049 and y = 226,153,980. Fermat poses the same equation as a challenge in 1657 ([Chapter 07](../07-scientific-revolution-and-calculus/README.md)), unaware that it is solved.

From India the digits travel west. About 773 an Indian astronomer visits the court of the caliph al-Mansur in Baghdad, and Brahmagupta's work is translated into Arabic. About 825 al-Khwarizmi writes a book on calculating with the Hindu numerals ([Chapter 05](../05-islamic-golden-age/README.md)). Latin translations reach Europe in the 1100s, and Fibonacci promotes the digits in 1202 ([Chapter 06](../06-medieval-and-renaissance-europe/README.md)). Europe calls them Arabic numerals. The Arabs call them Indian numerals. Both are right about the last hop.

### The Kerala School: Infinite Series

In Kerala, on the southwest coast of India, a line of teachers and students works from about 1350 to 1600. The founder is **Madhava of Sangamagrama** (c. 1340 to c. 1425). None of his own mathematical writing on series survives. Later Kerala texts, the *Tantrasangraha* of Nilakantha (1501) and the *Yuktibhasa* of Jyesthadeva (about 1530), credit him and give proofs.

An **infinite series** is a sum that never stops: add a term, then another, forever. The sum can still settle toward a fixed number, called its **limit**. Madhava finds:

$$\pi = 4\left(1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \frac{1}{9} - \cdots\right)$$

He also finds series for sine, cosine, and the arctangent. Europe meets these through James Gregory (1671), Isaac Newton (1669), and Gottfried Leibniz (1674). Europe calls the pi series the Leibniz series. Madhava is first by about 250 years.

<!-- diagram: type=series-convergence ref=madhava terms=1..16 caption="Partial sums of 4(1 - 1/3 + 1/5 - ...) zigzag toward pi" -->
![A plot of partial sums against number of terms 1 to 16. The points zigzag above and below a dashed line at pi = 3.14159: 4.0, 2.67, 3.47, 2.90, and onward, slowly closing in. After 16 terms the sum is 3.07915.](img/madhava-series.svg)

Each new term overshoots in the opposite direction. The sum zigzags around pi, and the zigzag shrinks slowly. After 16 terms the value is 3.07915, wrong in the second decimal. Getting 10 correct decimals this way takes billions of terms. A loop like that is a polling retry with no backoff: correct in the end, and slow.

Madhava sees the zigzag and fixes it. The true value sits roughly halfway between two neighboring partial sums. He adds an **end correction**: a small final term that estimates the rest of the infinite tail. If the last term used has denominator $p - 1$, add or subtract

$$\frac{p/2}{p^2 + 1}$$

with the sign of the next term that was left out.

```txt
  3 terms: 4 x (1 - 1/3 + 1/5)           = 3.46667   plain sum, error about 0.33
  last denominator 5, p = 6              the next term (-1/7) is negative
  correction: (6/2) / (36 + 1) = 3/37    = 0.08108
  4 x (1 - 1/3 + 1/5 - 3/37)             = 3.14234   error about 0.00075
```

Three terms plus one correction beat 1,300 plain terms. Madhava reaches pi to 11 decimals this way: 3.14159265359. The Kerala work stays in Kerala, written in Sanskrit and Malayalam. Europe builds calculus without it ([Chapter 07](../07-scientific-revolution-and-calculus/README.md)).

## What It Unlocked Next

* Indian digits with zero pass to Baghdad and become the working numerals of the Islamic world ([Chapter 05](../05-islamic-golden-age/README.md)).
* Al-Khwarizmi's books carry those digits to Europe in Latin, and Fibonacci spreads them to merchants ([Chapter 06](../06-medieval-and-renaissance-europe/README.md)).
* Aryabhata's sine table grows into the trigonometry of Islamic astronomers ([Chapter 05](../05-islamic-golden-age/README.md)).
* Negative numbers, standard in China and India, win acceptance in Europe only slowly, from the 1500s to the 1700s ([Chapter 07](../07-scientific-revolution-and-calculus/README.md)).
* Fangcheng elimination returns as Gaussian elimination and the matrix ([Chapter 08](../08-18th-and-19th-century-rigor/README.md)).
* Madhava's series anticipate the calculus and infinite series of Newton and Leibniz ([Chapter 07](../07-scientific-revolution-and-calculus/README.md)).
* The Chinese remainder theorem ends up inside RSA and modern cryptography ([Chapter 10](../10-modern-mathematics/README.md)).

## Connects To

* [Course 101](../../course/101/README.md): place value, negative numbers, and zero.
* [Arithmetic and number sense track](../../tracks/arithmetic-and-number-sense/README.md): why place value with zero makes arithmetic easy.
* [Algebra track](../../tracks/algebra/README.md): negative numbers and solving systems of equations.
* [Linear algebra track](../../tracks/linear-algebra/README.md): fangcheng is Gaussian elimination on a matrix.
* [Number theory track](../../tracks/number-theory/README.md): the Chinese remainder theorem and the equation $x^2 - Ny^2 = 1$.
* [Trigonometry track](../../tracks/trigonometry/README.md): the sine, from jya to sinus.
* [Calculus track](../../tracks/calculus/README.md): infinite series and their limits.
* [Story of an Idea: Zero](../story-of-an-idea/zero.md): the full journey of zero from gap to number.
* [Story of an Idea: Pi](../story-of-an-idea/pi.md): Liu Hui, Zu Chongzhi, Aryabhata, and Madhava in the long chase.
* [Story of an Idea: Infinity](../story-of-an-idea/infinity.md): infinite sums that settle on a finite value.
* Biographies: [Liu Hui](../biographies/liu-hui.md), [Aryabhata](../biographies/aryabhata.md), [Brahmagupta](../biographies/brahmagupta.md).

## Try It

1. Write the Sulba value $1 + \frac{1}{3} + \frac{1}{12} - \frac{1}{408}$ as one fraction. Square the top and bottom. How far is the top from twice the bottom?
2. Describe 3,608 in counting rods: which form (vertical or horizontal) does each place use, and what goes in each square?
3. Sunzi style: find the smallest number that leaves 1 when counted by threes, 2 by fives, and 3 by sevens. Use the 70, 21, 15 recipe.
4. Solve by the fangcheng method, keeping whole numbers until the end: 2x + y = 7 and x + 3y = 11.
5. Draw the gougu diagram for legs 6 and 8 on a 14 by 14 grid. Find the inner square and the hypotenuse.
6. Use Brahmagupta's rules: compute (-4) - (-7), 0 - 5, and (-2) x (-5).
7. Combine (17, 12) with (3, 2) by Brahmagupta's rule for $x^2 - 2y^2 = 1$. Check the result.
8. Compute $4(1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7})$, then apply Madhava's correction with p = 8. Compare both with pi = 3.14159.

<details>
<summary>Answers</summary>

1. 577/408: $577^2 = 332{,}929$ and $2 \times 408^2 = 332{,}928$, off by 1.
2. Thousands: 3 horizontal rods. Hundreds: 6 vertical (one crossbar on top, one upright rod). Tens: empty square. Ones: 8 vertical (crossbar, three upright rods).
3. 52: 1 x 70 + 2 x 21 + 3 x 15 = 157, and 157 - 105 = 52.
4. x = 2, y = 3: 2 x row 2 - row 1 gives 5y = 15, then 2x = 7 - 3.
5. 196 - 4 x 24 = 100, and the hypotenuse is 10.
6. 3, -5, 10: removing a debt is a gain, zero minus a fortune is a debt, a debt times a debt is a fortune.
7. (99, 70): (17 x 3 + 2 x 12 x 2, 17 x 2 + 12 x 3), and 9,801 - 2 x 4,900 = 1.
8. Plain 2.89524 (error about 0.25). The next term +1/9 is positive: add (8/2)/(64 + 1) = 4/65. Corrected 3.14139 (error about 0.0002).

</details>

## Code Corner

The program runs five methods from this chapter: the Sulba value for root 2, a brute-force search for the Sunzi remainder problem, fangcheng elimination of Nine Chapters problem 8.1 with whole numbers until the last step, the errors of the pi fractions of Aryabhata and Zu Chongzhi, and Madhava's series with and without his end correction. Full source: [code/main.go](code/main.go).

The fangcheng step, cross-multiplying like the clerk on the board:

```go
for i := 0; i < 3; i++ {
	for j := i + 1; j < 3; j++ {
		p, q := m[i][i], m[j][i]
		for k := 0; k < 4; k++ {
			m[j][k] = p*m[j][k] - q*m[i][k]
		}
	}
}
```

Madhava's sum and correction:

```go
s, sign := 0.0, 1.0
for k := 0; k < n; k++ {
	s += sign / float64(2*k+1)
	sign = -sign
}
p := float64(2 * n)
return 4 * s, 4 * (s + sign*(p/2)/(p*p+1))
```

After the loop, `sign` already holds the sign of the first term left out. That is exactly the sign Madhava gives the correction.

Run it:

```txt
cd code && go run main.go
```

Output:

```txt
Sulba Sutras: 1 + 1/3 + 1/(3*4) - 1/(3*4*34)
  1.4142157 vs root 2 = 1.4142136, error 2.1e-06

Sunzi: remainder 2 by 3, 3 by 5, 2 by 7
  smallest answer 23, then every 105 more: 128, 233

Nine Chapters 8.1: grain bundles (top, medium, low)
  board after elimination (whole numbers only):
       3    2    1 |   39
       0    5    1 |   24
       0    0   36 |   99
  top    = 37/4  dou = 9.25
  medium = 17/4  dou = 4.25
  low    = 11/4  dou = 2.75

Pi as a fraction: value and error
  Aryabhata 62832/20000  3.1416000  error +7.3e-06
  Zu Chongzhi 22/7       3.1428571  error +1.3e-03
  Zu Chongzhi 355/113    3.1415929  error +2.7e-07

Madhava: n terms, plain and with his end correction
  n= 1  plain 4.000000000 (error +8.6e-01)  corrected 3.200000000 (error +5.8e-02)
  n= 2  plain 2.666666667 (error -4.7e-01)  corrected 3.137254902 (error -4.3e-03)
  n= 5  plain 3.339682540 (error +2.0e-01)  corrected 3.141662738 (error +7.0e-05)
  n=10  plain 3.041839619 (error -1.0e-01)  corrected 3.141590242 (error -2.4e-06)
  n=16  plain 3.079153394 (error -6.2e-02)  corrected 3.141592419 (error -2.4e-07)
  n=50  plain 3.121594653 (error -2.0e-02)  corrected 3.141592653 (error -8.0e-10)
```

At 16 terms the plain sum is still wrong in the second decimal. The corrected sum is right to six. One line of insight beats a million loop iterations.

## Flashcards

Anki deck in [cards.tsv](cards.tsv) (tab-separated: front, back, tags).

## Go Deeper

* [MacTutor: The Indian Sulbasutras](https://mathshistory.st-andrews.ac.uk/HistTopics/Indian_sulbasutras/): altar geometry and the root 2 rule.
* [MacTutor: Nine Chapters on the Mathematical Art](https://mathshistory.st-andrews.ac.uk/HistTopics/Nine_chapters/): contents, fangcheng, and Liu Hui.
* [MacTutor: Chinese numerals](https://mathshistory.st-andrews.ac.uk/HistTopics/Chinese_numerals/): counting rods and the board.
* [MacTutor biography of Zu Chongzhi](https://mathshistory.st-andrews.ac.uk/Biographies/Zu_Chongzhi/): 355/113 and the lost book.
* [MacTutor: Indian numerals](https://mathshistory.st-andrews.ac.uk/HistTopics/Indian_numerals/): the road from Brahmi digits to zero.
* [MacTutor biography of Madhava](https://mathshistory.st-andrews.ac.uk/Biographies/Madhava/): the Kerala school and its series.
