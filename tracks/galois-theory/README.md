# Galois Theory Track

**Track:** Galois Theory · **Span:** beginner to advanced · **Course levels:** [301 Algebra II, Trig and Precalculus](../../course/301/README.md) (polynomials and complex numbers), [601 Proof and Higher Math](../../course/601/README.md) (groups, rings and fields)
**Prerequisites:** the quadratic formula and a little patience. The early rungs need only school algebra. The later rungs lean on groups from the [Abstract Algebra Track](../abstract-algebra/README.md). A refresher on polynomials lives in the [Algebra Track](../algebra/README.md).
**Files:** this README, [cards.tsv](cards.tsv) for Anki, [code/main.go](code/main.go), and the diagrams in [img/](img/).

## What the Field Studies

Galois theory asks one old question: which polynomial equations have a formula for their roots? A **root** is a number that makes the polynomial equal zero. A **formula by radicals** builds the roots from the coefficients with $+$, $-$, $\times$, $\div$ and roots such as $\sqrt{\ }$ and $\sqrt[3]{\ }$.

Degree 2 has the quadratic formula. Degrees 3 and 4 have longer formulas found in the 1500s. Degree 5 resisted everyone for 250 years. In 1832 Evariste Galois explained why. He stopped staring at the roots and studied the ways the roots can be shuffled without breaking any rule. Those shuffles form a **group**, and the shape of the group decides whether a formula exists.

The same tool settles three puzzles the Greeks left open for 2,000 years: doubling a cube, trisecting an angle, and drawing regular polygons with a ruler and compass.

## Why It Matters

The track is a story about limits, and limits are useful to know:

* **Impossibility saves time:** Galois theory proves that no quintic formula exists. Knowing a search is hopeless is worth as much as finding an answer, the same way the halting problem tells you not to write a perfect infinite-loop detector.
* **Numerical root finders:** since no general formula exists past degree 4, software finds roots by iteration. the Newton method and the eigenvalues of a companion matrix (the method behind root functions in many numeric libraries) exist because algebra ran out of formulas.
* **Finite fields:** the fields of this track have finite cousins called Galois fields. AES encryption does arithmetic in $GF(2^8)$. Reed-Solomon codes in RAID 6, QR codes and erasure-coded object storage use the same fields. CRC checksums divide polynomials over $GF(2)$.
* **Symmetry as a debugging habit:** the core move is to ask what stays unchanged when you shuffle things. Invariants such as checksums, conserved counts and idempotent operations are the same idea in an SRE uniform.

## Concept Map

<!-- diagram: type=concept-map tiers=beginner,intermediate,advanced nodes=12 caption="Galois theory concepts with prerequisite arrows" -->
![Concept map of Galois theory. The Quadratic Formula leads to Cubic and Quartic Formulas, Fields, and Symmetry of Roots. Cubic formulas lead to the Tower Law. Fields lead to Extensions and Degree, which leads to the Tower Law and the Galois Group. Symmetry of Roots leads to the Galois Group, which leads to Roots of Unity. Advanced nodes: the Tower Law leads to Ruler and Compass and to the Fundamental Theorem. The Galois Group also leads to the Fundamental Theorem, which leads to Solvable Groups and then No Quintic Formula. Roots of Unity also lead to Solvable Groups.](img/concept-map.svg)

Read the map top to bottom. An arrow from A to B means learn A first. Start at the orange box.

## Signature Diagram

<!-- diagram: type=lattice-pair fields=Q,Q(sqrt2),Q(sqrt3),Q(sqrt6),Q(sqrt2,sqrt3) groups={id},{id,tau},{id,sigma},{id,sigma tau},G highlight=Q(sqrt2) caption="Galois correspondence for Q(sqrt2, sqrt3)" -->
![Two diamond-shaped diagrams side by side. Left: the fields between Q and Q(root 2, root 3). Q is at the bottom, Q(root 2), Q(root 3) and Q(root 6) are in the middle, and Q(root 2, root 3) is at the top. Every edge has degree 2. Right: the subgroups of the Galois group, drawn upside down. The one-element group {id} is at the top, the three two-element groups are in the middle, and the whole four-element group is at the bottom. Q(root 2) and its partner {id, tau} are outlined in orange: tau is the symmetry that fixes root 2. Dashed arrows labeled fixes join Q to the whole group and the top field to {id}.](img/galois-correspondence.svg)

This picture is the whole theory in one frame. On the left are all the fields you build from $\mathbb{Q}$ with $\sqrt{2}$ and $\sqrt{3}$. On the right are all the groups of symmetries. Each field sits in the same spot as the group of symmetries that leaves it alone. A small field like $\mathbb{Q}$ is left alone by every symmetry. The big field at the top is left alone only by the do-nothing symmetry. Flip one diagram upside down and it matches the other exactly.

Galois saw that questions about fields, which are hard, turn into questions about finite groups, which you check by hand or by brute force. He wrote this down at 20, the night before a duel. Most people at 20 are still working out the laundry.

## The Concept Ladder

### Beginner

#### 1. The Quadratic Formula

A **polynomial equation** sets a sum of powers of $x$ to zero, such as $x^2 - 2x - 3 = 0$. Its **roots** are the values of $x$ that make it true. On a graph, the roots are where the curve crosses the $x$-axis. The **degree** is the highest power.

