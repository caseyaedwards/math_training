// Computability and complexity starter kit: a DFA, an NFA, a backtracking
// regex engine next to a linear one, a stack machine, a Turing machine,
// a step budget for programs with no known stopping time, growth rates, and
// brute force next to clever shortcuts for NP problems.
// Standard library only.
package main

import (
	"fmt"
	"math"
	"regexp"
	"sort"
	"strings"
	"time"
)

// ---------- 1. DFA: binary numbers divisible by 3 ----------

// mod3 runs the three-state DFA. The state is the value read so far, mod 3.
// Reading bit b moves state s to (2s + b) mod 3.
func mod3(bits string) (int, []int) {
	s := 0
	trace := []int{s}
	for _, c := range bits {
		b := int(c - '0')
		s = (2*s + b) % 3
		trace = append(trace, s)
	}
	return s, trace
}

// ---------- 2. NFA for (a|b)*abb, simulated with a set of states ----------

// nfaStep moves every live state on one character.
// States: 0 start (loops on a and b), 1 saw a, 2 saw ab, 3 saw abb (accept).
func nfaStep(set map[int]bool, c rune) map[int]bool {
	next := map[int]bool{}
	for s := range set {
		switch {
		case s == 0:
			next[0] = true
			if c == 'a' {
				next[1] = true
			}
		case s == 1 && c == 'b':
			next[2] = true
		case s == 2 && c == 'b':
			next[3] = true
		}
	}
	return next
}

func nfaAccepts(w string) (bool, string) {
	set := map[int]bool{0: true}
	var steps []string
	for _, c := range w {
		set = nfaStep(set, c)
		steps = append(steps, setString(set))
	}
	return set[3], strings.Join(steps, " ")
}

func setString(set map[int]bool) string {
	var ks []int
	for k := range set {
		ks = append(ks, k)
	}
	sort.Ints(ks)
	parts := make([]string, len(ks))
	for i, k := range ks {
		parts[i] = fmt.Sprint(k)
	}
	return "{" + strings.Join(parts, ",") + "}"
}

// ---------- 3. Backtracking regex engine versus a DFA ----------

type node struct {
	kind  byte // 'c' char, '.' concat, '+' one or more
	ch    byte
	left  *node
	right *node
}

var steps int

// match tries node n at position i and calls k on every way it can end.
// This is how Perl-style engines work: try one choice, back up, try another.
func match(n *node, s string, i int, k func(int) bool) bool {
	steps++
	switch n.kind {
	case 'c':
		return i < len(s) && s[i] == n.ch && k(i+1)
	case '.':
		return match(n.left, s, i, func(j int) bool { return match(n.right, s, j, k) })
	case '+':
		return match(n.left, s, i, func(j int) bool {
			if j > i && match(n, s, j, k) { // greedy: try another round first
				return true
			}
			return k(j)
		})
	}
	return false
}

// dfaAplusB accepts a+b with a three-state DFA and counts one step per byte.
func dfaAplusB(s string) (bool, int) {
	state, n := 0, 0 // 0 start, 1 seen a's, 2 seen final b, 3 dead
	for i := 0; i < len(s); i++ {
		n++
		switch {
		case (state == 0 || state == 1) && s[i] == 'a':
			state = 1
		case state == 1 && s[i] == 'b':
			state = 2
		default:
			state = 3
		}
	}
	return state == 2, n
}

// ---------- 4. Pushdown idea: balanced parentheses with a stack ----------

func balanced(s string) (bool, int) {
	stack, maxDepth := 0, 0
	for _, c := range s {
		if c == '(' {
			stack++ // push
			if stack > maxDepth {
				maxDepth = stack
			}
		} else {
			if stack == 0 {
				return false, maxDepth
			}
			stack-- // pop
		}
	}
	return stack == 0, maxDepth
}

// ---------- 5. Turing machine: add 1 to a binary number ----------

