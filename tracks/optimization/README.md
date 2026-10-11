# Optimization Track

**Track:** Optimization · **Span:** beginner to advanced · **Course levels:** [401 Calculus](../../course/401/README.md) (derivatives, gradients), [501 Linear Algebra, Probability and Discrete Math](../../course/501/README.md) (linear systems, graphs)
**Prerequisites:** plotting points and solving a pair of linear equations from [201](../../course/201/README.md). The early rungs use the derivative from the [Calculus Track](../calculus/README.md), and the linear programming rungs lean on the [Linear Algebra Track](../linear-algebra/README.md). Each rung defines what it needs.
**Files:** this README, [cards.tsv](cards.tsv) for Anki, [code/main.go](code/main.go), and the diagrams in [img/](img/).

## What the Field Studies

Optimization is the math of picking the best option. Every problem in the field has three parts:

* **Decision variables:** the knobs you control, such as the number of replicas or the size of a node pool.
* **Objective:** the one number you want as small or as large as possible, such as cost per hour or jobs per hour.
* **Constraints:** the rules a plan must obey, such as "fit in 10 CPU" or "finish before the maintenance window closes".

A plan that obeys every constraint is **feasible**. The best feasible plan is **optimal**. The field asks two questions about every problem: what does the best plan look like, and how fast can a computer find it? The answers depend on the shape of the problem. Smooth bowls are easy. Straight-edged regions are easy. Whole-number choices are hard, and much of real scheduling lives there.

## Why It Matters

You already optimize for a living. You mostly do it by hand:

* **Capacity planning:** the cheapest instance mix that covers CPU and memory demand is a linear program.
* **Kubernetes scheduling:** placing pods on nodes is bin packing. The scheduler scores nodes with strategies named `LeastAllocated` (spread out) and `MostAllocated` (pack tight).
* **Autoscaling:** too few replicas costs latency, too many costs money. The best count sits at the bottom of a curve.
* **On-call rotations and maintenance windows:** rules like "not the same person twice in a row" and "the database job runs before the app job" are constraints for a constraint solver.
* **Machine learning:** training a model is gradient descent on a loss function.
* **Routing:** shortest paths and maximum flows from the [Graph Theory Track](../graph-theory/README.md) are optimization problems with fast special-purpose algorithms.

## Concept Map

<!-- diagram: type=concept-map tiers=beginner,intermediate,advanced nodes=12 caption="Optimization concepts with prerequisite arrows" -->
![Concept map of optimization. What Optimizing Means leads to Extrema and Flat Tops, Convexity, and Linear Programming. Convexity leads to Gradient Descent, then Gradients and Contour Maps, then Lagrange Multipliers. Linear Programming leads to the Simplex Method, then Duality and Shadow Prices, which Lagrange Multipliers also feed. Linear Programming leads to Integer Programming, which leads to Bin Packing and Scheduling and to Constraint Solvers.](img/concept-map.svg)

Read the map top to bottom. An arrow from A to B means learn A first. Start at the orange box. The map has two branches. The left branch handles straight-edged problems: linear programs and their whole-number cousins. The right branch handles smooth curved problems with calculus. Duality is where they meet.

## Signature Diagram

<!-- diagram: type=lp-region constraints="2x+y<=10,x+3y<=15" objective="3x+4y" levels=12,20,25 caption="Feasible region and objective lines of a two-variable linear program" -->
![A linear program drawn on a grid. The gray feasible region is a four-sided polygon with corners (0, 0), (5, 0), (3, 4) and (0, 5), cut out by the lines 2x + y = 10 for CPU and x + 3y = 15 for memory. Dotted parallel lines show 3x + 4y = 12 and 3x + 4y = 20 crossing the region. The orange line 3x + 4y = 25 touches the region only at the corner (3, 4), marked as best. An orange arrow labeled better points up and to the right. Corner values: (0, 0) is 0, (5, 0) is 15, (0, 5) is 20, (3, 4) is 25.](img/lp-feasible-region.svg)

Two batch jobs share a cluster with 10 CPU cores and 15 GB of memory. A type A job needs 2 cores and 1 GB and earns 3 points. A type B job needs 1 core and 3 GB and earns 4 points. Every mix that fits is a point in the gray region. Every line of equal value, $3x + 4y = k$, is parallel to the others. Slide the line in the better direction until it is about to leave the region. The last point it touches is the best plan: 3 jobs of type A and 4 of type B, worth 25.

The best plan of a linear program always includes a corner. That one fact turns an infinite search into a short list of corners to check, and the whole simplex method grows from it.

## The Concept Ladder

### Beginner

#### 1. What Optimizing Means

Start with a fence. You have 40 m of fence and want the rectangular pen with the most area. The **decision variable** is the width $x$. The **constraint** is the fence: two widths and two heights use 40 m, so the height is $20 - x$. The **objective** is the area. Try a few widths, plot the results, and the best one stands out at the top of a hill.

$$A(x) = x(20 - x), \qquad 0 \le x \le 20$$