For degree 2, the problem has been solved since Babylon:

$$ax^2 + bx + c = 0 \quad\Longrightarrow\quad x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

<!-- diagram: type=function-plot f="x^2-2x-3" x=-2.5..4.5 marks=-1,3 axis=1 caption="The quadratic formula finds where the curve crosses zero" -->
![The parabola y = x squared minus 2x minus 3. It crosses the x-axis at x = -1 and x = 3, marked in orange. A dashed mirror line at x = 1 passes through the vertex (1, -4). Orange arrows show each root is 2 steps from the mirror line. Text: x = (2 plus or minus root 16) / 2 = 1 plus or minus 2. Roots: sum 2, product -3.](img/quadratic-parabola.svg)

Look at the plus-or-minus sign. The two roots sit as mirror images on either side of $x = 1$. That small symmetry is the seed of the whole track. The formula gives both roots at once because it cannot tell them apart.

<!-- diagram: type=timeline events=9 range="1800 BCE..1837" caption="3,600 years of hunting for formulas" -->
![A timeline with nine evenly spaced events. About 1800 BCE: Babylon solves quadratics on clay tablets. About 820: al-Khwarizmi, completing the square. 1545: Cardano prints cubic and quartic formulas. 1572: Bombelli uses complex numbers to tame the cubic. 1770: Lagrange studies how roots permute. 1799: Ruffini, a quintic proof with gaps. 1824: Abel, no general quintic formula, in orange. 1832: Galois, groups decide every case, in orange. 1837: Wantzel proves the cube and angle problems impossible.](img/history-timeline.svg)

Course link: [Polynomials and Complex Numbers](../../course/301/02-polynomials-and-complex-numbers/README.md) in 301. History: [Mesopotamia and Egypt](../../history/02-mesopotamia-and-egypt/README.md).

#### 2. Cubic and Quartic Formulas

In the early 1500s Scipione del Ferro and then Niccolo Tartaglia found a formula for the cubic. Gerolamo Cardano printed it in his book *Ars Magna* in 1545, together with the quartic formula of his student Lodovico Ferrari. Any cubic shifts into the form $x^3 + px + q = 0$, and then:

$$x = \sqrt[3]{-\frac{q}{2} + \sqrt{\frac{q^2}{4} + \frac{p^3}{27}}} \;+\; \sqrt[3]{-\frac{q}{2} - \sqrt{\frac{q^2}{4} + \frac{p^3}{27}}}$$

<!-- diagram: type=function-plot f="x^3-15x-4" x=-4.6..5 marks=-3.732,-0.268,4 caption="The Bombelli cubic: three real roots, complex detour" -->
![The cubic y = x cubed minus 15x minus 4. It crosses the x-axis three times, at about -3.73, -0.27 and 4, marked in orange. A box shows the Cardano formula for x cubed = 15x + 4: x = cube root of (2 + 11i) plus cube root of (2 - 11i) = (2 + i) + (2 - i) = 4, a detour through the square root of -121.](img/cubic-bombelli.svg)

The cubic $x^3 = 15x + 4$ has the plain root $x = 4$. The Cardano formula asks for $\sqrt{-121}$ on the way there. In 1572 Rafael Bombelli decided to calculate with such numbers anyway and found $(2 + i)^3 = 2 + 11i$. The imaginary parts cancel and out comes 4. Complex numbers entered mathematics as a tool for real answers, which is the most practical origin story a strange idea ever had.

The quartic formula exists too. It fills most of a page. Then everyone got stuck on degree 5.

History: [Gerolamo Cardano](../../history/biographies/cardano.md) and [Medieval and Renaissance Europe](../../history/06-medieval-and-renaissance-europe/README.md).

#### 3. Symmetry of Roots

The roots of $x^2 - 2$ are $\sqrt{2}$ and $-\sqrt{2}$. Using only fractions, you cannot tell them apart: any equation with rational coefficients that $\sqrt{2}$ satisfies, $-\sqrt{2}$ satisfies as well. Swapping them is a **symmetry**. It changes the numbers but breaks no rule.

Some expressions in the roots do not change under any shuffle. They are called **symmetric**, and they are always plain fractions built from the coefficients (Vieta formulas):

$$x^2 + bx + c = (x - r_1)(x - r_2) \implies r_1 + r_2 = -b, \quad r_1 r_2 = c$$

<!-- diagram: type=number-line range=-3..3 marks=-1.414,1.414 arrows=swap table=sum,product,difference caption="The swap of root 2 and minus root 2" -->
![A number line from -3 to 3 with orange points at minus root 2 and root 2. Two orange arcs show sigma swapping them. A table below: the sum of the roots is 0 before and after the swap, the same. The product is -2 before and after, the same. The first root minus the second is 2 root 2 before and minus 2 root 2 after: it flips.](img/root-swap.svg)

Joseph-Louis Lagrange noticed in 1770 that the cubic and quartic formulas work because certain expressions in the roots take only a few values when the roots are shuffled. Galois turned that hint into a theory. The rule to remember: an expression that every symmetry leaves alone is a plain rational number.

#### 4. Fields

