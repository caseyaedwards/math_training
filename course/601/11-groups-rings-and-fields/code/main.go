// The eight symmetries of a square: build them, compose them, check the group axioms.
package main

import "fmt"

// A symmetry is a map on corner coordinates (x, y), each in {-1, 1}.
type sym func(x, y int) (int, int)

var names = []string{"e", "r", "r2", "r3", "h", "v", "d", "a"}

var syms = map[string]sym{
	"e":  func(x, y int) (int, int) { return x, y },
	"r":  func(x, y int) (int, int) { return -y, x }, // turn 90 degrees counterclockwise
	"r2": func(x, y int) (int, int) { return -x, -y },
	"r3": func(x, y int) (int, int) { return y, -x },
	"h":  func(x, y int) (int, int) { return x, -y },  // mirror in the horizontal line
	"v":  func(x, y int) (int, int) { return -x, y },  // mirror in the vertical line
	"d":  func(x, y int) (int, int) { return y, x },   // mirror in the diagonal through A and C
	"a":  func(x, y int) (int, int) { return -y, -x }, // mirror in the diagonal through B and D
}

// Corners A, B, C, D, counterclockwise from the top right.
var corners = [4][2]int{{1, 1}, {-1, 1}, {-1, -1}, {1, -1}}

// fingerprint records where each corner lands; it identifies a symmetry.
func fingerprint(f sym) [4][2]int {
	var out [4][2]int
	for i, c := range corners {
		x, y := f(c[0], c[1])
		out[i] = [2]int{x, y}
	}
	return out
}

// compose returns the name of "do g first, then f".
func compose(f, g string) string {
	h := func(x, y int) (int, int) { return syms[f](syms[g](x, y)) }
	fp := fingerprint(h)
	for _, n := range names {
		if fingerprint(syms[n]) == fp {
			return n
		}
	}
	panic("not a symmetry: closure fails")
}

func main() {
	fmt.Println("Cayley table: row then column means do the column first, then the row")
	fmt.Printf("%4s |", "")
	for _, c := range names {
		fmt.Printf("%4s", c)
	}
	fmt.Println()
	fmt.Println("-----+--------------------------------")
	for _, r := range names {
		fmt.Printf("%4s |", r)
		for _, c := range names {
			fmt.Printf("%4s", compose(r, c))
		}
		fmt.Println()
	}

	// Associativity: check all 512 triples.
	ok := true
	for _, f := range names {
		for _, g := range names {
			for _, k := range names {
				if compose(compose(f, g), k) != compose(f, compose(g, k)) {
					ok = false
				}
			}
		}
	}
	fmt.Println("associative on all 512 triples:", ok)

	// Inverses: for each x find y with x y = e.
	for _, x := range names {
		for _, y := range names {
			if compose(x, y) == "e" {
				fmt.Printf("inverse of %-2s is %s\n", x, y)
			}
		}
	}
	fmt.Println("r h =", compose("r", "h"), "  but  h r =", compose("h", "r"))

	// Z6 is a ring but not a field: zero divisors.
	fmt.Print("pairs in Z6 with a*b = 0 and a, b nonzero:")
	for x := 1; x < 6; x++ {
		for y := x; y < 6; y++ {
			if x*y%6 == 0 {
				fmt.Printf(" %dx%d", x, y)
			}
		}
	}
	fmt.Println()
}
