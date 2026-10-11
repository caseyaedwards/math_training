# Optimization Diagrams

Hand-authored SVG diagrams for the [Optimization Track](../README.md), listed in the order they appear:

* [concept-map.svg](concept-map.svg): Optimization concept map.
* [lp-feasible-region.svg](lp-feasible-region.svg): Linear program feasible region with sliding objective lines.
* [fence-area.svg](fence-area.svg): Rectangles with the same fence and the area curve.
* [extrema-flat-tangents.svg](extrema-flat-tangents.svg): Local and global extrema with flat tangents, endpoints and a slope sign chart.
* [convex-vs-nonconvex.svg](convex-vs-nonconvex.svg): Convex bowl versus a bumpy function with a local-minimum trap.
* [gradient-descent-steps.svg](gradient-descent-steps.svg): Gradient descent with step sizes 0.1, 0.9 and 1.1.
* [contour-gradient.svg](contour-gradient.svg): Contour map with gradient arrows and a descent path.
* [lagrange-tangent.svg](lagrange-tangent.svg): Level curve tangent to the fence constraint, with parallel gradients.
* [lp-constraints-build.svg](lp-constraints-build.svg): Half-planes combining into the feasible region.
* [simplex-path.svg](simplex-path.svg): Simplex walk from corner to better corner.
* [duality-gap.svg](duality-gap.svg): Primal values and dual bounds meeting at the optimum.
* [integer-lattice.svg](integer-lattice.svg): Integer program where rounding the LP answer fails.
* [bin-packing-pods.svg](bin-packing-pods.svg): Pods packed onto nodes by first fit and first fit decreasing.
* [constraint-search-tree.svg](constraint-search-tree.svg): Backtracking search tree for a four-job schedule.
* [replica-cost-curve.svg](replica-cost-curve.svg): Hourly cost of n replicas with its minimum at n = 8.
* [instance-mix-lp.svg](instance-mix-lp.svg): Cost-minimizing instance mix with corners and cost lines.

The generator script lives outside the repository. Each embed in the track README carries a `<!-- diagram: ... -->` spec comment.
