// Solve a*x + b = c*x + d exactly, then check the answer.
package main

import (
	"fmt"
	"math/big"
)

// solve returns the solution of a*x + b = c*x + d,
// or a word when there is no single solution.
func solve(a, b, c, d *big.Rat) string {
	if a.Cmp(c) == 0 {
		if b.Cmp(d) == 0 {
			return "every x works"
		}
		return "no solution"
	}
	// (a - c) x = d - b
	left := new(big.Rat).Sub(a, c)
	right := new(big.Rat).Sub(d, b)
	x := new(big.Rat).Quo(right, left)

	// The check: substitute x into both sides.
	lhs := new(big.Rat).Add(new(big.Rat).Mul(a, x), b)
	rhs := new(big.Rat).Add(new(big.Rat).Mul(c, x), d)
	if lhs.Cmp(rhs) != 0 {
		panic("check failed")
	}
	return "x = " + x.RatString()
}

// r turns a string such as "3" or "1/2" into an exact fraction.
func r(s string) *big.Rat {
	v, ok := new(big.Rat).SetString(s)
	if !ok {
		panic(s)
	}
	return v
}

func main() {
	fmt.Println("3x + 5 = 20        ->", solve(r("3"), r("5"), r("0"), r("20")))
	fmt.Println("5x - 7 = 2x + 8    ->", solve(r("5"), r("-7"), r("2"), r("8")))
	fmt.Println("3x + 6 = 2x - 4    ->", solve(r("3"), r("6"), r("2"), r("-4")))
	fmt.Println("x/2 + 3 = x/4 + 4  ->", solve(r("1/2"), r("3"), r("1/4"), r("4")))
	fmt.Println("x + 1 = x + 2      ->", solve(r("1"), r("1"), r("1"), r("2")))
	fmt.Println("2x + 6 = 2x + 6    ->", solve(r("2"), r("6"), r("2"), r("6")))
	fmt.Println("140 + 12d = 500    ->", solve(r("12"), r("140"), r("0"), r("500")))
}
