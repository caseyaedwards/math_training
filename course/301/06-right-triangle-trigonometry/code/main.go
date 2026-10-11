// Right-triangle trigonometry. Go's math.Sin, math.Cos and math.Tan take
// RADIANS, so every degree value goes through deg() first.
// Run: go run main.go
package main

import (
	"fmt"
	"math"
)

func deg(d float64) float64   { return d * math.Pi / 180 } // degrees to radians
func toDeg(r float64) float64 { return r * 180 / math.Pi } // radians to degrees

func main() {
	fmt.Println("angle    sin     cos     tan")
	for _, a := range []float64{0, 15, 30, 45, 60, 75} {
		fmt.Printf("%4.0f°  %6.4f  %6.4f  %6.4f\n", a, math.Sin(deg(a)), math.Cos(deg(a)), math.Tan(deg(a)))
	}

	fmt.Println("The classic bug: math.Sin(30) treats 30 as radians:", math.Sin(30))

	// Tower: 40 m away, angle of elevation 35 degrees.
	fmt.Printf("tower height = 40 tan 35° = %.2f m\n", 40*math.Tan(deg(35)))

	// Ladder: 5 m long, top at 4 m. Inverse sine gives the angle.
	fmt.Printf("ladder angle = asin(4/5)   = %.2f°\n", toDeg(math.Asin(4.0/5)))

	// Solve a right triangle with hypotenuse 10 and one angle 25 degrees.
	opp, adj := 10*math.Sin(deg(25)), 10*math.Cos(deg(25))
	fmt.Printf("hyp 10, 25°: opp = %.3f, adj = %.3f, other angle = %.0f°\n", opp, adj, 90.0-25)
	fmt.Printf("check Pythagoras: opp² + adj² = %.6f\n", opp*opp+adj*adj)
}
