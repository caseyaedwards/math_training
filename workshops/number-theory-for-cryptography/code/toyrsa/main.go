// Command toyrsa walks through toy RSA, end to end, printing every step.
//
// FOR LEARNING ONLY. This program uses tiny primes and no padding.
// Anyone can break these keys by hand. Real systems use vetted
// libraries (for example Go crypto/tls, crypto/rsa, crypto/ecdh).
//
// Sections:
//
//  1. Modular arithmetic: clock arithmetic and the % operator
//  2. gcd and the extended Euclidean algorithm (with a table)
//  3. Modular inverse
//  4. Fast modular exponentiation (square-and-multiply trace)
//  5. Euler totient
//  6. RSA key generation, encryption, decryption
//  7. RSA signature and verification
//
// Run from the workshop folder: go run ./code/toyrsa
package main

import (
	"fmt"
	"math/big"
	"strconv"
	"strings"
)

func banner(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 64))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 64))
}

// mod returns a mod m in the range 0..m-1, even for negative a.
// Go % keeps the sign of a, so -3 % 7 is -3, not 4.
func mod(a, m int64) int64 {
	return ((a % m) + m) % m
}

// ---------------------------------------------------------------
// 1. Modular arithmetic
// ---------------------------------------------------------------
func sectionMod() {
	banner("1. Modular arithmetic: clock arithmetic and %")
	fmt.Println("Clock: 9 plus 5 hours lands on (9 + 5) % 12 =", (9+5)%12)
	fmt.Println("Clock: 3 minus 7 hours, Go (3 - 7) % 12 =", (3-7)%12, "(negative!)")
	fmt.Println("Clock: 3 minus 7 hours, mod(3 - 7, 12)  =", mod(3-7, 12))
	fmt.Println("Go % keeps the sign of the left side; mod() fixes it:")
	for _, a := range []int64{17, -3, 24, 100} {
		fmt.Printf("  %4d %% 7 = %2d    mod(%4d, 7) = %d\n", a, a%7, a, mod(a, 7))
	}
	fmt.Println("Reduce early, reduce often: (a * b) % m == ((a % m) * (b % m)) % m")
	var a, b, m int64 = 123456, 789012, 3233
	fmt.Printf("  (%d * %d) %% %d = %d\n", a, b, m, (a*b)%m)
	fmt.Printf("  ((%d %% %d) * (%d %% %d)) %% %d = %d\n", a, m, b, m, m, ((a%m)*(b%m))%m)
}

// ---------------------------------------------------------------
// 2. gcd and extended Euclid
// ---------------------------------------------------------------
func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// extendedGCD returns (g, x, y) with a*x + b*y = g = gcd(a, b).
func extendedGCD(a, b int64, verbose bool) (int64, int64, int64) {
	oldR, r := a, b
	oldX, x := int64(1), int64(0)
	oldY, y := int64(0), int64(1)
	if verbose {
		fmt.Printf("  %4s %6s %6s %6s\n", "q", "r", "x", "y")
		fmt.Printf("  %4s %6d %6d %6d\n", "", oldR, oldX, oldY)
		fmt.Printf("  %4s %6d %6d %6d\n", "", r, x, y)
	}
	for r != 0 {
		q := oldR / r
		oldR, r = r, oldR-q*r
		oldX, x = x, oldX-q*x
		oldY, y = y, oldY-q*y
		if verbose {
			fmt.Printf("  %4d %6d %6d %6d\n", q, r, x, y)
		}
	}
	return oldR, oldX, oldY
}

func sectionGCD() {
	banner("2. gcd and the extended Euclidean algorithm")
	fmt.Println("Euclid steps for gcd(3120, 17):")
	var a, b int64 = 3120, 17
	for b != 0 {
		fmt.Printf("  %d = %d * %d + %d\n", a, a/b, b, a%b)
		a, b = b, a%b
	}
	fmt.Println("  gcd =", a)
	fmt.Println()
	fmt.Println("Extended table for (3120, 17); each row keeps r = 3120*x + 17*y:")
	g, x, y := extendedGCD(3120, 17, true)
	fmt.Printf("  result: gcd = %d, x = %d, y = %d\n", g, x, y)
	fmt.Printf("  check: 3120 * (%d) + 17 * (%d) = %d\n", x, y, 3120*x+17*y)
}

