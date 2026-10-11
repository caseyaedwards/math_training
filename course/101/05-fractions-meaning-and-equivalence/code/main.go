// Fractions: math/big.Rat stores exact fractions in simplest form.
package main

import (
	"fmt"
	"math/big"
)

func main() {
	fmt.Println("18/24 =", big.NewRat(18, 24))

	// NewRat simplifies on the way in: 2/4, 4/8 and 3/6 all land on 1/2.
	half := big.NewRat(1, 2)
	for _, p := range [][2]int64{{2, 4}, {4, 8}, {3, 6}} {
		r := big.NewRat(p[0], p[1])
		fmt.Printf("%d/%d is stored as %v, equal to 1/2: %v\n", p[0], p[1], r, half.Cmp(r) == 0)
	}

	// Cmp returns 1 when the first is larger.
	fmt.Println("5/8 vs 3/5:", big.NewRat(5, 8).Cmp(big.NewRat(3, 5)))

	// Improper to mixed: quotient and remainder.
	for _, p := range [][2]int{{17, 5}, {23, 4}} {
		fmt.Printf("%d/%d = %d %d/%d\n", p[0], p[1], p[0]/p[1], p[0]%p[1], p[1])
	}

	// A fraction is a division.
	f, _ := big.NewRat(3, 4).Float64()
	fmt.Println("3/4 as a decimal:", f)
}
