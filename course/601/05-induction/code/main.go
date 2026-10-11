// Recursion has the shape of an induction proof: a base case and a step.
package main

import "fmt"

// stair returns 1 + 2 + ... + n.
func stair(n int) int {
	if n == 1 { // base case
		return 1
	}
	return stair(n-1) + n // step: reuse the answer for n - 1
}

func main() {
	ok := true
	for n := 1; n < 500; n++ {
		if stair(n) != n*(n+1)/2 {
			ok = false
		}
	}
	fmt.Println("stair(n) == n(n+1)/2 for n = 1..499:", ok)

	// 2^n < n! starts at n = 4.
	pow, fact := 1, 1
	for n := 1; n <= 7; n++ {
		pow *= 2
		fact *= n
		fmt.Printf("n = %d  2^n = %3d  n! = %4d  2^n < n!: %v\n", n, pow, fact, pow < fact)
	}
}
