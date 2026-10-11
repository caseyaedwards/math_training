// Algebraic topology starter kit: Euler characteristic, Betti numbers of
// simplicial complexes (ranks mod 2), winding numbers, a Brouwer fixed point,
// and a small persistent-homology run on a noisy ring of points.
// Standard library only.
package main

import (
	"fmt"
	"math"
	"sort"
)

// Complex is a simplicial complex given by its vertices, edges and triangles.
type Complex struct {
	V   int
	E   [][2]int
	Tri [][3]int
}

// rank2 returns the rank of a 0/1 matrix over the field with two elements.
// Each row is a bit mask (up to 64 columns is plenty here, so use []uint64).
func rank2(rows [][]uint64) int {
	rank := 0
	for len(rows) > 0 {
		piv := rows[len(rows)-1]
		rows = rows[:len(rows)-1]
		w, b := lowBit(piv)
		if w < 0 {
			continue
		}
		rank++
		var next [][]uint64
		for _, r := range rows {
			if r[w]>>b&1 == 1 {
				for i := range r {
					r[i] ^= piv[i]
				}
			}
			next = append(next, r)
		}
		rows = next
	}
	return rank
}

func lowBit(r []uint64) (int, uint) {
	for i, x := range r {
		if x != 0 {
			for b := uint(0); b < 64; b++ {
				if x>>b&1 == 1 {
					return i, b
				}
			}
		}
	}
	return -1, 0
}

func row(n int, cols ...int) []uint64 {
	r := make([]uint64, n/64+1)
	for _, c := range cols {
		r[c/64] ^= 1 << uint(c%64)
	}
	return r
}

// Betti returns b0, b1, b2 using b_k = (dim C_k - rank d_k) - rank d_{k+1}.
// Hollow tetrahedra are enough here, so there are no 3-simplices.
func (c Complex) Betti() (int, int, int) {
	var d1 [][]uint64
	for _, e := range c.E {
		d1 = append(d1, row(c.V, e[0], e[1]))
	}
	idx := map[[2]int]int{}
	for i, e := range c.E {
		idx[e] = i
	}
	var d2 [][]uint64
	for _, t := range c.Tri {
		d2 = append(d2, row(len(c.E), idx[[2]int{t[0], t[1]}], idx[[2]int{t[0], t[2]}], idx[[2]int{t[1], t[2]}]))
	}
	r1, r2 := rank2(d1), rank2(d2)
	return c.V - r1, len(c.E) - r1 - r2, len(c.Tri) - r2
}

// fromTriangles builds a complex from triangles, collecting their edges.
func fromTriangles(v int, tris [][3]int) Complex {
	seen := map[[2]int]bool{}
	c := Complex{V: v}
	for _, t := range tris {
		s := []int{t[0], t[1], t[2]}
		sort.Ints(s)
		c.Tri = append(c.Tri, [3]int{s[0], s[1], s[2]})
		for _, e := range [][2]int{{s[0], s[1]}, {s[0], s[2]}, {s[1], s[2]}} {
			if !seen[e] {
				seen[e] = true
				c.E = append(c.E, e)
			}
		}
	}
	return c
}

// torus3x3 triangulates a torus: a 3 by 3 grid with opposite sides glued.
func torus3x3() Complex {
	v := func(i, j int) int { return (i%3)*3 + j%3 }
	var tris [][3]int
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			tris = append(tris, [3]int{v(i, j), v(i+1, j), v(i+1, j+1)})
			tris = append(tris, [3]int{v(i, j), v(i, j+1), v(i+1, j+1)})
		}
	}
	return fromTriangles(9, tris)
}

// winding counts how many times a closed path goes around the origin.
func winding(f func(t float64) (float64, float64), n int) int {
	total := 0.0
	x0, y0 := f(0)
	prev := math.Atan2(y0, x0)
	for k := 1; k <= n; k++ {
		x, y := f(2 * math.Pi * float64(k) / float64(n))
		a := math.Atan2(y, x)
		d := a - prev
		for d > math.Pi {
			d -= 2 * math.Pi
		}
		for d < -math.Pi {
			d += 2 * math.Pi
		}
		total += d
		prev = a
	}
	return int(math.Round(total / (2 * math.Pi)))
}

// ripsBetti returns b0 and b1 of the Vietoris-Rips complex at scale eps.
func ripsBetti(pts [][2]float64, eps float64) (int, int) {
	n := len(pts)
	near := func(i, j int) bool { return dist(pts[i], pts[j]) <= eps }
	c := Complex{V: n}
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if near(i, j) {
				c.E = append(c.E, [2]int{i, j})
			}
		}
	}
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			for k := j + 1; k < n; k++ {
				if near(i, j) && near(i, k) && near(j, k) {
					c.Tri = append(c.Tri, [3]int{i, j, k})
				}
			}
		}
	}
	b0, b1, _ := c.Betti()
	return b0, b1
}

