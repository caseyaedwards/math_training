# 05 The Islamic Golden Age

**Era:** about 750 to 1450 · **Reading time:** about 18 minutes · **Previous:** [04 India and China](../04-india-and-china/README.md) · **Next:** [06 Medieval and Renaissance Europe](../06-medieval-and-renaissance-europe/README.md)

## The Big Idea

Scholars in Baghdad, Cairo, Persia, and Central Asia collect Greek geometry and Indian numbers in one place and fuse them. Out of that merger comes **algebra**: a set of general recipes for finding an unknown number, each recipe backed by a geometric proof. They also turn trigonometry into a subject of its own and push decimal arithmetic far enough to compute pi to 16 places.

## The World at That Time

In 750 the Abbasid family takes the caliphate. In 762 they found Baghdad on the Tigris, close to where the Babylonian scribes of [Chapter 02](../02-mesopotamia-and-egypt/README.md) once worked. The city sits on the trade roads between India, Persia, Byzantium, and the Mediterranean. Paper arrives from China around the same time and is far cheaper than papyrus or parchment. Cheap paper means more books, and more books mean more copies of old ideas.

Caliphs and wealthy families pay for the **translation movement**: a long project, from about 750 to 1000, to render Greek, Persian, Syriac, and Sanskrit works into Arabic. Euclid, Ptolemy, Archimedes, and Apollonius arrive from Greek. Indian astronomy arrives too: a Sanskrit astronomical work, probably based on [Brahmagupta](../biographies/brahmagupta.md), is translated in the 770s under the name *Sindhind*. The center of this effort is the **House of Wisdom** (Bayt al-Hikma) in Baghdad. It likely begins as a palace library under the early Abbasids and flourishes under Caliph al-Mamun, who rules from 813 to 833. Historians still debate how formal an institution it is. The books are real either way.

Daily life generates steady demand for math:

* **Inheritance law:** the Quran fixes the shares heirs receive. Splitting an estate correctly is a fraction problem with legal weight.
* **Trade:** merchants convert currencies, weights, and measures across an empire that runs from Spain to Central Asia.
* **Prayer:** Muslims pray five times a day at times set by the position of the sun. They face the **qibla**, the direction of Mecca. Both depend on the geometry of a round Earth and a moving sky.
* **Calendars:** the Islamic calendar is lunar. Each month starts when the new crescent Moon is first seen. Predicting that sighting is a hard astronomy problem.

Here is an inheritance split of the kind al-Khwarizmi works through at length. A man dies and leaves a wife, one son, and one daughter. With children present, the wife receives one eighth. The rest goes to the children, a son taking twice a daughter's share.

```txt
  estate                       = 240 dinars
  wife: 1/8 of 240             =  30      fixed share when there are children
  left for children: 240 - 30  = 210
  son : daughter               =  2 : 1   son takes twice the daughter's share
  3 equal parts: 210 / 3       =  70      2 + 1 = 3 parts
  son: 2 x 70                  = 140
  daughter: 1 x 70             =  70
  check: 30 + 140 + 70         = 240      nothing is left over
```

About half of al-Khwarizmi's algebra book is problems like this one. The first textbook of algebra is, in large part, a probate manual.

## Key People

| Person | Dates | One-Line Contribution |
|---|---|---|
| Translators of the House of Wisdom | about 750 to 1000 | Render Euclid, Ptolemy, and Indian astronomy into Arabic |
| [Muhammad ibn Musa al-Khwarizmi](../biographies/al-khwarizmi.md) | c. 780 to c. 850 | Writes the first book of algebra (c. 820) and a book on Hindu numerals (c. 825) |
| Thabit ibn Qurra | c. 826 to 901 | Translates Greek works, proves al-Khwarizmi's recipes from Euclid, finds a rule for amicable numbers |
| Al-Karaji | c. 953 to c. 1029 | Builds an algebra of polynomials, a table of binomial coefficients, and induction-like proofs |
| Ibn al-Haytham | c. 965 to c. 1040 | Writes the *Book of Optics* in Cairo: vision is light entering the eye, tested by experiment |
| [Omar Khayyam](../biographies/omar-khayyam.md) | 1048 to 1131 | Solves cubic equations with intersecting conic sections (c. 1070) and reforms the calendar (1079) |
| Nasir al-Din al-Tusi | 1201 to 1274 | Treats trigonometry as its own subject, independent of astronomy |
| Ulugh Beg | 1394 to 1449 | Ruler of Samarkand who builds a great observatory and star catalogue |
| Jamshid al-Kashi | c. 1380 to 1429 | Computes pi to 16 decimal places (1424) and teaches decimal fractions |

