// Optimization starter kit: a calculus minimum, gradient descent,
// a Lagrange check, the simplex method with shadow prices, branch and
// bound for an integer program, bin packing of pods onto nodes, and a
// tiny constraint solver. Standard library only.
package main

import (
	"fmt"
	"math"
	"sort"
	"strings"
)

// ---------- 1. Calculus: the cheapest replica count ----------

// cost is the hourly cost of n replicas: 50 per replica plus a
// latency penalty of 3200/n that shrinks as replicas are added.
func cost(n float64) float64 { return 50*n + 3200/n }

func replicaCost() {
	fmt.Println("== Cheapest replica count: C(n) = 50n + 3200/n ==")
	best, bestN := math.Inf(1), 0
	for n := 1; n <= 16; n++ {
		c := cost(float64(n))
		if n == 1 || n == 4 || n == 7 || n == 8 || n == 9 || n == 16 {
			fmt.Printf("n = %2d  cost = %6.1f\n", n, c)
		}
		if c < best {
			best, bestN = c, n
		}
	}
	fmt.Printf("scan minimum: n = %d, cost = %.1f\n", bestN, best)
	fmt.Printf("calculus: C'(n) = 50 - 3200/n^2 = 0 gives n = sqrt(64) = %.0f\n\n", math.Sqrt(3200.0/50))
}

// ---------- 2. Gradient descent in one dimension ----------

func gradientDescent() {
	fmt.Println("== Gradient descent on f(x) = (x - 3)^2 from x = 0 ==")
	for _, eta := range []float64{0.1, 0.5, 0.9, 1.1} {
		x := 0.0
		var first []string
		for k := 1; k <= 20; k++ {
			x = x - eta*2*(x-3) // f'(x) = 2(x - 3)
			if k <= 4 {
				first = append(first, fmt.Sprintf("%.3f", x))
			}
		}
		fmt.Printf("eta %.1f: first steps %s ... after 20 steps x = %.4f\n",
			eta, strings.Join(first, ", "), x)
	}
	fmt.Println()
}

// ---------- 3. Lagrange multiplier check ----------

func lagrange() {
	fmt.Println("== Fence by a river: maximize xy with 2x + y = L ==")
	for _, L := range []float64{40, 41} {
		bestA, bestX := 0.0, 0.0
		for i := 0; i <= 200000; i++ {
			x := L / 2 * float64(i) / 200000
			a := x * (L - 2*x)
			if a > bestA {
				bestA, bestX = a, x
			}
		}
		fmt.Printf("L = %.0f: x = %.3f, y = %.3f, area = %.3f\n", L, bestX, L-2*bestX, bestA)
	}
	fmt.Println("extra area from 1 more meter = 10.125, close to lambda = 10")
	fmt.Println()
}

// ---------- 4. Simplex method ----------

// simplex maximizes c.x subject to A x <= b, x >= 0, with b >= 0.
// It returns x, the optimal value, and the shadow price of each row.
func simplex(c []float64, A [][]float64, b []float64, names []string, verbose bool) ([]float64, float64, []float64, bool) {
	m, n := len(A), len(c)
	cols := n + m + 1
	T := make([][]float64, m+1)
	basis := make([]int, m)
	for i := 0; i < m; i++ {
		T[i] = make([]float64, cols)
		copy(T[i], A[i])
		T[i][n+i] = 1
		T[i][cols-1] = b[i]
		basis[i] = n + i
	}
	T[m] = make([]float64, cols)
	copy(T[m], c) // reduced costs; positive means "raising this helps"
	label := func(j int) string {
		if j < n {
			return names[j]
		}
		return fmt.Sprintf("s%d", j-n+1)
	}
	solution := func() []float64 {
		x := make([]float64, n)
		for i, bv := range basis {
			if bv < n {
				x[bv] = T[i][cols-1]
			}
		}
		return x
	}
	report := func(step int) {
		if verbose {
			x := solution()
			fmt.Printf("  corner %d: %s = %v, value %.2f\n", step, strings.Join(names, ","), fmtVec(x), math.Abs(T[m][cols-1]))
		}
	}
	report(0)
	for step := 1; step <= 50; step++ {
		e := -1
		for j := 0; j < n+m; j++ {
			if T[m][j] > 1e-9 && (e < 0 || T[m][j] > T[m][e]) {
				e = j
			}
		}
		if e < 0 {
			x := solution()
			y := make([]float64, m)
			for i := 0; i < m; i++ {
				y[i] = -T[m][n+i]
			}
			return x, -T[m][cols-1], y, true
		}
		r := -1
		for i := 0; i < m; i++ {
			if T[i][e] > 1e-9 {
				ratio := T[i][cols-1] / T[i][e]
				if r < 0 || ratio < T[r][cols-1]/T[r][e]-1e-12 {
					r = i
				}
			}
		}
		if r < 0 {
			return nil, math.Inf(1), nil, false // unbounded
		}
		if verbose {
			fmt.Printf("  pivot: %s enters, %s leaves\n", label(e), label(basis[r]))
		}
		p := T[r][e]
		for j := range T[r] {
			T[r][j] /= p
		}
		for i := 0; i <= m; i++ {
			if i != r && T[i][e] != 0 {
				f := T[i][e]
				for j := range T[i] {
					T[i][j] -= f * T[r][j]
				}
			}
		}
		basis[r] = e
		report(step)
	}
	return nil, 0, nil, false
}

