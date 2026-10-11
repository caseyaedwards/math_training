// Check substitution and integration-by-parts answers with Simpson's rule.
package main

import (
	"fmt"
	"math"
)

// simpson integrates f on [a, b] with n (even) strips, fitting parabolas through point triples.
func simpson(f func(float64) float64, a, b float64, n int) float64 {
	h := (b - a) / float64(n)
	sum := f(a) + f(b)
	for i := 1; i < n; i++ {
		w := 2.0
		if i%2 == 1 {
			w = 4
		}
		sum += w * f(a+float64(i)*h)
	}
	return sum * h / 3
}

func main() {
	checks := []struct {
		name    string
		f       func(float64) float64
		a, b    float64
		formula float64
	}{
		{"sub:   2x cos(x^2), 0..sqrt(pi/2)", func(x float64) float64 { return 2 * x * math.Cos(x*x) }, 0, math.Sqrt(math.Pi / 2), 1},
		{"sub:   x/(x^2+1), 0..1", func(x float64) float64 { return x / (x*x + 1) }, 0, 1, math.Log(2) / 2},
		{"sub:   (2x+3)^4, 0..1", func(x float64) float64 { return math.Pow(2*x+3, 4) }, 0, 1, (math.Pow(5, 5) - math.Pow(3, 5)) / 10},
		{"parts: x e^x, 0..1", func(x float64) float64 { return x * math.Exp(x) }, 0, 1, 1},
		{"parts: x cos x, 0..pi/2", func(x float64) float64 { return x * math.Cos(x) }, 0, math.Pi / 2, math.Pi/2 - 1},
		{"parts: ln x, 1..e", math.Log, 1, math.E, 1},
		{"parts: t e^-t, 0..50 (mean wait)", func(t float64) float64 { return t * math.Exp(-t) }, 0, 50, 1},
	}
	for _, c := range checks {
		fmt.Printf("%-36s simpson %.8f   formula %.8f\n", c.name, simpson(c.f, c.a, c.b, 1000), c.formula)
	}
}
