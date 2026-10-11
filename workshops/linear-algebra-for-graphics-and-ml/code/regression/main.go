// Command regression fits the least-squares line y = m x + b through
// request rate versus CPU, the same way you do it by hand.
//
// Data: x = request rate in hundreds of requests per second, y = CPU percent.
//
// It prints:
//  1. the sums the normal equations need
//  2. the normal equations as a 2x2 matrix system (A^T A) p = A^T y
//  3. the solution m, b by the determinant (Cramer) rule
//  4. predictions and residuals, with text bars
//  5. a capacity question: what rate reaches 80% CPU
//
// Run from the workshop folder: go run ./code/regression
package main

import (
	"fmt"
	"math"
	"strings"
)

var xs = []float64{1, 2, 3, 4, 5}      // hundreds of req/s
var ys = []float64{20, 31, 39, 52, 58} // CPU %

type Matrix [][]float64

func transpose(m Matrix) Matrix {
	out := make(Matrix, len(m[0]))
	for j := range out {
		out[j] = make([]float64, len(m))
		for i := range m {
			out[j][i] = m[i][j]
		}
	}
	return out
}

func matmul(a, b Matrix) Matrix {
	out := make(Matrix, len(a))
	for i := range a {
		out[i] = make([]float64, len(b[0]))
		for j := range b[0] {
			for k := range b {
				out[i][j] += a[i][k] * b[k][j]
			}
		}
	}
	return out
}

func det2(m Matrix) float64 { return m[0][0]*m[1][1] - m[0][1]*m[1][0] }

func section(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 64))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 64))
}

// z turns tiny rounding noise into a clean zero for printing.
func z(x float64) float64 {
	if math.Abs(x) < 1e-9 {
		return 0
	}
	return x
}

func main() {
	n := float64(len(xs))
	var sx, sy, sxx, sxy float64
	for i := range xs {
		sx += xs[i]
		sy += ys[i]
		sxx += xs[i] * xs[i]
		sxy += xs[i] * ys[i]
	}

	section("1. The sums")
	fmt.Println("  x (100 req/s)   y (CPU %)    x*x     x*y")
	for i := range xs {
		fmt.Printf("  %8.0f       %8.0f   %6.0f  %6.0f\n", xs[i], ys[i], xs[i]*xs[i], xs[i]*ys[i])
	}
	fmt.Printf("  sum x = %.0f   sum y = %.0f   sum x^2 = %.0f   sum xy = %.0f   n = %.0f\n", sx, sy, sxx, sxy, n)

	section("2. Normal equations (A^T A) p = A^T y, with p = (m, b)")
	a := make(Matrix, len(xs)) // each row is (x_i, 1)
	y := make(Matrix, len(ys))
	for i := range xs {
		a[i] = []float64{xs[i], 1}
		y[i] = []float64{ys[i]}
	}
	ata := matmul(transpose(a), a)
	aty := matmul(transpose(a), y)
	fmt.Println("  A = rows (x_i, 1): (1, 1) (2, 1) (3, 1) (4, 1) (5, 1)")
	fmt.Printf("  A^T A = [[%.0f, %.0f], [%.0f, %.0f]]   = [[sum x^2, sum x], [sum x, n]]\n",
		ata[0][0], ata[0][1], ata[1][0], ata[1][1])
	fmt.Printf("  A^T y = [%.0f, %.0f]             = [sum xy, sum y]\n", aty[0][0], aty[1][0])

	section("3. Solve with the determinant (Cramer) rule")
	d := det2(ata)
	dm := det2(Matrix{{aty[0][0], ata[0][1]}, {aty[1][0], ata[1][1]}})
	db := det2(Matrix{{ata[0][0], aty[0][0]}, {ata[1][0], aty[1][0]}})
	m, b := dm/d, db/d
	fmt.Printf("  det(A^T A) = %.0f*%.0f - %.0f*%.0f = %.0f\n", ata[0][0], ata[1][1], ata[0][1], ata[1][0], d)
	fmt.Printf("  m = %.0f / %.0f = %.4f   CPU points per 100 req/s\n", dm, d, m)
	fmt.Printf("  b = %.0f / %.0f = %.4f   CPU %% at zero traffic\n", db, d, b)
	fmt.Printf("  fitted line: CPU = %.1f * x + %.1f\n", m, b)

	section("4. Predictions and residuals (residual = actual - predicted)")
	resid := make([]float64, len(xs))
	fmt.Println("  x    actual   predicted   residual")
	var sumR, sumR2, dotRX float64
	for i := range xs {
		pred := m*xs[i] + b
		resid[i] = ys[i] - pred
		sumR += resid[i]
		sumR2 += resid[i] * resid[i]
		dotRX += resid[i] * xs[i]
		fmt.Printf("  %.0f    %6.0f   %9.1f   %+8.1f\n", xs[i], ys[i], pred, resid[i])
	}
	fmt.Printf("  sum of residuals         = %+.4f  (always 0 with an intercept)\n", z(sumR))
	fmt.Printf("  sum of squared residuals = %.2f\n", sumR2)
	fmt.Printf("  residuals dot x          = %+.4f  (residuals are orthogonal to the x column)\n", z(dotRX))

	fmt.Println()
	fmt.Println("  residual bars (each # = 0.25 CPU points; left = below the line)")
	for i, r := range resid {
		k := int(math.Round(math.Abs(r) / 0.25))
		left, right := strings.Repeat(" ", 10), strings.Repeat(" ", 10)
		if r < 0 {
			left = fmt.Sprintf("%10s", strings.Repeat("#", k))
		} else if r > 0 {
			right = fmt.Sprintf("%-10s", strings.Repeat("#", k))
		}
		fmt.Printf("  x=%.0f  %s|%s  %+.1f\n", xs[i], left, right, r)
	}

	section("5. Capacity: what rate reaches 80% CPU")
	x80 := (80 - b) / m
	fmt.Printf("  80 = %.1f x + %.1f  ->  x = (80 - %.1f) / %.1f = %.2f\n", m, b, b, m, x80)
	fmt.Printf("  about %.0f requests per second (an extrapolation past the data)\n", x80*100)
}
