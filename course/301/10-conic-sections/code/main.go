// Conic sections: complete the square for a circle, check the focus
// properties of a parabola and an ellipse, and classify equations.
// Run: go run main.go
package main

import (
	"fmt"
	"math"
)

// circleFrom takes x^2 + y^2 + Dx + Ey + F = 0 and returns center and radius
// by completing the square: (x + D/2)^2 + (y + E/2)^2 = D^2/4 + E^2/4 - F.
func circleFrom(D, E, F float64) (h, k, r float64) {
	h, k = -D/2, -E/2
	return h, k, math.Sqrt(D*D/4 + E*E/4 - F)
}

// classify uses the signs of A and C in Ax^2 + Cy^2 + ... = 0.
func classify(A, C float64) string {
	switch {
	case A == 0 || C == 0:
		return "parabola"
	case A == C:
		return "circle"
	case A*C > 0:
		return "ellipse"
	default:
		return "hyperbola"
	}
}

func dist(x1, y1, x2, y2 float64) float64 { return math.Hypot(x2-x1, y2-y1) }

func main() {
	h, k, r := circleFrom(-6, 4, -12)
	fmt.Printf("x²+y²-6x+4y-12=0: center (%g, %g), radius %g\n", h, k, r)

	fmt.Println("Parabola y = x²/4, focus (0,1), directrix y = -1:")
	for _, x := range []float64{-4, -1, 2, 6} {
		y := x * x / 4
		fmt.Printf("  P(%g, %g): to focus %.4f, to directrix %.4f\n", x, y, dist(x, y, 0, 1), y+1)
	}

	fmt.Println("Ellipse x²/25 + y²/9 = 1, foci (±4, 0):")
	for _, t := range []float64{0, 0.7, 2, 4} {
		x, y := 5*math.Cos(t), 3*math.Sin(t) // a standard way to walk around an ellipse
		fmt.Printf("  P(%6.3f, %6.3f): PF1 + PF2 = %.4f\n", x, y, dist(x, y, -4, 0)+dist(x, y, 4, 0))
	}

	for _, eq := range []struct {
		name string
		A, C float64
	}{{"x² - y² = 1", 1, -1}, {"y = 2x² + 3", 2, 0}, {"2x² + 2y² = 8", 2, 2}, {"x² + 4y² = 4", 1, 4}} {
		fmt.Printf("%-14s -> %s\n", eq.name, classify(eq.A, eq.C))
	}
}