<!-- diagram: type=rectangles-and-curve perimeter=40 widths=4,10,16 f="x*(20-x)" caption="Same fence, different areas" -->
![Left: three rectangles drawn to scale, each with 40 m of fence. A 4 by 16 rectangle has area 64, a 10 by 10 square in orange has area 100, and a 16 by 4 rectangle has area 64. Right: the curve of area x times 20 minus x for widths 0 to 20. It rises from 0, peaks at (10, 100), marked in orange as a flat top, and falls back to 0. The points (4, 64) and (16, 64) are marked.](img/fence-area.svg)

The square wins. Note what the top of the hill looks like: flat. That flatness is the key to the next rung.

Course link: [201 Algebra I and Geometry](../../course/201/README.md) for functions and area.

#### 2. Extrema and Flat Tops

An **extremum** is a maximum or a minimum. A **local** maximum beats its neighbors. A **global** maximum beats every point in the allowed range. At a smooth local extremum inside the range, the tangent line is flat: the derivative is zero. Those points are **critical points**. But the best value can also sit at an end of the range, where the slope is anything at all. Check both kinds of candidates and compare values.

$$f'(x) = 0 \text{ at a smooth interior extremum}, \qquad f''(x) > 0 \Rightarrow \text{local min}, \quad f''(x) < 0 \Rightarrow \text{local max}$$

<!-- diagram: type=function-plot f="x^3-6x^2+9x+1" x=0.25..4.25 marks=1,3 endpoints=true signchart=true caption="Local and global extrema on a closed interval" -->
![The curve f(x) = x cubed minus 6x squared plus 9x plus 1 on the interval from 0.25 to 4.25. Orange flat tangent lines mark a local maximum at (1, 5) and a local and global minimum at (3, 1). Hollow dots mark the endpoints: f(0.25) = 2.89 and the global maximum at the right end, f(4.25) = 7.64. Below, a sign chart of the slope 3(x - 1)(x - 3) shows plus (rising) before 1, minus (falling) between 1 and 3, and plus (rising) after 3.](img/extrema-flat-tangents.svg)

The local maximum at $x = 1$ is not the global one. The right endpoint beats it. An autoscaler that only looks for flat spots misses edge cases, much like people do.

Course link: [401 Calculus: Optimization and Linear Approximation](../../course/401/04-optimization-and-linear-approximation/README.md). Related: [Calculus Track](../calculus/README.md), rung 7.

#### 3. Convexity

A function is **convex** when it is shaped like a bowl: pick any two points on the graph, join them with a straight segment (a **chord**), and the chord never dips below the graph. A region is convex when the segment between any two of its points stays inside it. Convexity is the single most useful property in the field, because in a convex problem every local minimum is a global minimum. A downhill walk cannot get stuck.

$$f(tx + (1 - t)y) \le t f(x) + (1 - t) f(y) \quad \text{for all } x, y \text{ and } 0 \le t \le 1$$

<!-- diagram: type=function-plot-pair f1="x^2" f2="0.25x^4-2x^2+0.6x+4" chords=true caption="Convex bowl versus a bumpy function with a trap" -->
![Left: the bowl f(x) = x squared with an orange chord from x = -2.5 to x = 1.5 lying above the curve, and one bottom at 0. Right: a bumpy function with two valleys. An orange chord from x = -2 to x = 1.95 passes under a hump, so the curve pokes above the chord. The deeper valley near x = -2.07 is the true bottom. The shallower valley near x = 1.92 is marked as a trap, a local minimum.](img/convex-vs-nonconvex.svg)

For a twice-differentiable function of one variable, convex means $f''(x) \ge 0$ everywhere: the slope never decreases. Sums of convex functions are convex, and so is the maximum of convex functions. Those two rules certify most convex problems you meet in practice.

Related: [Real Analysis Track](../real-analysis/README.md) for the careful definitions.

#### 4. Gradient Descent

Many functions have no formula for their minimum. Walk downhill instead. At the current point, measure the slope and take a step against it. The **step size** $\eta$ (eta, also called the **learning rate**) decides everything. Too small crawls. Too large overshoots, and past a limit each overshoot grows.

$$x_{k+1} = x_k - \eta\, f'(x_k)$$

<!-- diagram: type=iteration-panels f="(x-3)^2" x0=0 eta=0.1,0.9,1.1 caption="Gradient descent with three step sizes" -->
![Three panels of the parabola (x - 3) squared, each starting at x = 0 with orange arrows for each step. With eta 0.1 the steps creep down one side: 0, 0.60, 1.08, 1.46, 1.77. With eta 0.9 the steps jump across the valley and back while closing in: 0, 5.40, 1.08, 4.54, 1.77. With eta 1.1 the jumps grow and climb the walls: 0, 6.60, -1.32, 8.18, -3.22.](img/gradient-descent-steps.svg)

For $f(x) = (x - 3)^2$ each step multiplies the distance to the minimum by $1 - 2\eta$. With $\eta = 0.1$ the factor is 0.8. With $\eta = 0.9$ it is $-0.8$: same shrink rate, plus a bounce. With $\eta = 1.1$ it is $-1.2$, and the walk diverges. With $\eta = 0.5$ the factor is 0 and one step lands exactly on 3. Real systems never know the perfect step in advance, which is why learning-rate schedules and exponential backoff exist.

