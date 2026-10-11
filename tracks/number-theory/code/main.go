// Number theory toolkit: sieve, Euclid, extended Euclid, fast modular power, toy RSA.
// Run with: go run main.go
package main

import "fmt"

// sieve returns all primes up to n (Sieve of Eratosthenes).
func sieve(n int) []int {
	composite := make([]bool, n+1)
	var primes []int
	for i := 2; i <= n; i++ {
		if composite[i] {
			continue
		}
		primes = append(primes, i)
		for j := i * i; j <= n; j += i {
			composite[j] = true
		}
	}
	return primes
}

// gcd uses the Euclidean algorithm: gcd(a, b) = gcd(b, a mod b).
func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// extGCD returns g, x, y with a*x + b*y = g = gcd(a, b) (Bezout).
func extGCD(a, b int) (int, int, int) {
	if b == 0 {
		return a, 1, 0
	}
	g, x, y := extGCD(b, a%b)
	return g, y, x - (a/b)*y
}

// powMod computes base^exp mod m by repeated squaring.
func powMod(base, exp, m int) int {
	result := 1
	base %= m
	for exp > 0 {
		if exp&1 == 1 {
			result = result * base % m
		}
		base = base * base % m
		exp >>= 1
	}
	return result
}

func main() {
	p := sieve(100)
	fmt.Printf("primes up to 100 (%d): %v\n", len(p), p)

	fmt.Println("gcd(84, 36) =", gcd(84, 36))
	g, x, y := extGCD(240, 46)
	fmt.Printf("Bezout: 240*(%d) + 46*(%d) = %d\n", x, y, g)

	fmt.Println("7^100 mod 5 =", powMod(7, 100, 5))
	fmt.Println("Fermat check 3^12 mod 13 =", powMod(3, 12, 13))

	// Toy RSA with tiny primes. Real keys use primes with hundreds of digits.
	pr, q := 61, 53
	n := pr * q
	phi := (pr - 1) * (q - 1)
	e := 17
	_, d, _ := extGCD(e, phi)
	d = ((d % phi) + phi) % phi
	msg := 65
	c := powMod(msg, e, n)
	back := powMod(c, d, n)
	fmt.Printf("RSA: n=%d phi=%d e=%d d=%d\n", n, phi, e, d)
	fmt.Printf("RSA: message %d -> ciphertext %d -> decrypted %d\n", msg, c, back)
}
