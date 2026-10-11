// The extended Euclidean algorithm: gcd plus Bezout coefficients.
package main

import "fmt"

// egcd returns (g, x, y) with a*x + b*y == g == gcd(a, b).
func egcd(a, b int) (int, int, int) {
	if b == 0 {
		return a, 1, 0
	}
	g, x, y := egcd(b, a%b)  // solve the smaller pair first
	return g, y, x - (a/b)*y // back-substitute one line
}

func main() {
	for _, p := range [][2]int{{1071, 462}, {252, 198}, {161, 28}, {89, 55}} {
		a, b := p[0], p[1]
		g, x, y := egcd(a, b)
		fmt.Printf("gcd(%d, %d) = %d = %d*(%d) + %d*(%d)\n", a, b, g, a, x, b, y)
	}

	// Count the division steps on consecutive Fibonacci numbers, the slow case.
	a, b, steps := 89, 55, 0
	for b != 0 {
		a, b = b, a%b
		steps++
	}
	fmt.Println("division steps for (89, 55):", steps)
}