## Key Ideas

### Restoring and Balancing

Around 820, al-Khwarizmi writes *The Compendious Book on Calculation by al-jabr and al-muqabala*. The two Arabic words in the title name two moves:

* **Al-jabr** means **restoring**. A subtracted amount on one side is restored by adding it to both sides. The word also names the setting of a broken bone. Medieval Spain has barbers who advertise as *algebristas*, bone-setters.
* **Al-muqabala** means **balancing**. Equal amounts on both sides are cancelled.

These are the same moves you use today when you "move a term across the equals sign". The difference is the notation: there is none. Al-Khwarizmi writes everything in words. A square is *mal* (wealth), the unknown is *shay* (thing), and a plain number is *dirham*, a coin. This style is called **rhetorical algebra**: algebra in sentences. Symbols arrive centuries later, in [Chapter 06](../06-medieval-and-renaissance-europe/README.md).

He accepts only positive numbers as answers and as coefficients. Without negatives, $x^2 + 10x = 39$ and $x^2 + 21 = 10x$ are different kinds of problem, not the same one rearranged. That forces him to sort equations into six **standard forms** and give a recipe for each:

```txt
  form   in words                          modern
  1      squares equal roots               a x^2 = b x
  2      squares equal numbers             a x^2 = c
  3      roots equal numbers               b x   = c
  4      squares and roots equal numbers   x^2 + b x = c
  5      squares and numbers equal roots   x^2 + c   = b x
  6      roots and numbers equal squares   b x + c   = x^2
```

Restoring and balancing turn any messy problem into one of the six. Then the matching recipe finishes it. Software people know this pattern: normalize the input, then dispatch on its shape.

```txt
  x^2 = 40x - 4x^2          a problem with a subtraction in it
  x^2 + 4x^2 = 40x          al-jabr: restore 4x^2 to both sides
  5x^2 = 40x                collect the squares: form 1
  x = 8                     divide both sides by 5x (x is positive)
  check: 64 = 320 - 256     both sides equal 64
```

Form 4 is the famous one. His own example is a square plus ten roots equal to thirty-nine. The recipe: halve the roots, square the half, add it to the number, take the square root, subtract the half. He backs the recipe with a picture.

<!-- diagram: type=historical-method ref=completing-the-square caption="Al-Khwarizmi solves x^2 + 10x = 39 by completing a square" -->
![Al-Khwarizmi solves x squared plus 10x equals 39: left, an L-shape made of an x by x square and two 5 by x rectangles, with a dashed 5 by 5 corner marked missing; right, the corner filled with area 5 x 5 = 25, making a full square of area 64; caption 39 + 25 = 64, the side is 8, the side is x + 5, and x = 3](img/completing-the-square.svg)

On the left, the square $x^2$ sits in the corner. The ten roots ($10x$) are split into two rectangles, each 5 by $x$, attached to two sides. Together they make an L-shape with area 39. One 5 by 5 corner is missing. On the right, that corner is filled in with area 25. Now the shape is a true square of area $39 + 25 = 64$. Its side is 8. The side is also $x + 5$. That gives $x = 3$.

```txt
  x^2 + 10x = 39             a square plus ten roots equal thirty-nine
  10 / 2    = 5              halve the roots
  5 x 5     = 25             square the half: the missing corner
  39 + 25   = 64             add it: area of the full square
  sqrt(64)  = 8              side of the full square
  8 - 5     = 3              the side is x + 5, subtract the half
  check: 9 + 30 = 39         3^2 + 10 x 3
```