func fmtVec(x []float64) string {
	parts := make([]string, len(x))
	for i, v := range x {
		parts[i] = strings.TrimRight(strings.TrimRight(fmt.Sprintf("%.2f", v), "0"), ".")
		if parts[i] == "" || parts[i] == "-0" {
			parts[i] = "0"
		}
	}
	return "(" + strings.Join(parts, ", ") + ")"
}

func linearProgram() {
	fmt.Println("== Simplex: maximize 3x + 4y, 2x + y <= 10 (CPU), x + 3y <= 15 (memory) ==")
	c := []float64{3, 4}
	A := [][]float64{{2, 1}, {1, 3}}
	b := []float64{10, 15}
	x, v, y, _ := simplex(c, A, b, []string{"x", "y"}, true)
	fmt.Printf("optimum x = %s, value = %.2f\n", fmtVec(x), v)
	fmt.Printf("shadow prices (dual): CPU u = %.2f, memory v = %.2f\n", y[0], y[1])
	fmt.Printf("dual check: 2u + v = %.2f >= 3, u + 3v = %.2f >= 4, 10u + 15v = %.2f\n",
		2*y[0]+y[1], y[0]+3*y[1], 10*y[0]+15*y[1])
	_, v11, _, _ := simplex(c, A, []float64{11, 15}, []string{"x", "y"}, false)
	fmt.Printf("one more CPU core: value %.2f -> %.2f\n\n", v, v11)
}

// ---------- 5. Corner method for a cost-minimizing instance mix ----------

func instanceMix() {
	fmt.Println("== Cheapest instance mix: minimize 0.34c + 0.25m ==")
	fmt.Println("   need 8c + 4m >= 64 CPU and 16c + 32m >= 192 GB")
	price := func(c, m float64) float64 { return 0.34*c + 0.25*m }
	ok := func(c, m float64) bool {
		return 8*c+4*m >= 64-1e-9 && 16*c+32*m >= 192-1e-9 && c >= -1e-9 && m >= -1e-9
	}
	// Each corner sits where two boundary lines meet.
	lines := [][3]float64{{8, 4, 64}, {16, 32, 192}, {1, 0, 0}, {0, 1, 0}}
	for i := 0; i < len(lines); i++ {
		for j := i + 1; j < len(lines); j++ {
			a, b := lines[i], lines[j]
			det := a[0]*b[1] - a[1]*b[0]
			if det == 0 {
				continue
			}
			c := (a[2]*b[1] - a[1]*b[2]) / det
			m := (a[0]*b[2] - a[2]*b[0]) / det
			c, m = math.Abs(c), math.Abs(m) // print 0, not -0
			if ok(c, m) {
				fmt.Printf("  corner (c, m) = (%.3f, %.3f): $%.3f per hour\n", c, m, price(c, m))
			}
		}
	}
	bc, bm, best := 0, 0, math.Inf(1)
	for c := 0; c <= 20; c++ {
		for m := 0; m <= 20; m++ {
			if ok(float64(c), float64(m)) && price(float64(c), float64(m)) < best-1e-9 {
				bc, bm, best = c, m, price(float64(c), float64(m))
			}
		}
	}
	fmt.Printf("best whole instances: c = %d, m = %d, $%.2f per hour\n\n", bc, bm, best)
}

