// Command transforms shows 2D transforms as matrices, using only the standard library.
//
// It prints:
//  1. where the basis vectors land under scale, rotate, shear, reflect
//  2. rotate-then-scale versus scale-then-rotate (order matters)
//  3. a house polygon rotated by 30 degrees, every coordinate shown
//  4. homogeneous 3x3 matrices: rotate by 30 degrees, then translate by (3, 1)
//
// Optional flag:
//
//	-svg PATH   also write the original and rotated house as an SVG file
//
// Run from the workshop folder: go run ./code/transforms
package main

import (
	"flag"
	"fmt"
	"math"
	"os"
	"strings"
)

// Matrix is a list of rows.
type Matrix [][]float64

// Vec is a column vector stored as a plain slice.
type Vec []float64

// matmul returns a times b. Row i of a meets column j of b.
func matmul(a, b Matrix) Matrix {
	rows, inner, cols := len(a), len(b), len(b[0])
	if len(a[0]) != inner {
		panic("inner sizes must match")
	}
	out := make(Matrix, rows)
	for i := 0; i < rows; i++ {
		out[i] = make([]float64, cols)
		for j := 0; j < cols; j++ {
			for k := 0; k < inner; k++ {
				out[i][j] += a[i][k] * b[k][j]
			}
		}
	}
	return out
}

// matvec applies matrix m to the column vector v.
func matvec(m Matrix, v Vec) Vec {
	out := make(Vec, len(m))
	for i := range m {
		for k := range v {
			out[i] += m[i][k] * v[k]
		}
	}
	return out
}

func column(m Matrix, j int) Vec {
	out := make(Vec, len(m))
	for i := range m {
		out[i] = m[i][j]
	}
	return out
}

// clean turns tiny rounding noise (and -0) into a plain 0.
func clean(x float64) float64 {
	if math.Abs(x) < 5e-10 {
		return 0
	}
	return x
}

func fmtVec(v Vec) string {
	parts := make([]string, len(v))
	for i, x := range v {
		parts[i] = fmt.Sprintf("%.4f", clean(x))
	}
	return "(" + strings.Join(parts, ", ") + ")"
}

func showMatrix(name string, m Matrix) {
	fmt.Printf("%s =\n", name)
	for _, row := range m {
		fmt.Print("   [")
		for _, x := range row {
			fmt.Printf(" %8.4f", clean(x))
		}
		fmt.Println(" ]")
	}
}

func scale(sx, sy float64) Matrix { return Matrix{{sx, 0}, {0, sy}} }

func rotate(deg float64) Matrix {
	t := deg * math.Pi / 180
	c, s := math.Cos(t), math.Sin(t)
	return Matrix{{c, -s}, {s, c}}
}

func shearX(k float64) Matrix { return Matrix{{1, k}, {0, 1}} }
func reflectYAxis() Matrix    { return Matrix{{-1, 0}, {0, 1}} }
func translateH(tx, ty float64) Matrix {
	return Matrix{{1, 0, tx}, {0, 1, ty}, {0, 0, 1}}
}

// rotateH is a 3x3 homogeneous rotation about the origin.
func rotateH(deg float64) Matrix {
	t := deg * math.Pi / 180
	c, s := math.Cos(t), math.Sin(t)
	return Matrix{{c, -s, 0}, {s, c, 0}, {0, 0, 1}}
}

var house = []Vec{{0, 0}, {2, 0}, {2, 2}, {1, 3}, {0, 2}}

func section(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 64))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 64))
}

func partBasis() {
	section("1. Columns are where the basis vectors land")
	iHat, jHat := Vec{1, 0}, Vec{0, 1}
	cases := []struct {
		name string
		m    Matrix
	}{
		{"scale(2, 0.5)", scale(2, 0.5)},
		{"rotate(90)", rotate(90)},
		{"shearX(1)", shearX(1)},
		{"reflect over y-axis", reflectYAxis()},
	}
	for _, c := range cases {
		fmt.Println()
		showMatrix(c.name, c.m)
		fmt.Printf("   i-hat (1, 0) -> %-18s = column 1 %s\n", fmtVec(matvec(c.m, iHat)), fmtVec(column(c.m, 0)))
		fmt.Printf("   j-hat (0, 1) -> %-18s = column 2 %s\n", fmtVec(matvec(c.m, jHat)), fmtVec(column(c.m, 1)))
	}
}

