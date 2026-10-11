// Limits preview: approach a point numerically, watch secant slopes
// settle into a tangent slope, and watch rectangle sums settle into an area.
// Run: go run main.go
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println("(x²-1)/(x-1) near x = 1 (undefined AT 1):")
	for _, h := range []float64{0.1, 0.01, 0.001} {
		for _, x := range []float64{1 - h, 1 + h} {
			fmt.Printf("  x = %-6v -> %.4f\n", x, (x*x-1)/(x-1))
		}
	}

	fmt.Println("sin(x)/x near 0, x in radians, then x in degrees:")
	for _, x := range []float64{0.1, 0.01, 0.001} {
		rad := math.Sin(x) / x
		deg := math.Sin(x*math.Pi/180) / x
		fmt.Printf("  x = %-6v radians: %.6f   degrees: %.6f\n", x, rad, deg)
	}
	fmt.Printf("  (π/180 = %.6f)\n", math.Pi/180)

	fmt.Println("secant slopes of y = x² from x = 1 to x = 1 + h:")
	for _, h := range []float64{1, 0.5, 0.1, 0.01, 0.001} {
		fmt.Printf("  h = %-6v slope = %.4f\n", h, ((1+h)*(1+h)-1)/h)
	}

	fmt.Println("left rectangle sums for the area under y = x² on [0, 1]:")
	for _, n := range []int{4, 16, 100, 10000} {
		sum := 0.0
		w := 1 / float64(n)
		for k := 0; k < n; k++ {
			x := float64(k) * w
			sum += x * x * w
		}
		fmt.Printf("  n = %-6d area ≈ %.6f\n", n, sum)
	}
	fmt.Println("  exact: 1/3 ≈ 0.333333")
}
