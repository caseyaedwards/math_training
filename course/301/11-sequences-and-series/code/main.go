// Sequences and series: closed-form sums checked against loops,
// partial sums of an infinite geometric series, and the doubling
// growth of a Go slice.
// Run: go run main.go
package main

import "fmt"

func main() {
	// Arithmetic: 7, 11, 15, ... (d = 4). Loop versus formula n(a1 + an)/2.
	a1, d, n := 7, 4, 20
	loop := 0
	for k := 0; k < n; k++ {
		loop += a1 + k*d
	}
	an := a1 + (n-1)*d
	fmt.Printf("arithmetic: a20 = %d, loop sum = %d, formula = %d\n", an, loop, n*(a1+an)/2)

	// Geometric: 3, 6, 12, ... (r = 2). Formula a1(r^n - 1)/(r - 1).
	g, sum := 3, 0
	for k := 0; k < 8; k++ {
		sum += g
		g *= 2
	}
	fmt.Printf("geometric: first 8 terms sum to %d, formula = %d\n", sum, 3*(256-1))

	// Infinite geometric 1/2 + 1/4 + ... : partial sums approach 1.
	s, term := 0.0, 0.5
	for k := 1; k <= 30; k++ {
		s += term
		term /= 2
		if k == 1 || k == 2 || k == 5 || k == 10 || k == 30 {
			fmt.Printf("  S_%-2d = %.10f   gap to 1 = %.2e\n", k, s, 1-s)
		}
	}

	// A Go slice grows its capacity geometrically as you append.
	var xs []int
	last := -1
	fmt.Print("slice capacities while appending 2,000 ints:")
	for i := 0; i < 2000; i++ {
		xs = append(xs, i)
		if cap(xs) != last {
			last = cap(xs)
			fmt.Print(" ", last)
		}
	}
	fmt.Println()
}