// ---------------------------------------------------------------
// 3. Modular inverse
// ---------------------------------------------------------------
func modInverse(e, m int64) (int64, error) {
	g, x, _ := extendedGCD(e, m, false)
	if g != 1 {
		return 0, fmt.Errorf("%d has no inverse mod %d (gcd = %d)", e, m, g)
	}
	return mod(x, m), nil
}

func sectionInverse() {
	banner("3. Modular inverse")
	d, _ := modInverse(17, 3120)
	fmt.Println("inverse of 17 mod 3120 =", d)
	fmt.Printf("check: 17 * %d = %d = %d * 3120 + %d\n", d, 17*d, 17*d/3120, 17*d%3120)
	lib := new(big.Int).ModInverse(big.NewInt(17), big.NewInt(3120))
	fmt.Println("math/big: new(big.Int).ModInverse(17, 3120) =", lib)
	if _, err := modInverse(6, 3120); err != nil {
		fmt.Println("no inverse case:", err)
	}
}

// ---------------------------------------------------------------
// 4. Fast modular exponentiation
// ---------------------------------------------------------------

// modPow is left-to-right square-and-multiply.
func modPow(base, exp, m int64, verbose bool) int64 {
	result := int64(1)
	bits := strconv.FormatInt(exp, 2)
	if verbose {
		fmt.Printf("  exponent %d in binary = %s\n", exp, bits)
		fmt.Printf("  %3s  %-18s %6s\n", "bit", "action", "result")
	}
	for _, bit := range bits {
		result = (result * result) % m
		action := "square"
		if bit == '1' {
			result = (result * base) % m
			action = "square, multiply"
		}
		if verbose {
			fmt.Printf("  %3c  %-18s %6d\n", bit, action, result)
		}
	}
	return result
}

// bigPow wraps math/big Exp, the library version of modPow.
func bigPow(b, e, m int64) int64 {
	return new(big.Int).Exp(big.NewInt(b), big.NewInt(e), big.NewInt(m)).Int64()
}

func sectionPow() {
	banner("4. Fast modular exponentiation (square-and-multiply)")
	fmt.Println("Compute 65^17 mod 3233:")
	r := modPow(65, 17, 3233, true)
	fmt.Println("  modPow result             =", r)
	fmt.Println("  big.Int Exp(65, 17, 3233) =", bigPow(65, 17, 3233))
	full := new(big.Int).Exp(big.NewInt(65), big.NewInt(17), nil)
	fmt.Println("  65^17 in full             =", full)
	fmt.Printf("  (%d digits; it overflows int64, which holds 19)\n", len(full.String()))
	fmt.Println("  65^17 in full, mod 3233   =", new(big.Int).Mod(full, big.NewInt(3233)))
	fmt.Println()
	fmt.Println("Multiplications needed for exponent 2753:")
	bits := strconv.FormatInt(2753, 2)
	ones := strings.Count(bits, "1")
	fmt.Printf("  binary %s: %d squarings + %d multiplies = %d steps, versus 2752 for naive repeated multiply\n",
		bits, len(bits), ones, len(bits)+ones)
}

// ---------------------------------------------------------------
// 5. Euler totient
// ---------------------------------------------------------------
func phiBruteForce(n int64) int64 {
	var count int64
	for k := int64(1); k <= n; k++ {
		if gcd(k, n) == 1 {
			count++
		}
	}
	return count
}

func sectionTotient() {
	banner("5. Euler totient")
	for _, n := range []int64{10, 12, 13} {
		var coprime []int64
		for k := int64(1); k <= n; k++ {
			if gcd(k, n) == 1 {
				coprime = append(coprime, k)
			}
		}
		fmt.Printf("  phi(%d) = %d: %v\n", n, len(coprime), coprime)
	}
	fmt.Println("For n = p*q with p, q prime: phi(n) = (p - 1)(q - 1)")
	fmt.Println("  phi(3233) by counting =", phiBruteForce(3233))
	fmt.Println("  (61 - 1) * (53 - 1)   =", 60*52)
	fmt.Println("Euler theorem check: 65^3120 mod 3233 =", bigPow(65, 3120, 3233))
}

