// Truth tables by brute force: try every row, print the result.
package main

import "fmt"

func tf(b bool) string {
	if b {
		return "T"
	}
	return "F"
}

func implies(p, q bool) bool { return !p || q }

func main() {
	rows := []bool{true, false}

	fmt.Println("P Q | P->Q | not Q -> not P")
	for _, p := range rows {
		for _, q := range rows {
			fmt.Printf("%s %s |  %s   |  %s\n", tf(p), tf(q), tf(implies(p, q)), tf(implies(!q, !p)))
		}
	}

	// De Morgan: check both laws on all four rows.
	ok := true
	for _, p := range rows {
		for _, q := range rows {
			if !(p && q) != (!p || !q) || !(p || q) != (!p && !q) {
				ok = false
			}
		}
	}
	fmt.Println("De Morgan holds on every row:", ok)

	// n letters give 2^n rows.
	for n := 1; n <= 4; n++ {
		fmt.Printf("%d letters -> %d rows\n", n, 1<<n)
	}
}
