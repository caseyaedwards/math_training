// Newton's method, a batch-size optimum, and linear approximations versus the truth.
package main

import (
	"fmt"
	"math"
)

// newton solves f(x) = 0 by sliding down tangent lines.
func newton(f func(float64) float64, x float64, steps int) float64 {
	h := 1e-7
	for i := 1; i <= steps; i++ {
		slope := (f(x+h) - f(x-h)) / (2 * h)
		x = x - f(x)/slope
		fmt.Printf("    step %d: x = %.10f\n", i, x)
	}
	return x
}

func main() {
	fmt.Println("Newton on x^2 - 2 from x = 1:")
	newton(func(x float64) float64 { return x*x - 2 }, 1, 4)

	fmt.Println("Batch cost C(b) = 50/b + 0.02b, scan b = 10..100:")
	best, bestC := 0, math.Inf(1)
	for b := 10; b <= 100; b += 10 {
		c := 50/float64(b) + 0.02*float64(b)
		fmt.Printf("    b = %3d  C = %.3f ms\n", b, c)
		if c < bestC {
			best, bestC = b, c
		}
	}
	fmt.Printf("  best of the scan: b = %d, C = %.3f ms (calculus says b = 50)\n", best, bestC)

	fmt.Println("Linear approximation versus the truth:")
	fmt.Printf("    sqrt(4.1): tangent 2.025000, true %.6f\n", math.Sqrt(4.1))
	fmt.Printf("    1.01^10:   tangent 1.100000, true %.6f\n", math.Pow(1.01, 10))
	fmt.Printf("    sqrt(9):   tangent 3.250000, true %.6f  (too far from the anchor)\n", math.Sqrt(9))
}