func partOrder() {
	section("2. Order matters: rotate(90) and scale(2, 1)")
	r, s := rotate(90), scale(2, 1)
	sr := matmul(s, r) // rotate first, then scale (rightmost acts first)
	rs := matmul(r, s) // scale first, then rotate
	showMatrix("S R  (rotate first, then scale)", sr)
	showMatrix("R S  (scale first, then rotate)", rs)
	v := Vec{1, 0}
	fmt.Println()
	fmt.Printf("v = %s\n", fmtVec(v))
	fmt.Printf("   rotate then scale: R v = %s  then S -> %s\n", fmtVec(matvec(r, v)), fmtVec(matvec(sr, v)))
	fmt.Printf("   scale then rotate: S v = %s  then R -> %s\n", fmtVec(matvec(s, v)), fmtVec(matvec(rs, v)))
	fmt.Println("   same two moves, different order, different answer")
}

func rotatedHouse(deg float64) []Vec {
	m := rotate(deg)
	out := make([]Vec, len(house))
	for i, p := range house {
		out[i] = matvec(m, p)
	}
	return out
}

func partHouse() {
	section("3. Rotate the house by 30 degrees")
	c, s := math.Cos(math.Pi/6), math.Sin(math.Pi/6)
	fmt.Printf("cos 30 = %.4f   sin 30 = %.4f\n", c, s)
	showMatrix("R(30)", rotate(30))
	fmt.Println()
	fmt.Println("  point      x' = x cos - y sin      y' = x sin + y cos")
	rh := rotatedHouse(30)
	for i, p := range house {
		fmt.Printf("  (%.0f, %.0f)  ->  (%7.4f, %7.4f)\n", p[0], p[1], clean(rh[i][0]), clean(rh[i][1]))
	}
	fmt.Println()
	fmt.Printf("length of peak before: %.4f   after: %.4f\n",
		math.Hypot(house[3][0], house[3][1]), math.Hypot(rh[3][0], rh[3][1]))
}

func partHomogeneous() {
	section("4. Homogeneous coordinates: rotate 30, then translate (3, 1)")
	t, r := translateH(3, 1), rotateH(30)
	m := matmul(t, r) // rotate first, then translate
	showMatrix("T(3, 1)", t)
	showMatrix("R(30) as 3x3", r)
	showMatrix("M = T R", m)
	fmt.Println()
	for _, p := range house {
		out := matvec(m, Vec{p[0], p[1], 1})
		fmt.Printf("  (%.0f, %.0f, 1) -> (%7.4f, %7.4f, %.0f)\n", p[0], p[1], out[0], out[1], out[2])
	}
	fmt.Println()
	fmt.Println("a 2x2 matrix always sends (0, 0) to (0, 0); the 3x3 trick moves it")
}

func writeSVG(path string) error {
	const size, unit, ox, oy = 360.0, 60.0, 180.0, 260.0
	pts := func(vs []Vec) string {
		parts := make([]string, len(vs))
		for i, p := range vs {
			parts[i] = fmt.Sprintf("%.1f,%.1f", ox+unit*p[0], oy-unit*p[1])
		}
		return strings.Join(parts, " ")
	}
	h := size - 60
	svg := fmt.Sprintf(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f">
  <rect width="%.0f" height="%.0f" fill="#ffffff"/>
  <line x1="0" y1="%.0f" x2="%.0f" y2="%.0f" stroke="#868e96"/>
  <line x1="%.0f" y1="0" x2="%.0f" y2="%.0f" stroke="#868e96"/>
  <polygon points="%s" fill="none" stroke="#343a40" stroke-width="2" stroke-dasharray="6 4"/>
  <polygon points="%s" fill="none" stroke="#d9480f" stroke-width="3"/>
</svg>
`, size, h, size, h, oy, size, oy, ox, ox, h, pts(house), pts(rotatedHouse(30)))
	if err := os.WriteFile(path, []byte(svg), 0o644); err != nil {
		return err
	}
	fmt.Printf("\nwrote %s\n", path)
	return nil
}

func main() {
	svgPath := flag.String("svg", "", "also write the original and rotated house as SVG to this path")
	flag.Parse()
	partBasis()
	partOrder()
	partHouse()
	partHomogeneous()
	if *svgPath != "" {
		if err := writeSVG(*svgPath); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	}
}