A **field** is a set of numbers where you add, subtract, multiply and divide (except by zero) and always land back inside the set. The fractions $\mathbb{Q}$, the reals $\mathbb{R}$ and the complex numbers $\mathbb{C}$ are fields. The integers $\mathbb{Z}$ are not, since $1 \div 2$ leaves them.

The most useful fields in this track sit between $\mathbb{Q}$ and $\mathbb{C}$. Adding $\sqrt{2}$ to $\mathbb{Q}$ gives

$$\mathbb{Q}(\sqrt{2}) = \{\, a + b\sqrt{2} : a, b \in \mathbb{Q} \,\}, \qquad \frac{1}{a + b\sqrt{2}} = \frac{a - b\sqrt{2}}{a^2 - 2b^2}$$

<!-- diagram: type=nested-sets sets=C,R,Q(sqrt2),Q samples=i,pi,sqrt2,1/2 caption="Fields nest like directories" -->
![Four nested rounded boxes. The outer box is C, the complex numbers, holding i, 2 - 3i and root -5. Inside it is R, the real numbers, holding pi, cube root of 2 and e. Inside that is Q(root 2), numbers a + b root 2, holding root 2, 1 + 3 root 2 and 1/(1 + root 2). The innermost orange box is Q, the fractions, holding 1/2, -3, 7 and 0.75. A side panel defines a field, notes that the integers are not a field, and notes that Q(i) is a field inside C but not inside R.](img/nested-fields.svg)

The division formula works because $a^2 - 2b^2$ is never zero for rational $a, b$ not both zero, which is the same fact as $\sqrt{2}$ being irrational. Think of $\mathbb{Q}(\sqrt{2})$ as $\mathbb{Q}$ with one extra package installed. Everything still compiles.

Course link: [Groups, Rings and Fields](../../course/601/11-groups-rings-and-fields/README.md) in 601.

### Intermediate

#### 5. Field Extensions and Degree

When a field $K$ sits inside a bigger field $L$, call $L$ an **extension** of $K$. Every element of $\mathbb{Q}(\sqrt{2})$ needs exactly two rational coordinates, $a$ and $b$. The number of coordinates is the **degree** $[L : K]$. In linear algebra language, it is the dimension of $L$ as a vector space over $K$.

A number $\alpha$ has a **minimal polynomial** over $\mathbb{Q}$: the lowest-degree polynomial with rational coefficients and leading coefficient 1 that has $\alpha$ as a root. Such a polynomial is **irreducible**, which means it does not factor into smaller polynomials with rational coefficients. Its degree is the degree of the extension:

$$[\mathbb{Q}(\alpha) : \mathbb{Q}] = \deg(\text{minimal polynomial of } \alpha)$$

<!-- diagram: type=lattice-grid a=-1..3 b=-1..3 points=(1,1),(3,2) table=degrees caption="Q(sqrt2) as a plane of rational coordinates" -->
![Left: a grid of points (a, b) standing for a + b root 2. The point (1, 1) is 1 + root 2. An orange arrow labeled square it goes to the orange point (3, 2), which is 3 + 2 root 2, since (1 + root 2) squared = 3 + 2 root 2. Right: a table of fields with basis and degree. Q(root 2): basis 1, root 2, degree 2. Q(i): 1, i, degree 2. Q(cube root 2): 1, cube root 2, cube root 4, degree 3. Q(root 2, root 3): 1, root 2, root 3, root 6, degree 4.](img/extension-basis.svg)

The minimal polynomial of $\sqrt[3]{2}$ is $x^3 - 2$. A cubic that factors over $\mathbb{Q}$ has a linear factor, which means a rational root. The only candidates are $\pm 1$ and $\pm 2$, and none works. Degree 3 it is.

Track link: [Linear Algebra Track](../linear-algebra/README.md) for bases and dimension.

#### 6. The Tower Law

Stack fields $K \subseteq L \subseteq M$. Each step has a degree, and the degrees multiply:

$$[M : K] = [M : L]\,[L : K]$$

<!-- diagram: type=tower left=Q,Q(sqrt2),Q(sqrt2,sqrt3) right=Q,Q(cbrt2),Q(cbrt2,omega) degrees=2,2;3,2 caption="Tower law: degrees multiply" -->
![Two vertical towers of fields. Left: Q, then Q(root 2) at degree 2, then Q(root 2, root 3) at degree 2 more, with an orange bracket labeled 2 times 2 = 4 and basis 1, root 2, root 3, root 6. Right: Q, then Q(cube root 2) at degree 3, then Q(cube root 2, omega) at degree 2 more, with an orange bracket labeled 3 times 2 = 6. A footnote defines omega as (-1 + root -3)/2, a cube root of 1.](img/tower-law.svg)

The reason is plain bookkeeping. If $L$ has basis $1, \sqrt{2}$ over $\mathbb{Q}$ and $M$ has basis $1, \sqrt{3}$ over $L$, then the products $1, \sqrt{2}, \sqrt{3}, \sqrt{6}$ form a basis of $M$ over $\mathbb{Q}$. A useful consequence: the degree of any number inside $M$ divides $[M : K]$. That one divisibility fact kills the cube-doubling problem in rung 12.

#### 7. Automorphisms and the Galois Group

