// Euler characteristic from face lists, and a stretch map from (-1, 1) onto the whole line.
package main

import (
	"fmt"
	"math"
)

// chi counts vertices, edges and faces of a surface given as a list of faces.
// Each face is a cycle of vertex ids. Each edge is shared by two faces.
func chi(faces [][]int) (v, e, f int) {
	verts := map[int]bool{}
	edges := map[[2]int]bool{}
	for _, face := range faces {
		for i, a := range face {
			b := face[(i+1)%len(face)]
			verts[a] = true
			if a > b {
				a, b = b, a
			}
			edges[[2]int{a, b}] = true
		}
	}
	return len(verts), len(edges), len(faces)
}

// torusGrid glues an n-by-n grid of squares: top to bottom, left to right.
func torusGrid(n int) [][]int {
	id := func(i, j int) int { return (i%n)*n + j%n }
	var faces [][]int
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			faces = append(faces, []int{id(i, j), id(i, j+1), id(i+1, j+1), id(i+1, j)})
		}
	}
	return faces
}

func main() {
	shapes := []struct {
		name  string
		faces [][]int
	}{
		{"tetrahedron", [][]int{{0, 1, 2}, {0, 1, 3}, {0, 2, 3}, {1, 2, 3}}},
		{"cube", [][]int{{0, 1, 2, 3}, {4, 5, 6, 7}, {0, 1, 5, 4}, {1, 2, 6, 5}, {2, 3, 7, 6}, {3, 0, 4, 7}}},
		{"octahedron", [][]int{{0, 2, 4}, {0, 4, 3}, {0, 3, 5}, {0, 5, 2}, {1, 2, 4}, {1, 4, 3}, {1, 3, 5}, {1, 5, 2}}},
		{"square pyramid", [][]int{{0, 1, 2, 3}, {0, 1, 4}, {1, 2, 4}, {2, 3, 4}, {3, 0, 4}}},
		{"torus 3x3 grid", torusGrid(3)},
		{"torus 5x5 grid", torusGrid(5)},
	}
	for _, s := range shapes {
		v, e, f := chi(s.faces)
		fmt.Printf("%-15s V=%2d E=%2d F=%2d  V-E+F = %d\n", s.name, v, e, f, v-e+f)
	}

	// f(x) = x / (1 - |x|) stretches (-1, 1) onto all reals; g undoes it.
	f := func(x float64) float64 { return x / (1 - math.Abs(x)) }
	g := func(y float64) float64 { return y / (1 + math.Abs(y)) }
	for _, x := range []float64{-0.99, -0.5, 0, 0.5, 0.9, 0.999} {
		fmt.Printf("x = %6.3f  f(x) = %9.3f  g(f(x)) = %6.3f\n", x, f(x), g(f(x)))
	}
}
