// Logic and set theory toolkit: truth tables, a De Morgan check,
// power sets with bitmasks, and Cantor's diagonal argument on a finite list.
// Run with: go run main.go
package main

import (
	"fmt"
	"strings"
)

func implies(p, q bool) bool { return !p || q }

func tf(b bool) string {
	if b {
		return "T"
	}
	return "F"
}

func main() {
	// 1. Truth table for p -> q and its contrapositive (not q -> not p).
	fmt.Println("p q | p->q | !q->!p")
	for _, p := range []bool{true, false} {
		for _, q := range []bool{true, false} {
			fmt.Printf("%s %s |  %s   |   %s\n", tf(p), tf(q), tf(implies(p, q)), tf(implies(!q, !p)))
		}
	}

	// 2. De Morgan: !(p && q) == (!p || !q) for every row.
	ok := true
	for _, p := range []bool{true, false} {
		for _, q := range []bool{true, false} {
			if !(p && q) != (!p || !q) {
				ok = false
			}
		}
	}
	fmt.Println("De Morgan holds on all 4 rows:", ok)

	// 3. Power set of {a, b, c}: bit i of the mask says "include element i".
	elems := []string{"a", "b", "c"}
	var subsets []string
	for mask := 0; mask < 1<<len(elems); mask++ {
		var parts []string
		for i, e := range elems {
			if mask&(1<<i) != 0 {
				parts = append(parts, e)
			}
		}
		subsets = append(subsets, "{"+strings.Join(parts, ",")+"}")
	}
	fmt.Printf("power set has %d subsets: %s\n", len(subsets), strings.Join(subsets, " "))

	// 4. Cantor's diagonal: flip the i-th bit of the i-th row.
	rows := []string{"0110", "1010", "0011", "1111"}
	diag := make([]byte, len(rows))
	for i, r := range rows {
		if r[i] == '0' {
			diag[i] = '1'
		} else {
			diag[i] = '0'
		}
	}
	d := string(diag)
	found := false
	for _, r := range rows {
		if r == d {
			found = true
		}
	}
	fmt.Printf("diagonal-flipped string %s is in the list: %v\n", d, found)
}