An **automorphism** of a field $L$ is a one-to-one, onto map from $L$ to itself that respects addition and multiplication. An automorphism always fixes 1, therefore every integer, therefore every fraction. It also sends each root of a rational polynomial to a root of the same polynomial, because it respects the arithmetic in $f(r) = 0$.

The **Galois group** $\mathrm{Gal}(L/K)$ collects every automorphism of $L$ that leaves each element of $K$ unchanged. A **group** is a set of moves where doing two moves in a row is again a move, a do-nothing move exists, and every move undoes. For $\mathbb{Q}(\sqrt{2}, \sqrt{3})$, the only freedom is the sign of $\sqrt{2}$ and the sign of $\sqrt{3}$:

$$\mathrm{Gal}(\mathbb{Q}(\sqrt{2}, \sqrt{3}) / \mathbb{Q}) = \{\mathrm{id},\ \sigma,\ \tau,\ \sigma\tau\}, \qquad \sigma: \sqrt{2} \mapsto -\sqrt{2}, \quad \tau: \sqrt{3} \mapsto -\sqrt{3}$$

<!-- diagram: type=table+cayley elements=id,sigma,tau,sigma-tau caption="The four symmetries of Q(sqrt2, sqrt3)" -->
![Left: a table of what each symmetry does to root 2, root 3 and root 6. id changes nothing. sigma sends root 2 to minus root 2 and root 6 to minus root 6. tau sends root 3 to minus root 3 and root 6 to minus root 6. sigma tau negates root 2 and root 3 and leaves root 6 alone. Sign changes are orange. Right: the 4 by 4 composition table. The identity appears in orange on the whole diagonal, because each symmetry undoes itself.](img/galois-group-klein.svg)

An extension is **Galois** when it has as many symmetries as its degree. The splitting field of a polynomial, the smallest field holding all its roots, is always Galois over $\mathbb{Q}$. A warning example: $\mathbb{Q}(\sqrt[3]{2})$ has degree 3 but only one symmetry, because the other two cube roots of 2 are not real and do not live in that field. It has nowhere to send $\sqrt[3]{2}$.

Track link: [Abstract Algebra Track](../abstract-algebra/README.md) for group axioms and permutation groups.

#### 8. Roots of Unity

The solutions of $x^n = 1$ are the **$n$th roots of unity**. They sit evenly spaced on the unit circle in the complex plane, at the corners of a regular $n$-gon:

$$\zeta = \cos\frac{360^\circ}{n} + i \sin\frac{360^\circ}{n}, \qquad \text{roots } 1, \zeta, \zeta^2, \dots, \zeta^{n-1}$$

<!-- diagram: type=unit-circle n=5 map="z->z^2" caption="Fifth roots of unity: z goes to z squared" -->
![The unit circle with the five fifth roots of unity at the corners of a regular pentagon: 1 on the right in black, z, z squared, z cubed and z to the 4th in orange. Orange arrows show the symmetry sigma sending z to z squared, z squared to z to the 4th, z to the 4th to z cubed, and z cubed back to z. The root 1 stays fixed. Side text: the Galois group is cyclic of order 4, the units mod 5 under multiplication, and it is abelian.](img/roots-of-unity.svg)

For $n = 5$, $\zeta$ is a root of $x^4 + x^3 + x^2 + x + 1$, which is irreducible, which means degree 4. A symmetry is decided by where it sends $\zeta$, and $\zeta \mapsto \zeta^2$ generates all four. In general $\mathrm{Gal}(\mathbb{Q}(\zeta_n)/\mathbb{Q})$ is the group of units mod $n$ under multiplication. That group is **abelian**: the order of two moves never matters. Abelian groups are the building blocks that radicals produce, and that fact drives rung 10.

Track link: [Complex Analysis Track](../complex-analysis/README.md) for the complex plane, and [Number Theory Track](../number-theory/README.md) for units mod $n$.

### Advanced

#### 9. The Fundamental Theorem of Galois Theory

Let $L/K$ be a finite Galois extension with group $G$. Then fields between $K$ and $L$ match subgroups of $G$ one to one. A field $M$ matches the subgroup $H$ of symmetries that leave $M$ alone. The match turns the picture upside down, and it tracks sizes exactly:

$$M \longleftrightarrow H, \qquad [L : M] = |H|, \qquad [M : K] = \frac{|G|}{|H|}$$

Also, $M$ is Galois over $K$ exactly when $H$ is a **normal subgroup**: a subgroup that stays the same when every element is conjugated, $gHg^{-1} = H$ for every $g$ in $G$.

<!-- diagram: type=lattice-pair fields=Q,Q(omega),Q(cbrt2)x3,Q(cbrt2,omega) groups=S3,A3,order2x3,{e} highlight=Q(omega),A3 caption="Splitting field of x^3 - 2 and the subgroups of S3" -->
![Two lattices. Left: Q at the bottom. Above it, Q(omega) at degree 2, outlined in orange, and three cubic fields Q(cube root 2), Q(omega cube root 2), Q(omega squared cube root 2) at degree 3, with Q(cube root 2) outlined in orange. At the top, Q(cube root 2, omega) of degree 6. Right: the upside-down subgroup lattice of S3: S3 at the bottom, A3 in orange, three two-element subgroups {e, (23)}, {e, (13)}, {e, (12)}, and {e} at the top. Notes: the swap (23) fixes Q(cube root 2). A3 is normal and its field Q(omega) is the only middle field that is Galois over Q.](img/s3-lattice.svg)