Related: [Numerical Methods Track](../numerical-methods/README.md), rung 8, for the same idea from the floating-point side.

### Intermediate

#### 5. Gradients and Contour Maps

With two or more variables, the slope becomes a vector. The **gradient** $\nabla f$ lists the partial derivatives, one per variable. It points in the direction of steepest climb, and its length says how steep. A **contour** (level curve) joins points with equal value, like the lines on a hiking map. The gradient always crosses contours at a right angle, because moving along a contour does not change the height at all.

$$\nabla f(x, y) = \left( \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right), \qquad \mathbf{x}_{k+1} = \mathbf{x}_k - \eta\, \nabla f(\mathbf{x}_k)$$

<!-- diagram: type=contour-path f="x^2+4y^2" levels=1,4,9,16 lr=0.1 start=(-3.5,1.6) caption="Contour map with gradient arrows and a descent path" -->
![Four nested ovals, the contours f = 1, 4, 9 and 16 of x squared plus 4 y squared. Black arrows on the f = 9 oval point outward, each at a right angle to the oval. An orange path starts at (-3.5, 1.6), drops quickly toward the x-axis because the y direction is steep, then creeps along the axis to the minimum at the origin.](img/contour-gradient.svg)

The bowl is steeper in $y$ than in $x$, so the walk fixes $y$ first and then crawls in $x$. Long narrow valleys slow gradient descent down. Every training run that plateaus for a while is living in one.

Course link: [401 Calculus: Multivariable Intro](../../course/401/12-multivariable-intro/README.md). Related: [Calculus Track](../calculus/README.md), rung 10.

#### 6. Lagrange Multipliers

Now add a rule that must hold exactly, such as "use exactly 40 m of fence". Picture the level curves of the objective and the curve of the constraint. Walk along the constraint. While you cross level curves, you are still improving. The best point is where a level curve just touches the constraint and does not cross it. There the two curves share a tangent, so their gradients point the same way. The stretch factor between them is the **Lagrange multiplier** $\lambda$.

$$\nabla f = \lambda\, \nabla g, \qquad g(x, y) = c$$

<!-- diagram: type=lagrange f="x*y" g="2x+y=40" levels=100,200,300 point=(10,20) caption="Level curve tangent to the constraint" -->
![A fence beside a river: maximize xy subject to 2x + y = 40. The straight constraint line runs from (0, 40) to (20, 0). Level curves xy = 100 and xy = 300 are gray. The orange level curve xy = 200 touches the line only at (10, 20), marked as best with area 200. At that point an orange arrow grad f = (20, 10) and a shorter black arrow grad g = (2, 1) point the same way, both at right angles to the line.](img/lagrange-tangent.svg)

The multiplier carries a meaning: it is the rate at which the best value improves when the constraint loosens. Here $\lambda = 10$, so one more meter of fence buys about 10 more square meters. Check: with 41 m the best area is 210.125. This price-of-a-constraint idea comes back as shadow prices in rung 9.

Related: [Linear Algebra Track](../linear-algebra/README.md) for vectors and parallel directions.

#### 7. Linear Programming

A **linear program** (LP) has a linear objective and linear constraints: no squares, no products of variables, only sums of numbers times variables. Each inequality keeps one side of a line, a **half-plane**. Stack the half-planes and their overlap is the **feasible region**, a convex polygon (a polytope in more dimensions).

$$\text{maximize } \mathbf{c}^\top \mathbf{x} \quad \text{subject to} \quad A\mathbf{x} \le \mathbf{b}, \quad \mathbf{x} \ge 0$$

<!-- diagram: type=half-plane-panels constraints="2x+y<=10,x+3y<=15" caption="Each constraint keeps a half-plane; the overlap is the region" -->
![Three panels. Left: the line 2x + y = 10 with the side containing the origin shaded, labeled CPU. Middle: the line x + 3y = 15 with the side containing the origin shaded, labeled memory. Right: the overlap with x and y at least 0, a gray four-sided region with orange corners at (0, 0), (5, 0), (3, 4) and (0, 5).](img/lp-constraints-build.svg)

To find which side of a line to keep, test the origin. If $(0, 0)$ satisfies the inequality, shade the side that holds it. The **fundamental theorem of linear programming** says: if an LP has a best value, a corner achieves it. With two variables, list the corners, plug each into the objective, and pick the best. That is the whole algorithm for small problems, and it is how Worked Example 2 prices an instance mix.

Course link: [201 Algebra I and Geometry](../../course/201/README.md) for inequalities, [501: Solving Systems with Gaussian Elimination](../../course/501/11-solving-systems-gaussian-elimination/README.md) for finding corners.

#### 8. The Simplex Method

Real LPs have thousands of variables and astronomically many corners. The **simplex method** of George Dantzig (1947) avoids listing them. Start at a corner. Look at the edges leaving it. If an edge improves the objective, walk along it to the next corner. When no edge improves, stop. Because the region is convex and the objective is linear, a corner with no better neighbor is the global best.

$$\text{corner} \to \text{better neighbor} \to \cdots \to \text{no better neighbor} = \text{optimal}$$