// ---------------------------------------------------------------
// 6 and 7. RSA
// ---------------------------------------------------------------
func sectionRSA() {
	banner("6. Toy RSA: key generation, encryption, decryption")
	fmt.Println("WARNING: toy RSA. Tiny primes, no padding. For learning only.")
	var p, q int64 = 61, 53
	n := p * q
	phi := (p - 1) * (q - 1)
	var e int64 = 17
	d, _ := modInverse(e, phi)
	rows := [][2]string{
		{fmt.Sprintf("p = %d, q = %d", p, q), "two secret primes"},
		{fmt.Sprintf("n = p * q = %d", n), "public modulus"},
		{fmt.Sprintf("phi = (p-1)(q-1) = %d", phi), "secret"},
		{fmt.Sprintf("e = %d, gcd(e, phi) = %d", e, gcd(e, phi)), "public exponent"},
		{fmt.Sprintf("d = e^-1 mod phi = %d", d), "private exponent"},
		{fmt.Sprintf("check: e * d mod phi = %d", e*d%phi), "d really undoes e"},
	}
	for _, row := range rows {
		fmt.Printf("  %-30s %s\n", row[0], row[1])
	}
	fmt.Printf("  public key  (n, e) = (%d, %d)\n", n, e)
	fmt.Printf("  private key (n, d) = (%d, %d)\n", n, d)
	fmt.Println()

	var m int64 = 65
	c := modPow(m, e, n, false)
	back := modPow(c, d, n, false)
	fmt.Printf("  message m = %d\n", m)
	fmt.Printf("  encrypt c = m^e mod n = %d^%d mod %d = %d\n", m, e, n, c)
	fmt.Printf("  decrypt   c^d mod n = %d^%d mod %d = %d\n", c, d, n, back)
	fmt.Println()

	text := "HI"
	var codes, cipher, plain []int64
	for _, ch := range text {
		codes = append(codes, int64(ch))
	}
	for _, x := range codes {
		cipher = append(cipher, modPow(x, e, n, false))
	}
	var out strings.Builder
	for _, x := range cipher {
		y := modPow(x, d, n, false)
		plain = append(plain, y)
		out.WriteRune(rune(y))
	}
	fmt.Printf("  text %q as numbers   %v\n", text, codes)
	fmt.Printf("  ciphertext             %v\n", cipher)
	fmt.Printf("  decrypted numbers      %v -> %q\n", plain, out.String())

	banner("7. Toy RSA: sign and verify")
	var h int64 = 123
	s := modPow(h, d, n, false)
	v := modPow(s, e, n, false)
	verdict := func(ok bool) string {
		if ok {
			return "VALID"
		}
		return "INVALID"
	}
	fmt.Printf("  message digest h = %d  (toy stand-in for a real hash)\n", h)
	fmt.Printf("  sign   s = h^d mod n = %d^%d mod %d = %d\n", h, d, n, s)
	fmt.Printf("  verify s^e mod n = %d^%d mod %d = %d -> %s\n", s, e, n, v, verdict(v == h))
	forged := s + 1
	fv := modPow(forged, e, n, false)
	fmt.Printf("  tampered s = %d: s^e mod n = %d -> %s\n", forged, fv, verdict(fv == h))
	fmt.Println()
	fmt.Println("Why it is toy: factor n by trial division:")
	for k := int64(2); k < n; k++ {
		if n%k == 0 {
			fmt.Printf("  %d = %d * %d  (found after %d tries)\n", n, k, n/k, k-1)
			break
		}
	}
}

func main() {
	sectionMod()
	sectionGCD()
	sectionInverse()
	sectionPow()
	sectionTotient()
	sectionRSA()
}
