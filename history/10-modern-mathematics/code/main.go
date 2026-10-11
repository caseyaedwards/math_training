// Chapter 10: toy RSA, square-and-multiply, map coloring, Mandelbrot.
package main

import (
	"fmt"
	"math/big"
	"strings"
)

// powMod computes base^exp mod m by repeated squaring, printing each step.
func powMod(base, exp, m int64, show bool) int64 {
	result, sq := int64(1), base%m
	for e := exp; e > 0; e >>= 1 {
		if e&1 == 1 {
			result = result * sq % m
		}
		if show {
			fmt.Printf("  bit %d  square = %4d  result = %4d\n", e&1, sq, result)
		}
		sq = sq * sq % m
	}
	return result
}

// colorings counts proper colorings of a map with k colors.
// adj lists pairs of regions that share a border.
func colorings(n, k int, adj [][2]int) (int, []int) {
	count, first := 0, []int(nil)
	col := make([]int, n)
	var try func(i int)
	try = func(i int) {
		if i == n {
			if count == 0 {
				first = append([]int(nil), col...)
			}
			count++
			return
		}
		for c := 1; c <= k; c++ {
			col[i] = c
			ok := true
			for _, e := range adj {
				if e[1] == i && col[e[0]] == c {
					ok = false
				}
			}
			if ok {
				try(i + 1)
			}
		}
	}
	try(0)
	return count, first
}

func main() {
	// Toy RSA with math/big, as in the 1977 scheme.
	p, q := big.NewInt(61), big.NewInt(53)
	one := big.NewInt(1)
	n := new(big.Int).Mul(p, q)
	phi := new(big.Int).Mul(new(big.Int).Sub(p, one), new(big.Int).Sub(q, one))
	e := big.NewInt(17)
	d := new(big.Int).ModInverse(e, phi)
	m := big.NewInt(65)
	c := new(big.Int).Exp(m, e, n)
	back := new(big.Int).Exp(c, d, n)
	fmt.Printf("Toy RSA: n = %v, phi = %v, e = %v, d = %v\n", n, phi, e, d)
	fmt.Printf("  encrypt %v -> %v, decrypt %v -> %v\n", m, c, c, back)

	fmt.Println("\nSquare-and-multiply: 65^17 mod 3233 (17 = binary 10001)")
	fmt.Println("  answer:", powMod(65, 17, 3233, true))

	// Wheel map: 0 = center, 1..5 = ring, 6 = outer region.
	var adj [][2]int
	for i := 1; i <= 5; i++ {
		adj = append(adj, [2]int{0, i}, [2]int{i, 6})
		if i > 1 {
			adj = append(adj, [2]int{i - 1, i})
		}
	}
	adj = append(adj, [2]int{1, 5}) // close the ring
	fmt.Println("\nWheel map (center, ring of 5, outer region)")
	for k := 2; k <= 4; k++ {
		cnt, first := colorings(7, k, adj)
		fmt.Printf("  %d colors: %4d colorings  first: %v\n", k, cnt, first)
	}

	fmt.Println("\nMandelbrot set, real -2.2..0.8, imaginary -1.2..1.2")
	for y := 0; y < 21; y++ {
		var row strings.Builder
		for x := 0; x < 61; x++ {
			cr, ci := -2.2+float64(x)*0.05, float64(10-y)*0.12
			zr, zi, i := 0.0, 0.0, 0
			for ; i < 50 && zr*zr+zi*zi <= 4; i++ {
				zr, zi = zr*zr-zi*zi+cr, 2*zr*zi+ci
			}
			row.WriteByte(" .:-=+*%#@"[min(i, 50)*9/50])
		}
		fmt.Println(strings.TrimRight(row.String(), " "))
	}
}