<!-- diagram: type=lp-path region=(0,0),(5,0),(3,4),(0,5) path=(0,0),(0,5),(3,4) caption="Simplex walks from corner to better corner" -->
![The batch-job feasible region. Orange arrows walk from the start corner (0, 0) with value 0 straight up to (0, 5) with value 20, then along the memory edge to (3, 4) with value 25, where it stops. The corner (5, 0) with value 15 is never visited. A side panel shows the pivot log from the Go program.](img/simplex-path.svg)

In algebra, each corner is a set of constraints held tight, and each step swaps one tight constraint for another. That swap is a **pivot**, the same row operation as Gaussian elimination. The program in [code/main.go](code/main.go) prints its pivots: $y$ enters first because it earns the most per unit, then $x$. Simplex is usually fast, although a carefully built cube (Klee and Minty, 1972) forces it to visit every corner.

Related: [Linear Algebra Track](../linear-algebra/README.md) for row operations.

#### 9. Duality and Shadow Prices

Every maximization LP has a twin minimization LP called its **dual**. In the batch-job problem, imagine a buyer who wants to rent your cluster. They offer $u$ per CPU core and $v$ per GB. For the offer to tempt you, renting out the resources for one type A job must pay at least the 3 points the job earns: $2u + v \ge 3$. Same for type B: $u + 3v \ge 4$. The buyer wants the cheapest such offer. Any valid offer is an upper bound on what your jobs can earn. Any valid job plan is a lower bound. At the optimum, the two meet.

$$\text{weak duality: } \mathbf{c}^\top \mathbf{x} \le \mathbf{b}^\top \mathbf{y}, \qquad \text{strong duality: } \max \mathbf{c}^\top \mathbf{x} = \min \mathbf{b}^\top \mathbf{y}$$

<!-- diagram: type=number-line range=0..50 primal=0,14,15,20 dual=30,40,45 meet=25 caption="Primal values below, dual bounds above, meeting at 25" -->
![A number line from 0 to 50. Black dots at 0, 14, 15 and 20 are values of feasible job plans such as (0, 0), (2, 2), (5, 0) and (0, 5). Hollow orange dots at 30, 40 and 45 are bounds from feasible price offers (1.5, 1), (4, 0) and (0, 3). The two sets meet at 25, marked by a dashed orange line labeled both reach 25. Notes below give the dual LP, the optimal prices u = 1 and v = 1, and the check that one more core raises the best value to 26.](img/duality-gap.svg)

The optimal dual values are **shadow prices**: what one more unit of each resource is worth. Here a core and a GB are each worth 1 point. The Go program confirms it: with 11 cores instead of 10, the best value goes from 25 to 26. A resource with slack, one that the best plan does not use up, has a shadow price of 0. That rule is **complementary slackness**, and it tells a capacity planner exactly which resource to buy more of.

Related: rung 6, where $\lambda$ played the same role for one smooth constraint.

### Advanced

#### 10. Integer Programming

Clouds sell whole instances. Schedulers place whole pods. When variables must be whole numbers, the problem is an **integer program** (IP). The feasible plans are now separate grid points, not a solid region, and the nice corner theorem breaks. Worse, rounding the LP answer can land outside the region or far from the best.

$$\text{maximize } \mathbf{c}^\top \mathbf{x} \quad \text{subject to} \quad A\mathbf{x} \le \mathbf{b}, \quad \mathbf{x} \in \mathbb{Z}_{\ge 0}^n$$

<!-- diagram: type=lattice-lp constraints="x+y<=6,5x+9y<=45" objective="5x+8y" lp=(2.25,3.75) ip=(0,5) caption="Rounding the LP optimum fails" -->
![The region x + y at most 6 and 5x + 9y at most 45, with 25 black grid points inside it. The LP best is a hollow orange circle at (2.25, 3.75) with value 41.25. Rounding to (2, 4), marked with an orange X, breaks 5x + 9y at most 45. Rounding down to (2, 3) gives only 34. The integer best is the orange dot at (0, 5) with value 40, on the orange line 5x + 8y = 40.](img/integer-lattice.svg)

**Branch and bound** fixes this without checking every point. Solve the LP. If $x = 2.25$, split into two subproblems, one with $x \le 2$ and one with $x \ge 3$, and repeat. The LP value of a subproblem is an upper bound on anything inside it. When that bound cannot beat the best whole-number plan found so far, discard the whole branch. The program finds $(0, 5)$ in 9 nodes. Integer programming is NP-hard in general, yet modern solvers handle problems with millions of variables by bounding hard and branching smart.

Related: [Computability and Complexity Track](../computability-and-complexity/README.md) for what NP-hard means, [Combinatorics Track](../combinatorics/README.md) for why the number of plans explodes.

#### 11. Bin Packing and Scheduling

**Bin packing:** put items of given sizes into as few bins of fixed capacity as possible. Pods are items, nodes are bins, CPU requests are sizes. Finding the true minimum is NP-hard, so schedulers use fast rules. **First fit** puts each item into the first bin with room. **First fit decreasing** (FFD) sorts the items from big to small first. Big items placed late find only fragments of space, so sorting helps a lot.