For $x^3 - 2$ the roots are $\sqrt[3]{2}$, $\omega\sqrt[3]{2}$ and $\omega^2\sqrt[3]{2}$, where $\omega$ is a cube root of 1. All six shuffles of three roots are symmetries, which means the Galois group is $S_3$ and the splitting field has degree 6. Six subgroups match six fields. The three cubic fields match three subgroups that are not normal, and none of those fields is Galois over $\mathbb{Q}$. This is a theorem, not a coincidence of one example.

#### 10. Solvable Groups

A group is **solvable** when it breaks into a chain of layers, each one abelian:

$$\{e\} = G_0 \subset G_1 \subset \dots \subset G_k = G, \quad G_i \text{ normal in } G_{i+1}, \quad G_{i+1}/G_i \text{ abelian}$$

A quick test uses **commutators**, $aba^{-1}b^{-1}$, which measure how far $a$ and $b$ are from commuting. The subgroup they generate is the **derived subgroup** $G'$. Take it again and again. The group is solvable exactly when this **derived series** reaches $\{e\}$.

<!-- diagram: type=chain-columns groups=S3,S4,S5 sizes=6-3-1;24-12-4-1;120-60-60 caption="Derived series of S3, S4 and S5" -->
![Three columns of boxes connected by downward arrows. S3, size 6, goes to A3, size 3, then to {e}, size 1: solvable. S4, size 24, goes to A4, size 12, then V4, size 4, then {e}, size 1: solvable. S5, size 120, goes to A5, size 60, then to A5 again, size 60, with the arrow labeled nothing peeled, all in orange: not solvable.](img/derived-series.svg)

Why this matters for formulas: adding an $n$th root, with the roots of unity already present, adds one abelian layer to the Galois group (a cyclic one). A formula by radicals is a stack of such roots, which means a stack of abelian layers. $S_3$ and $S_4$ peel down to nothing, and that is why the cubic and quartic formulas exist. $S_5$ peels once to $A_5$ and then sticks. $A_5$ equals its own commutator subgroup. It is the smallest group that is not solvable, at 60 elements.

#### 11. No Quintic Formula

**Galois theorem:** a polynomial with rational coefficients is solvable by radicals exactly when its Galois group is solvable. To kill the quintic formula, one quintic with Galois group $S_5$ suffices. Here is one:

$$f(x) = x^5 - 4x + 2$$

<!-- diagram: type=function-plot f="x^5-4x+2" x=-1.85..1.75 marks=-1.519,0.508,1.244 caption="x^5 - 4x + 2 has three real roots" -->
![The curve y = x to the 5th minus 4x plus 2. It crosses the x-axis three times, at about -1.519, 0.508 and 1.244, marked in orange. A box notes that the other 2 roots are complex, -0.117 plus or minus 1.438i, that complex conjugation swaps just those 2, and that the Galois group is S5.](img/quintic-three-roots.svg)

The argument has four short steps. First, $f$ is irreducible (Eisenstein criterion at the prime 2). Second, its group contains a 5-cycle, because 5 divides the degree of the splitting field. Third, the graph crosses zero exactly three times, the other two roots are a complex pair, and complex conjugation swaps just that pair: a single swap. Fourth, a 5-cycle and a single swap generate all of $S_5$. Worked Example 4 shows the details.

Careful with the wording. **Abel-Ruffini** (Abel, 1824) says no single formula works for every quintic. Some quintics are fine: $x^5 - 2$ has root $\sqrt[5]{2}$, and its Galois group has 20 elements and is solvable. Galois theory tells you which case you are in.

History: [Evariste Galois](../../history/biographies/galois.md) and [18th and 19th Century Rigor](../../history/08-18th-and-19th-century-rigor/README.md).

#### 12. Ruler and Compass

The Greek rules: start with two points at distance 1. Draw lines through two known points, and circles with a known center through a known point. New points come from intersections. Each intersection solves a linear or quadratic equation, which means each new number is at most one square root deeper. Combine with the tower law:

$$\alpha \text{ constructible} \implies [\mathbb{Q}(\alpha) : \mathbb{Q}] = 2^k \text{ for some } k$$

<!-- diagram: type=tower levels=1,2,4,8,16 outliers=cbrt2,cos20 caption="Ruler and compass reach only degrees 1, 2, 4, 8, ..." -->
![A vertical tower of boxes labeled degree 1, 2, 4, 8, 16, each step labeled times 2 and one square root. Examples beside the tower: root 2 has degree 2, root (2 + root 2) has degree 4, cos(360 degrees / 17) has degree 8. To the right, two orange boxes, cube root of 2 with degree 3 and cos 20 degrees with degree 3, under the heading 3 divides no power of 2.](img/constructible-degrees.svg)

<!-- diagram: type=geometry-pair left=cube(1),cube(cbrt2) right=angle(60),rays(20,40) caption="Doubling the cube and trisecting 60 degrees" -->
![Left: a cube with side 1 and volume 1 beside a larger orange cube with side cube root of 2, about 1.26, and volume 2. Caption: doubling the cube needs cube root of 2. Right: a 60 degree angle with two orange dashed rays at 20 and 40 degrees. Caption: trisecting 60 degrees needs cos 20 degrees.](img/cube-and-angle.svg)

