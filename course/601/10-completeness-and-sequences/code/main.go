// Sequences that climb toward a ceiling, and rationals that never reach it.
package main

import (
	"fmt"
	"math"
	"math/big"
)

func main() {
	// a(1) = sqrt(2), a(n+1) = sqrt(2 + a(n)): increasing, bounded by 2.
	fmt.Println("a(n+1) = sqrt(2 + a(n))")
	a := math.Sqrt(2)
	for n := 1; n <= 8; n++ {
		fmt.Printf("  a(%d) = %.10f   gap to 2 = %.2e\n", n, a, 2-a)
		a = math.Sqrt(2 + a)
	}

	// Newton's method for sqrt(2) in exact fractions: x -> (x + 2/x) / 2.
	// Every term is rational. The limit, sqrt(2), is not.
	fmt.Println("Newton steps for sqrt(2), exact fractions")
	x := big.NewRat(3, 2)
	two := big.NewRat(2, 1)
	half := big.NewRat(1, 2)
	for i := 1; i <= 4; i++ {
		sq := new(big.Rat).Mul(x, x)
		diff := new(big.Rat).Sub(sq, two)
		f, _ := diff.Float64()
		fmt.Printf("  x = %-22s x^2 - 2 = %.3e\n", x.RatString(), f)
		inv := new(big.Rat).Quo(two, x)
		x = new(big.Rat).Mul(new(big.Rat).Add(x, inv), half)
	}

	// The epsilon-N game for a(n) = n/(n+1) -> 1: N = ceil(1/eps) works.
	fmt.Println("n/(n+1) -> 1: the N that answers each eps")
	for _, eps := range []float64{0.1, 0.01, 0.001} {
		N := int(math.Ceil(1 / eps))
		v := float64(N+1) / float64(N+2)
		fmt.Printf("  eps = %-6g N = %-5d first term after N: |a - 1| = %.6f\n", eps, N, 1-v)
	}
}
