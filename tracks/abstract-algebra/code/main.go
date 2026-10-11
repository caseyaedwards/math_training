// Abstract algebra starter kit: check group axioms by brute force,
// find element orders and generators, compose symmetries of a triangle,
// count necklaces with Burnside, and run a toy Diffie-Hellman exchange.
// Standard library only.
package main

import "fmt"

// isGroup checks closure, associativity, identity and inverses for a
// finite set {0..n-1} with operation op. It returns the identity or -1.
func isGroup(n int, op func(a, b int) int, elems []int) (bool, int) {
	in := map[int]bool{}
	for _, e := range elems {
		in[e] = true
	}
	for _, a := range elems {
		for _, b := range elems {
			if !in[op(a, b)] {
				return false, -1 // not closed
			}
			for _, c := range elems {
				if op(op(a, b), c) != op(a, op(b, c)) {
					return false, -1
				}
			}
		}
	}
	id := -1
	for _, e := range elems {
		ok := true
		for _, a := range elems {
			if op(e, a) != a || op(a, e) != a {
				ok = false
				break
			}
		}
		if ok {
			id = e
		}
	}
	if id < 0 {
		return false, -1
	}
	for _, a := range elems {
		found := false
		for _, b := range elems {
			if op(a, b) == id {
				found = true
			}
		}
		if !found {
			return false, id
		}
	}
	return true, id
}

func rangeN(lo, n int) []int {
	var out []int
	for i := lo; i < n; i++ {
		out = append(out, i)
	}
	return out
}

type perm [3]int // image of vertices 0, 1, 2

func compose(a, b perm) perm { // a after b
	return perm{a[b[0]], a[b[1]], a[b[2]]}
}

func main() {
	fmt.Println("== Which structures are groups? ==")
	add12 := func(a, b int) int { return (a + b) % 12 }
	ok, id := isGroup(12, add12, rangeN(0, 12))
	fmt.Println("Z/12 under +       :", ok, "identity", id)
	mul7 := func(a, b int) int { return a * b % 7 }
	ok, id = isGroup(7, mul7, rangeN(1, 7))
	fmt.Println("{1..6} under x mod 7:", ok, "identity", id)
	mul6 := func(a, b int) int { return a * b % 6 }
	ok, _ = isGroup(6, mul6, rangeN(1, 6))
	fmt.Println("{1..5} under x mod 6:", ok, "(2 x 3 = 0 escapes the set)")

	fmt.Println("\n== Orders of elements in Z/12 ==")
	var gens []int
	for a := 0; a < 12; a++ {
		k, x := 1, a
		for x != 0 {
			x = (x + a) % 12
			k++
		}
		if a == 0 {
			k = 1
		}
		fmt.Printf("%d:%d ", a, k)
		if k == 12 {
			gens = append(gens, a)
		}
	}
	fmt.Println("\ngenerators:", gens)

	fmt.Println("\n== Symmetries of a triangle (vertices 0, 1, 2) ==")
	r := perm{1, 2, 0} // rotate 120 degrees
	s := perm{0, 2, 1} // flip that fixes vertex 0
	fmt.Println("r after s:", compose(r, s))
	fmt.Println("s after r:", compose(s, r))
	fmt.Println("same?", compose(r, s) == compose(s, r), "-> the group is not commutative")
	x, n := r, 1
	for x != (perm{0, 1, 2}) {
		x = compose(r, x)
		n++
	}
	fmt.Println("order of r:", n)

	fmt.Println("\n== Burnside: 4-bead necklaces, 2 colors, up to rotation ==")
	total := 0
	for rot := 0; rot < 4; rot++ {
		fixed := 0
		for c := 0; c < 16; c++ {
			same := true
			for i := 0; i < 4; i++ {
				if (c>>i)&1 != (c>>((i+rot)%4))&1 {
					same = false
				}
			}
			if same {
				fixed++
			}
		}
		fmt.Printf("rotate by %d: fixes %d colorings\n", rot, fixed)
		total += fixed
	}
	fmt.Printf("distinct necklaces = %d / 4 = %d\n", total, total/4)

	fmt.Println("\n== Toy Diffie-Hellman in the field mod p ==")
	p, g := 23, 5
	alice, bob := 6, 15 // secrets
	powmod := func(b, e, m int) int {
		res := 1
		for ; e > 0; e-- {
			res = res * b % m
		}
		return res
	}
	A, B := powmod(g, alice, p), powmod(g, bob, p)
	fmt.Printf("public: p=%d g=%d, Alice sends %d, Bob sends %d\n", p, g, A, B)
	fmt.Printf("shared secret: Alice computes %d, Bob computes %d\n", powmod(B, alice, p), powmod(A, bob, p))
	for k := 1; k < p; k++ {
		if powmod(g, k, p) == A {
			fmt.Printf("an eavesdropper brute-forces k=%d here, but not with a 2,048-bit p\n", k)
			break
		}
	}
}