**Doubling the cube** needs a side of $\sqrt[3]{2}$, degree 3. **Trisecting** $60^\circ$ needs $\cos 20^\circ$, a root of $8x^3 - 6x - 1$, also degree 3. Three divides no power of 2. Pierre Wantzel proved both impossible in 1837, ending 2,000 years of attempts. Some angles do trisect: $90^\circ$ splits into three $30^\circ$ angles with no trouble. The theorem says no single method works for every angle.

The same idea decides regular polygons. Gauss showed at 19 that the 17-gon is constructible. The full answer (Gauss and Wantzel): a regular $n$-gon is constructible exactly when $n$ is a power of 2 times distinct **Fermat primes**, primes of the form $2^{2^m} + 1$.

Track link: [Geometry Track](../geometry/README.md) for the classical constructions.

## Worked Examples

### Example 1: Run the Cardano Formula on the Bombelli Cubic

Solve $x^3 - 15x - 4 = 0$. Here $p = -15$ and $q = -4$.

```txt
  q/2 = -2,  q^2/4 = 4                                 plug in q = -4
  p^3/27 = (-15)^3 / 27 = -3375 / 27 = -125            plug in p = -15
  q^2/4 + p^3/27 = 4 - 125 = -121                      the number under the square root
  sqrt(-121) = 11i                                     11^2 = 121, and i^2 = -1
  x = cbrt(2 + 11i) + cbrt(2 - 11i)                    Cardano formula, -q/2 = 2
  (2 + i)^3 = 8 + 12i + 6i^2 + i^3                     binomial expansion
            = 8 + 12i - 6 - i = 2 + 11i                i^2 = -1, i^3 = -i
  cbrt(2 + 11i) = 2 + i, cbrt(2 - 11i) = 2 - i         matching cube roots
  x = (2 + i) + (2 - i) = 4                            imaginary parts cancel
  check: 64 - 60 - 4 = 0                               4^3 - 15*4 - 4
  x^3 - 15x - 4 = (x - 4)(x^2 + 4x + 1)                divide out the root 4
  x = -2 +/- sqrt(3) = -0.268, -3.732                  quadratic formula on the rest
```

### Example 2: Find the Galois Group of Q(sqrt2, sqrt3)

```txt
  [Q(sqrt2) : Q] = 2                                   x^2 - 2 has no rational root
  is sqrt3 in Q(sqrt2)? suppose sqrt3 = a + b sqrt2    test for a shortcut
  3 = a^2 + 2b^2 + 2ab sqrt2                           square both sides
  ab = 0                                               sqrt2 is irrational
  b = 0 gives sqrt3 = a, rational: impossible          sqrt3 is irrational
  a = 0 gives b^2 = 3/2, rational b: impossible        sqrt(3/2) is irrational
  [Q(sqrt2, sqrt3) : Q(sqrt2)] = 2                     x^2 - 3 stays irreducible
  [Q(sqrt2, sqrt3) : Q] = 2 x 2 = 4                    tower law
  each symmetry sends sqrt2 to +/- sqrt2               roots of x^2 - 2
  each symmetry sends sqrt3 to +/- sqrt3               roots of x^2 - 3
  2 x 2 = 4 choices, all of them work                  4 symmetries = degree 4, Galois
  sigma tau sends sqrt6 = sqrt2 sqrt3 to (-)(-) = +    signs multiply
  every element squared is id                          the Klein four-group
```

### Example 3: Prove cos 20 Degrees Is Not Constructible

```txt
  cos(3t) = 4 cos^3(t) - 3 cos(t)                      triple-angle identity
  t = 20 deg, cos 60 deg = 1/2                         choose the angle
  1/2 = 4c^3 - 3c                                      let c = cos 20 deg
  8c^3 - 6c - 1 = 0                                    multiply by 2, rearrange
  rational roots must be +/-1, +/-1/2, +/-1/4, +/-1/8  rational root test
  f(1) = 1, f(-1) = -3, f(1/2) = -3, f(-1/2) = 1       none is zero
  f(1/4) = -2.375, f(-1/4) = 0.375                     none is zero
  f(1/8) = -1.734, f(-1/8) = -0.266                    none is zero
  no rational root: the cubic is irreducible           a cubic that factors has a linear factor
  [Q(c) : Q] = 3                                       degree of the minimal polynomial
  3 is not a power of 2                                constructible degrees are 2^k
  cos 20 deg is not constructible                      60 deg cannot be trisected
```

### Example 4: Show x^5 - 4x + 2 Has Galois Group S5

```txt
  2 divides 0, 0, 0, -4, 2; 4 does not divide 2         Eisenstein at p = 2
  f is irreducible, degree 5                           Eisenstein criterion
  5 = [Q(r) : Q] divides [L : Q] = |G|                 tower law, L = splitting field
  G has an element of order 5: a 5-cycle               Cauchy theorem for groups
  f'(x) = 5x^4 - 4 = 0 at x = +/-0.946 only            f has 2 turning points
  f has at most 3 real roots                           at most one crossing per rising or falling stretch
  f(-2) = -22, f(-1) = 5, f(1) = -1, f(2) = 26          three sign changes
  exactly 3 real roots, 2 complex roots                5 - 3 = 2
  complex conjugation swaps the 2, fixes the 3         conjugation is a symmetry of L
  G contains a 5-cycle and a single swap               two facts above
  for a prime p, they generate all of S_p              standard group lemma
  G = S5, which is not solvable                        derived series stalls at A5
  the roots have no expression by radicals             Galois theorem
```

