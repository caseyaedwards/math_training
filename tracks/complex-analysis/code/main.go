// Complex analysis starter kit: rotation by i, polar form, Euler formula,
// roots of unity, a power series, contour integrals and a Mandelbrot set.
// Standard library only (math/cmplx handles complex numbers).
package main

import (
	"fmt"
	"math"
	"math/cmplx"
	"strings"
)

func show(z complex128) string {
	return fmt.Sprintf("%+.3f %+.3fi", real(z), imag(z))
}

func main() {
	fmt.Println("== Multiplying by i turns 90 degrees ==")
	z := complex(2, 1)
	for k := 0; k < 4; k++ {
		fmt.Printf("i^%d z = %s   |.| = %.3f\n", k, show(z), cmplx.Abs(z))
		z *= 1i
	}

	fmt.Println("\n== Polar form: lengths multiply, angles add ==")
	a, b := complex(1, 1), complex(1, math.Sqrt(3))
	for _, w := range []complex128{a, b, a * b} {
		r, th := cmplx.Polar(w)
		fmt.Printf("%s  length %.4f  angle %6.1f deg\n", show(w), r, th*180/math.Pi)
	}

	fmt.Println("\n== Euler formula ==")
	fmt.Println("e^(i pi)   =", show(cmplx.Exp(1i*math.Pi)))
	fmt.Println("e^(i pi/2) =", show(cmplx.Exp(1i*math.Pi/2)))

	fmt.Println("\n== Sixth roots of unity ==")
	var sum complex128
	for k := 0; k < 6; k++ {
		w := cmplx.Exp(complex(0, 2*math.Pi*float64(k)/6))
		sum += w
		fmt.Printf("k=%d %s   w^6 = %s\n", k, show(w), show(cmplx.Pow(w, 6)))
	}
	fmt.Println("sum of roots =", show(sum))

	fmt.Println("\n== Power series for e^(i pi), partial sums ==")
	term, s := complex(1, 0), complex(0, 0)
	for k := 0; k <= 16; k++ {
		s += term
		if k%4 == 0 {
			fmt.Printf("S%-2d = %s\n", k+1, show(s))
		}
		term *= 1i * math.Pi / complex(float64(k+1), 0)
	}

	fmt.Println("\n== Contour integral of 1/z around circles (10,000 steps) ==")
	loop := func(center complex128, radius float64) complex128 {
		n := 10000
		var total complex128
		for k := 0; k < n; k++ {
			t0 := 2 * math.Pi * float64(k) / float64(n)
			t1 := 2 * math.Pi * float64(k+1) / float64(n)
			z0 := center + cmplx.Rect(radius, t0)
			z1 := center + cmplx.Rect(radius, t1)
			total += (1 / ((z0 + z1) / 2)) * (z1 - z0) // midpoint rule
		}
		return total
	}
	fmt.Println("around 0:    ", show(loop(0, 1.3)), " (2 pi i =", show(2i*math.Pi)+")")
	fmt.Println("around 3.8:  ", show(loop(3.8, 1.3)))

	fmt.Println("\n== Residue check: integral of 1/(1+x^2) over [-1000, 1000] ==")
	n, L := 2000000, 1000.0
	h := 2 * L / float64(n)
	total := 0.0
	for k := 0; k < n; k++ {
		x := -L + (float64(k)+0.5)*h
		total += h / (1 + x*x)
	}
	fmt.Printf("numeric %.6f, pi %.6f (the tails past 1000 hold the last 0.002)\n", total, math.Pi)

	fmt.Println("\n== Mandelbrot set: c where z -> z^2 + c stays bounded ==")
	for row := 0; row < 15; row++ {
		var line strings.Builder
		for col := 0; col < 60; col++ {
			c := complex(-2.1+2.7*float64(col)/59, 1.2-2.4*float64(row)/14)
			z := complex(0, 0)
			inside := true
			for it := 0; it < 50; it++ {
				z = z*z + c
				if cmplx.Abs(z) > 2 {
					inside = false
					break
				}
			}
			if inside {
				line.WriteByte('#')
			} else {
				line.WriteByte('.')
			}
		}
		fmt.Println(line.String())
	}
}