$$\text{nodes} \ge \left\lceil \frac{\text{total demand}}{\text{node capacity}} \right\rceil, \qquad \text{FFD} \le \tfrac{11}{9}\,\text{OPT} + \tfrac{6}{9}$$

<!-- diagram: type=bin-packing items=1,2,3,4,4,5,5,6 capacity=10 methods=first-fit,ffd caption="First fit versus first fit decreasing" -->
![Two panels of 10-CPU nodes drawn as tall boxes with pods stacked inside. Left, first fit in arrival order 1, 2, 3, 4, 4, 5, 5, 6, uses 4 nodes: (1, 2, 3, 4), (4, 5), (5) and (6), leaving 0, 1, 5 and 4 CPU free. Right, first fit decreasing with order 6, 5, 5, 4, 4, 3, 2, 1, uses 3 nodes: (6, 4), (5, 5) and (4, 3, 2, 1), each full. Big pods are orange, small pods gray.](img/bin-packing-pods.svg)

Total demand is 30 CPU, so no packing beats 3 nodes. FFD hits that floor here. The Kubernetes scheduler places one pod at a time as it arrives, so it is closer to plain first fit with a scoring rule. Its default `LeastAllocated` strategy spreads pods out for headroom. The `MostAllocated` strategy packs them tight so the cluster autoscaler can remove empty nodes. The descheduler exists partly to repack after arrival order has made a mess.

Related: [Combinatorics Track](../combinatorics/README.md), [Computability and Complexity Track](../computability-and-complexity/README.md).

#### 12. Constraint Solvers

Some problems have no objective at all, only rules: find any schedule that satisfies everything. A **constraint satisfaction problem** (CSP) has variables, a **domain** of allowed values for each, and **constraints** between them. A **constraint solver** searches by **backtracking**: assign one variable, check the rules, and back up the moment a rule breaks, skipping every completion of that partial plan. Better solvers add **propagation**: after each choice, cross off values that can no longer work.

$$\text{variables } x_i \in D_i, \qquad \text{find an assignment with every constraint } C_j(x) \text{ true}$$

<!-- diagram: type=search-tree vars=A,B,C,D domain=1..3 constraints="A,B,C all different; D<B; A!=1" caption="Backtracking search tree for a four-job schedule" -->
![A search tree with levels for jobs A, B, C and D, each tried in slots 1, 2 and 3. Gray circles with an x below them break a rule and end their branch: A = 1, B equal to A, C equal to A or B, D not before B. Black circles are partial schedules that pass. Three orange leaves are complete valid schedules: A = 2, B = 3, C = 1, D = 1; A = 2, B = 3, C = 1, D = 2; and A = 3, B = 2, C = 1, D = 1. The title notes 33 tries versus 81 full schedules for brute force.](img/constraint-search-tree.svg)

Four maintenance jobs, three slots. Jobs A, B and C share a database and need different slots. Job D must run before job B. Job A cannot run in slot 1. Backtracking tries 33 partial schedules. Brute force checks all 81 full ones. Look at the subtrees under B = 1: they die at job D, because nothing runs before slot 1. Propagation spots that at once and prunes B = 1 before trying C at all. Industrial solvers such as SAT solvers, CP-SAT and MIP solvers combine propagation, clever branching and learning from conflicts. They build sports leagues, airline crew rosters and on-call rotations.

Related: [Logic and Set Theory Track](../logic-and-set-theory/README.md) for satisfiability, [Graph Theory Track](../graph-theory/README.md) for graph coloring, which is a CSP.

## Worked Examples

### Example 1: Cheapest Replica Count

Each replica costs 50 dollars per hour. Latency penalties cost $3200/n$ dollars per hour with $n$ replicas. Find the cheapest $n$.

<!-- diagram: type=function-plot f="50n+3200/n" x=0..17 parts=true mark=8 caption="Cost of n replicas" -->
![The total cost curve 50n plus 3200 over n for n from 2 to 17, with its two parts drawn as gray dashed and dotted curves. The rising line 50n and the falling curve 3200 over n cross at n = 8, where each is 400. The total has a flat bottom at n = 8 with cost 800, marked in orange. A side table lists costs: n = 1 is 3,250, n = 4 is 1,000, n = 7 is 807.1, n = 8 is 800.0, n = 9 is 805.6, n = 16 is 1,000.](img/replica-cost-curve.svg)

```txt
  C(n)   = 50n + 3200/n                       server cost plus latency penalty
  C'(n)  = 50 - 3200/n^2                      derivative of each term
  50 - 3200/n^2 = 0                           flat top or flat bottom
  n^2    = 3200 / 50 = 64                     solve for n^2
  n      = 8                                  n must be positive
  C''(n) = 6400/n^3 > 0                       curve bends up: a minimum
  C(8)   = 400 + 400 = 800 dollars per hour   plug in
```

At the best point the two costs are equal. That is a pattern: when one cost grows linearly and the other shrinks like $1/n$, the best balance spends the same on both. Also note the flat bottom: 7 or 9 replicas cost only a few dollars more, so pick the one with the better failure story.

### Example 2: Cheapest Instance Mix

