// Truth tables: the contrapositive always agrees with the original; the converse does not.
package main

import "fmt"

func implies(p, q bool) bool { return !p || q }

func tf(b bool) string {
	if b {
		return "T"
	}
	return "F"
}

func main() {
	fmt.Println("P Q | P=>Q  notQ=>notP  Q=>P")
	for _, p := range []bool{true, false} {
		for _, q := range []bool{true, false} {
			fmt.Printf("%s %s |   %s        %s          %s\n",
				tf(p), tf(q), tf(implies(p, q)), tf(implies(!q, !p)), tf(implies(q, p)))
		}
	}

	// Cases check: n^2 mod 4 is always 0 or 1.
	seen := map[int]bool{}
	for n := -1000; n <= 1000; n++ {
		r := (n * n) % 4
		seen[r] = true
	}
	fmt.Println("remainders of n^2 mod 4 for n in [-1000, 1000]:", seen)
}
