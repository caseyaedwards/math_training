// Greek methods in Go: Archimedes, Euclid, Eratosthenes, and root 2.
// Run: go run main.go
package main

import (
	"fmt"
	"math"
)

// archimedes doubles the sides of polygons around a circle of radius 1.
// s is the side of the inside polygon. Pythagoras gives the next side:
// s2 = sqrt(2 - sqrt(4 - s*s)). The outside side is s / sqrt(1 - s*s/4).
// Half the perimeter of each polygon brackets pi.
func archimedes() {
	fmt.Println("Archimedes: half-perimeters for a circle of radius 1")
	fmt.Printf("%6s  %9s  %9s\n", "sides", "inside", "outside")
	s, n := 1.0, 6 // a hexagon inside a radius-1 circle has side 1
	for n <= 96 {
		t := s / math.Sqrt(1-s*s/4)
		fmt.Printf("%6d  %9.5f  %9.5f\n", n, float64(n)*s/2, float64(n)*t/2)
		s = math.Sqrt(2 - math.Sqrt(4-s*s))
		n *= 2
	}
	fmt.Printf("his bounds: %.5f < pi < %.5f\n\n", 3+10.0/71, 22.0/7)
}

// gcd runs the Euclidean algorithm and prints each division.
func gcd(a, b int) int {
	for b != 0 {
		fmt.Printf("  %5d = %3d x %4d + %4d\n", a, a/b, b, a%b)
		a, b = b, a%b
	}
	return a
}

// sieve returns the primes up to n by crossing out multiples.
func sieve(n int) []int {
	crossed := make([]bool, n+1)
	var primes []int
	for p := 2; p <= n; p++ {
		if crossed[p] {
			continue
		}
		primes = append(primes, p)
		for m := p * p; m <= n; m += p {
			crossed[m] = true
		}
	}
	return primes
}

// smallestFactor returns the smallest divisor of n greater than 1.
func smallestFactor(n int) int {
	for d := 2; d*d <= n; d++ {
		if n%d == 0 {
			return d
		}
	}
	return n
}

func main() {
	archimedes()

	fmt.Println("Euclid VII.2: gcd(1071, 462)")
	fmt.Println("  gcd =", gcd(1071, 462))
	fmt.Println()

	fmt.Println("Eratosthenes: primes up to 60")
	fmt.Println(" ", sieve(60))
	fmt.Println()

	fmt.Println("Euclid IX.20: multiply primes, add 1, find a new prime factor")
	product := 1
	for _, p := range []int{2, 3, 5, 7, 11, 13} {
		product *= p
		f := smallestFactor(product + 1)
		fmt.Printf("  up to %2d: %5d + 1 = %5d, smallest prime factor %d\n",
			p, product, product+1, f)
	}
	fmt.Println()

	fmt.Println("Root 2: fractions p/q that come close, but p*p - 2*q*q is never 0")
	p, q := 1, 1
	for i := 0; i < 7; i++ {
		p, q = p+2*q, p+q
		fmt.Printf("  %4d/%-4d = %.7f  p*p - 2*q*q = %2d\n",
			p, q, float64(p)/float64(q), p*p-2*q*q)
	}
}
