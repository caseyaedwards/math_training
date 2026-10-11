// Negative numbers: check the sign rules instead of trusting them.
package main

import "fmt"

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	checks := 0
	for a := -5; a <= 5; a++ {
		for b := -5; b <= 5; b++ {
			if a-b != a+(-b) {
				panic("subtract is not add-the-opposite")
			}
			positive := a*b > 0
			sameSign := a != 0 && b != 0 && (a > 0) == (b > 0)
			if positive != sameSign {
				panic("sign rule broken")
			}
			if abs(a-b) != abs(b-a) {
				panic("distance is not symmetric")
			}
			checks++
		}
	}
	fmt.Println("sign rules hold for", checks, "pairs")

	fmt.Println("2 + (-5) =", 2+(-5))
	fmt.Println("-4 - (-9) =", -4-(-9))
	fmt.Println("(-6) * (-7) =", (-6)*(-7))
	fmt.Println("clock skew 125 - (-340) =", 125-(-340), "ms")

	// Go integer division rounds toward zero.
	fmt.Println("-7 / 2 =", -7/2, "  -7 % 2 =", -7%2)
}
