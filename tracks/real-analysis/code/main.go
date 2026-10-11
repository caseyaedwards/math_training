// Real analysis starter kit: epsilon-N, series that converge and one that
// does not, a nested-interval hunt for the square root of 2, Riemann sums
// and a sequence of functions that fails to converge uniformly.
// Standard library only.
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println("== Epsilon-N for a_n = 1 + (-1)^n / n ==")
	for _, eps := range []float64{0.15, 0.01, 0.001} {
		N := int(math.Floor(1/eps)) + 1 // smallest n with 1/n < eps
		fmt.Printf("eps = %-6g N = %-5d check |a_N - 1| = %.6f\n", eps, N, 1/float64(N))
	}

	fmt.Println("\n== Partial sums ==")
	geo, harm, alt := 0.0, 0.0, 0.0
	for n := 1; n <= 1000000; n++ {
		geo += math.Pow(0.5, float64(n))
		harm += 1 / float64(n)
		alt += math.Pow(-1, float64(n+1)) / float64(n)
		if n == 10 || n == 1000 || n == 1000000 {
			fmt.Printf("n = %-8d 1/2+1/4+... = %.6f   1+1/2+1/3+... = %8.4f   1-1/2+1/3-... = %.6f\n", n, geo, harm, alt)
		}
	}
	fmt.Printf("limits:      geometric -> 1, harmonic -> infinity (like ln n = %.4f), alternating -> ln 2 = %.6f\n", math.Log(1e6), math.Ln2)

	fmt.Println("\n== Nested intervals close in on sqrt(2) ==")
	lo, hi := 1.0, 2.0
	for step := 1; step <= 30; step++ {
		mid := (lo + hi) / 2
		if mid*mid < 2 {
			lo = mid
		} else {
			hi = mid
		}
		if step%6 == 0 {
			fmt.Printf("step %2d: [%.10f, %.10f] width %.1e\n", step, lo, hi, hi-lo)
		}
	}

	fmt.Println("\n== Riemann sums for x^2 on [0, 1] (exact 1/3) ==")
	for _, n := range []int{5, 50, 500, 5000} {
		lower, upper := 0.0, 0.0
		for k := 0; k < n; k++ {
			a, b := float64(k)/float64(n), float64(k+1)/float64(n)
			lower += a * a / float64(n)
			upper += b * b / float64(n)
		}
		fmt.Printf("n = %-5d lower %.6f  upper %.6f  gap %.6f\n", n, lower, upper, upper-lower)
	}

	fmt.Println("\n== x^n on [0, 1): pointwise to 0, but not uniformly ==")
	for _, n := range []int{1, 10, 100, 1000} {
		x := math.Pow(0.5, 1/float64(n)) // the point where x^n = 0.5
		fmt.Printf("n = %-5d x^n is still 0.5 at x = %.6f\n", n, x)
	}
	fmt.Println("For every n some x < 1 has x^n = 0.5: the worst-case error never shrinks.")
}
