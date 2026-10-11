// Command diffiehellman runs a toy Diffie-Hellman key exchange with p = 23, g = 5.
//
// FOR LEARNING ONLY. A 23-element group falls to brute force in
// microseconds. Real systems use vetted libraries and large groups or
// elliptic curves (for example Go crypto/ecdh with X25519).
//
// Prints:
//
//  1. The powers of g mod p (g generates every nonzero residue)
//  2. Alice and Bob each picking a secret and sending a public value
//  3. Both sides reaching the same shared secret
//  4. What an eavesdropper (Eve) sees, and a brute-force attack
//
// Run from the workshop folder: go run ./code/diffiehellman
package main

import (
	"fmt"
	"strings"
)

const (
	P           = 23
	G           = 5
	aliceSecret = 6
	bobSecret   = 15
)

func banner(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 60))
}

// modPow computes base^exp mod m by square-and-multiply.
func modPow(base, exp, m int) int {
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
	banner(fmt.Sprintf("1. Powers of g = %d mod p = %d", G, P))
	seen := map[int]bool{}
	for k := 1; k < P; k++ {
		v := modPow(G, k, P)
		seen[v] = true
		fmt.Printf("  %d^%-2d mod %d = %2d  %s\n", G, k, P, v, strings.Repeat("#", v))
	}
	fmt.Printf("  distinct values: %d of %d -> g is a generator\n", len(seen), P-1)

	banner("2. Each side picks a secret and publishes g^secret mod p")
	a, b := aliceSecret, bobSecret
	A := modPow(G, a, P)
	B := modPow(G, b, P)
	fmt.Printf("  Alice secret a = %-3d  sends A = %d^%d mod %d = %d\n", a, G, a, P, A)
	fmt.Printf("  Bob   secret b = %-3d  sends B = %d^%d mod %d = %d\n", b, G, b, P, B)

	banner("3. Both sides compute the shared secret")
	sAlice := modPow(B, a, P)
	sBob := modPow(A, b, P)
	fmt.Printf("  Alice: B^a mod p = %d^%d mod %d = %d\n", B, a, P, sAlice)
	fmt.Printf("  Bob:   A^b mod p = %d^%d mod %d = %d\n", A, b, P, sBob)
	fmt.Printf("  direct: g^(a*b) mod p = %d^%d mod %d = %d\n", G, a*b, P, modPow(G, a*b, P))
	fmt.Printf("  match: %v\n", sAlice == sBob)

	banner("4. What Eve sees on the wire")
	fmt.Printf("  p = %d, g = %d, A = %d, B = %d\n", P, G, A, B)
	fmt.Println("  Eve does NOT see a, b, or the shared secret.")
	fmt.Println("  Naive guess g^(A*B) mod p =", modPow(G, A*B, P), "(wrong)")
	fmt.Println("  Naive guess A*B mod p     =", A*B%P, "(wrong)")
	fmt.Println("  Brute force: try every x until g^x mod p == A")
	for x := 1; x < P; x++ {
		if modPow(G, x, P) == A {
			fmt.Printf("    found x = %d after %d tries; secret = B^x mod p = %d\n", x, x, modPow(B, x, P))
			break
		}
	}
	fmt.Println("  With a 2048-bit p the same loop needs about 2^2048 tries.")
	fmt.Println("  This hard problem is the discrete logarithm problem.")
}
