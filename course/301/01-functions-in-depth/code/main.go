// Functions as values: composition, inverses and a domain check.
// Run: go run main.go
package main

import (
	"fmt"
	"math"
)

// fn is a real function of one real variable.
type fn func(float64) float64

// compose returns the function x -> f(g(x)). g runs first.
func compose(f, g fn) fn {
	return func(x float64) float64 { return f(g(x)) }
}

func main() {
	square := func(x float64) float64 { return x * x }
	addOne := func(x float64) float64 { return x + 1 }

	fmt.Println("f(g(2)) =", compose(square, addOne)(2)) // 9
	fmt.Println("g(f(2)) =", compose(addOne, square)(2)) // 5: order matters

	// Celsius to Fahrenheit and back.
	cToF := func(c float64) float64 { return 9.0/5.0*c + 32 }
	fToC := func(f float64) float64 { return 5.0 / 9.0 * (f - 32) }
	for _, c := range []float64{-40, 0, 37, 100} {
		back := fToC(cToF(c))
		fmt.Printf("C=%6.1f  F=%6.1f  back=%6.1f\n", c, cToF(c), back)
	}

	// Domain check for f(x) = sqrt(x-3)/(x-5): NaN or Inf means "outside the domain".
	f := func(x float64) float64 { return math.Sqrt(x-3) / (x - 5) }
	for _, x := range []float64{2, 3, 4, 5, 6} {
		y := f(x)
		ok := !math.IsNaN(y) && !math.IsInf(y, 0)
		fmt.Printf("x=%v  f(x)=%v  in domain: %v\n", x, y, ok)
	}
}
