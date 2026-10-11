// Area between curves, volume of a solid of revolution, and average values,
// each computed by adding thin slices.
package main

import (
	"fmt"
	"math"
)

// sum adds f(x)*dx over n midpoint slices of [a, b].
func sum(f func(float64) float64, a, b float64, n int) float64 {
	dx := (b - a) / float64(n)
	s := 0.0
	for i := 0; i < n; i++ {
		s += f(a+(float64(i)+0.5)*dx) * dx
	}
	return s
}

func main() {
	n := 100000
	between := sum(func(x float64) float64 { return x - x*x }, 0, 1, n)
	fmt.Printf("area between y = x and y = x^2:   %.6f (exact 1/6 = %.6f)\n", between, 1.0/6)

	disks := sum(func(x float64) float64 { r := math.Sqrt(x); return math.Pi * r * r }, 0, 4, n)
	fmt.Printf("volume, sqrt(x) spun on [0, 4]:   %.6f (exact 8 pi = %.6f)\n", disks, 8*math.Pi)

	avg := sum(math.Sin, 0, math.Pi, n) / math.Pi
	fmt.Printf("average of sin x on [0, pi]:      %.6f (exact 2/pi = %.6f)\n", avg, 2/math.Pi)

	rate := func(t float64) float64 { return 200 + 100*math.Sin(math.Pi*t/30) }
	total := sum(rate, 0, 45, n)
	fmt.Printf("requests in 45 s: %.1f, average rate %.2f req/s\n", total, total/45)

	load := func(h float64) float64 { return 500 + 300*math.Sin(math.Pi*(h-6)/12) }
	head := sum(func(h float64) float64 { return 1000 - load(h) }, 0, 24, n)
	fmt.Printf("headroom over a day: %.0f req/s-hours = %.0f million spare requests\n", head, head*3600/1e6)
}
