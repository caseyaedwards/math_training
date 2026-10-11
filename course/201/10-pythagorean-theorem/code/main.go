// Pythagorean theorem: distances, the converse test, and a triple finder.
package main

import (
	"fmt"
	"math"
)

// distance between two points on the plane.
func distance(x1, y1, x2, y2 float64) float64 {
	dx, dy := x2-x1, y2-y1
	return math.Sqrt(dx*dx + dy*dy)
}

// kind uses the converse: compare c^2 with a^2 + b^2, c the longest side.
func kind(a, b, c int) string {
	s := a*a + b*b
	switch {
	case c*c == s:
		return "right"
	case c*c < s:
		return "acute"
	default:
		return "obtuse"
	}
}

func main() {
	fmt.Println("legs 6 and 8, hypotenuse:", math.Hypot(6, 8))
	fmt.Println("distance (1,2) to (7,10):", distance(1, 2, 7, 10))
	fmt.Printf("unit cube space diagonal: %.4f\n", math.Sqrt(3))
	fmt.Println("3, 4, 5 is", kind(3, 4, 5))
	fmt.Println("6, 8, 11 is", kind(6, 8, 11))
	fmt.Println("7, 24, 25 is", kind(7, 24, 25))

	fmt.Println("whole-number right triangles with c <= 30:")
	for c := 1; c <= 30; c++ {
		for a := 1; a < c; a++ {
			for b := a; b < c; b++ {
				if a*a+b*b == c*c {
					fmt.Printf("  %d, %d, %d\n", a, b, c)
				}
			}
		}
	}
}
