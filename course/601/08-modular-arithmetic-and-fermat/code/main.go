// Fast modular powers, Fermat checks, an inverse, and a Carmichael number.
package main

import "fmt"

// powMod computes b^e mod m by repeated squaring.
func powMod(b, e, m int) int {
	result := 1
	b %= m
	for e > 0 {
		if e&1 == 1 {
			result = result * b % m
		}
		b = b * b % m
		e >>= 1
	}
	return result
}

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// fermatAll reports whether a^(n-1) = 1 mod n for every a coprime to n.
func fermatAll(n int) bool {
	for a := 2; a < n; a++ {
		if gcd(a, n) == 1 && powMod(a, n-1, n) != 1 {
			return false
		}
	}
	return true
}

func main() {
	fmt.Println("2^100 mod 7  =", powMod(2, 100, 7))
	fmt.Println("7^222 mod 11 =", powMod(7, 222, 11))
	fmt.Println("3^100 mod 13 =", powMod(3, 100, 13))
	for x := 1; x < 26; x++ {
		if 7*x%26 == 1 {
			fmt.Println("inverse of 7 mod 26 =", x)
		}
	}
	fmt.Println("Fermat holds for all bases, n = 13: ", fermatAll(13))
	fmt.Println("Fermat holds for all bases, n = 15: ", fermatAll(15))
	fmt.Println("Fermat holds for all bases, n = 561:", fermatAll(561), " (561 = 3 * 11 * 17)")
	fmt.Println("Go remainder of -1 % 7 =", -1%7, "(math says 6)")
}
