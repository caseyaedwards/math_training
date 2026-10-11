// Topology starter kit: Euler characteristic from face lists, winding
// numbers of loops, counting holes in letter bitmaps, and a tiny
// topological data analysis of points on a circle.
// Standard library only.
package main

import (
	"fmt"
	"math"
	"math/rand/v2"
)

// euler computes V - E + F from a list of faces (each face lists its
// vertices in order). Edges are collected from face boundaries.
func euler(faces [][]int) (v, e, f int) {
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

// winding adds up the turning angle of a closed polygon around the origin.
func winding(pts [][2]float64) int {
	total := 0.0
	for i := range pts {
		a, b := pts[i], pts[(i+1)%len(pts)]
		d := math.Atan2(b[1], b[0]) - math.Atan2(a[1], a[0])
		for d > math.Pi {
			d -= 2 * math.Pi
		}
		for d < -math.Pi {
			d += 2 * math.Pi
		}
		total += d
	}
	return int(math.Round(total / (2 * math.Pi)))
}

// holes counts regions of '.' that do not touch the border of the bitmap.
func holes(img []string) int {
	h, w := len(img), len(img[0])
	seen := make([][]bool, h)
	for i := range seen {
		seen[i] = make([]bool, w)
	}
	count := 0
	for r := 0; r < h; r++ {
		for c := 0; c < w; c++ {
			if img[r][c] != '.' || seen[r][c] {
				continue
			}
			touches := false
			stack := [][2]int{{r, c}}
			seen[r][c] = true
			for len(stack) > 0 {
				p := stack[len(stack)-1]
				stack = stack[:len(stack)-1]
				if p[0] == 0 || p[1] == 0 || p[0] == h-1 || p[1] == w-1 {
					touches = true
				}
				for _, d := range [][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
					q := [2]int{p[0] + d[0], p[1] + d[1]}
					if q[0] >= 0 && q[1] >= 0 && q[0] < h && q[1] < w && img[q[0]][q[1]] == '.' && !seen[q[0]][q[1]] {
						seen[q[0]][q[1]] = true
						stack = append(stack, q)
					}
				}
			}
			if !touches {
				count++
			}
		}
	}
	return count
}

// components counts clusters of points when balls of radius r touch.
func components(pts [][2]float64, r float64) int {
	parent := make([]int, len(pts))
	for i := range parent {
		parent[i] = i
	}
	var find func(int) int
	find = func(i int) int {
		for parent[i] != i {
			i = parent[i]
		}
		return i
	}
	for i := range pts {
		for j := i + 1; j < len(pts); j++ {
			if math.Hypot(pts[i][0]-pts[j][0], pts[i][1]-pts[j][1]) <= 2*r {
				parent[find(i)] = find(j)
			}
		}
	}
	n := 0
	for i := range parent {
		if find(i) == i {
			n++
		}
	}
	return n
}

func main() {
	fmt.Println("== Euler characteristic V - E + F ==")
	solids := []struct {
		name  string
		faces [][]int
	}{
		{"tetrahedron", [][]int{{0, 1, 2}, {0, 1, 3}, {0, 2, 3}, {1, 2, 3}}},
		{"cube", [][]int{{0, 1, 2, 3}, {4, 5, 6, 7}, {0, 1, 5, 4}, {1, 2, 6, 5}, {2, 3, 7, 6}, {3, 0, 4, 7}}},
		{"octahedron", [][]int{{0, 2, 4}, {2, 1, 4}, {1, 3, 4}, {3, 0, 4}, {0, 2, 5}, {2, 1, 5}, {1, 3, 5}, {3, 0, 5}}},
	}
	// A torus: a 3 x 3 grid of squares whose opposite edges are glued.
	var torus [][]int
	id := func(r, c int) int { return (r%3)*3 + c%3 }
	for r := 0; r < 3; r++ {
		for c := 0; c < 3; c++ {
			torus = append(torus, []int{id(r, c), id(r, c+1), id(r+1, c+1), id(r+1, c)})
		}
	}
	solids = append(solids, struct {
		name  string
		faces [][]int
	}{"torus (3x3 grid)", torus})
	for _, s := range solids {
		v, e, f := euler(s.faces)
		fmt.Printf("%-17s V=%2d E=%2d F=%2d  chi=%d\n", s.name, v, e, f, v-e+f)
	}

	fmt.Println("\n== Winding number around the origin ==")
	square := [][2]float64{{1, 1}, {-1, 1}, {-1, -1}, {1, -1}}
	away := [][2]float64{{3, 1}, {2, 1}, {2, 2}, {3, 2}}
	var twice [][2]float64
	for k := 0; k < 16; k++ {
		a := 4 * math.Pi * float64(k) / 16
		twice = append(twice, [2]float64{math.Cos(a), math.Sin(a)})
	}
	fmt.Println("square around 0:", winding(square))
	fmt.Println("square away from 0:", winding(away))
	fmt.Println("circle traced twice:", winding(twice))

	fmt.Println("\n== Holes in letters ==")
	letters := map[string][]string{
		"C": {".....", ".###.", ".#...", ".#...", ".###.", "....."},
		"O": {".....", ".###.", ".#.#.", ".#.#.", ".###.", "....."},
		"B": {".....", ".##..", ".#.#.", ".###.", ".#.#.", ".###.", "....."},
	}
	for _, k := range []string{"C", "O", "B"} {
		fmt.Printf("%s: %d hole(s)\n", k, holes(letters[k]))
	}

	fmt.Println("\n== 24 noisy points on a circle: clusters as balls grow ==")
	rng := rand.New(rand.NewPCG(8, 8))
	var pts [][2]float64
	for k := 0; k < 24; k++ {
		a := 2*math.Pi*float64(k)/24 + 0.16*(rng.Float64()-0.5)
		rad := 1 + 0.16*(rng.Float64()-0.5)
		pts = append(pts, [2]float64{rad * math.Cos(a), rad * math.Sin(a)})
	}
	for _, r := range []float64{0.05, 0.10, 0.13, 0.16, 0.30} {
		fmt.Printf("radius %.2f: %2d piece(s)\n", r, components(pts, r))
	}
	fmt.Println("one piece around an empty middle = one loop, the circle")
}
