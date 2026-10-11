// Command main replays two methods from the Islamic Golden Age:
// al-Khwarizmi's recipe for "squares and roots equal numbers"
// and Omar Khayyam's cubic x^3 + 4x = 16, found by bisection and
// checked against his parabola-and-circle picture.
package main

import (
	"fmt"
	"math"
)

// khwarizmi solves x^2 + b*x = c with his spoken recipe.
// It prints each step and returns the one positive root.
func khwarizmi(b, c float64) float64 {
	fmt.Printf("Solve x^2 + %gx = %g\n", b, c)
	half := b / 2
	fmt.Printf("  halve the roots:        %g / 2 = %g\n", b, half)
	sq := half * half
	fmt.Printf("  square the half:        %g x %g = %g\n", half, half, sq)
	total := c + sq
	fmt.Printf("  add it to the number:   %g + %g = %g\n", c, sq, total)
	side := math.Sqrt(total)
	fmt.Printf("  take the root:          sqrt(%g) = %g\n", total, side)
	x := side - half
	fmt.Printf("  subtract the half:      %g - %g = %g\n", side, half, x)
	fmt.Printf("  check: %g^2 + %g x %g = %g\n\n", x, b, x, x*x+b*x)
	return x
}

// bisect finds a root of f between lo and hi, where f(lo) and f(hi)
// have opposite signs. Each pass halves the interval.
func bisect(f func(float64) float64, lo, hi float64, steps int) float64 {
	for i := 1; i <= steps; i++ {
		mid := (lo + hi) / 2
		if f(lo)*f(mid) <= 0 {
			hi = mid
		} else {
			lo = mid
		}
		if i <= 5 || i == steps {
			fmt.Printf("  step %2d: root is in [%.6f, %.6f]\n", i, lo, hi)
		}
	}
	return (lo + hi) / 2
}

func main() {
	fmt.Println("== al-Khwarizmi: complete the square ==")
	khwarizmi(10, 39) // his own example
	khwarizmi(6, 16)
	khwarizmi(8, 48)

	fmt.Println("== Omar Khayyam: x^3 + 4x = 16 ==")
	f := func(x float64) float64 { return x*x*x + 4*x - 16 }
	fmt.Println("Bisection on [0, 3]:")
	x := bisect(f, 0, 3, 30)
	fmt.Printf("  bisection root: %.9f\n", x)

	// Khayyam's curves: parabola y = x^2/2 and the circle with
	// center (2, 0) and radius 2. A root lies where both agree.
	y := x * x / 2
	dist := math.Hypot(x-2, y)
	fmt.Printf("  parabola point: (%.6f, %.6f)\n", x, y)
	fmt.Printf("  distance to circle center (2, 0): %.6f (radius 2)\n", dist)
	fmt.Printf("  geometric answer: x = 2, check 2^3 + 4 x 2 = %d\n", 2*2*2+4*2)
}
