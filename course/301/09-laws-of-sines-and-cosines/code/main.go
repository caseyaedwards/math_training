// Laws of sines and cosines: a small triangle solver that handles
// SAS, SSS, ASA and the ambiguous SSA case. Angles are in degrees.
// Run: go run main.go
package main

import (
	"fmt"
	"math"
)

func rad(d float64) float64 { return d * math.Pi / 180 }
func deg(r float64) float64 { return r * 180 / math.Pi }

// sas returns side c from sides a, b and the included angle C.
func sas(a, b, C float64) float64 {
	return math.Sqrt(a*a + b*b - 2*a*b*math.Cos(rad(C)))
}

// sssAngle returns angle C (opposite side c) from three sides.
func sssAngle(a, b, c float64) float64 {
	return deg(math.Acos((a*a + b*b - c*c) / (2 * a * b)))
}

// ssa returns every possible angle B given angle A, its opposite side a,
// and side b. It returns zero, one or two angles.
func ssa(A, a, b float64) []float64 {
	s := b * math.Sin(rad(A)) / a
	if s > 1 {
		return nil // side a is too short to reach the base line
	}
	B1 := deg(math.Asin(s))
	out := []float64{B1}
	if B2 := 180 - B1; A+B2 < 180 && math.Abs(B2-B1) > 1e-9 {
		out = append(out, B2) // the obtuse twin also fits
	}
	return out
}

func main() {
	fmt.Printf("SAS 5, 8, 60°: c = %.4f\n", sas(5, 8, 60))
	fmt.Printf("SSS 7, 8, 9: angle opposite 9 = %.2f°\n", sssAngle(7, 8, 9))

	// ASA: towers 10 km apart, angles 50° and 60°. Law of sines.
	C := 180.0 - 50 - 60
	fmt.Printf("ASA towers: fire is %.3f km from A and %.3f km from B\n",
		10*math.Sin(rad(60))/math.Sin(rad(C)), 10*math.Sin(rad(50))/math.Sin(rad(C)))

	for _, tc := range [][3]float64{{30, 6, 10}, {50, 8, 6}, {30, 3, 10}} {
		Bs := ssa(tc[0], tc[1], tc[2])
		fmt.Printf("SSA A=%.0f° a=%.0f b=%.0f: %d triangle(s)", tc[0], tc[1], tc[2], len(Bs))
		for _, B := range Bs {
			Cang := 180 - tc[0] - B
			c := tc[1] * math.Sin(rad(Cang)) / math.Sin(rad(tc[0]))
			fmt.Printf("  [B=%.2f° C=%.2f° c=%.3f]", B, Cang, c)
		}
		fmt.Println()
	}

	fmt.Printf("area with sides 5, 8 and 60° between: %.4f\n", 0.5*5*8*math.Sin(rad(60)))
}
