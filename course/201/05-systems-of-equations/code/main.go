// Solve a*x + b*y = e and c*x + d*y = f exactly.
// The formula is elimination done once, in general.
package main

import (
	"fmt"
	"math/big"
)

func solve2(a, b, e, c, d, f int64) string {
	det := a*d - b*c
	if det == 0 {
		return "no single solution (parallel lines or the same line)"
	}
	x := big.NewRat(e*d-b*f, det)
	y := big.NewRat(a*f-e*c, det)
	return fmt.Sprintf("x = %s, y = %s", x.RatString(), y.RatString())
}

func main() {
	fmt.Println("2x + 3y = 12, x - y = 1     :", solve2(2, 3, 12, 1, -1, 1))
	fmt.Println("3x + 2y = 16, 5x - 2y = 0   :", solve2(3, 2, 16, 5, -2, 0))
	fmt.Println("2x + 3y = 13, 5x - 2y = 4   :", solve2(2, 3, 13, 5, -2, 4))
	fmt.Println("s + l = 15, 16s + 64l = 528 :", solve2(1, 1, 15, 16, 64, 528))
	fmt.Println("x + 2y = 4, 2x + 4y = 8     :", solve2(1, 2, 4, 2, 4, 8))
}
