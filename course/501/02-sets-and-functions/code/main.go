// Sets as map[int]bool, plus a one-to-one check for functions.
package main

import (
	"fmt"
	"sort"
)

type set map[int]bool

func of(xs ...int) set {
	s := set{}
	for _, x := range xs {
		s[x] = true
	}
	return s
}

func (a set) union(b set) set {
	out := set{}
	for x := range a {
		out[x] = true
	}
	for x := range b {
		out[x] = true
	}
	return out
}

func (a set) inter(b set) set {
	out := set{}
	for x := range a {
		if b[x] {
			out[x] = true
		}
	}
	return out
}

func (a set) minus(b set) set {
	out := set{}
	for x := range a {
		if !b[x] {
			out[x] = true
		}
	}
	return out
}

func (a set) String() string {
	xs := []int{}
	for x := range a {
		xs = append(xs, x)
	}
	sort.Ints(xs)
	return fmt.Sprint(xs)
}

// oneToOne reports whether f gives different outputs for different inputs.
func oneToOne(f func(int) int, domain []int) bool {
	seen := map[int]bool{}
	for _, x := range domain {
		y := f(x)
		if seen[y] {
			return false
		}
		seen[y] = true
	}
	return true
}

func main() {
	A, B := of(1, 2, 3, 4), of(3, 4, 5, 6)
	U := of(1, 2, 3, 4, 5, 6, 7, 8)
	fmt.Println("A union B:  ", A.union(B))
	fmt.Println("A inter B:  ", A.inter(B))
	fmt.Println("A minus B:  ", A.minus(B))
	fmt.Println("complement A:", U.minus(A))
	fmt.Println("|A u B| =", len(A.union(B)), "= 4 + 4 - 2 =", len(A)+len(B)-len(A.inter(B)))

	dom := []int{-3, -2, -1, 0, 1, 2, 3}
	fmt.Println("x*x one-to-one on -3..3:", oneToOne(func(x int) int { return x * x }, dom))
	fmt.Println("2x+1 one-to-one on -3..3:", oneToOne(func(x int) int { return 2*x + 1 }, dom))

	f := func(x int) int { return x + 2 }
	g := func(x int) int { return 5 * x }
	fmt.Println("g(f(1)) =", g(f(1)), " f(g(1)) =", f(g(1)))
}
