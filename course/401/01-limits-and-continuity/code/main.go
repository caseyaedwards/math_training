// Limits by sneaking up on a point, and bisection (the Intermediate Value Theorem at work).
package main

import (
	"fmt"
	"math"
)

func f(x float64) float64 { return (x*x - 1) / (x - 1) }

func g(x float64) float64 { return x*x*x + x - 1 }

func main() {
	fmt.Println("Approach x = 1 in f(x) = (x^2 - 1)/(x - 1):")
	for _, h := range []float64{0.1, 0.01, 0.001} {
		fmt.Printf("  x = %-6g f = %-8.4f   x = %-6g f = %.4f\n", 1-h, f(1-h), 1+h, f(1+h))
	}

	fmt.Println("sin(x)/x near 0 (radians):")
	for _, x := range []float64{0.1, 0.01, 0.001} {
		fmt.Printf("  x = %-6g ratio = %.8f\n", x, math.Sin(x)/x)
	}

	fmt.Println("Bisection on x^3 + x - 1 over [0, 1]:")
	lo, hi := 0.0, 1.0 // g(lo) < 0 < g(hi)
	for step := 1; step <= 40; step++ {
		mid := (lo + hi) / 2
		if g(mid) < 0 {
			lo = mid
		} else {
			hi = mid
		}
		if step <= 4 || step == 40 {
			fmt.Printf("  step %2d: [%.10f, %.10f]\n", step, lo, hi)
		}
	}
}
