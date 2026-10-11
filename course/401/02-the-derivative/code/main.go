// Difference quotients: watch secant slopes become a derivative,
// then watch floating point ruin the party when h gets too small.
package main

import "fmt"

func f(x float64) float64 { return x * x }

// N is a request counter: total requests after t seconds.
func N(t float64) float64 { return 5*t*t + 100*t }

func main() {
	fmt.Println("Slope of x^2 at x = 1, (f(1+h) - f(1)) / h:")
	for _, h := range []float64{1, 0.1, 0.01, 1e-4, 1e-8, 1e-12, 1e-15} {
		fmt.Printf("  h = %-6g slope = %.15f\n", h, (f(1+h)-f(1))/h)
	}

	fmt.Println("Counter N(t) = 5t^2 + 100t, rate ending at t = 20:")
	for _, w := range []float64{10, 5, 1, 0.1, 0.001} {
		fmt.Printf("  window %-6g s: %.3f req/s\n", w, (N(20)-N(20-w))/w)
	}
	fmt.Println("  derivative N'(20) = 10*20 + 100 =", 10*20+100, "req/s")
}