A compute instance has 8 CPU, 16 GB and costs \$0.34 per hour. A memory instance has 4 CPU, 32 GB and costs \$0.25 per hour. You need at least 64 CPU and 192 GB. Let $c$ and $m$ count the instances.

<!-- diagram: type=lp-region sense=min constraints="8c+4m>=64,16c+32m>=192" objective="0.34c+0.25m" caption="Cost-minimizing instance mix" -->
![The feasible region for the instance mix is gray and unbounded upward and to the right, above the lines 8c + 4m = 64 and 16c + 32m = 192. Corners: (0, 16) costs 4.00 dollars, (12, 0) costs 4.08 dollars, and the orange hollow corner (6.67, 2.67) costs 2.93 dollars, where the orange cost line 0.34c + 0.25m = 2.93 touches. A dashed line marks cost 4.00. The orange dot (6, 4) is the best whole-number mix at 3.04 dollars.](img/instance-mix-lp.svg)

```txt
  minimize 0.34c + 0.25m                       hourly cost
  8c + 4m   >= 64   ->  2c + m  >= 16          CPU, divide by 4
  16c + 32m >= 192  ->  c + 2m  >= 12          memory, divide by 16
  corner on m-axis: (0, 16)   cost 4.00        c = 0 in the CPU line
  corner on c-axis: (12, 0)   cost 4.08        m = 0 in the memory line
  2c + m = 16 and c + 2m = 12                  where the two lines meet
  m = 16 - 2c, so c + 32 - 4c = 12             substitute
  c = 20/3 = 6.67, m = 8/3 = 2.67              solve
  cost = 0.34(6.67) + 0.25(2.67) = 2.93        cheapest corner
  whole instances: try (6, 4)                  near the corner, both rules hold
  check: 48 + 16 = 64 CPU, 96 + 128 = 224 GB   feasible
  cost = 2.04 + 1.00 = 3.04 per hour           best whole mix (code confirms)
```

The mix beats both pure fleets by about 25%. The fractional answer is not buyable, and the whole-number answer is not found by rounding the corner. $(7, 3)$ also works but costs \$3.13.

### Example 3: Fence Along a River With Lagrange

Fence three sides of a rectangle; a river forms the fourth. You have 40 m. The two short sides are $x$, the long side is $y$.

```txt
  maximize f = xy                              area
  subject to g = 2x + y = 40                   fence used
  grad f = (y, x),  grad g = (2, 1)            partial derivatives
  y = 2 lambda,  x = lambda                    grad f = lambda grad g
  y = 2x                                       eliminate lambda
  2x + 2x = 40, so x = 10                      put into the constraint
  y = 20, area = 200, lambda = 10              read off the rest
  check: with 41 m, area = 10.25 x 20.5        same method
       = 210.125, a gain of about 10           lambda is the price of 1 m
```

### Example 4: Pack Pods with First Fit Decreasing

Pods request 1, 2, 3, 4, 4, 5, 5 and 6 CPU. Nodes have 10 CPU.

```txt
  total = 30 CPU, floor = ceil(30/10) = 3 nodes     lower bound
  sort: 6, 5, 5, 4, 4, 3, 2, 1                      big first
  6 -> node 1 (free 4)                              no nodes yet, open one
  5 -> node 2 (free 5)                              does not fit node 1
  5 -> node 2 (free 0)                              first node with room
  4 -> node 1 (free 0)                              fits node 1 exactly
  4 -> node 3 (free 6)                              nodes 1 and 2 are full
  3 -> node 3 (free 3)                              first node with room
  2 -> node 3 (free 1)                              first node with room
  1 -> node 3 (free 0)                              first node with room
  3 nodes used = lower bound, so this is optimal
```

In arrival order, first fit needs 4 nodes: the small pods fill node 1, and the two 5s and the 6 cannot share. Same pods, same rule, one sort, one fewer node.

## Big Theorems to Know

* **Extreme Value Theorem:** a continuous function on a closed, bounded interval reaches a maximum and a minimum.
* **Fermat Theorem on Critical Points:** at an interior extremum of a differentiable function, the derivative is zero.
* **Local Equals Global for Convex Problems:** every local minimum of a convex function over a convex set is a global minimum.
* **Lagrange and KKT Conditions:** at a constrained optimum, the objective gradient is a combination of constraint gradients. The Karush-Kuhn-Tucker conditions extend this to inequality constraints.
* **Fundamental Theorem of Linear Programming:** if an LP has an optimal value, some corner of the feasible region achieves it.
* **Weak and Strong Duality:** every feasible dual value bounds every feasible primal value, and at the optimum they are equal.
* **Complementary Slackness:** a constraint with slack has a shadow price of zero, and a positive shadow price means the constraint is tight.
* **Polynomial-Time LP (Khachiyan 1979, Karmarkar 1984):** linear programs are solvable in polynomial time, by the ellipsoid method and by interior-point methods.
* **NP-Hardness of Integer Programming and Bin Packing:** no known algorithm solves every instance in polynomial time, and finding one proves P = NP.
* **Gradient Descent Rate:** for a convex function whose slope changes at most at rate $L$, step size $1/L$ gives $f(x_k) - f^* \le \dfrac{L \lVert x_0 - x^* \rVert^2}{2k}$.

