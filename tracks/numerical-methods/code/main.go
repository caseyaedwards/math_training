// Numerical methods starter kit: floating-point surprises, machine
// epsilon, Kahan summation, cancellation, bisection versus Newton,
// numerical integration and step-size stability.
// Standard library only.
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println("== Floating-point surprises ==")
	a, b := 0.1, 0.2
	fmt.Println("0.1 + 0.2 == 0.3 ?", a+b == 0.3)
	fmt.Printf("0.1 + 0.2 = %.20f\n", a+b)
	fmt.Printf("0.3       = %.20f\n", 0.3)
	var f32 float32 = 16777216 // 2^24
	fmt.Println("float32: 16777216 + 1 =", f32+1, "(counter stuck)")
	fmt.Println("float64 integers are exact up to 2^53 =", int64(1)<<53)

	fmt.Println("\n== Machine epsilon ==")
	eps := 1.0
	for 1+eps/2 > 1 {
		eps /= 2
	}
	fmt.Printf("smallest eps with 1 + eps > 1: %g (2^-52)\n", eps)
	fmt.Printf("gap between doubles near 1e16: %g\n", math.Nextafter(1e16, math.Inf(1))-1e16)

	fmt.Println("\n== Adding 0.1 ten million times (true answer 1,000,000) ==")
	naive, sum, comp := 0.0, 0.0, 0.0
	for i := 0; i < 10_000_000; i++ {
		naive += 0.1
		y := 0.1 - comp // Kahan: carry the lost low bits forward
		t := sum + y
		comp = (t - sum) - y
		sum = t
	}
	fmt.Printf("naive sum: %.6f\n", naive)
	fmt.Printf("Kahan sum: %.6f\n", sum)

	fmt.Println("\n== Cancellation: (1 - cos x) / x^2, true value near 0.5 ==")
	for _, x := range []float64{1e-2, 1e-4, 1e-6, 1e-8} {
		bad := (1 - math.Cos(x)) / (x * x)
		s := math.Sin(x / 2)
		good := 2 * s * s / (x * x) // same formula, rewritten: 1 - cos x = 2 sin^2(x/2)
		fmt.Printf("x = %-6g naive %.10f   rewritten %.10f\n", x, bad, good)
	}

	fmt.Println("\n== Root of x^2 - 2: iterations to reach 1e-12 ==")
	lo, hi, n := 1.0, 2.0, 0
	for hi-lo > 1e-12 {
		mid := (lo + hi) / 2
		if mid*mid < 2 {
			lo = mid
		} else {
			hi = mid
		}
		n++
	}
	fmt.Printf("bisection: %d steps -> %.12f\n", n, (lo+hi)/2)
	x, k := 3.0, 0
	for math.Abs(x*x-2) > 1e-12 {
		x -= (x*x - 2) / (2 * x)
		k++
		fmt.Printf("  newton step %d: %.15f\n", k, x)
	}
	fmt.Printf("newton:    %d steps -> %.12f\n", k, x)

	fmt.Println("\n== Integrate x^2 on [0, 2] (exact 8/3 = 2.666667) ==")
	fx := func(t float64) float64 { return t * t }
	for _, m := range []int{4, 40} {
		h := 2 / float64(m)
		trap := (fx(0) + fx(2)) / 2
		simp := fx(0) + fx(2)
		for i := 1; i < m; i++ {
			trap += fx(float64(i) * h)
			w := 2.0
			if i%2 == 1 {
				w = 4
			}
			simp += w * fx(float64(i)*h)
		}
		fmt.Printf("%2d strips: trapezoid %.6f  Simpson %.6f\n", m, trap*h, simp*h/3)
	}

	fmt.Println("\n== Euler on y' = -10y, y(0) = 1: value at t = 2 (exact 2.06e-09) ==")
	for _, h := range []float64{0.25, 0.2, 0.05, 0.01} {
		y := 1.0
		for i := 0; i < int(math.Round(2/h)); i++ {
			y *= 1 - 10*h
		}
		fmt.Printf("h = %-5g factor %+.2f per step -> %g\n", h, 1-10*h, y)
	}
}
