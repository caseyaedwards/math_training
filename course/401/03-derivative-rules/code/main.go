// Check each derivative rule against a numeric slope (central difference).
package main

import (
	"fmt"
	"math"
)

// deriv estimates f'(x) with a symmetric secant, which is more accurate than a one-sided one.
func deriv(f func(float64) float64, x float64) float64 {
	h := 1e-5
	return (f(x+h) - f(x-h)) / (2 * h)
}

func main() {
	x := 1.3
	checks := []struct {
		name string
		f    func(float64) float64
		rule float64
	}{
		{"power    4x^5 - 3x^2 + 7", func(t float64) float64 { return 4*math.Pow(t, 5) - 3*t*t + 7 }, 20*math.Pow(x, 4) - 6*x},
		{"product  x^2 sin x", func(t float64) float64 { return t * t * math.Sin(t) }, 2*x*math.Sin(x) + x*x*math.Cos(x)},
		{"quotient x/(x^2+1)", func(t float64) float64 { return t / (t*t + 1) }, (1 - x*x) / math.Pow(x*x+1, 2)},
		{"chain    (3x^2+1)^5", func(t float64) float64 { return math.Pow(3*t*t+1, 5) }, 30 * x * math.Pow(3*x*x+1, 4)},
		{"chain    ln(x^2+1)", func(t float64) float64 { return math.Log(t*t + 1) }, 2 * x / (x*x + 1)},
		{"exp      e^x", math.Exp, math.Exp(x)},
	}
	fmt.Printf("at x = %g\n", x)
	for _, c := range checks {
		fmt.Printf("  %-26s numeric %14.6f   rule %14.6f\n", c.name, deriv(c.f, x), c.rule)
	}
}
