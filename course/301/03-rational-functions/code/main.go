// Rational functions: watch values near a vertical asymptote, far out
// toward a horizontal asymptote, and solve a work-rate problem exactly.
// Run: go run main.go
package main

import (
	"fmt"
	"math/big"
)

func f(x float64) float64 { return (2*x + 1) / (x - 3) }

func main() {
	fmt.Println("Near the vertical asymptote x = 3:")
	for _, x := range []float64{2.9, 2.99, 2.999, 3.001, 3.01, 3.1} {
		fmt.Printf("  f(%-6v) = %10.1f\n", x, f(x))
	}

	fmt.Println("Far out, toward the horizontal asymptote y = 2:")
	for _, x := range []float64{10, 100, 1000, 1e6} {
		fmt.Printf("  f(%-7v) = %.6f\n", x, f(x))
	}

	// Work rate with exact fractions: A drains a queue in 6 h, B in 3 h.
	rateA := big.NewRat(1, 6)
	rateB := big.NewRat(1, 3)
	together := new(big.Rat).Add(rateA, rateB)
	hours := new(big.Rat).Inv(together)
	fmt.Println("Combined rate (jobs per hour):", together.RatString())
	fmt.Println("Hours for one job together:  ", hours.RatString())
}
