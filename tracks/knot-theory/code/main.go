// Knot theory starter kit: writhe, Kauffman bracket, Jones polynomial and
// Fox colorings computed from planar diagram (PD) codes. Standard library only.
//
// A PD code lists each crossing as X[a, b, c, d]: the four edge labels met
// counterclockwise, starting from the incoming under-strand a.
package main

import (
	"fmt"
	"sort"
	"strings"
)

// Crossing is one X[a, b, c, d] entry of a PD code.
type Crossing [4]int

// Poly is a Laurent polynomial: exponent -> coefficient.
type Poly map[int]int

func mul(p, q Poly) Poly {
	r := Poly{}
	for a, x := range p {
		for b, y := range q {
			r[a+b] += x * y
		}
	}
	return clean(r)
}

func add(p, q Poly) Poly {
	r := Poly{}
	for k, v := range p {
		r[k] += v
	}
	for k, v := range q {
		r[k] += v
	}
	return clean(r)
}

func clean(p Poly) Poly {
	for k, v := range p {
		if v == 0 {
			delete(p, k)
		}
	}
	return p
}

// format prints a polynomial in the variable v, lowest power first.
func format(p Poly, v string) string {
	var ks []int
	for k := range p {
		ks = append(ks, k)
	}
	sort.Ints(ks)
	var b strings.Builder
	for i, k := range ks {
		c := p[k]
		switch {
		case i == 0 && c < 0:
			b.WriteString("-")
		case i > 0 && c < 0:
			b.WriteString(" - ")
		case i > 0:
			b.WriteString(" + ")
		}
		if c < 0 {
			c = -c
		}
		if c != 1 || k == 0 {
			fmt.Fprintf(&b, "%d", c)
		}
		if k != 0 {
			b.WriteString(v)
			if k != 1 {
				fmt.Fprintf(&b, "^%d", k)
			}
		}
	}
	return b.String()
}

// writhe adds the crossing signs. The over-strand runs b->d or d->b;
// the crossing is positive when it runs d->b.
func writhe(pd []Crossing) int {
	n := 2 * len(pd)
	w := 0
	for _, x := range pd {
		if (x[1]-x[3]+n)%n == 1 {
			w++
		} else {
			w--
		}
	}
	return w
}

// find is union-find with path halving.
func find(par map[int]int, x int) int {
	if _, ok := par[x]; !ok {
		par[x] = x
	}
	for par[x] != x {
		par[x] = par[par[x]]
		x = par[x]
	}
	return x
}

// bracket computes the Kauffman bracket by summing over all 2^n states.
// A-smoothing joins (a,b) and (c,d). B-smoothing joins (a,d) and (b,c).
func bracket(pd []Crossing) Poly {
	d := Poly{2: -1, -2: -1} // loop value -A^2 - A^-2
	total := Poly{}
	n := len(pd)
	for state := 0; state < 1<<n; state++ {
		par := map[int]int{}
		union := func(x, y int) { par[find(par, x)] = find(par, y) }
		nA := 0
		for i, x := range pd {
			if state>>i&1 == 0 {
				union(x[0], x[1])
				union(x[2], x[3])
				nA++
			} else {
				union(x[0], x[3])
				union(x[1], x[2])
			}
		}
		roots := map[int]bool{}
		for _, x := range pd {
			for _, e := range x {
				roots[find(par, e)] = true
			}
		}
		term := Poly{nA - (n - nA): 1}
		for k := 1; k < len(roots); k++ {
			term = mul(term, d)
		}
		total = add(total, term)
	}
	return total
}

// jones returns V(t) = (-A^3)^(-w) <K> with A = t^(-1/4).
func jones(pd []Crossing) Poly {
	w := writhe(pd)
	sign := 1
	if w%2 != 0 {
		sign = -1
	}
	v := mul(Poly{-3 * w: sign}, bracket(pd))
	out := Poly{}
	for e, c := range v {
		if e%4 != 0 {
			panic("fractional power: not a knot")
		}
		out[-e/4] = c
	}
	return out
}

// colorings counts Fox p-colorings: label each arc 0..p-1 so that at every
// crossing 2*over = under1 + under2 (mod p).
func colorings(pd []Crossing, p int) int {
	par := map[int]int{}
	for _, x := range pd {
		par[find(par, x[1])] = find(par, x[3]) // b and d lie on the same arc
	}
	for _, x := range pd {
		find(par, x[0])
		find(par, x[2])
	}
	idx := map[int]int{}
	for e := range par {
		r := find(par, e)
		if _, ok := idx[r]; !ok {
			idx[r] = len(idx)
		}
	}
	arcs := len(idx)
	col := make([]int, arcs)
	count := 0
	var rec func(i int)
	rec = func(i int) {
		if i == arcs {
			for _, x := range pd {
				o := col[idx[find(par, x[1])]]
				u1 := col[idx[find(par, x[0])]]
				u2 := col[idx[find(par, x[2])]]
				if (2*o-u1-u2)%p != 0 {
					return
				}
			}
			count++
			return
		}
		for c := 0; c < p; c++ {
			col[i] = c
			rec(i + 1)
		}
	}
	rec(0)
	return count
}

func mirror(pd []Crossing) []Crossing {
	out := make([]Crossing, len(pd))
	for i, x := range pd {
		out[i] = Crossing{x[1], x[2], x[3], x[0]}
	}
	return out
}

func report(name string, pd []Crossing) Poly {
	fmt.Printf("== %s ==\n", name)
	fmt.Printf("crossings %d, writhe %d\n", len(pd), writhe(pd))
	fmt.Printf("Kauffman bracket: %s\n", format(bracket(pd), "A"))
	v := jones(pd)
	fmt.Printf("Jones polynomial: %s\n", format(v, "t"))
	c3 := colorings(pd, 3)
	verdict := "not tricolorable"
	if c3 > 3 {
		verdict = "tricolorable"
	}
	fmt.Printf("3-colorings: %d (%s), 5-colorings: %d\n\n", c3, verdict, colorings(pd, 5))
	return v
}

func main() {
	trefoil := []Crossing{{1, 4, 2, 5}, {3, 6, 4, 1}, {5, 2, 6, 3}}
	figure8 := []Crossing{{4, 2, 5, 1}, {8, 6, 1, 5}, {6, 3, 7, 4}, {2, 7, 3, 8}}

	vl := report("Left-handed trefoil 3_1", trefoil)
	vr := report("Right-handed trefoil (mirror)", mirror(trefoil))
	report("Figure-eight knot 4_1", figure8)

	fmt.Println("== Knot sums: the Jones polynomial multiplies ==")
	fmt.Println("granny = trefoil + trefoil:", format(mul(vl, vl), "t"))
	fmt.Println("square = trefoil + mirror: ", format(mul(vl, vr), "t"))
}