func increment(input string) []string {
	tape := map[int]byte{}
	for i := 0; i < len(input); i++ {
		tape[i] = input[i]
	}
	head, state := len(input)-1, "carry"
	var snaps []string
	snap := func() {
		lo, hi := 0, len(input)-1
		for k := range tape {
			lo = min(lo, k)
			hi = max(hi, k)
		}
		var b strings.Builder
		for i := lo - 1; i <= hi+1; i++ {
			c, ok := tape[i]
			if !ok {
				c = '_'
			}
			if i == head {
				b.WriteString("[" + string(c) + "]")
			} else {
				b.WriteString(" " + string(c) + " ")
			}
		}
		snaps = append(snaps, strings.TrimRight(fmt.Sprintf("%-6s %s", state, b.String()), " "))
	}
	snap()
	for state != "halt" {
		c, ok := tape[head]
		if !ok {
			c = '_'
		}
		if c == '1' { // 1 plus carry: write 0, keep carrying left
			tape[head] = '0'
			head--
		} else { // 0 or blank plus carry: write 1, done
			tape[head] = '1'
			state = "halt"
		}
		snap()
	}
	return snaps
}

// ---------- 6. Living with the halting problem: a step budget ----------

// collatz runs n -> n/2 or 3n+1 until 1, giving up after budget steps.
func collatz(n, budget int) (int, bool) {
	for s := 0; s < budget; s++ {
		if n == 1 {
			return s, true
		}
		if n%2 == 0 {
			n /= 2
		} else {
			n = 3*n + 1
		}
	}
	return budget, n == 1
}

// ---------- 7. Subset sum: find versus check ----------

func subsetSum(nums []int, target int) (checked int, found [][]int) {
	n := len(nums)
	for mask := 0; mask < 1<<n; mask++ {
		checked++
		sum := 0
		var pick []int
		for i := 0; i < n; i++ {
			if mask&(1<<i) != 0 {
				sum += nums[i]
				pick = append(pick, nums[i])
			}
		}
		if sum == target {
			found = append(found, pick)
		}
	}
	return
}

// ---------- 8. 3-SAT and its reduction to independent set ----------

// A literal is +v for x_v and -v for NOT x_v.
var formula = [][3]int{{1, 2, -3}, {-1, -2, 3}, {1, -2, 3}}

func litName(l int) string {
	if l < 0 {
		return fmt.Sprintf("!x%d", -l)
	}
	return fmt.Sprintf("x%d", l)
}

func satisfies(assign [4]bool, f [][3]int) bool {
	for _, cl := range f {
		ok := false
		for _, l := range cl {
			v := l
			if v < 0 {
				v = -v
			}
			if assign[v] == (l > 0) {
				ok = true
			}
		}
		if !ok {
			return false
		}
	}
	return true
}

// ---------- 9. Vertex cover: 2-approximation versus optimum ----------

var vcNames = "ABCDEFG"
var vcEdges = [][2]int{{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}, {4, 5}, {4, 6}}

func covers(mask int) bool {
	for _, e := range vcEdges {
		if mask&(1<<e[0]) == 0 && mask&(1<<e[1]) == 0 {
			return false
		}
	}
	return true
}

func names(mask int) string {
	var b strings.Builder
	for i := 0; i < len(vcNames); i++ {
		if mask&(1<<i) != 0 {
			b.WriteByte(vcNames[i])
		}
	}
	return b.String()
}

func popcount(x int) int {
	c := 0
	for ; x > 0; x &= x - 1 {
		c++
	}
	return c
}

// ---------- 10. Scheduling: greedy LPT versus optimal ----------

func lpt(jobs []int, machines int) (int, [][]int) {
	js := append([]int(nil), jobs...)
	sort.Sort(sort.Reverse(sort.IntSlice(js)))
	load := make([]int, machines)
	plan := make([][]int, machines)
	for _, j := range js {
		best := 0
		for m := 1; m < machines; m++ {
			if load[m] < load[best] {
				best = m
			}
		}
		load[best] += j
		plan[best] = append(plan[best], j)
	}
	return maxOf(load), plan
}

func bestTwoMachine(jobs []int) int {
	best := math.MaxInt
	for mask := 0; mask < 1<<len(jobs); mask++ {
		a, b := 0, 0
		for i, j := range jobs {
			if mask&(1<<i) != 0 {
				a += j
			} else {
				b += j
			}
		}
		best = min(best, max(a, b))
	}
	return best
}

