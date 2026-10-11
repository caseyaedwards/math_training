// Linear algebra starter kit: vectors, matrices, elimination,
// determinants, eigenvalues by power iteration, PageRank and least squares.
// Standard library only.
package main

import (
	"fmt"
	"math"
)

type Vec []float64
type Mat [][]float64

func dot(u, v Vec) float64 {
	s := 0.0
	for i := range u {
		s += u[i] * v[i]
	}
	return s
}

func (a Mat) mulVec(v Vec) Vec {
	out := make(Vec, len(a))
	for i := range a {
		out[i] = dot(a[i], v)
	}
	return out
}

func det2(a Mat) float64 { return a[0][0]*a[1][1] - a[0][1]*a[1][0] }

// solve runs Gaussian elimination with partial pivoting on A x = b.
func solve(a Mat, b Vec) Vec {
	n := len(a)
	m := make(Mat, n)
	for i := range a {
		m[i] = append(append(Vec{}, a[i]...), b[i])
	}
	for col := 0; col < n; col++ {
		p := col
		for r := col + 1; r < n; r++ {
			if math.Abs(m[r][col]) > math.Abs(m[p][col]) {
				p = r
			}
		}
		m[col], m[p] = m[p], m[col]
		for r := col + 1; r < n; r++ {
			f := m[r][col] / m[col][col]
			for c := col; c <= n; c++ {
				m[r][c] -= f * m[col][c]
			}
		}
	}
	x := make(Vec, n)
	for r := n - 1; r >= 0; r-- {
		s := m[r][n]
		for c := r + 1; c < n; c++ {
			s -= m[r][c] * x[c]
		}
		x[r] = s / m[r][r]
	}
	return x
}

func main() {
	u, v := Vec{1, 2}, Vec{3, -1}
	fmt.Println("== Vectors ==")
	fmt.Println("u + v =", Vec{u[0] + v[0], u[1] + v[1]})
	a, b := Vec{4, 1}, Vec{2, 3}
	cos := dot(a, b) / math.Sqrt(dot(a, a)*dot(b, b))
	fmt.Printf("(4,1)·(2,3) = %.0f, angle %.1f degrees\n", dot(a, b), math.Acos(cos)*180/math.Pi)
	t := dot(a, b) / dot(a, a)
	fmt.Printf("projection of (2,3) onto (4,1) = (%.3f, %.3f)\n", t*a[0], t*a[1])

	fmt.Println("\n== Matrix as a machine ==")
	rot := Mat{{0, -1}, {1, 0}}
	fmt.Println("rotate 90:", Vec{1, 0}, "->", rot.mulVec(Vec{1, 0}), ",", Vec{0, 1}, "->", rot.mulVec(Vec{0, 1}))
	A := Mat{{2, 1}, {1, 2}}
	fmt.Println("A(1,1) =", A.mulVec(Vec{1, 1}), " A(1,-1) =", A.mulVec(Vec{1, -1}))
	fmt.Println("det A =", det2(A), " det [[3,1],[1,2]] =", det2(Mat{{3, 1}, {1, 2}}))

	fmt.Println("\n== Solve x + y = 5, x - y = 1 ==")
	fmt.Println("x, y =", solve(Mat{{1, 1}, {1, -1}}, Vec{5, 1}))
	fmt.Println("3x3 example:", solve(Mat{{2, 1, 1}, {4, -6, 0}, {-2, 7, 2}}, Vec{5, -2, 9}))

	fmt.Println("\n== Power iteration on A ==")
	x := Vec{1, 0}
	var lam float64
	for i := 0; i < 40; i++ {
		y := A.mulVec(x)
		lam = math.Sqrt(dot(y, y) / dot(x, x))
		n := math.Sqrt(dot(y, y))
		x = Vec{y[0] / n, y[1] / n}
	}
	fmt.Printf("largest eigenvalue %.6f, direction (%.4f, %.4f)\n", lam, x[0], x[1])

	fmt.Println("\n== PageRank: A->B, A->C, B->C, C->A, damping 0.85 ==")
	links := map[int][]int{0: {1, 2}, 1: {2}, 2: {0}}
	r := Vec{1.0 / 3, 1.0 / 3, 1.0 / 3}
	for it := 0; it < 100; it++ {
		nr := Vec{0.05, 0.05, 0.05} // (1 - 0.85) / 3
		for p := 0; p < 3; p++ {
			for _, q := range links[p] {
				nr[q] += 0.85 * r[p] / float64(len(links[p]))
			}
		}
		r = nr
	}
	fmt.Printf("A %.3f  B %.3f  C %.3f\n", r[0], r[1], r[2])

	fmt.Println("\n== Least squares line through 5 points ==")
	xs := Vec{1, 2, 3, 4, 5}
	ys := Vec{1.5, 3.8, 3.2, 5.5, 5.0}
	// Normal equations for y = c0 + c1 x: (A^T A) c = A^T y.
	var n, sx, sxx, sy, sxy float64
	for i := range xs {
		n++
		sx += xs[i]
		sxx += xs[i] * xs[i]
		sy += ys[i]
		sxy += xs[i] * ys[i]
	}
	c := solve(Mat{{n, sx}, {sx, sxx}}, Vec{sy, sxy})
	fmt.Printf("y = %.2f + %.2f x\n", c[0], c[1])
}
