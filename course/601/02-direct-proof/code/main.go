// Smoke tests for claims before you prove them. Passing is evidence, not proof.
package main

import "fmt"

func main() {
	// Claim: 8 divides n^2 - 1 for every odd n.
	bad := 0
	for n := 1; n <= 10001; n += 2 {
		if (n*n-1)%8 != 0 {
			bad++
		}
	}
	fmt.Println("odd n up to 10001 with 8 not dividing n^2 - 1:", bad)

	// Claim: odd + odd is even, for a grid of values including negatives.
	bad = 0
	for a := -99; a <= 99; a += 2 {
		for b := -99; b <= 99; b += 2 {
			if (a+b)%2 != 0 {
				bad++
			}
		}
	}
	fmt.Println("odd pairs in [-99, 99] with an odd sum:", bad)

	// Claim: the sum of three consecutive integers is 3(n + 1).
	for _, n := range []int{-5, 0, 7, 100} {
		fmt.Printf("n = %4d  sum = %4d  3(n+1) = %4d\n", n, n+(n+1)+(n+2), 3*(n+1))
	}
}
