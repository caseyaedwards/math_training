// The Fundamental Theorem, checked numerically:
// (1) adding up a rate gives the counter, (2) the slope of the accumulated area is the rate.
package main

import (
	"fmt"
	"math"
)

// rate is requests per second at time t.
func rate(t float64) float64 { return 200 + 100*math.Sin(math.Pi*t/30) }

// counter is the exact antiderivative of rate with counter(0) = 0.
func counter(t float64) float64 { return 200*t + 3000/math.Pi*(1-math.Cos(math.Pi*t/30)) }

// accumulate adds rate * dt from a to b with midpoint strips.
func accumulate(a, b float64, n int) float64 {
	dt := (b - a) / float64(n)
	sum := 0.0
	for i := 0; i < n; i++ {
		sum += rate(a+(float64(i)+0.5)*dt) * dt
	}
	return sum
}

func main() {
	fmt.Println("Part 2: area under the rate = change in the counter")
	for _, n := range []int{3, 30, 3000} {
		fmt.Printf("  strips %5d: sum of rate*dt from 10 to 40 = %.4f\n", n, accumulate(10, 40, n))
	}
	fmt.Printf("  counter(40) - counter(10)              = %.4f\n", counter(40)-counter(10))

	fmt.Println("Part 1: slope of the accumulated area = the rate")
	for _, x := range []float64{5, 15, 45} {
		h := 1e-3
		slope := (accumulate(0, x+h, 2000) - accumulate(0, x-h, 2000)) / (2 * h)
		fmt.Printf("  x = %2.0f: slope of A(x) = %.4f   rate(x) = %.4f\n", x, slope, rate(x))
	}
}