func dist(a, b [2]float64) float64 { return math.Hypot(a[0]-b[0], a[1]-b[1]) }

func main() {
	fmt.Println("== Euler characteristic V - E + F ==")
	for _, s := range []struct {
		name    string
		v, e, f int
	}{{"tetrahedron", 4, 6, 4}, {"cube", 8, 12, 6}, {"octahedron", 6, 12, 8}, {"icosahedron", 12, 30, 20}, {"picture-frame torus", 16, 32, 16}} {
		fmt.Printf("%-20s %2d - %2d + %2d = %d\n", s.name, s.v, s.e, s.f, s.v-s.e+s.f)
	}

	fmt.Println("\n== Betti numbers (b0, b1, b2) ==")
	hollow := Complex{V: 3, E: [][2]int{{0, 1}, {0, 2}, {1, 2}}}
	filled := fromTriangles(3, [][3]int{{0, 1, 2}})
	sphere := fromTriangles(4, [][3]int{{0, 1, 2}, {0, 1, 3}, {0, 2, 3}, {1, 2, 3}})
	torus := torus3x3()
	for _, s := range []struct {
		name string
		c    Complex
	}{{"hollow triangle", hollow}, {"filled triangle", filled}, {"hollow tetrahedron", sphere}, {"3x3 torus", torus}} {
		b0, b1, b2 := s.c.Betti()
		fmt.Printf("%-19s V=%d E=%2d F=%2d  b=(%d, %d, %d)  chi=%d\n", s.name, s.c.V, len(s.c.E), len(s.c.Tri), b0, b1, b2, b0-b1+b2)
	}

	fmt.Println("\n== Winding numbers around the origin ==")
	loops := []struct {
		name string
		f    func(t float64) (float64, float64)
	}{
		{"small loop off to the side", func(t float64) (float64, float64) { return 2 + math.Cos(t), math.Sin(t) }},
		{"unit circle", func(t float64) (float64, float64) { return math.Cos(t), math.Sin(t) }},
		{"double loop", func(t float64) (float64, float64) {
			return math.Cos(2*t) + 0.45*math.Cos(t), math.Sin(2*t) + 0.45*math.Sin(t)
		}},
		{"clockwise circle", func(t float64) (float64, float64) { return math.Cos(t), -math.Sin(t) }},
	}
	for _, l := range loops {
		fmt.Printf("%-27s %2d\n", l.name, winding(l.f, 2000))
	}

	fmt.Println("\n== Brouwer in one dimension ==")
	f := func(x float64) float64 { return 0.9 - 0.75*x + 0.15*math.Sin(6*x) }
	lo, hi := 0.0, 1.0
	for i := 0; i < 60; i++ {
		m := (lo + hi) / 2
		if f(m) > m {
			lo = m
		} else {
			hi = m
		}
	}
	fmt.Printf("f(x) = 0.9 - 0.75x + 0.15 sin 6x has fixed point x = %.4f, f(x) = %.4f\n", lo, f(lo))

	fmt.Println("\n== Persistent homology of a noisy ring of 12 points ==")
	jr := []float64{0.05, -0.04, 0.08, -0.06, 0.02, 0.07, -0.03, 0.04, -0.08, 0.06, -0.02, 0.03}
	ja := []float64{3, -4, 2, 5, -2, 4, -5, 1, 3, -3, 4, -1}
	var pts [][2]float64
	for k := 0; k < 12; k++ {
		a := (30*float64(k) + ja[k]) * math.Pi / 180
		pts = append(pts, [2]float64{(1 + jr[k]) * math.Cos(a), (1 + jr[k]) * math.Sin(a)})
	}
	for _, eps := range []float64{0.3, 0.5, 1.0, 1.5, 1.9} {
		b0, b1 := ripsBetti(pts, eps)
		fmt.Printf("eps %.1f: b0 = %2d, b1 = %d\n", eps, b0, b1)
	}
	var ds []float64
	for i := 0; i < 12; i++ {
		for j := i + 1; j < 12; j++ {
			ds = append(ds, dist(pts[i], pts[j]))
		}
	}
	sort.Float64s(ds)
	birth, death := -1.0, -1.0
	for _, d := range ds {
		_, b1 := ripsBetti(pts, d)
		if b1 > 0 && birth < 0 {
			birth = d
		}
		if b1 == 0 && birth >= 0 && death < 0 {
			death = d
		}
	}
	fmt.Printf("the loop is born at eps = %.3f and dies at eps = %.3f\n", birth, death)
}