func maxOf(xs []int) int {
	m := xs[0]
	for _, x := range xs {
		m = max(m, x)
	}
	return m
}

func main() {
	fmt.Println("== 1. DFA: is a binary number divisible by 3? ==")
	for _, w := range []string{"110", "1101", "1111", "10010"} {
		s, tr := mod3(w)
		var v int64
		fmt.Sscanf(w, "%b", &v)
		fmt.Printf("%-6s (=%2d) states %v -> end in %d, divisible: %v\n", w, v, tr, s, s == 0)
	}

	fmt.Println()
	fmt.Println("== 2. NFA for (a|b)*abb, tracking every live state ==")
	re := regexp.MustCompile(`^(a|b)*abb$`)
	for _, w := range []string{"aabb", "babb", "abab"} {
		ok, tr := nfaAccepts(w)
		fmt.Printf("%-5s sets %s -> accept %v (Go regexp agrees: %v)\n", w, tr, ok, re.MatchString(w) == ok)
	}

	fmt.Println()
	fmt.Println("== 3. Catastrophic backtracking: (a+)+b on a string of n a's ==")
	pat := &node{kind: '.', left: &node{kind: '+', left: &node{kind: '+', left: &node{kind: 'c', ch: 'a'}}}, right: &node{kind: 'c', ch: 'b'}}
	goRE := regexp.MustCompile(`^(a+)+b$`)
	for _, n := range []int{5, 10, 15, 20, 25} {
		s := strings.Repeat("a", n)
		steps = 0
		ok := match(pat, s, 0, func(j int) bool { return j == len(s) })
		_, d := dfaAplusB(s)
		start := time.Now()
		g := goRE.MatchString(s)
		fast := time.Since(start) < time.Millisecond
		fmt.Printf("n=%2d  backtracking steps %10d  match %v | DFA steps %2d | Go regexp match %v, under 1 ms %v\n", n, steps, ok, d, g, fast)
	}

	fmt.Println()
	fmt.Println("== 4. Stack machine: balanced parentheses ==")
	for _, w := range []string{"(()())", "((()))", "(()", "())("} {
		ok, d := balanced(w)
		fmt.Printf("%-7s balanced %-5v max stack depth %d\n", w, ok, d)
	}

	fmt.Println()
	fmt.Println("== 5. Turing machine: binary increment ==")
	for _, w := range []string{"1011", "111"} {
		fmt.Printf("input %s\n", w)
		for _, sn := range increment(w) {
			fmt.Println("  " + sn)
		}
	}

	fmt.Println()
	fmt.Println("== 6. Step budget for a program with no known bound (Collatz) ==")
	for _, c := range [][2]int{{27, 100}, {27, 1000}, {97, 1000}} {
		st, done := collatz(c[0], c[1])
		if done {
			fmt.Printf("n=%d budget %4d -> halted after %d steps\n", c[0], c[1], st)
		} else {
			fmt.Printf("n=%d budget %4d -> budget spent, verdict unknown\n", c[0], c[1])
		}
	}

	fmt.Println()
	fmt.Println("== 7. Growth: steps for input size n, and time at 10^9 steps per second ==")
	fmt.Printf("%4s %10s %10s %10s %22s %16s\n", "n", "n", "n log2 n", "n^2", "2^n", "2^n time")
	for _, n := range []int{10, 20, 30, 40, 50, 60} {
		p := math.Pow(2, float64(n))
		fmt.Printf("%4d %10d %10.0f %10d %22.0f %16s\n", n, n, float64(n)*math.Log2(float64(n)), n*n, p, human(p/1e9))
	}

	fmt.Println()
	fmt.Println("== 8. Subset sum: find versus check ==")
	nums := []int{3, 34, 4, 12, 5, 2}
	checked, found := subsetSum(nums, 9)
	fmt.Printf("set %v target 9: brute force checked %d subsets, found %v\n", nums, checked, found)
	fmt.Printf("checking the certificate [4 5]: 4 + 5 = %d, one addition\n", 4+5)

	fmt.Println()
	fmt.Println("== 9. 3-SAT to independent set ==")
	var parts []string
	for _, cl := range formula {
		parts = append(parts, "("+litName(cl[0])+" | "+litName(cl[1])+" | "+litName(cl[2])+")")
	}
	fmt.Println("formula:", strings.Join(parts, " & "))
	nsat := 0
	for m := 0; m < 8; m++ {
		a := [4]bool{false, m&1 != 0, m&2 != 0, m&4 != 0}
		if satisfies(a, formula) {
			nsat++
		}
	}
	fmt.Printf("satisfying assignments: %d of 8\n", nsat)
	// Build the graph: one vertex per literal slot, triangles inside clauses,
	// conflict edges between opposite literals in different clauses.
	type lit struct{ c, p, l int }
	var vs []lit
	for c, cl := range formula {
		for p, l := range cl {
			vs = append(vs, lit{c, p, l})
		}
	}
	adj := make([][]bool, len(vs))
	for i := range adj {
		adj[i] = make([]bool, len(vs))
	}
	tri, conf := 0, 0
	var conflicts []string
	for i := range vs {
		for j := i + 1; j < len(vs); j++ {
			if vs[i].c == vs[j].c {
				adj[i][j], adj[j][i] = true, true
				tri++
			} else if vs[i].l == -vs[j].l {
				adj[i][j], adj[j][i] = true, true
				conf++
				conflicts = append(conflicts, fmt.Sprintf("C%d:%s-C%d:%s", vs[i].c+1, litName(vs[i].l), vs[j].c+1, litName(vs[j].l)))
			}
		}
	}
	fmt.Printf("graph: %d vertices, %d triangle edges, %d conflict edges\n", len(vs), tri, conf)
	fmt.Println("conflict edges:", strings.Join(conflicts, " "))
	nIS := 0
	var first string
	for a := 0; a < len(vs); a++ {
		for b := a + 1; b < len(vs); b++ {
			for c := b + 1; c < len(vs); c++ {
				if !adj[a][b] && !adj[a][c] && !adj[b][c] {
					nIS++
					if first == "" {
						first = fmt.Sprintf("C1:%s C2:%s C3:%s", litName(vs[a].l), litName(vs[b].l), litName(vs[c].l))
					}
				}
			}
		}
	}
	fmt.Printf("independent sets of size 3: %d, first: %s\n", nIS, first)
	fmt.Printf("satisfiable: %v, independent set of size 3 exists: %v\n", nsat > 0, nIS > 0)

	fmt.Println()
	fmt.Println("== 10. Vertex cover: matching 2-approximation versus optimum ==")
	used := 0
	var picked []string
	for _, e := range vcEdges {
		if used&(1<<e[0]) == 0 && used&(1<<e[1]) == 0 {
			used |= 1<<e[0] | 1<<e[1]
			picked = append(picked, string(vcNames[e[0]])+string(vcNames[e[1]]))
		}
	}
	fmt.Printf("matching edges %v -> cover %s, size %d, valid %v\n", picked, names(used), popcount(used), covers(used))
	best := -1
	for m := 0; m < 1<<len(vcNames); m++ {
		if covers(m) && (best < 0 || popcount(m) < popcount(best)) {
			best = m
		}
	}
	fmt.Printf("optimum by brute force: %s, size %d (checked %d subsets)\n", names(best), popcount(best), 1<<len(vcNames))

	fmt.Println()
	fmt.Println("== 11. Scheduling jobs 3,3,2,2,2 on 2 machines ==")
	jobs := []int{3, 3, 2, 2, 2}
	mk, plan := lpt(jobs, 2)
	fmt.Printf("greedy longest-first: machines %v -> makespan %d\n", plan, mk)
	fmt.Printf("optimum by brute force: makespan %d (checked %d splits)\n", bestTwoMachine(jobs), 1<<len(jobs))
}

func human(sec float64) string {
	switch {
	case sec < 1e-3:
		return fmt.Sprintf("%.1f us", sec*1e6)
	case sec < 1:
		return fmt.Sprintf("%.1f ms", sec*1e3)
	case sec < 60:
		return fmt.Sprintf("%.1f s", sec)
	case sec < 86400:
		return fmt.Sprintf("%.1f min", sec/60)
	case sec < 86400*365:
		return fmt.Sprintf("%.1f days", sec/86400)
	}
	return fmt.Sprintf("%.1f years", sec/(86400*365))
}
