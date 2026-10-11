// Factor x^2 + bx + c by searching for two integers,
// and solve a*x^2 + b*x + c = 0 with the quadratic formula.
package main

import (
	"fmt"
	"math"
)

// factor looks for integers p and q with p*q = c and p + q = b.
// Then x^2 + bx + c = (x + p)(x + q).
func factor(b, c int) string {
	for p := -100; p <= 100; p++ {
		q := b - p
		if p*q == c && p <= q {
			return "(x " + term(p) + ")(x " + term(q) + ")"
		}
	}
	return "no integer factors"
}

// term writes 3 as "+ 3" and -3 as "- 3".
func term(n int) string {
	if n < 0 {
		return fmt.Sprintf("- %d", -n)
	}
	return fmt.Sprintf("+ %d", n)
}

// roots applies the quadratic formula.
func roots(a, b, c float64) string {
	d := b*b - 4*a*c // the discriminant
	switch {
	case d < 0:
		return fmt.Sprintf("discriminant %g < 0: no real roots", d)
	case d == 0:
		return fmt.Sprintf("discriminant 0: one root x = %g", -b/(2*a))
	default:
		r1 := (-b - math.Sqrt(d)) / (2 * a)
		r2 := (-b + math.Sqrt(d)) / (2 * a)
		return fmt.Sprintf("discriminant %g: x = %.4g or x = %.4g", d, r1, r2)
	}
}

func main() {
	fmt.Println("x^2 + 5x + 6   =", factor(5, 6))
	fmt.Println("x^2 - x - 6    =", factor(-1, -6))
	fmt.Println("x^2 + 7x + 12  =", factor(7, 12))
	fmt.Println("x^2 + 0x - 49  =", factor(0, -49))
	fmt.Println("x^2 + x + 1    =", factor(1, 1))
	fmt.Println()
	fmt.Println("x^2 - x - 6 = 0    :", roots(1, -1, -6))
	fmt.Println("2x^2 + 3x - 2 = 0  :", roots(2, 3, -2))
	fmt.Println("x^2 + 2x - 1 = 0   :", roots(1, 2, -1))
	fmt.Println("x^2 - 6x + 9 = 0   :", roots(1, -6, 9))
	fmt.Println("x^2 + 2 = 0        :", roots(1, 0, 2))
}