The recipe ignores the second solution, $x = -13$. A side length cannot be negative, and for al-Khwarizmi a number that is not a length or a count is not a number at all.

### Two Pictures of One Square

Al-Khwarizmi gives two figures for form 4. The one above is his second. His first splits the ten roots into four strips instead of two.

<!-- diagram: type=historical-method ref=khwarizmi-four-strips caption="Al-Khwarizmi's first figure: four strips of 2.5x and four corners of 6.25" -->
![Al-Khwarizmi's first figure for x squared plus 10x equals 39: a central x by x square with a 2.5 by x strip on each of its four sides, forming a cross; four corner squares of 2.5 by 2.5, each area 6.25, complete a large square; side notes: cross shape x^2 + 4 strips of 2.5x = 39, corners 4 x 2.5 x 2.5 = 25, whole square 39 + 25 = 64, side 8 = 2.5 + x + 2.5, x = 8 - 5 = 3](img/khwarizmi-four-strips.svg)

The square $x^2$ sits in the middle. Each of its four sides gets a strip 2.5 wide, because $10 / 4 = 2.5$. The result is a plus-shaped cross of area 39. Four small corner squares, each $2.5 \times 2.5 = 6.25$, are missing. Together they add $4 \times 6.25 = 25$. The completed square has area 64 and side 8. The side runs 2.5, then $x$, then 2.5. Subtract the two margins and $x = 3$.

Both pictures add the same 25 and land on the same answer. Two proofs of one fact is not waste. It is a cross-check, like computing a checksum two different ways.

Form 5 has a twist. In $x^2 + 21 = 10x$ two positive answers exist, and al-Khwarizmi gives both:

```txt
  x^2 + 21 = 10x             squares and numbers equal roots: form 5
  10 / 2   = 5               halve the roots
  5 x 5    = 25              square the half
  25 - 21  = 4               subtract the number
  sqrt(4)  = 2               take the root
  5 - 2    = 3               one answer: subtract the root from the half
  5 + 2    = 7               another answer: add the root to the half
  check: 9 + 21 = 30 = 10 x 3 and 49 + 21 = 70 = 10 x 7
```

He also warns that when the squared half is smaller than the number, the problem is impossible. In modern words, the roots are not real. He notices the wall but does not climb it. Europe climbs it in [Chapter 06](../06-medieval-and-renaissance-europe/README.md).

A second strand runs through the same years: numbers themselves. Al-Khwarizmi writes a book on the Indian place-value digits, including zero, around 825. The Arabic original is lost. A Latin translation survives and opens with *Dixit Algoritmi*, "al-Khwarizmi says". His name becomes the word **algorithm**: a fixed list of steps that solves a class of problems. In 952, al-Uqlidisi of Damascus adapts the digits for pen and paper (the Indian method used a dust board that erases as you go) and already uses decimal fractions.

Al-Karaji, working in Baghdad around 1000, pushes algebra past geometry. He treats $x$, $x^2$, $x^3$, and higher powers as objects to add and multiply, with no picture behind them. He builds a table of the numbers that appear when you expand $(a + b)^n$, now called **binomial coefficients**, and reasons from one row to the next. That step-by-step argument is an early form of **proof by induction**: show a pattern holds at the start, show each case passes it to the next, and it holds for all.

```txt
  row 1:        1   1               (a+b)^1 = a + b
  row 2:      1   2   1             (a+b)^2 = a^2 + 2ab + b^2
  row 3:    1   3   3   1           each inner entry = sum of the two above
  row 4:  1   4   6   4   1         (a+b)^4 has these five coefficients
```

### Cubics Where Two Curves Cross

A **cubic equation** has $x^3$ in it. No recipe of halving and squaring solves it. Around 1070, Omar Khayyam sorts cubics into types, as al-Khwarizmi sorted quadratics, and solves each type with geometry. His tool is the **conic section**: the curves you get by slicing a cone, which include the circle and the **parabola**, the U-shaped curve a thrown stone traces. He finds the answer where two such curves cross.

<!-- diagram: type=historical-method ref=khayyam-cubic caption="Omar Khayyam solves x^3 + 4x = 16 where a parabola meets a circle" -->
![Omar Khayyam solves x cubed plus 4x equals 16: axes from 0 to 4; the parabola y = x^2/2 rises from the origin; the half-circle with center (2, 0) and radius 2 runs from 0 to 4 on the x-axis; they cross at the point (2, 2), with a dashed line down to x = 2; side notes: Khayyam 4 = a^2 and a = 2, parabola x^2 = a y that is y = x^2/2, circle on diameter 16/4 = 4, they cross at x = 2, check 8 + 8 = 16](img/khayyam-cubic.svg)

The problem is $x^3 + 4x = 16$. This is Khayyam's type "a cube and roots equal a number". Write the 4 as $a^2$, which makes $a = 2$. Draw the parabola $x^2 = a y$, that is $y = x^2 / 2$. Draw a circle whose diameter runs along the $x$-axis from 0 to $16 / a^2 = 4$. That circle has center $(2, 0)$ and radius 2. The two curves meet at the origin and at one more point, $(2, 2)$. The $x$-coordinate of that second point, 2, is the answer. Check: $8 + 8 = 16$.

Why does it work? A point on both curves satisfies both equations. Substitute one into the other and the cubic falls out:

```txt
  (x - 2)^2 + y^2 = 4              circle: center (2, 0), radius 2
  x^2 - 4x + y^2  = 0              expand and cancel the 4s
  y = x^2 / 2                      the point is also on the parabola
  x^2 - 4x + x^4 / 4 = 0           substitute y
  x (x^3 / 4 + x - 4) = 0          factor out x
  x^3 + 4x - 16 = 0                the other factor, times 4
  x^3 + 4x = 16                    the original cubic
```

Khayyam gets a length, not a decimal. To read off a number, you measure the drawing. He hopes someone finds an arithmetic recipe like al-Khwarizmi's. Italian algebraists do, about 470 years later, in [Chapter 06](../06-medieval-and-renaissance-europe/README.md). Khayyam has other work too. In 1079 he leads a reform of the Persian solar calendar, the Jalali calendar, which drifts from the seasons more slowly than the Gregorian calendar adopted in Europe in 1582. Many know him only as a poet.

### Trigonometry, Decimals, and the Sky

The questions of prayer and the calendar live on a sphere: the sky above, or the Earth below. **Spherical trigonometry** is the math of triangles drawn on a sphere, with sides made of arcs of great circles. Scholars in this era replace the Greek chord tables with the sine, take the tangent from shadow measurements, and prove the rules for spherical triangles.

```txt
                    N pole
                      *
                     / \
       your city    /   \    Mecca
      (lat, lon)   A-----B   (21.4 N, 39.8 E)
                    \___/
                great-circle arc A to B
       the qibla is the angle at A between north and the arc to B
```

<!-- diagram: type=spherical-triangle ref=sphere-triangle caption="A triangle on a sphere with one corner at the North Pole" -->
![A sphere with a triangle drawn on it: one corner at the North Pole, two corners on the equator, all three angles 90 degrees, for a total of 270 degrees](../08-18th-and-19th-century-rigor/img/sphere-triangle.svg)

This picture comes from [Chapter 08](../08-18th-and-19th-century-rigor/README.md), where it makes a different point. Here, notice the shape: a triangle on a sphere with one corner at the North Pole. Its sides are arcs, and its angles add to more than 180 degrees. Flat-plane trigonometry gets such triangles wrong. Spherical trigonometry gets them right.

The qibla from a given city is one angle of a spherical triangle. Its corners are the North Pole, the city, and Mecca. The sides are known from latitudes and longitudes. Solve the triangle and you get the direction to face. Al-Biruni (973 to c. 1050) works out such problems in detail and also measures the radius of the Earth from a mountain top.

Prayer times come from the sun. One common rule starts the afternoon prayer (Asr) when the shadow of a stick equals its length plus its noon shadow. Shadows are tangents in disguise:

```txt
  stick height              = 1.0 m
  noon shadow               = 0.4 m     measured at midday
  Asr shadow                = 1.0 + 0.4 = 1.4 m     the rule
  tan(sun altitude)         = height / shadow = 1 / 1.4
  sun altitude              = about 35.5 degrees    inverse tangent
  Asr starts when the sun drops to 35.5 degrees in the afternoon
```

Nasir al-Din al-Tusi, in the 13th century, writes the *Treatise on the Quadrilateral*. It treats plane and spherical trigonometry as a subject of its own, not a chapter of astronomy. From 1259 he directs a new observatory at Maragha in Persia.

Ibn al-Haytham works on light rather than the sky. His *Book of Optics*, written in Cairo in the 1010s, argues that we see because light travels from objects into the eye, and he tests his claims with experiments. Translated into Latin, it shapes European optics for six centuries.

The era ends in Samarkand. Ulugh Beg, grandson of the conqueror Timur, builds an observatory there in the 1420s. Its great instrument is a stone arc about 40 m in radius, sunk into the hillside. His team measures star positions for a catalogue of about 1,000 stars. On that team, al-Kashi computes pi in 1424 by trapping a circle between polygons, as Archimedes did in [Chapter 03](../03-ancient-greece/README.md).

<!-- diagram: type=historical-method ref=archimedes-pi caption="Trap the circle between two polygons" -->
![Archimedes traps a circle of radius 1 between an inner and an outer hexagon, with a dashed inner 12-gon; a table of half-perimeters: 6 sides 3.00000 inside and 3.46410 outside, 12 sides 3.10583 and 3.21539, 24 sides 3.13263 and 3.15966, 48 sides 3.13935 and 3.14609, 96 sides 3.14103 and 3.14271; Archimedes concludes 3 10/71 < pi < 3 1/7](../03-ancient-greece/img/archimedes-pi.svg)

The method is the one in the picture: each doubling of the sides squeezes the polygons closer to the circle. Archimedes stops at 96 sides. Al-Kashi keeps doubling, 27 times past the hexagon:

```txt
  sides                 n sin(180 / n), half the perimeter of the inscribed polygon
  6                     3.000000
  12                    3.105829            double the sides
  24                    3.132629            double again
  96                    3.141032            where Archimedes stops
  3 x 2^28              3.14159265358979    805,306,368 sides: al-Kashi
```

He reports $2\pi$ to the equivalent of 16 decimal places, in both base 60 and base 10. No one beats it for about 170 years. In his *Key of Arithmetic* (1427) he teaches **decimal fractions**: digits after a point, each worth one tenth of the one before. Astronomers of his time still compute in base 60, the Babylonian system of [Chapter 02](../02-mesopotamia-and-egypt/README.md). Al-Kashi shows the base-10 way is easier for everyone else.

## What It Unlocked Next

* Algebra as a general method, carried to Europe through 12th-century Latin translations: see [06 Medieval and Renaissance Europe](../06-medieval-and-renaissance-europe/README.md).
* The Hindu-Arabic digits 0 to 9 and written column arithmetic, which Fibonacci teaches to Italian merchants in 1202: see [06 Medieval and Renaissance Europe](../06-medieval-and-renaissance-europe/README.md).
* The open problem of the cubic, solved by formula in Italy in the 1500s: see [06 Medieval and Renaissance Europe](../06-medieval-and-renaissance-europe/README.md).
* Curves as answers to equations, an idea Descartes turns into coordinate geometry: see [07 The Scientific Revolution and Calculus](../07-scientific-revolution-and-calculus/README.md).
* Sine and tangent tables and spherical trigonometry, which European navigators and astronomers inherit.
* Decimal fractions, which Stevin popularizes in Europe in 1585.

## Connects To

* [Course 201: Algebra I and Geometry](../../course/201/README.md): linear equations and the quadratics you solve here with squares.
* [Course 301: Algebra II, Trig and Precalculus](../../course/301/README.md): polynomials, conics, and trigonometry from this chapter.
* [Algebra track](../../tracks/algebra/README.md): completing the square and the quadratic formula in full.
* [Trigonometry track](../../tracks/trigonometry/README.md): sine and tangent, the tools behind qibla and prayer times.
* [Geometry track](../../tracks/geometry/README.md): the area arguments al-Khwarizmi uses as proofs.
* [Combinatorics track](../../tracks/combinatorics/README.md): binomial coefficients, from al-Karaji to Pascal.
* [Story of zero](../story-of-an-idea/zero.md): how the Indian digits travel west through Baghdad.
* [Story of notation](../story-of-an-idea/notation.md): from algebra in words to algebra in symbols.
* [Story of pi](../story-of-an-idea/pi.md): al-Kashi holds the record for about 170 years.
* [Biography of al-Khwarizmi](../biographies/al-khwarizmi.md): the man behind the words algebra and algorithm.
* [Biography of Omar Khayyam](../biographies/omar-khayyam.md): cubics, calendars, and poems.

## Try It

1. Use al-Khwarizmi's recipe to solve $x^2 + 6x = 16$. Write each step in words.
2. Solve $x^2 + 4x = 60$ by completing the square.
3. Draw the four-strip figure for $x^2 + 8x = 48$. How wide is each strip, what is the area of each corner, and what is $x$?
4. Find both positive answers to $x^2 + 21 = 10x$ without looking at the worked example.
5. Apply al-jabr and al-muqabala to $x^2 + 5 = 2x^2 - 4$. Which standard form do you reach, and what is $x$?
6. A woman leaves an estate of 480 dinars to her husband, one son, and one daughter. With children present, the husband takes one quarter. The children split the rest, a son taking twice a daughter's share. Find each share.
7. Khayyam style: for $x^3 + 9x = 54$, name the parabola and the circle, then check that $x = 3$ lies on both.
8. A stick 2 m tall casts a 0.5 m shadow at noon. How long is its shadow when Asr begins? Use a calculator to find the sun altitude at that moment.

<details>
<summary>Answers</summary>

1. $x = 2$: halve 6 to get 3, square to get 9, add to 16 to get 25, root is 5, subtract 3.
2. $x = 6$: half is 2, square is 4, $60 + 4 = 64$, root 8, $8 - 2 = 6$.
3. Each strip is $8 / 4 = 2$ wide, each corner is $2 \times 2 = 4$, four corners add 16, $48 + 16 = 64$, side 8, $x = 8 - 4 = 4$.
4. $x = 3$ and $x = 7$: half is 5, $25 - 21 = 4$, root 2, then $5 - 2$ and $5 + 2$.
5. Restore the 4: $x^2 + 9 = 2x^2$. Balance away $x^2$: $9 = x^2$, form 2 (squares equal numbers), $x = 3$.
6. Husband 120, son 240, daughter 120: $480 / 4 = 120$, the remaining 360 splits into 3 parts of 120, the son takes two.
7. $a^2 = 9$ gives $a = 3$. Parabola $x^2 = 3y$, circle on diameter $54 / 9 = 6$, center $(3, 0)$, radius 3. At $x = 3$ the parabola gives $y = 3$, and $(3 - 3)^2 + 3^2 = 9$, on the circle. Check: $27 + 27 = 54$.
8. Shadow $2 + 0.5 = 2.5$ m. $\tan(\text{altitude}) = 2 / 2.5 = 0.8$, altitude about 38.7 degrees.

</details>

## Code Corner

The program at [code/main.go](code/main.go) runs al-Khwarizmi's recipe step by step, in his order of words, for three equations of form 4. Then it solves Khayyam's cubic $x^3 + 4x = 16$ by **bisection**: start with an interval where the left side is too small at one end and too big at the other, cut the interval in half, keep the half where the sign changes, and repeat. It is `git bisect` for numbers. Finally it checks that the root lands on both of Khayyam's curves.

```go
// khwarizmi solves x^2 + b*x = c with his spoken recipe.
func khwarizmi(b, c float64) float64 {
	half := b / 2                  // halve the roots
	sq := half * half              // square the half
	side := math.Sqrt(c + sq)      // add, take the root
	return side - half             // subtract the half
}

// bisect finds a root of f between lo and hi.
func bisect(f func(float64) float64, lo, hi float64, steps int) float64 {
	for i := 1; i <= steps; i++ {
		mid := (lo + hi) / 2
		if f(lo)*f(mid) <= 0 {
			hi = mid
		} else {
			lo = mid
		}
	}
	return (lo + hi) / 2
}
```

The excerpt above is simplified: it drops the print statements and folds two steps into one line. The full file prints each step. Run it:

```txt
cd code && go run main.go
```

Real output:

```txt
== al-Khwarizmi: complete the square ==
Solve x^2 + 10x = 39
  halve the roots:        10 / 2 = 5
  square the half:        5 x 5 = 25
  add it to the number:   39 + 25 = 64
  take the root:          sqrt(64) = 8
  subtract the half:      8 - 5 = 3
  check: 3^2 + 10 x 3 = 39

Solve x^2 + 6x = 16
  halve the roots:        6 / 2 = 3
  square the half:        3 x 3 = 9
  add it to the number:   16 + 9 = 25
  take the root:          sqrt(25) = 5
  subtract the half:      5 - 3 = 2
  check: 2^2 + 6 x 2 = 16

Solve x^2 + 8x = 48
  halve the roots:        8 / 2 = 4
  square the half:        4 x 4 = 16
  add it to the number:   48 + 16 = 64
  take the root:          sqrt(64) = 8
  subtract the half:      8 - 4 = 4
  check: 4^2 + 8 x 4 = 48

== Omar Khayyam: x^3 + 4x = 16 ==
Bisection on [0, 3]:
  step  1: root is in [1.500000, 3.000000]
  step  2: root is in [1.500000, 2.250000]
  step  3: root is in [1.875000, 2.250000]
  step  4: root is in [1.875000, 2.062500]
  step  5: root is in [1.968750, 2.062500]
  step 30: root is in [2.000000, 2.000000]
  bisection root: 2.000000000
  parabola point: (2.000000, 2.000000)
  distance to circle center (2, 0): 2.000000 (radius 2)
  geometric answer: x = 2, check 2^3 + 4 x 2 = 16
```

Bisection needs 30 halvings to pin the root to about nine decimal places. Khayyam needs one drawing and a ruler. Each method has its price.

## Flashcards

Anki deck in [cards.tsv](cards.tsv) (tab-separated: front, back, tags).

## Go Deeper

* [MacTutor: Arabic mathematics, a forgotten brilliance?](https://mathshistory.st-andrews.ac.uk/HistTopics/Arabic_mathematics/): a broad survey of the era.
* [MacTutor biography of al-Khwarizmi](https://mathshistory.st-andrews.ac.uk/Biographies/Al-Khwarizmi/): his life, his six forms, and his figures.
* [MacTutor biography of Omar Khayyam](https://mathshistory.st-andrews.ac.uk/Biographies/Khayyam/): the cubic types and the calendar.
* [MacTutor biography of al-Kashi](https://mathshistory.st-andrews.ac.uk/Biographies/Al-Kashi/): pi, decimal fractions, and Samarkand.
* [MacTutor: Arabic numerals](https://mathshistory.st-andrews.ac.uk/HistTopics/Arabic_numerals/): how the digits travel from India through Baghdad to Europe.
* [MacTutor biography of Nasir al-Din al-Tusi](https://mathshistory.st-andrews.ac.uk/Biographies/Al-Tusi_Nasir/): trigonometry as its own subject.