## Open Problems and Fun Facts

* **The homework story:** as a graduate student, Dantzig arrived late to a statistics class, copied two problems from the board, and solved them as homework. They were famous unsolved problems.
* **A Nobel for linear programming:** Leonid Kantorovich and Tjalling Koopmans shared the 1975 economics prize for the theory of optimal allocation of resources. Dantzig, oddly, did not share it.
* **The diet problem:** in 1945 George Stigler looked for the cheapest diet meeting nutritional needs, an early LP. His answer leaned heavily on wheat flour, cabbage and dried navy beans. Optimal is not the same as appetizing.
* **Open problem:** is there a strongly polynomial algorithm for linear programming, with a step count that depends only on the number of variables and constraints and not on the size of the numbers? Steve Smale listed it among his problems for the 21st century.
* **Open problem:** the polynomial Hirsch conjecture. Francisco Santos disproved the original Hirsch conjecture on the diameter of polytopes in 2010, but nobody knows whether every polytope has a short corner-to-corner path of polynomial length.
* **Bin packing with a tight bound:** the bound $\text{FFD} \le \frac{11}{9}\text{OPT} + \frac{6}{9}$ took decades to pin down. György Dósa settled the exact additive constant in 2007.

## Starter Problems

1. You have 60 m of fence for a rectangular pen. What size gives the most area, and what is that area?
2. Find the minimum of $f(x) = x^2 - 6x + 11$ and where it happens.
3. Is $f(x) = |x|$ convex? Does it have a flat top or flat bottom where its minimum sits?
4. Run gradient descent on $f(x) = x^2$ with $\eta = 0.25$ from $x_0 = 8$. Give the next three points. For which $\eta$ does the walk diverge?
5. Maximize $x + y$ subject to $x + 2y \le 8$, $3x + y \le 9$, $x, y \ge 0$. List the corners.
6. In the batch-job LP, memory grows from 15 GB to 18 GB. Use the shadow price $v = 1$ to predict the new best value, then check by solving.
7. Pack pods of 7, 6, 4 and 3 CPU onto 10-CPU nodes with first fit decreasing. How many nodes, and is that optimal?

<details>
<summary>Answers</summary>

1. A 15 m by 15 m square, area 225 m². Area $x(30 - x)$ peaks at $x = 15$.
2. $f'(x) = 2x - 6 = 0$ gives $x = 3$ and $f(3) = 9 - 18 + 11 = 2$. Since $f'' = 2 > 0$ it is the minimum.
3. Yes, it is convex: every chord lies on or above the V shape. Its minimum at $x = 0$ is a sharp corner where the derivative does not exist. That is why the candidate list includes points with no derivative.
4. Each step is $x - 0.25 \cdot 2x = 0.5x$: 4, 2, 1. The factor is $1 - 2\eta$, so the walk diverges when $|1 - 2\eta| > 1$, that is when $\eta > 1$.
5. Corners $(0, 0)$, $(3, 0)$, $(0, 4)$ and $(2, 3)$, the last from solving $x + 2y = 8$ and $3x + y = 9$. Values 0, 3, 4 and 5. The best is $(2, 3)$ with value 5.
6. Prediction: $25 + 3 \times 1 = 28$. Check: $2x + y = 10$ and $x + 3y = 18$ give $x = 2.4$, $y = 5.2$, value $7.2 + 20.8 = 28$.
7. Sorted 7, 6, 4, 3: 7 opens node 1, 6 opens node 2, 4 joins node 2, 3 joins node 1. Two nodes, both full. Total demand 20 means at least 2 nodes, so it is optimal.

</details>

## Code Corner

[code/main.go](code/main.go) finds the cheapest replica count, runs gradient descent with four step sizes, checks the Lagrange fence, solves the batch-job LP with a small simplex method and reads off shadow prices, prices the instance mix by corners, solves the integer program by branch and bound, packs pods with first fit and FFD, and backtracks through the maintenance schedule. Run it with `go run main.go` inside `code/`.