// ---------- 6. Branch and bound for an integer program ----------

// solveBounded maximizes c.x with A x <= b, lo <= x <= hi. It shifts
// x = lo + x' so the simplex sees x' >= 0. All entries of A are
// nonnegative here, so a negative right-hand side means infeasible.
func solveBounded(c []float64, A [][]float64, b, lo, hi []float64) ([]float64, float64, bool) {
	n := len(c)
	var rows [][]float64
	var rhs []float64
	for i, row := range A {
		r := b[i]
		for j := 0; j < n; j++ {
			r -= row[j] * lo[j]
		}
		if r < -1e-9 {
			return nil, 0, false
		}
		rows = append(rows, row)
		rhs = append(rhs, r)
	}
	for j := 0; j < n; j++ {
		if !math.IsInf(hi[j], 1) {
			if hi[j] < lo[j] {
				return nil, 0, false
			}
			row := make([]float64, n)
			row[j] = 1
			rows = append(rows, row)
			rhs = append(rhs, hi[j]-lo[j])
		}
	}
	xs, v, _, ok := simplex(c, rows, rhs, []string{"x", "y"}, false)
	if !ok {
		return nil, 0, false
	}
	for j := 0; j < n; j++ {
		xs[j] += lo[j]
		v += c[j] * lo[j]
	}
	return xs, v, true
}

func integerProgram() {
	fmt.Println("== Integer program: maximize 5x + 8y, x + y <= 6, 5x + 9y <= 45, x, y whole ==")
	c := []float64{5, 8}
	A := [][]float64{{1, 1}, {5, 9}}
	b := []float64{6, 45}
	inf := math.Inf(1)
	x, v, _ := solveBounded(c, A, b, []float64{0, 0}, []float64{inf, inf})
	fmt.Printf("LP relaxation: x = %s, value %.2f\n", fmtVec(x), v)
	fmt.Printf("rounded (2, 4): 5x + 9y = %d > 45, infeasible\n", 5*2+9*4)
	best, bestX := math.Inf(-1), []float64(nil)
	nodes := 0
	var branch func(lo, hi []float64, depth int)
	branch = func(lo, hi []float64, depth int) {
		nodes++
		pad := strings.Repeat("  ", depth+1)
		desc := fmt.Sprintf("x in [%g, %g], y in [%g, %g]", lo[0], hi[0], lo[1], hi[1])
		desc = strings.ReplaceAll(desc, "+Inf", "inf")
		xs, val, ok := solveBounded(c, A, b, lo, hi)
		if !ok {
			fmt.Printf("%s%s: infeasible\n", pad, desc)
			return
		}
		if val <= best+1e-9 {
			fmt.Printf("%s%s: LP %.2f at %s, cannot beat %.0f, prune\n", pad, desc, val, fmtVec(xs), best)
			return
		}
		for j := range xs {
			f := xs[j] - math.Floor(xs[j]+1e-9)
			if f > 1e-6 && f < 1-1e-6 {
				fmt.Printf("%s%s: LP %.2f at %s, branch on %s\n", pad, desc, val, fmtVec(xs), []string{"x", "y"}[j])
				h2 := append([]float64{}, hi...)
				h2[j] = math.Floor(xs[j])
				branch(append([]float64{}, lo...), h2, depth+1)
				l2 := append([]float64{}, lo...)
				l2[j] = math.Ceil(xs[j])
				branch(l2, append([]float64{}, hi...), depth+1)
				return
			}
		}
		fmt.Printf("%s%s: whole-number point %s, value %.0f, new best\n", pad, desc, fmtVec(xs), val)
		best, bestX = val, xs
	}
	branch([]float64{0, 0}, []float64{inf, inf}, 0)
	fmt.Printf("branch and bound: best %s, value %.0f, %d nodes\n", fmtVec(bestX), best, nodes)
	count, bv := 0, 0
	for x := 0; x <= 6; x++ {
		for y := 0; y <= 6; y++ {
			if x+y <= 6 && 5*x+9*y <= 45 {
				count++
				if 5*x+8*y > bv {
					bv = 5*x + 8*y
				}
			}
		}
	}
	fmt.Printf("brute force over %d feasible points: best value %d\n\n", count, bv)
}

