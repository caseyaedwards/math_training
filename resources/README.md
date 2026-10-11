# Resources

A hand-checked list of plain, old-school math pages on the open web: professor home pages, lecture notes, classic tutorials, and free books. Most pages here are simple HTML with a few GIF or JPEG figures. They load fast, print well, and explain one idea at a time.

Every URL in this folder was fetched and read in October 2026. Each one loaded and covered the topic described. Links rot, so run the checker before a study session (see [Keeping the Links Alive](#keeping-the-links-alive)).

## Files in This Folder

* [README.md](README.md): this list, grouped by course level and by track.
* [free-textbooks.md](free-textbooks.md): complete free textbooks (HTML or PDF), grouped by level.
* [linkcheck](linkcheck/README.md): a standard-library Go program that checks every URL in `resources/*.md`.

## How to Use This List

1. Start from the lesson you are working on in [course](../course/README.md) or [tracks](../tracks/README.md).
2. Find the matching section below. The **By Course Level** section gives two to five starter picks per level. The **By Track** section gives the full list for each subject.
3. Read the one-line note and the tags. Pick a page that matches your mood: a picture-heavy page for a first look, a page with exercises for practice, or a free book for depth.
4. Open one page at a time. Old professor pages often go deeper than the lesson. Stop when the page stops answering your question.

Tags:

* `[plain-html]`: simple HTML page or site, light on scripts, easy to read and print.
* `[pictures]`: figures, diagrams, or drawings carry a large part of the explanation.
* `[exercises]`: problems to try, often with answers or full solutions.
* `[free-book]`: a complete book, free to read online or download.
* `[pdf]`: the main content is a PDF.
* `[notes]`: lecture notes or handouts from a university course.
* `[reference]`: a lookup source, not a course to read front to back.
* `[archive]`: a frozen copy of a classic page (for example, on the Internet Archive).

## By Course Level

### 101 Foundations

Course: [course/101](../course/101/README.md).

* [Skill in Arithmetic](https://www.themathpage.com/Arith/arithmetic.htm), Lawrence Spector (TheMathPage): a patient, page-by-page arithmetic course from addition to percents. `[plain-html]` `[exercises]`
* [Math Is Fun: The World of Numbers](https://www.mathsisfun.com/numbers/index.html), Rod Pierce: friendly picture explanations of fractions, decimals, negatives, and place value. `[pictures]` `[exercises]`
* [Egyptian Fractions](https://r-knott.surrey.ac.uk/Fractions/egyptian.html), Ron Knott (University of Surrey): a classic hobby page that makes fractions feel like a puzzle. `[plain-html]` `[exercises]`

### 201 Algebra I and Geometry

Course: [course/201](../course/201/README.md).

* [Paul's Online Notes: Algebra](https://tutorial.math.lamar.edu/Classes/Alg/Alg.aspx), Paul Dawkins (Lamar University): clear worked examples for equations, inequalities, and functions. `[plain-html]` `[exercises]`
* [Euclid's Elements](https://mathcs.clarku.edu/~djoyce/elements/elements.html), David E. Joyce (Clark University): every proposition of Euclid with a figure and a plain guide to each proof. `[plain-html]` `[pictures]`
* [Free Online Algebra Course](https://www.themathpage.com/Alg/algebra.htm), Lawrence Spector (TheMathPage): short lessons that ask a question, then reveal the answer when you are ready. `[plain-html]` `[exercises]`

### 301 Algebra II, Trig and Precalculus

Course: [course/301](../course/301/README.md).

* [Dave's Short Trig Course](https://mathcs.clarku.edu/~djoyce/trig/), David E. Joyce (Clark University): the classic short trig course, built around a few clean diagrams. `[plain-html]` `[pictures]` `[exercises]`
* [Algebra/Trig Review](https://tutorial.math.lamar.edu/Extras/AlgebraTrigReview/AlgebraTrigIntro.aspx), Paul Dawkins (Lamar University): a fast refresher of the algebra and trig that calculus assumes. `[plain-html]` `[exercises]`
* [Precalculus](https://www.themathpage.com/aPreCalc/precalculus.htm), Lawrence Spector (TheMathPage): functions, logs, and polynomials in the same question-and-reveal style. `[plain-html]` `[exercises]`

### 401 Calculus

Course: [course/401](../course/401/README.md).

* [Calculus Made Easy](https://www.gutenberg.org/ebooks/33283), Silvanus P. Thompson (Project Gutenberg): a 1910 book that treats a derivative as a ratio of small changes. `[free-book]` `[plain-html]`
* [Paul's Online Notes: Calculus I](https://tutorial.math.lamar.edu/Classes/CalcI/CalcI.aspx), Paul Dawkins (Lamar University): limits through integrals, one worked example after another. `[plain-html]` `[exercises]`
* [Visual Calculus](https://web.archive.org/web/20160110032905/http://archives.math.utk.edu/visual.calculus/), Lawrence S. Husch (University of Tennessee): the 1990s tutorial site with animated GIFs of limits, tangents, and Riemann sums. `[archive]` `[pictures]`
* [The Calculus Page Problems List](https://www.math.ucdavis.edu/~kouba/ProblemsList.html), Duane Kouba (UC Davis): hundreds of calculus problems with complete, line-by-line solutions. `[plain-html]` `[exercises]`

### 501 Linear Algebra, Probability and Discrete Math

Course: [course/501](../course/501/README.md).

* [MIT 18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/), Gilbert Strang (MIT OpenCourseWare): video lectures on matrices, with notes and problem sets. `[notes]` `[exercises]`
* [Introduction to Probability](https://math.dartmouth.edu/~prob/prob/prob.pdf), Charles Grinstead and J. Laurie Snell (Dartmouth): a gentle, example-driven probability book with simulations. `[free-book]` `[pdf]` `[exercises]`
* [Combinatorics and Graph Theory](https://www.whitman.edu/mathematics/cgt_online/book/), David Guichard (Whitman College): counting, recurrences, and graphs in a short HTML book. `[free-book]` `[exercises]`

### 601 Proof and Higher Math

Course: [course/601](../course/601/README.md).

* [Book of Proof](https://richardhammack.github.io/BookOfProof/), Richard Hammack (Virginia Commonwealth University): the standard free introduction to sets, logic, and proof techniques. `[free-book]` `[pdf]` `[exercises]`
* [Basic Analysis](https://www.jirka.org/ra/), Jiří Lebl (Oklahoma State University): a careful first course in real analysis. `[free-book]` `[exercises]`
* [Abstract Algebra: Theory and Applications](https://judsonbooks.org/abstract-algebra-theory-and-applications/), Thomas W. Judson: groups, rings, and fields with applications to codes and cryptography. `[free-book]` `[exercises]`
* [Topology Without Tears](https://www.topologywithouttears.net/), Sidney A. Morris: a slow, friendly first topology book. `[free-book]` `[pdf]` `[exercises]`

## By Track

### Arithmetic and Number Sense

Track: [tracks/arithmetic-and-number-sense](../tracks/arithmetic-and-number-sense/README.md). Levels: 101.

* [Skill in Arithmetic](https://www.themathpage.com/Arith/arithmetic.htm), Lawrence Spector (TheMathPage): the full arithmetic course, including mental math tricks. `[plain-html]` `[exercises]`
* [Math Is Fun: The World of Numbers](https://www.mathsisfun.com/numbers/index.html), Rod Pierce: short illustrated pages on every number topic. `[pictures]` `[exercises]`
* [Egyptian Fractions](https://r-knott.surrey.ac.uk/Fractions/egyptian.html), Ron Knott (University of Surrey): writes fractions as sums of unit fractions, the way scribes did. `[plain-html]` `[exercises]`
* [mathcentre Topics](https://www.mathcentre.ac.uk/students/topics/), mathcentre (UK universities): one-page leaflets and short tutorials on fractions, percentages, and indices. `[pdf]` `[exercises]`
* [Diagnostic Tests](https://www.math.toronto.edu/burbulla/), Dietrich Burbulla (University of Toronto): short self-tests that show which high-school topics need review. `[plain-html]` `[exercises]`

### Algebra

Track: [tracks/algebra](../tracks/algebra/README.md). Levels: 101 to 301.

* [Paul's Online Notes: Algebra](https://tutorial.math.lamar.edu/Classes/Alg/Alg.aspx), Paul Dawkins (Lamar University): equations, graphing, polynomials, exponentials, and logs. `[plain-html]` `[exercises]`
* [Free Online Algebra Course](https://www.themathpage.com/Alg/algebra.htm), Lawrence Spector (TheMathPage): algebra as a set of skills, each with a reveal-the-answer drill. `[plain-html]` `[exercises]`
* [Purplemath Lessons](https://www.purplemath.com/modules/index.htm), Elizabeth Stapel: a long-running site that explains algebra the way a tutor talks. `[plain-html]` `[exercises]`
* [Math 1010 Online](https://www.math.utah.edu/online/1010/), University of Utah: a full intermediate algebra course written as plain web pages. `[plain-html]` `[notes]` `[exercises]`
* [MathPages: Algebra](https://www.mathpages.com/home/ialgebra.htm), Kevin Brown: short essays on classic algebra questions, for curiosity rather than drills. `[plain-html]`
* [Math Is Fun: Algebra Index](https://www.mathsisfun.com/algebra/index.html), Rod Pierce: picture-first explanations of every algebra topic. `[pictures]` `[exercises]`

### Geometry

Track: [tracks/geometry](../tracks/geometry/README.md). Levels: 201.

* [Euclid's Elements](https://mathcs.clarku.edu/~djoyce/elements/elements.html), David E. Joyce (Clark University): the whole of Euclid, every proposition with a figure. `[plain-html]` `[pictures]`
* [Euclid Book I](https://personal.math.ubc.ca/~cass/euclid/), Bill Casselman (University of British Columbia): links to the 1847 Oliver Byrne color edition and other readings of Book I. `[plain-html]` `[pictures]`
* [Pythagorean Theorem and Its Many Proofs](https://www.cut-the-knot.org/pythagoras/index.shtml), Alexander Bogomolny (Cut the Knot): more than a hundred proofs, each with a diagram. `[plain-html]` `[pictures]`
* [The Geometry Junkyard](https://ics.uci.edu/~eppstein/junkyard/), David Eppstein (UC Irvine): a 1990s link garden of geometry curiosities, tilings, and polyhedra. `[plain-html]` `[pictures]`
* [Euler's Formula, V - E + F = 2](https://ics.uci.edu/~eppstein/junkyard/euler/), David Eppstein (UC Irvine): twenty proofs of one formula, a great bridge to graph theory. `[plain-html]` `[pictures]`
* [Geometry in Art and Architecture](https://math.dartmouth.edu/~matc/math5.geometry/), Dartmouth College: a course on geometry seen through buildings and paintings. `[plain-html]` `[pictures]` `[notes]`
* [Beyond the Third Dimension](https://www.math.brown.edu/tbanchof/Beyond3d/), Thomas Banchoff (Brown University): an online book on picturing four dimensions. `[pictures]` `[free-book]`
* [Visual Dictionary of Special Plane Curves](http://xahlee.info/SpecialPlaneCurves_dir/specialPlaneCurves.html), Xah Lee: a picture catalog of cycloids, spirals, and conics. `[pictures]` `[reference]`

### Trigonometry

Track: [tracks/trigonometry](../tracks/trigonometry/README.md). Levels: 301.

* [Dave's Short Trig Course](https://mathcs.clarku.edu/~djoyce/trig/), David E. Joyce (Clark University): angles, sines, cosines, and identities from a handful of figures. `[plain-html]` `[pictures]` `[exercises]`
* [Trigonometry](https://www.themathpage.com/aTrig/trigonometry.htm), Lawrence Spector (TheMathPage): a complete trig course in the question-and-reveal style. `[plain-html]` `[exercises]`
* [Math Is Fun: Trigonometry Index](https://www.mathsisfun.com/algebra/trigonometry-index.html), Rod Pierce: unit circle and triangle pages with interactive drawings. `[pictures]`
* [Trigonometric Identities Leaflet](https://www.mathcentre.ac.uk/resources/uploaded/mc-ty-trigids-2009-1.pdf), mathcentre: a short teach-yourself unit on the core identities. `[pdf]` `[exercises]`

### Calculus

Track: [tracks/calculus](../tracks/calculus/README.md). Levels: 401.

* [Calculus Made Easy](https://www.gutenberg.org/ebooks/33283), Silvanus P. Thompson: a short, plain calculus book from 1910. `[free-book]` `[plain-html]`
* [Paul's Online Notes: Calculus I](https://tutorial.math.lamar.edu/Classes/CalcI/CalcI.aspx), [Calculus II](https://tutorial.math.lamar.edu/Classes/CalcII/CalcII.aspx), [Calculus III](https://tutorial.math.lamar.edu/Classes/CalcIII/CalcIII.aspx), Paul Dawkins (Lamar University): worked examples for every calculus topic. `[plain-html]` `[exercises]`
* [Calculus I Practice Problems](https://tutorial.math.lamar.edu/Problems/CalcI/CalcI.aspx), Paul Dawkins: practice sets with full solutions. `[exercises]`
* [Visual Calculus](https://web.archive.org/web/20160110032905/http://archives.math.utk.edu/visual.calculus/), Lawrence S. Husch (University of Tennessee): animated pictures of limits, derivatives, and integrals. `[archive]` `[pictures]`
* [The Calculus Page Problems List](https://www.math.ucdavis.edu/~kouba/ProblemsList.html), Duane Kouba (UC Davis): problem sets with step-by-step solutions for every topic. `[plain-html]` `[exercises]`
* [Calculus for the Intelligent Person](https://www.math.hawaii.edu/~lee/calculus/), Lee Lady (University of Hawaii): essays that explain why calculus works, not only how. `[plain-html]` `[pdf]`
* [Elementary Calculus: An Infinitesimal Approach](https://people.math.wisc.edu/~hkeisler/calc.html), H. Jerome Keisler (University of Wisconsin): calculus with infinitely small numbers, close to how Leibniz thought. `[free-book]` `[pdf]` `[pictures]`
* [Calculus Tutorials](https://math.hmc.edu/calculus/), Harvey Mudd College: short review tutorials, each with a quiz. `[plain-html]` `[exercises]`
* [The University of Minnesota Calculus Initiative](http://www.geom.uiuc.edu/education/calc-init/), The Geometry Center: 1990s lab modules on rates, rotations, and modeling. `[plain-html]` `[pictures]`
* [An Intuitive Introduction to Limits](https://betterexplained.com/articles/an-intuitive-introduction-to-limits/), Kalid Azad (BetterExplained): limits explained as a game of accuracy. `[pictures]`
* [MIT 18.01 Single Variable Calculus](https://ocw.mit.edu/courses/18-01-single-variable-calculus-fall-2006/), David Jerison (MIT OpenCourseWare): lecture videos, notes, and exams. `[notes]` `[exercises]`
* [Math 1a: Functions and Calculus](https://people.math.harvard.edu/~knill/teaching/math1a_2011/), Oliver Knill (Harvard): a full course of one-page handouts with sketches. `[notes]` `[pictures]`

### Number Theory

Track: [tracks/number-theory](../tracks/number-theory/README.md). Levels: 501, 601.

* [The Prime Pages](https://t5k.org/), Chris Caldwell: records, proofs, and a glossary for everything about primes. `[plain-html]` `[reference]`
* [Proofs That There Are Infinitely Many Primes](https://t5k.org/notes/proofs/infinite/), Chris Caldwell (The Prime Pages): several short proofs side by side. `[plain-html]`
* [The Prime Glossary](https://t5k.org/glossary/), Chris Caldwell: one short page per term, with examples. `[plain-html]` `[reference]`
* [Dave's Numbers](https://mathcs.clarku.edu/~djoyce/numbers/), David E. Joyce (Clark University): a list of primes to 10,000, Pythagorean triples, and notes on Dedekind. `[plain-html]`
* [Math 126 Number Theory](https://mathcs.clarku.edu/~djoyce/ma126/), David E. Joyce (Clark University): course notes and exercises for a first number theory course. `[notes]` `[exercises]`
* [Number Theory Notes](https://crypto.stanford.edu/pbc/notes/numbertheory/), Ben Lynn (Stanford): crisp notes on modular arithmetic aimed at cryptography. `[plain-html]` `[notes]`
* [Elementary Number Theory](https://wstein.org/ent/), William Stein: primes, congruences, and RSA with computer examples. `[free-book]` `[pdf]`
* [Fibonacci Numbers and the Golden Section](https://r-knott.surrey.ac.uk/Fibonacci/fib.html), Ron Knott (University of Surrey): the classic hobby site on Fibonacci numbers in nature and math. `[plain-html]` `[pictures]` `[exercises]`
* [MathPages: Number Theory](https://www.mathpages.com/home/inumber.htm), Kevin Brown: dozens of short essays on classic number puzzles. `[plain-html]`
* [The On-Line Encyclopedia of Integer Sequences](https://oeis.org/), founded by N. J. A. Sloane: type in a few numbers and find the sequence. `[reference]`

### Logic and Proofs

Track: [tracks/logic-and-set-theory](../tracks/logic-and-set-theory/README.md). Levels: 501, 601.

* [Book of Proof](https://richardhammack.github.io/BookOfProof/), Richard Hammack (Virginia Commonwealth University): sets, logic, and proof methods with many exercises. `[free-book]` `[pdf]` `[exercises]`
* [Logic](https://www.math.hawaii.edu/~ramsey/Logic.html), Tom Ramsey (University of Hawaii): a plain one-page tour of AND, OR, NOT, IF-THEN, and quantifiers. `[plain-html]`
* [Gödel's Theorems](https://www.math.hawaii.edu/~dale/godel/godel.html), Dale Myers (University of Hawaii): Cantor, the Halting Problem, and Gödel in a few short pages. `[plain-html]`
* [Introduction to Proofs](https://math.berkeley.edu/~hutching/teach/proofs.pdf), Michael Hutchings (UC Berkeley): a short handout on how to read and write a proof. `[pdf]` `[notes]`
* [forall x: Calgary](https://forallx.openlogicproject.org/), P. D. Magnus and Tim Button: an introduction to formal logic with truth tables and natural deduction. `[free-book]` `[pdf]` `[exercises]`
* [Proofs in Mathematics](https://www.cut-the-knot.org/proofs/index.shtml), Alexander Bogomolny (Cut the Knot): an essay on what proofs are, with worked samples. `[plain-html]`
* [Introduction to Higher Mathematics](https://www.whitman.edu/mathematics/higher_math_online/), Patrick Keef and David Guichard (Whitman College): logic, sets, functions, and induction. `[free-book]` `[exercises]`
* [Math Is Fun: Set Theory Index](https://www.mathsisfun.com/sets/index.html), Rod Pierce: pictures of sets, Venn diagrams, and set notation. `[pictures]`

### Discrete Math and Combinatorics

Tracks: [tracks/discrete-math](../tracks/discrete-math/README.md), [tracks/combinatorics](../tracks/combinatorics/README.md). Levels: 501.

* [Combinatorics and Graph Theory](https://www.whitman.edu/mathematics/cgt_online/book/), David Guichard (Whitman College): counting, inclusion-exclusion, generating functions, and graphs. `[free-book]` `[exercises]`
* [Mathematics for Computer Science](https://courses.csail.mit.edu/6.042/spring18/mcs.pdf), Lehman, Leighton, and Meyer (MIT): the standard discrete math text for programmers. `[free-book]` `[pdf]` `[exercises]`
* [Notes on Discrete Mathematics](https://www.cs.yale.edu/homes/aspnes/classes/202/notes.pdf), James Aspnes (Yale): long, friendly notes from a computer science view. `[free-book]` `[pdf]`
* [Math 114 Discrete Mathematics](https://mathcs.clarku.edu/~djoyce/ma114/), David E. Joyce (Clark University): a plain course page with notes and assignments. `[notes]` `[exercises]`
* [Foundations of Combinatorics with Applications](https://mathweb.ucsd.edu/~ebender/CombText/), Edward Bender and S. Gill Williamson (UC San Diego): a full counting textbook in PDF chapters. `[free-book]` `[pdf]`
* [generatingfunctionology](https://www2.math.upenn.edu/~wilf/DownldGF.html), Herbert Wilf (University of Pennsylvania): the classic short book on generating functions. `[free-book]` `[pdf]`
* [A=B](https://www2.math.upenn.edu/~wilf/AeqB.html), Petkovšek, Wilf, and Zeilberger: how a computer proves sum identities. `[free-book]` `[pdf]`
* [MIT 6.042J Mathematics for Computer Science](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/), MIT OpenCourseWare: lectures and problem sets for the book above. `[notes]` `[exercises]`

### Graph Theory

Track: [tracks/graph-theory](../tracks/graph-theory/README.md). Levels: 501.

* [Graph Theory](https://diestel-graph-theory.com/), Reinhard Diestel: the standard graduate text, with a free preview of the main text for online viewing. `[free-book]`
* [MathWorld: Graph Theory](https://mathworld.wolfram.com/GraphTheory.html), Eric Weisstein: a jumping-off point into hundreds of graph definitions with drawings. `[reference]` `[pictures]`
* [Random Walks and Electric Networks](https://math.dartmouth.edu/~doyle/docs/walks/walks.pdf), Peter Doyle and J. Laurie Snell: random walks on graphs explained with resistors and current. `[free-book]` `[pdf]` `[pictures]`
* [Traveling Salesman Problem](https://www.math.uwaterloo.ca/tsp/), William Cook (University of Waterloo): history, pictures, and records for the most famous graph problem. `[pictures]`
* [Spectral Graph Theory](https://fanchung.ucsd.edu/research/revised.html), Fan Chung (UC San Diego): chapters on eigenvalues of graphs. `[pdf]` `[free-book]`
* [Lecture Slides for Algorithm Design](https://www.cs.princeton.edu/~wayne/kleinberg-tardos/), Kevin Wayne (Princeton): slides for graph algorithms such as BFS, shortest paths, and flows. `[pictures]` `[notes]`

### Probability

Track: [tracks/probability](../tracks/probability/README.md). Levels: 501.

* [Introduction to Probability](https://math.dartmouth.edu/~prob/prob/prob.pdf), Grinstead and Snell (Dartmouth): example-first probability with simulations. `[free-book]` `[pdf]` `[exercises]`
* [Probability: Rolling Two Dice](https://www.math.hawaii.edu/~ramsey/Probability/TwoDice.html), Tom Ramsey (University of Hawaii): a single plain page that builds the 36-outcome table. `[plain-html]` `[pictures]`
* [Random: Probability, Mathematical Statistics, Stochastic Processes](https://www.randomservices.org/random/), Kyle Siegrist (University of Alabama in Huntsville): a large web text with small simulation apps. `[free-book]` `[exercises]`
* [Seeing Theory](https://seeing-theory.brown.edu/), Brown University: animated visual introductions to probability and statistics. `[pictures]`
* [Univariate Distribution Relationship Chart](https://www.math.wm.edu/~leemis/chart/UDR/UDR.html), Lawrence Leemis (William and Mary): one diagram that connects 76 probability distributions. `[pictures]` `[reference]`
* [Optimal Stopping and Applications](https://www.math.ucla.edu/~tom/Stopping/Contents.html), Thomas Ferguson (UCLA): the secretary problem and friends, in plain HTML chapters. `[free-book]` `[exercises]`
* [Probability Theory and Stochastic Processes with Applications](https://people.math.harvard.edu/~knill/probability/), Oliver Knill (Harvard): a deeper free text for after the basics. `[free-book]` `[pdf]`
* [MIT 18.600 Probability and Random Variables](https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/), Scott Sheffield (MIT OpenCourseWare): lecture slides and problem sets. `[notes]` `[exercises]`

### Statistics

Track: [tracks/statistics](../tracks/statistics/README.md). Levels: 501.

* [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/), NIST: an engineering stats handbook with process monitoring and control charts. `[plain-html]` `[pictures]` `[reference]`
* [Online Statistics Education](https://onlinestatbook.com/2/index.html), David Lane (Rice University): a full intro statistics book in HTML. `[free-book]` `[exercises]`
* [SticiGui](https://www.stat.berkeley.edu/~stark/SticiGui/Text/toc.htm), Philip Stark (UC Berkeley): intro statistics with interactive figures and a skeptical voice. `[free-book]` `[pictures]`
* [OpenIntro Statistics](https://www.openintro.org/book/os/), Diez, Çetinkaya-Rundel, and Barr: a widely used free intro textbook. `[free-book]` `[pdf]` `[exercises]`
* [All of Statistics](https://www.stat.cmu.edu/~larry/all-of-statistics/), Larry Wasserman (Carnegie Mellon): the book page for a compact tour of statistics, with data and errata. `[reference]`
* [Math Is Fun: Data](https://www.mathsisfun.com/data/index.html), Rod Pierce: mean, median, standard deviation, and charts in pictures. `[pictures]` `[exercises]`
* [Gallery of Data Visualization](https://datavis.ca/gallery/), Michael Friendly (York University): famous good and bad statistical charts. `[pictures]`

### Linear Algebra

Track: [tracks/linear-algebra](../tracks/linear-algebra/README.md). Levels: 501.

* [MIT 18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/), Gilbert Strang (MIT OpenCourseWare): video lectures, notes, and problem sets. `[notes]` `[exercises]`
* [18.06 Course Page](https://web.mit.edu/18.06/www/), MIT: the live course page with problem sets and old exams. `[exercises]`
* [Linear Algebra](https://hefferon.net/linearalgebra/), Jim Hefferon (Saint Michael's College): a complete free text with full answers to exercises. `[free-book]` `[pdf]` `[exercises]`
* [A First Course in Linear Algebra](https://linear.pugetsound.edu/), Robert Beezer (University of Puget Sound): an open HTML text with many examples. `[free-book]` `[exercises]`
* [Introduction to Applied Linear Algebra](https://web.stanford.edu/~boyd/vmls/), Stephen Boyd and Lieven Vandenberghe (Stanford): vectors, matrices, and least squares for data work. `[free-book]` `[pdf]`
* [An Intuitive Guide to Linear Algebra](https://betterexplained.com/articles/linear-algebra-guide/), Kalid Azad (BetterExplained): matrices as spreadsheets of operations. `[pictures]`
* [Math 115A Linear Algebra](https://www.math.ucla.edu/~tao/resource/general/115a.3.02f/), Terence Tao (UCLA): a plain 2002 course page with notes for a proof-based course. `[notes]`
* [Kenneth Kuttler Books](https://klkuttler.com/), Kenneth Kuttler: free texts on linear algebra, calculus, and analysis. `[free-book]` `[pdf]`

### Differential Equations

Track: [tracks/differential-equations](../tracks/differential-equations/README.md). Levels: 401, 601.

* [Paul's Online Notes: Differential Equations](https://tutorial.math.lamar.edu/Classes/DE/DE.aspx), Paul Dawkins (Lamar University): first-order, second-order, Laplace, and series methods. `[plain-html]` `[exercises]`
* [Notes on Diffy Qs](https://www.jirka.org/diffyqs/), Jiří Lebl: a free engineering-style ODE text. `[free-book]` `[exercises]`
* [MIT 18.03 Differential Equations](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/), Arthur Mattuck and others (MIT OpenCourseWare): lectures and problem sets. `[notes]` `[exercises]`
* [William Trench Free Texts](https://ramanujan.math.trinity.edu/wtrench/texts/index.shtml), William Trench (Trinity University): free books on ODEs, real analysis, and linear algebra. `[free-book]` `[pdf]`
* [Ordinary Differential Equations and Dynamical Systems](https://www.mat.univie.ac.at/~gerald/ftp/book-ode/), Gerald Teschl (University of Vienna): a free graduate ODE book. `[free-book]` `[pdf]`
* [MathPages: Calculus and Differential Equations](https://www.mathpages.com/home/icalculu.htm), Kevin Brown: short essays on classic ODE puzzles. `[plain-html]`

### Complex Analysis

Track: [tracks/complex-analysis](../tracks/complex-analysis/README.md). Levels: 601.

* [Complex Numbers](https://mathcs.clarku.edu/~djoyce/complex/), David E. Joyce (Clark University): a short illustrated introduction to complex arithmetic and geometry. `[plain-html]` `[pictures]`
* [A Visual, Intuitive Guide to Imaginary Numbers](https://betterexplained.com/articles/a-visual-intuitive-guide-to-imaginary-numbers/), Kalid Azad (BetterExplained): i as a rotation. `[pictures]`
* [Intuitive Understanding of Euler's Formula](https://betterexplained.com/articles/intuitive-understanding-of-eulers-formula/), Kalid Azad (BetterExplained): $e^{i\theta}$ as motion around a circle. `[pictures]`
* [Complex Analysis](https://cain.math.gatech.edu/winter99/complex.html), George Cain (Georgia Tech): a short free undergraduate text in PDF chapters. `[free-book]` `[pdf]`
* [A First Course in Complex Analysis](https://matthbeck.github.io/complex.html), Beck, Marchesi, Pixton, and Sabalka: a free modern undergraduate text. `[free-book]` `[pdf]` `[exercises]`
* [MIT 18.04 Complex Variables with Applications](https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/), MIT OpenCourseWare: notes and problem sets. `[notes]` `[exercises]`

### Real Analysis

Track: [tracks/real-analysis](../tracks/real-analysis/README.md). Levels: 601.

* [Basic Analysis](https://www.jirka.org/ra/), Jiří Lebl: a careful free first course. `[free-book]` `[exercises]`
* [Introduction to Analysis Notes](https://www.math.ucdavis.edu/~hunter/intro_analysis_pdf/intro_analysis.html), John Hunter (UC Davis): clean chapter PDFs on sequences, continuity, and differentiability. `[notes]` `[pdf]`
* [Course 121 Analysis](https://www.maths.tcd.ie/~dwilkins/Courses/121/), David Wilkins (Trinity College Dublin): plain lecture notes from a first-year analysis course. `[notes]` `[pdf]`
* [A Course of Pure Mathematics](https://www.gutenberg.org/ebooks/38769), G. H. Hardy (Project Gutenberg): a 1908 book on rigorous calculus. `[free-book]`
* [Math 131AH Honors Analysis](https://www.math.ucla.edu/~tao/resource/general/131ah.1.03w/), Terence Tao (UCLA): a 2003 course page with notes that grew into his Analysis book. `[notes]`
* [MIT 18.100A Introduction to Analysis](https://ocw.mit.edu/courses/18-100a-introduction-to-analysis-fall-2012/), MIT OpenCourseWare: lecture notes and problem sets. `[notes]` `[exercises]`

### Abstract Algebra

Track: [tracks/abstract-algebra](../tracks/abstract-algebra/README.md). Levels: 601.

* [Abstract Algebra: Theory and Applications](https://judsonbooks.org/abstract-algebra-theory-and-applications/), Thomas W. Judson: the standard free undergraduate text. `[free-book]` `[exercises]`
* [Math 225 Modern Algebra I](https://mathcs.clarku.edu/~djoyce/ma225/), David E. Joyce (Clark University): course notes and exercises for a first algebra course. `[notes]` `[exercises]`
* [Math 4120 Modern Algebra](https://www.math.clemson.edu/~macaule/classes/m20_math4120/), Matthew Macauley (Clemson): lecture slides full of Cayley diagrams and pictures of groups. `[notes]` `[pictures]`
* [Undergraduate Course Materials](https://math.berkeley.edu/~gbergman/ug.hndts/), George Bergman (UC Berkeley): handouts that patch common gaps in algebra courses. `[notes]`
* [MIT 18.701 Algebra I](https://ocw.mit.edu/courses/18-701-algebra-i-fall-2010/), Michael Artin (MIT OpenCourseWare): notes and problem sets. `[notes]` `[exercises]`
* [MathWorld: Group](https://mathworld.wolfram.com/Group.html), Eric Weisstein: a quick definition with links to every named group. `[reference]`

### Topology

Track: [tracks/topology](../tracks/topology/README.md). Levels: 601.

* [Topology Without Tears](https://www.topologywithouttears.net/), Sidney A. Morris: a slow, friendly first book. `[free-book]` `[pdf]` `[exercises]`
* [Course 212 Topology](https://www.maths.tcd.ie/~dwilkins/Courses/212/), David Wilkins (Trinity College Dublin): plain lecture notes on metric and topological spaces. `[notes]` `[pdf]`
* [An Introduction to Set Theory and Topology](https://www.math.wustl.edu/~freiwald/), Ronald Freiwald (Washington University in St. Louis): a free text on sets, cardinality, and metric and topological spaces, linked from his home page. `[free-book]` `[pdf]`
* [Algebraic Topology](https://pi.math.cornell.edu/~hatcher/AT/ATpage.html), Allen Hatcher (Cornell): the standard free graduate text, with many pictures. `[free-book]` `[pdf]` `[pictures]`
* [The Knot Atlas](https://katlas.org/wiki/Main_Page), Dror Bar-Natan and Scott Morrison: a picture table of knots and their invariants. `[pictures]` `[reference]`
* [Dror Bar-Natan Image Gallery](https://www.math.toronto.edu/~drorbn/Gallery/), Dror Bar-Natan (University of Toronto): photos and drawings of knots and symmetry. `[pictures]`
* [MIT 18.901 Introduction to Topology](https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/), MIT OpenCourseWare: notes and problem sets. `[notes]` `[exercises]`

### Information Theory

Track: [tracks/information-theory](../tracks/information-theory/README.md). Levels: 501, 601.

* [A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf), Claude Shannon (1948, hosted at Harvard): the paper that founded the field, very readable in its first sections. `[pdf]`
* [Information Theory, Inference, and Learning Algorithms](https://www.inference.org.uk/itila/book.html), David MacKay (Cambridge): a free book on entropy, coding, and inference, with many figures. `[free-book]` `[pdf]` `[exercises]`
* [MIT 6.050J Information and Entropy](https://ocw.mit.edu/courses/6-050j-information-and-entropy-spring-2008/), MIT OpenCourseWare: an undergraduate course that links bits to physics. `[notes]`
* [Introduction to Coding Theory](https://www.cs.cmu.edu/~venkatg/teaching/codingtheory/), Venkatesan Guruswami (Carnegie Mellon): lecture notes on error-correcting codes. `[notes]` `[pdf]`
* [MathWorld: Entropy](https://mathworld.wolfram.com/Entropy.html), Eric Weisstein: a one-page definition. `[reference]`

### Numerical Methods

Track: [tracks/numerical-methods](../tracks/numerical-methods/README.md). Levels: 401 to 601.

* [What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html), David Goldberg (hosted by Oracle): the classic paper on rounding error. `[plain-html]`
* [The Floating-Point Guide](https://floating-point-gui.de/), Michael Borgwardt: the short version of Goldberg, for programmers. `[plain-html]`
* [Trefethen Books](https://people.maths.ox.ac.uk/trefethen/books.html), Nick Trefethen (Oxford): book pages, some with free chapters. `[reference]`
* [Approximation Theory and Approximation Practice](https://people.maths.ox.ac.uk/trefethen/ATAP/), Nick Trefethen (Oxford): approximation of functions, with code on every page. `[pictures]`
* [John Burkardt Python Source Codes](https://people.sc.fsu.edu/~jburkardt/py_src/py_src.html), John Burkardt (Florida State): hundreds of small numerical programs, each a plain page. `[plain-html]` `[reference]`
* [Netlib](https://www.netlib.org/), AT&T Bell Labs and University of Tennessee: the original archive of numerical software (LAPACK, BLAS). `[plain-html]` `[reference]`
* [MIT 18.330 Introduction to Numerical Analysis](https://ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/), Laurent Demanet (MIT OpenCourseWare): notes and problem sets. `[notes]` `[exercises]`
* [Numerical Recipes](https://numerical.recipes/), Press, Teukolsky, Vetterling, and Flannery: a standard numerical methods book; older editions read online. `[reference]`

### History of Mathematics

Folder: [history](../history/README.md). Levels: all.

* [MacTutor History of Mathematics](https://mathshistory.st-andrews.ac.uk/), University of St Andrews: biographies of every major mathematician plus topic essays. `[plain-html]` `[reference]`
* [MacTutor History Topics](https://mathshistory.st-andrews.ac.uk/HistTopics/), University of St Andrews: essays on number systems, pi, calculus, and more. `[plain-html]`
* [Babylonian Numerals](https://mathshistory.st-andrews.ac.uk/HistTopics/Babylonian_numerals/), MacTutor: base 60 explained with clay-tablet pictures. `[plain-html]` `[pictures]`
* [Famous Curves Index](https://mathshistory.st-andrews.ac.uk/Curves/), MacTutor: the history and picture of each classic curve. `[pictures]`
* [History of Mathematics](https://mathcs.clarku.edu/~djoyce/mathhist/), David E. Joyce (Clark University): a plain timeline, chronology, and reading list. `[plain-html]`
* [The History of Mathematics](https://www.maths.tcd.ie/pub/HistMath/), David Wilkins (Trinity College Dublin): transcribed original papers by Newton, Hamilton, Riemann, and others. `[plain-html]`
* [Mathematical Problems of David Hilbert](https://mathcs.clarku.edu/~djoyce/hilbert/), David E. Joyce (Clark University): the 1900 problem list with status notes. `[plain-html]`
* [Oliver Knill History Pages](https://people.math.harvard.edu/~knill/history/), Oliver Knill (Harvard): photos and notes on historic mathematical objects. `[pictures]`
* [Milestones in the History of Data Visualization](https://datavis.ca/milestones/), Michael Friendly (York University): a timeline of charts from 1600 onward. `[pictures]`

## General Purpose Sites

Use these when a lesson needs a second explanation and the track list above does not cover it.

* [Paul's Online Notes](https://tutorial.math.lamar.edu/), Paul Dawkins (Lamar University): algebra through differential equations, plus [cheat sheets](https://tutorial.math.lamar.edu/Extras/CheatSheets_Tables.aspx). `[plain-html]` `[exercises]`
* [Cut the Knot: Interactive Mathematics Miscellany and Puzzles](https://www.cut-the-knot.org/), Alexander Bogomolny: thousands of short pages on proofs, puzzles, and geometry. `[plain-html]` `[pictures]`
* [Wolfram MathWorld](https://mathworld.wolfram.com/), Eric Weisstein: the largest free math encyclopedia. `[reference]`
* [MathPages](https://www.mathpages.com/), Kevin Brown: hundreds of essays on classic problems, in plain HTML. `[plain-html]`
* [TheMathPage](https://www.themathpage.com/), Lawrence Spector: arithmetic through calculus in one plain style. `[plain-html]` `[exercises]`
* [Math Is Fun](https://www.mathsisfun.com/), Rod Pierce: picture-first explanations at a gentle pace. `[pictures]` `[exercises]`
* [BetterExplained](https://betterexplained.com/), Kalid Azad: intuition-first essays on e, logs, calculus, and more. `[pictures]`
* [The Math Doctors](https://www.themathdoctors.org/), the volunteers of Ask Dr. Math: questions and answers from the people who ran Ask Dr. Math. `[plain-html]`
* [Math Fun Facts](https://math.hmc.edu/funfacts/), Francis Su (Harvey Mudd College): short surprising facts, each with a picture and a reference. `[plain-html]` `[pictures]`
* [The Free Lecture Notes Page](https://people.math.wisc.edu/~angenent/Free-Lecture-Notes/), Sigurd Angenent (University of Wisconsin): free notes for calculus, linear algebra, and ODE courses. `[notes]` `[pdf]`
* [Online Texts](https://cain.math.gatech.edu/textbooks/onlinebooks.html), George Cain (Georgia Tech): an old, hand-kept list of free math books. `[plain-html]` `[reference]`
* [What's New](https://terrytao.wordpress.com/), Terence Tao (UCLA): research blog with clear expository posts and [career advice](https://terrytao.wordpress.com/career-advice/). `[notes]`
* [This Week's Finds in Mathematical Physics](https://math.ucr.edu/home/baez/twf.html), John Baez (UC Riverside): a 1993-2010 column, an early math blog in plain text. `[plain-html]`
* [Feature Column](https://www.ams.org/publicoutreach/feature-column/), American Mathematical Society: monthly essays on math for a general reader. `[pictures]`

## Keeping the Links Alive

Run the checker from the repository root:

```txt
go run ./resources/linkcheck/main.go            # every link with its status
go run ./resources/linkcheck/main.go -failed    # only links that need attention
```

The program reads every `resources/*.md` file, fetches each URL once, and prints `OK`, `OK-CERT`, `BLOCKED`, `MOVED`, or `DEAD`. `OK-CERT` means the old university server has an expired or mismatched certificate. The page still loads in a browser after a warning.

When a link dies, search the Internet Archive at `web.archive.org` for the old address before you replace it. Many 1990s professor pages survive there intact, the way [Visual Calculus](https://web.archive.org/web/20160110032905/http://archives.math.utk.edu/visual.calculus/) does.

### Last Check

Run on 2026-10-11 with `-failed` (every link not shown is `OK`). The Internet Archive and a few university servers sometimes answer a burst of requests with `429` or `403`. Rerun the checker, or open the link in a browser, before you remove it.

```txt
Checked 201 unique URLs: OK 201
```

### Sites Checked and Left Out

These well-known sites failed verification from a script in October 2026. Try them in a browser:

* S.O.S. Math (`sosmath.com`): the domain now redirects to an unrelated advertising site. Do not use it.
* Ask Dr. Math archive (`mathforum.org`): the old host is down. NCTM holds the archive behind a free account. The Math Doctors (above) continue the service.
* Visual Calculus original host (`archives.math.utk.edu`): the host no longer resolves. Use the archived copy above.
* Project Euler (`projecteuler.net`): answers scripts with 401 or 403. It is a well-known set of programming math problems.
* The Feynman Lectures chapter pages (`feynmanlectures.caltech.edu`): chapter pages block scripts.
* John Beachy and Dave Rusin pages at Northern Illinois University (`math.niu.edu/~beachy`, `~rusin`): the pages return 404 or certificate errors.
