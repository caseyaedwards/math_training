// Polynomials and complex numbers: synthetic division, powers of i,
// and quadratics with negative discriminants.
// Run: go run main.go
package main

import (
	"fmt"
	"math/cmplx"
)

// synthetic divides the polynomial with the given coefficients
// (highest power first) by (x - r). It returns the quotient and remainder.
func synthetic(coeffs []float64, r float64) ([]float64, float64) {
	out := []float64{coeffs[0]}
	for _, c := range coeffs[1:] {
		out = append(out, c+out[len(out)-1]*r)
	}
	return out[:len(out)-1], out[len(out)-1]
}

// quadRoots solves ax^2 + bx + c = 0 over the complex numbers.
func quadRoots(a, b, c complex128) (complex128, complex128) {
	d := cmplx.Sqrt(b*b - 4*a*c)
	return (-b + d) / (2 * a), (-b - d) / (2 * a)
}

func main() {
	q, rem := synthetic([]float64{1, -6, 11, -6}, 1)
	fmt.Println("x^3-6x^2+11x-6 divided by (x-1):", q, "remainder", rem)

	z := complex(3, 2)
	fmt.Println("(3+2i)(1-4i) =", z*complex(1, -4))
	fmt.Println("(3+2i)/(1-i)  =", z/complex(1, -1))
	fmt.Println("i*(3+2i)      =", 1i*z, " (a quarter turn)")
	fmt.Println("|3+4i|        =", cmplx.Abs(complex(3, 4)))

	p := complex(1, 0)
	for n := 1; n <= 8; n++ {
		p *= 1i
		fmt.Printf("i^%d = %v\n", n, p)
	}

	r1, r2 := quadRoots(1, -4, 13)
	fmt.Println("roots of x^2-4x+13:", r1, r2)
}
