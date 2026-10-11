// Chapter 07: The Scientific Revolution and Calculus.
// Four small experiments with the tools of the 1600s:
// slopes by shrinking steps, areas by thin strips,
// logarithms that turn products into sums, and
// Pascal's triangle applied to the problem of points.
package main

import (
	"fmt"
	"math"
)

func f(x float64) float64 { return x * x }

// slope returns the slope of the secant from (x, f(x)) to (x+h, f(x+h)).
func slope(x, h float64) float64 {
	return (f(x+h) - f(x)) / h
}

// leftSum adds n strips under f on [a, b], each strip as tall as
// the curve at its left edge.
func leftSum(a, b float64, n int) float64 {
	w := (b - a) / float64(n)
	total := 0.0
	for i := 0; i < n; i++ {
		total += f(a+float64(i)*w) * w
	}
	return total
}

// pascal returns rows 0..n of the arithmetic triangle.
func pascal(n int) [][]int {
	rows := [][]int{{1}}
	for r := 1; r <= n; r++ {
		prev := rows[r-1]
		row := make([]int, r+1)
		row[0], row[r] = 1, 1
		for k := 1; k < r; k++ {
			row[k] = prev[k-1] + prev[k]
		}
		rows = append(rows, row)
	}
	return rows
}

// points splits the stakes when player A needs a more wins and
// player B needs b more. Play at most a+b-1 more fair rounds and
// count the outcomes in which A gets at least a wins.
func points(a, b int) (aWays, total int) {
	n := a + b - 1
	row := pascal(n)[n]
	for k := a; k <= n; k++ {
		aWays += row[k]
	}
	return aWays, 1 << n
}

func main() {
	fmt.Println("1. Slope of y = x^2 at x = 1 (secant slopes)")
	for _, h := range []float64{1, 0.5, 0.1, 0.01, 0.001} {
		fmt.Printf("   h = %-6g slope = %.4f\n", h, slope(1, h))
	}

	fmt.Println("\n2. Area under y = x^2 from 0 to 2 (left strips)")
	for _, n := range []int{8, 100, 1000, 100000} {
		fmt.Printf("   n = %-7d area = %.6f\n", n, leftSum(0, 2, n))
	}
	fmt.Printf("   exact 8/3   area = %.6f\n", 8.0/3.0)

	fmt.Println("\n3. Logarithms (base 10, as in Briggs)")
	l2, l3, l6 := math.Log10(2), math.Log10(3), math.Log10(6)
	fmt.Printf("   log 2 + log 3 = %.5f + %.5f = %.5f\n", l2, l3, l2+l3)
	fmt.Printf("   log 6         = %.5f\n", l6)
	fmt.Printf("   10^(log 2 + log 3) = %.4f\n", math.Pow(10, l2+l3))

	fmt.Println("\n4. Pascal's triangle and the problem of points")
	for r, row := range pascal(7) {
		fmt.Printf("   row %d: %v\n", r, row)
	}
	for _, c := range [][2]int{{1, 2}, {1, 3}, {2, 3}} {
		aw, t := points(c[0], c[1])
		fmt.Printf("   A needs %d, B needs %d: A gets %d/%d of the stakes\n",
			c[0], c[1], aw, t)
	}
}
