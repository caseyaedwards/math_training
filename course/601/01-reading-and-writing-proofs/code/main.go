// Hunt for counterexamples. A hit disproves a "for every" claim. No hit proves nothing.
package main

import "fmt"

func isPrime(n int) bool {
	if n < 2 {
		return false
	}
	for d := 2; d*d <= n; d++ {
		if n%d == 0 {
			return false
		}
	}
	return true
}

func main() {
	// Claim: n*n + n + 41 is prime for every n >= 1.
	for n := 1; n < 100; n++ {
		v := n*n + n + 41
		if !isPrime(v) {
			fmt.Printf("n*n + n + 41: first counterexample n = %d, value %d = %d * %d\n", n, v, 41, v/41)
			break
		}
	}

	// Claim: every odd number greater than 1 is prime.
	for n := 3; ; n += 2 {
		if !isPrime(n) {
			fmt.Printf("odd numbers are prime: first counterexample %d\n", n)
			break
		}
	}

	// Claim: 2^n - 1 is prime whenever n is prime.
	for n := 2; n < 40; n++ {
		if isPrime(n) && !isPrime(1<<n-1) {
			fmt.Printf("2^n - 1 for prime n: first counterexample n = %d, value %d\n", n, 1<<n-1)
			break
		}
	}
}
