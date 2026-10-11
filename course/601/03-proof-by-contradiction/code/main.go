// Euclid numbers: (product of the first primes) + 1, and their smallest prime factor.
package main

import "fmt"

func smallestFactor(n int) int {
	for d := 2; d*d <= n; d++ {
		if n%d == 0 {
			return d
		}
	}
	return n
}

func main() {
	product := 1
	for _, p := range []int{2, 3, 5, 7, 11, 13, 17} {
		product *= p
		n := product + 1
		q := smallestFactor(n)
		note := "prime"
		if q != n {
			note = fmt.Sprintf("= %d * %d", q, n/q)
		}
		fmt.Printf("up to %2d: N = %7d  %s\n", p, n, note)
	}
}