```txt
== Cheapest replica count: C(n) = 50n + 3200/n ==
n =  1  cost = 3250.0
n =  4  cost = 1000.0
n =  7  cost =  807.1
n =  8  cost =  800.0
n =  9  cost =  805.6
n = 16  cost = 1000.0
scan minimum: n = 8, cost = 800.0
calculus: C'(n) = 50 - 3200/n^2 = 0 gives n = sqrt(64) = 8

== Gradient descent on f(x) = (x - 3)^2 from x = 0 ==
eta 0.1: first steps 0.600, 1.080, 1.464, 1.771 ... after 20 steps x = 2.9654
eta 0.5: first steps 3.000, 3.000, 3.000, 3.000 ... after 20 steps x = 3.0000
eta 0.9: first steps 5.400, 1.080, 4.536, 1.771 ... after 20 steps x = 2.9654
eta 1.1: first steps 6.600, -1.320, 8.184, -3.221 ... after 20 steps x = -112.0128

== Fence by a river: maximize xy with 2x + y = L ==
L = 40: x = 10.000, y = 20.000, area = 200.000
L = 41: x = 10.250, y = 20.500, area = 210.125
extra area from 1 more meter = 10.125, close to lambda = 10

== Simplex: maximize 3x + 4y, 2x + y <= 10 (CPU), x + 3y <= 15 (memory) ==
  corner 0: x,y = (0, 0), value 0.00
  pivot: y enters, s2 leaves
  corner 1: x,y = (0, 5), value 20.00
  pivot: x enters, s1 leaves
  corner 2: x,y = (3, 4), value 25.00
optimum x = (3, 4), value = 25.00
shadow prices (dual): CPU u = 1.00, memory v = 1.00
dual check: 2u + v = 3.00 >= 3, u + 3v = 4.00 >= 4, 10u + 15v = 25.00
one more CPU core: value 25.00 -> 26.00

== Cheapest instance mix: minimize 0.34c + 0.25m ==
   need 8c + 4m >= 64 CPU and 16c + 32m >= 192 GB
  corner (c, m) = (6.667, 2.667): $2.933 per hour
  corner (c, m) = (0.000, 16.000): $4.000 per hour
  corner (c, m) = (12.000, 0.000): $4.080 per hour
best whole instances: c = 6, m = 4, $3.04 per hour

== Integer program: maximize 5x + 8y, x + y <= 6, 5x + 9y <= 45, x, y whole ==
LP relaxation: x = (2.25, 3.75), value 41.25
rounded (2, 4): 5x + 9y = 46 > 45, infeasible
  x in [0, inf], y in [0, inf]: LP 41.25 at (2.25, 3.75), branch on x
    x in [0, 2], y in [0, inf]: LP 41.11 at (2, 3.89), branch on y
      x in [0, 2], y in [0, 3]: whole-number point (2, 3), value 34, new best
      x in [0, 2], y in [4, inf]: LP 41.00 at (1.8, 4), branch on x
        x in [0, 1], y in [4, inf]: LP 40.56 at (1, 4.44), branch on y
          x in [0, 1], y in [4, 4]: whole-number point (1, 4), value 37, new best
          x in [0, 1], y in [5, inf]: whole-number point (0, 5), value 40, new best
        x in [2, 2], y in [4, inf]: infeasible
    x in [3, inf], y in [0, inf]: LP 39.00 at (3, 3), cannot beat 40, prune
branch and bound: best (0, 5), value 40, 9 nodes
brute force over 25 feasible points: best value 40

== Packing pods (CPU) [1 2 3 4 4 5 5 6] onto nodes of 10 CPU ==
lower bound: ceil(30 / 10) = 3 nodes
first fit, arrival order:  4 nodes [[1 2 3 4] [4 5] [5] [6]]
first fit decreasing:      3 nodes [[6 4] [5 5] [4 3 2 1]]

== Constraint solver: 4 jobs, 3 slots ==
brute force: 81 full schedules checked, 3 valid
backtracking: 33 partial schedules tried
  A=2 B=3 C=1 D=1
  A=2 B=3 C=1 D=2
  A=3 B=2 C=1 D=1
```

Read the branch-and-bound log from the bottom up. The last line, the branch $x \ge 3$, has an LP bound of 39. The best whole-number plan found so far is worth 40. The solver discards that whole branch without looking inside it. That one comparison is the reason integer solvers finish at all.

## Flashcards

[cards.tsv](cards.tsv) holds the key definitions and theorems for Anki import.

## Resources

* [Paul's Online Math Notes: Lagrange Multipliers](https://tutorial.math.lamar.edu/Classes/CalcIII/LagrangeMultipliers.aspx): patient worked examples for rungs 5 and 6.
* [Boyd and Vandenberghe: Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/): the standard text on convexity and duality, with the full book available on the page.
* [MIT OCW 15.053 Optimization Methods in Management Science](https://ocw.mit.edu/courses/15-053-optimization-methods-in-management-science-spring-2013/): free lectures on linear programming, simplex, duality and integer programming.
* [MacTutor: George Dantzig](https://mathshistory.st-andrews.ac.uk/Biographies/Dantzig_George/): the life of the inventor of the simplex method.
* [Kubernetes: Resource Bin Packing](https://kubernetes.io/docs/concepts/scheduling-eviction/resource-bin-packing/): how kube-scheduler scores nodes with `MostAllocated` and `RequestedToCapacityRatio`.
* [Google OR-Tools](https://developers.google.com/optimization): a free solver suite for LP, integer programming, bin packing and constraint programming, with worked examples for each problem type.

## Where to Go Next

* [Calculus Track](../calculus/README.md) for derivatives and gradients, the engine of rungs 2 to 6.
* [Linear Algebra Track](../linear-algebra/README.md) for the matrices behind simplex pivots and duality.
* [Numerical Methods Track](../numerical-methods/README.md) for gradient descent and the Newton method in floating point.
* [Graph Theory Track](../graph-theory/README.md) for shortest paths and maximum flow, which are linear programs with fast special algorithms.
* [Combinatorics Track](../combinatorics/README.md) for counting the plans an integer program must avoid checking.
* [Computability and Complexity Track](../computability-and-complexity/README.md) for why bin packing and integer programming are hard.
