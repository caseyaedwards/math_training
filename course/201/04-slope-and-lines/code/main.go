// Find the line through two points, with exact fractions.
package main

import (
	"fmt"
	"math/big"
)

func lineThrough(x1, y1, x2, y2 int64) string {
	if x1 == x2 {
		return fmt.Sprintf("x = %d (vertical, slope undefined)", x1)
	}
	m := big.NewRat(y2-y1, x2-x1) // rise over run
	// b = y1 - m*x1
	b := new(big.Rat).Sub(big.NewRat(y1, 1), new(big.Rat).Mul(m, big.NewRat(x1, 1)))
	sign := "+"
	if b.Sign() < 0 {
		sign = "-"
		b.Neg(b)
	}
	return fmt.Sprintf("y = %sx %s %s", m.RatString(), sign, b.RatString())
}

func main() {
	fmt.Println("(1, 1) and (3, 5):    ", lineThrough(1, 1, 3, 5))
	fmt.Println("(2, 3) and (6, 1):    ", lineThrough(2, 3, 6, 1))
	fmt.Println("(0, 140) and (10, 260):", lineThrough(0, 140, 10, 260))
	fmt.Println("(2, 5) and (7, 5):    ", lineThrough(2, 5, 7, 5))
	fmt.Println("(3, 1) and (3, 6):    ", lineThrough(3, 1, 3, 6))
}
