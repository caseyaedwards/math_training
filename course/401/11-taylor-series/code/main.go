// Taylor polynomials built term by term, and the small-x shortcuts SREs use daily.
package main

import (
	"fmt"
	"math"
)

// sinTaylor adds the terms x - x^3/3! + x^5/5! - ... up to the given degree.
func sinTaylor(x float64, degree int) float64 {
	term, sum := x, 0.0
	for k := 1; k <= degree; k += 2 {
		sum += term
		term *= -x * x / float64((k+1)*(k+2)) // next odd term from the previous one
	}
	return sum
}

// expTaylor adds 1 + x + x^2/2! + ... up to the given degree.
func expTaylor(x float64, degree int) float64 {
	term, sum := 1.0, 0.0
	for k := 0; k <= degree; k++ {
		sum += term
		term *= x / float64(k+1)
	}
	return sum
}

func main() {
	fmt.Println("degree   sin(1) approx   sin(3) approx   e^1 approx")
	for _, d := range []int{1, 3, 5, 7, 9} {
		fmt.Printf("%6d   %13.9f   %13.9f   %11.9f\n", d, sinTaylor(1, d), sinTaylor(3, d), expTaylor(1, d))
	}
	fmt.Printf("  true   %13.9f   %13.9f   %11.9f\n", math.Sin(1), math.Sin(3), math.E)

	fmt.Println("At least one of 100 parts fails, each with chance p:")
	for _, p := range []float64{0.0001, 0.001, 0.01, 0.05} {
		fmt.Printf("  p = %-6g exact %.4f   estimate 100p = %.4f\n", p, 1-math.Pow(1-p, 100), 100*p)
	}
	fmt.Printf("ln(1.03) = %.5f vs 0.03;  sqrt(1.02) = %.5f vs 1.01\n", math.Log(1.03), math.Sqrt(1.02))
}