// ---------- 7. Bin packing pods onto nodes ----------

func firstFit(items []int, capacity int) [][]int {
	var bins [][]int
	var free []int
	for _, it := range items {
		placed := false
		for i := range bins {
			if free[i] >= it {
				bins[i] = append(bins[i], it)
				free[i] -= it
				placed = true
				break
			}
		}
		if !placed {
			bins = append(bins, []int{it})
			free = append(free, capacity-it)
		}
	}
	return bins
}

func binPacking() {
	pods := []int{1, 2, 3, 4, 4, 5, 5, 6}
	capacity := 10
	sum := 0
	for _, p := range pods {
		sum += p
	}
	fmt.Printf("== Packing pods (CPU) %v onto nodes of %d CPU ==\n", pods, capacity)
	fmt.Printf("lower bound: ceil(%d / %d) = %d nodes\n", sum, capacity, (sum+capacity-1)/capacity)
	ff := firstFit(pods, capacity)
	fmt.Printf("first fit, arrival order:  %d nodes %v\n", len(ff), ff)
	sorted := append([]int{}, pods...)
	sort.Sort(sort.Reverse(sort.IntSlice(sorted)))
	ffd := firstFit(sorted, capacity)
	fmt.Printf("first fit decreasing:      %d nodes %v\n\n", len(ffd), ffd)
}

// ---------- 8. A tiny constraint solver ----------

// Jobs A, B, C, D each get a maintenance slot 1, 2 or 3.
// A, B and C share a database: all different. D runs before B.
// A cannot run in slot 1.
var jobs = []string{"A", "B", "C", "D"}

func consistent(s map[string]int) bool {
	get := func(k string) (int, bool) { v, ok := s[k]; return v, ok }
	pairs := [][2]string{{"A", "B"}, {"A", "C"}, {"B", "C"}}
	for _, p := range pairs {
		a, ok1 := get(p[0])
		b, ok2 := get(p[1])
		if ok1 && ok2 && a == b {
			return false
		}
	}
	if a, ok := get("A"); ok && a == 1 {
		return false
	}
	d, ok1 := get("D")
	b, ok2 := get("B")
	if ok1 && ok2 && d >= b {
		return false
	}
	return true
}

func solve(i int, s map[string]int, nodes *int, out *[]string) {
	if i == len(jobs) {
		*out = append(*out, fmt.Sprintf("A=%d B=%d C=%d D=%d", s["A"], s["B"], s["C"], s["D"]))
		return
	}
	for v := 1; v <= 3; v++ {
		*nodes++
		s[jobs[i]] = v
		if consistent(s) {
			solve(i+1, s, nodes, out)
		}
		delete(s, jobs[i])
	}
}

func constraintSolver() {
	fmt.Println("== Constraint solver: 4 jobs, 3 slots ==")
	brute := 0
	for a := 1; a <= 3; a++ {
		for b := 1; b <= 3; b++ {
			for c := 1; c <= 3; c++ {
				for d := 1; d <= 3; d++ {
					if consistent(map[string]int{"A": a, "B": b, "C": c, "D": d}) {
						brute++
					}
				}
			}
		}
	}
	nodes := 0
	var sols []string
	solve(0, map[string]int{}, &nodes, &sols)
	fmt.Printf("brute force: 81 full schedules checked, %d valid\n", brute)
	fmt.Printf("backtracking: %d partial schedules tried\n", nodes)
	for _, s := range sols {
		fmt.Println("  " + s)
	}
}

func main() {
	replicaCost()
	gradientDescent()
	lagrange()
	linearProgram()
	instanceMix()
	integerProgram()
	binPacking()
	constraintSolver()
}
