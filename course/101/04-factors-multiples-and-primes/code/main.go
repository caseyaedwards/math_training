// Factors, multiples and primes: sieve, factorize, Euclid.
package main

import "fmt"

// primesBelow returns every prime less than n (Sieve of Eratosthenes).
func primesBelow(n int) []int {
	composite := make([]bool, n)
	var primes []int
	for p := 2; p < n; p++ {
		if composite[p] {
			continue
		}
		primes = append(primes, p)
		for m := p * p; m < n; m += p {
			composite[m] = true
		}
	}
	return primes
}

// factorize returns the prime factors of n, smallest first.
func factorize(n int) []int {
	var fs []int
	for p := 2; p*p <= n; p++ { // only up to the square root
		for n%p == 0 {
			fs = append(fs, p)
			n /= p
		}
	}
	if n > 1 {
		fs = append(fs, n)
	}
	return fs
}

// gcd is Euclid's algorithm. With show set, it prints each step.
func gcd(a, b int, show bool) int {
	for b != 0 {
		if show {
			fmt.Printf("  %d = %d × %d + %d\n", a, a/b, b, a%b)
		}
		a, b = b, a%b
	}
	return a
}

func main() {
	fmt.Println("primes below 50:", primesBelow(50))
	for _, n := range []int{84, 60, 360, 91} {
		fmt.Println(n, "=", factorize(n))
	}
	fmt.Println("gcd(84, 60):")
	g := gcd(84, 60, true)
	fmt.Println("  gcd =", g, " lcm =", 84*60/g)
	fmt.Println("jobs every 6 and 15 min meet every", 6*15/gcd(6, 15, false), "min")
}