## Big Theorems to Know

* **Fundamental Theorem of Algebra (Gauss, 1799):** every polynomial of degree $n$ has $n$ complex roots, counted with repetition. The roots always exist. The question is only how to write them.
* **Vieta Formulas:** the coefficients of a polynomial are the symmetric functions of its roots.
* **Tower Law:** $[M : K] = [M : L][L : K]$.
* **Fundamental Theorem of Galois Theory:** for a finite Galois extension, intermediate fields and subgroups match one to one with inclusions reversed, and normal subgroups match Galois subextensions.
* **Galois Solvability Theorem (1832):** over $\mathbb{Q}$, a polynomial is solvable by radicals exactly when its Galois group is solvable.
* **Abel-Ruffini Theorem (1824):** no formula by radicals solves every polynomial of degree 5 or higher.
* **Non-Solvability of $S_n$:** $S_n$ is solvable for $n \le 4$ and not solvable for $n \ge 5$, because $A_n$ is simple and non-abelian for $n \ge 5$.
* **Prime Degree Criterion:** an irreducible polynomial over $\mathbb{Q}$ of prime degree $p$ with exactly two non-real roots has Galois group $S_p$.
* **Wantzel (1837):** a constructible real number has degree a power of 2 over $\mathbb{Q}$. Doubling the cube and trisecting a general angle are impossible.
* **Gauss-Wantzel Theorem:** a regular $n$-gon is constructible exactly when $n$ is a power of 2 times distinct Fermat primes.
* **Lindemann (1882):** $\pi$ is transcendental (the root of no rational polynomial), and squaring the circle is impossible. This one needs analysis, not only Galois theory.

## Open Problems and Fun Facts

* **A short life:** Galois died in 1832, aged 20, after a duel. The night before, he wrote a letter to his friend Auguste Chevalier summarizing his results. Joseph Liouville published the work in 1846, fourteen years later. Earlier submissions to the Paris Academy were lost or rejected as unclear.
* **Abel on a budget:** Niels Henrik Abel paid to print his 1824 impossibility proof himself and squeezed it into six pages to save money. He died in 1829 at 26. A letter offering him a professorship in Berlin arrived two days after his death.
* **A stolen secret:** Tartaglia gave Cardano the cubic formula on a promise of secrecy. Cardano printed it anyway, after finding that del Ferro had it first. The quarrel lasted years. Credit disputes in mathematics predate code review by several centuries.
* **The 17-gon:** Gauss found the construction of the regular 17-gon in 1796, at 19. According to a popular story, it convinced him to choose mathematics over languages.
* **Open problem, Fermat primes:** only five are known: 3, 5, 17, 257 and 65,537. Nobody knows whether a sixth exists. Each new one adds a constructible polygon.
* **Open problem, inverse Galois problem:** is every finite group the Galois group of some extension of $\mathbb{Q}$? Every symmetric group is, and Shafarevich proved every solvable group is. The general question is still open after more than a century.

## Starter Problems

1. Solve $x^2 - 6x + 5 = 0$ with the quadratic formula. Check the Vieta formulas for the sum and product of the roots.
2. Write $\dfrac{1}{1 + \sqrt{2}}$ in the form $a + b\sqrt{2}$.
3. What is the degree of $\mathbb{Q}(\sqrt{5})$ over $\mathbb{Q}$? Give a basis.
4. Find $[\mathbb{Q}(\sqrt[3]{2}, \sqrt{3}) : \mathbb{Q}]$.
5. Is $\sqrt{1 + \sqrt{3}}$ constructible with ruler and compass?
6. Is the regular 9-gon constructible?
7. Write a chain of subgroups that shows $S_3$ is solvable.

<details>
<summary>Answers</summary>

1. $x = \frac{6 \pm \sqrt{36 - 20}}{2} = \frac{6 \pm 4}{2}$, which gives 1 and 5. Sum $1 + 5 = 6 = -(-6)$. Product $1 \cdot 5 = 5$. Both match.
2. $-1 + \sqrt{2}$. Multiply top and bottom by $1 - \sqrt{2}$: $\frac{1 - \sqrt{2}}{1 - 2} = -1 + \sqrt{2}$.
3. Degree 2, basis $1, \sqrt{5}$. The minimal polynomial is $x^2 - 5$.
4. 6. Both 2 and 3 divide the total by the tower law, which means 6 divides it. Also the total is at most $3 \times 2 = 6$.
5. Yes. It comes from two square roots in a row, and its degree is 4, a power of 2.
6. No. $9 = 3^2$ uses the Fermat prime 3 twice, and the primes must be distinct. Equivalently, it needs $\cos 40^\circ$, which has degree 3.
7. $\{e\} \subset A_3 \subset S_3$. The layers have sizes 3 and 2. Groups of prime size are cyclic, which means abelian.

</details>

## Code Corner

