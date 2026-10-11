// Chapter 08: The 18th and 19th Centuries: Rigor.
// Four small programs: Euler's bridge test, Gauss's pairing sum,
// Cantor's listing of the fractions, and Cantor's diagonal.
package main

import (
	"fmt"
	"sort"
	"strings"
)

// eulerPath reports the degree of each land mass and whether a walk
// exists that crosses every bridge exactly once. Euler's rule for a
// connected multigraph: zero odd-degree nodes gives a closed walk,
// two gives an open walk, any other count gives no walk at all.
func eulerPath(edges [][2]string) (map[string]int, int, bool) {
	deg := map[string]int{}
	adj := map[string][]string{}
	for _, e := range edges {
		deg[e[0]]++
		deg[e[1]]++
		adj[e[0]] = append(adj[e[0]], e[1])
		adj[e[1]] = append(adj[e[1]], e[0])
	}
	// Connectivity check: walk the graph from any node.
	var start string
	for n := range deg {
		start = n
		break
	}
	seen := map[string]bool{start: true}
	queue := []string{start}
	for len(queue) > 0 {
		n := queue[0]
		queue = queue[1:]
		for _, m := range adj[n] {
			if !seen[m] {
				seen[m] = true
				queue = append(queue, m)
			}
		}
	}
	odd := 0
	for _, d := range deg {
		if d%2 == 1 {
			odd++
		}
	}
	ok := len(seen) == len(deg) && (odd == 0 || odd == 2)
	return deg, odd, ok
}

func report(name string, edges [][2]string) {
	deg, odd, ok := eulerPath(edges)
	names := make([]string, 0, len(deg))
	for n := range deg {
		names = append(names, n)
	}
	sort.Strings(names)
	parts := []string{}
	for _, n := range names {
		parts = append(parts, fmt.Sprintf("%s=%d", n, deg[n]))
	}
	fmt.Printf("   %s: degrees %s, odd nodes %d, walk exists: %v\n",
		name, strings.Join(parts, " "), odd, ok)
}

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// rationals lists positive fractions along Cantor's zigzag:
// diagonal by diagonal (top + bottom = s), switching direction each
// time, skipping repeats such as 2/2.
func rationals(count int) []string {
	out := []string{}
	for s := 2; len(out) < count; s++ {
		for i := 1; i < s && len(out) < count; i++ {
			top := i
			if s%2 == 0 {
				top = s - i
			}
			bottom := s - top
			if gcd(top, bottom) == 1 {
				out = append(out, fmt.Sprintf("%d/%d", top, bottom))
			}
		}
	}
	return out
}

// diagonal builds a row that differs from row n in place n.
func diagonal(rows []string) (diag, flipped string) {
	for i, r := range rows {
		diag += string(r[i])
		if r[i] == '0' {
			flipped += "1"
		} else {
			flipped += "0"
		}
	}
	return diag, flipped
}

func main() {
	fmt.Println("1. Euler and the bridges")
	konigsberg := [][2]string{
		{"A", "B"}, {"A", "B"}, {"A", "C"}, {"A", "C"},
		{"A", "D"}, {"B", "D"}, {"C", "D"},
	}
	report("Konigsberg, 7 bridges", konigsberg)
	report("with an 8th bridge B-C", append(konigsberg, [2]string{"B", "C"}))

	fmt.Println("\n2. Gauss: 1 + 2 + ... + 100")
	sum := 0
	for k := 1; k <= 100; k++ {
		sum += k
	}
	fmt.Printf("   loop: %d   pairing: 50 x 101 = %d   formula n(n+1)/2 = %d\n",
		sum, 50*101, 100*101/2)

	fmt.Println("\n3. Cantor: the fractions in one list")
	fmt.Println("   " + strings.Join(rationals(11), ", "))

	fmt.Println("\n4. Cantor: the diagonal")
	rows := []string{"010110", "110010", "000101", "101100", "011001", "111010"}
	d, fl := diagonal(rows)
	for i, r := range rows {
		fmt.Printf("   s%d = %s  differs from new in place %d\n", i+1, r, i+1)
	}
	fmt.Printf("   diagonal %s, flipped (new) %s\n", d, fl)
}
