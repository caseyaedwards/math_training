// Trig graphs and identities: an ASCII plot of a daily traffic model and
// numeric spot checks of the main identities.
// Run: go run main.go
package main

import (
	"fmt"
	"math"
	"strings"
)

// traffic models requests per second at hour t of the day.
func traffic(t float64) float64 {
	return 500 + 300*math.Sin(2*math.Pi*(t-6)/24)
}

func main() {
	fmt.Println("hour  rps  (one # per 25 rps)")
	for h := 0; h <= 24; h += 2 {
		r := traffic(float64(h))
		fmt.Printf("%4d %4.0f  %s\n", h, r, strings.Repeat("#", int(math.Round(r/25))))
	}

	// Spot-check identities at a few angles. Each difference is ~0 up to rounding.
	fmt.Println("\nangle  sin²+cos²-1   sin2x-2sinxcosx   cos(-x)-cos(x)   sin(a+b)-formula")
	for _, x := range []float64{0.3, 1.0, 2.5, -4.0} {
		s, c := math.Sin(x), math.Cos(x)
		b := 0.7
		sumFormula := math.Sin(x)*math.Cos(b) + math.Cos(x)*math.Sin(b)
		fmt.Printf("%5.1f  %11.1e   %15.1e   %14.1e   %16.1e\n",
			x, s*s+c*c-1, math.Sin(2*x)-2*s*c, math.Cos(-x)-c, math.Sin(x+b)-sumFormula)
	}

	fmt.Printf("\nsin 75° = %.6f, (√6+√2)/4 = %.6f\n",
		math.Sin(75*math.Pi/180), (math.Sqrt(6)+math.Sqrt(2))/4)
}