[code/main.go](code/main.go) solves a quadratic and the Bombelli cubic by formula with `complex128`, shuffles the roots, checks the four symmetries of $\mathbb{Q}(\sqrt{2}, \sqrt{3})$, walks the fifth roots of unity, computes the derived series of $S_3$, $S_4$ and $S_5$ by brute force, finds all five roots of $x^5 - 4x + 2$, and tests constructibility. Run it with `go run main.go` inside `code/`.

```txt
== Quadratic formula: x^2 - 2x - 3 ==
roots -1 and 3, sum 2, product -3

== Cardano: x^3 - 15x - 4 (Bombelli 1572) ==
u = cube root of (2 + 11i) = (2.0000+1.0000i)
v = cube root of (2 - 11i) = (2.0000-1.0000i)
root 1 =   4.0000   |f(root)| = 1.5e-14
root 2 =  -3.7321   |f(root)| = 1.4e-14
root 3 =  -0.2679   |f(root)| = 1.3e-14
exact: 4, -2 + sqrt3 = -0.2679, -2 - sqrt3 = -3.7321

== Shuffle the three roots ==
over all 6 orders: r1+r2+r3 takes 1 value, r1r2+r1r3+r2r3 takes 1, r1r2r3 takes 1
r1 + 2 r2 + 3 r3 takes 6 values (not symmetric)
(r1-r2)(r1-r3)(r2-r3) takes 2 values: [-114.315353 114.315353]

== The four symmetries of Q(sqrt2, sqrt3) ==
name        sqrt2  sqrt3  sqrt6  respects x*y?
id          +      +      +      true
sigma       -      +      -      true
tau         +      -      -      true
sigma tau   -      -      +      true
every symmetry applied twice gives id: the group is the Klein four-group

== Fifth roots of unity: sigma sends z to z^2 ==
z -> z^2 -> z^4 -> z^3 -> z^1   (order 4, cyclic)
check: z^2 is a root of x^4+x^3+x^2+x+1, residual 1.1e-16

== Derived series (commutator subgroups) ==
S3: [6 3 1]  solvable
S4: [24 12 4 1]  solvable
S5: [120 60 60]  NOT solvable: stuck at A5

== The quintic x^5 - 4x + 2 ==
Eisenstein at p = 2: 2 divides 0, 0, 0, -4, 2 and 4 does not divide 2 -> irreducible
real root -1.51851   f = -1.2e-15
real root  0.50850   f = -1.9e-16
real root  1.24360   f = 8.2e-17
complex pair  -0.11679 +/- 1.43845i
3 real roots: complex conjugation swaps the other 2
a 5-cycle and a swap generate a group of size 120 = |S5|

== Ruler and compass ==
x^3 - 2:        rational roots [] -> irreducible, degree 3
8x^3 - 6x - 1:  rational roots [] -> irreducible, degree 3
cos 20 deg = 0.939693, 8c^3 - 6c - 1 = 0.0e+00
cube root of 2 = 1.259921, cubed = 2.000000
3 is not a power of 2: neither number is constructible
constructible regular n-gons, n = 3..30: 3 4 5 6 8 10 12 15 16 17 20 24 30
```

Two lines carry the track. The derived series line shows $S_5$ stuck at 60 elements, which is the whole reason for the missing quintic formula, found by a computer in a fraction of a second. The shuffle line shows $(r_1 - r_2)(r_1 - r_3)(r_2 - r_3)$ taking just two values, $\pm 114.3$: it is unchanged by the three even shuffles and flips sign under the three swaps. Its square, $13{,}068$, is the **discriminant**, a symmetric function and a plain integer.

## Flashcards

[cards.tsv](cards.tsv) holds the key definitions and theorems for Anki import.

## Resources

* [MacTutor: Evariste Galois](https://mathshistory.st-andrews.ac.uk/Biographies/Galois/): the life, the duel, and the fate of the manuscripts.
* [MacTutor: Niels Henrik Abel](https://mathshistory.st-andrews.ac.uk/Biographies/Abel/): the first complete proof that the quintic has no general formula.
* [MacTutor: Girolamo Cardano](https://mathshistory.st-andrews.ac.uk/Biographies/Cardan/): the cubic formula and the quarrel with Tartaglia.
* [MacTutor: Quadratic, Cubic and Quartic Equations](https://mathshistory.st-andrews.ac.uk/HistTopics/Quadratic_etc_equations/): the long history from Babylon to the Renaissance in one essay.
* [J.S. Milne: Fields and Galois Theory](https://www.jmilne.org/math/CourseNotes/ft.html): free course notes, rigorous and complete, for when the advanced rungs feel too gentle.
* [Wolfram MathWorld: Constructible Number](https://mathworld.wolfram.com/ConstructibleNumber.html): compact definitions with links to the classic construction problems.

## Where to Go Next

* [Abstract Algebra Track](../abstract-algebra/README.md) for groups, normal subgroups and finite fields in full.
* [Number Theory Track](../number-theory/README.md) for units mod $n$, Fermat primes and cyclotomic polynomials.
* [Complex Analysis Track](../complex-analysis/README.md) for the complex plane where all these roots live.
* [Geometry Track](../geometry/README.md) for the constructions that rung 12 rules out and the many it allows.
