// Fraction operations with exact arithmetic, plus a check of flip-and-multiply.
package main

import (
	"fmt"
	"math/big"
	"math/rand"
)

func r(a, b int64) *big.Rat { return big.NewRat(a, b) }

func main() {
	fmt.Println("1/3 + 1/4 =", new(big.Rat).Add(r(1, 3), r(1, 4)).RatString())
	fmt.Println("5/6 - 3/8 =", new(big.Rat).Sub(r(5, 6), r(3, 8)).RatString())
	fmt.Println("2/3 × 3/4 =", new(big.Rat).Mul(r(2, 3), r(3, 4)).RatString())
	fmt.Println("3/2 ÷ 1/4 =", new(big.Rat).Quo(r(3, 2), r(1, 4)).RatString())
	fmt.Println("5/2 × 4/3 =", new(big.Rat).Mul(r(5, 2), r(4, 3)).RatString())

	// Check: x ÷ y equals x × (flipped y), on 1,000 random fractions.
	rng := rand.New(rand.NewSource(1))
	ok := 0
	for i := 0; i < 1000; i++ {
		a, b, c, d := rng.Int63n(20)+1, rng.Int63n(20)+1, rng.Int63n(20)+1, rng.Int63n(20)+1
		x, y := r(a, b), r(c, d)
		quo := new(big.Rat).Quo(x, y)
		flip := new(big.Rat).Mul(x, r(d, c))
		if quo.Cmp(flip) == 0 {
			ok++
		}
	}
	fmt.Println("flip-and-multiply agreed", ok, "of 1000 times")
}
