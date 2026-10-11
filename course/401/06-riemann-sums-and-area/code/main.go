// Riemann sums for x^2 on [0, 2] four ways, and a request total from rate buckets.
package main

import "fmt"

func f(x float64) float64 { return x * x }

// riemann adds n strips of width dx; pick sets where in each strip the height is sampled.
func riemann(a, b float64, n int, pick float64) float64 {
	dx := (b - a) / float64(n)
	sum := 0.0
	for i := 0; i < n; i++ {
		x := a + (float64(i)+pick)*dx
		sum += f(x) * dx
	}
	return sum
}

func main() {
	fmt.Println("     n        left       right    midpoint   trapezoid   (exact 2.666667)")
	for _, n := range []int{4, 8, 16, 100, 1000} {
		l, r := riemann(0, 2, n, 0), riemann(0, 2, n, 1)
		fmt.Printf("%6d  %10.6f  %10.6f  %10.6f  %10.6f\n", n, l, r, riemann(0, 2, n, 0.5), (l+r)/2)
	}

	rates := []float64{120, 180, 260, 300, 220, 140} // req/s, one value per minute
	total := 0.0
	for _, r := range rates {
		total += r * 60 // rate times width of the bucket
	}
	fmt.Printf("requests over 6 minutes: %.0f\n", total)
}
