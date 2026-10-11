// Powers of two, the exponent rules checked by brute force,
// and a scientific-notation formatter.
package main

import (
	"fmt"
	"math"
)

// pow multiplies base by itself n times. No shortcuts, no math.Pow.
func pow(base, n int) int {
	result := 1
	for i := 0; i < n; i++ {
		result *= base
	}
	return result
}

// sci splits x into a mantissa m with 1 <= |m| < 10 and an exponent e,
// so that x = m * 10^e.
func sci(x float64) (float64, int) {
	if x == 0 {
		return 0, 0
	}
	e := int(math.Floor(math.Log10(math.Abs(x))))
	m := x / math.Pow(10, float64(e))
	return m, e
}

func main() {
	fmt.Println("powers of two an SRE meets daily:")
	for _, n := range []int{10, 20, 30, 32, 40} {
		fmt.Printf("  2^%-2d = %d\n", n, pow(2, n))
	}

	ok := true
	for a := 0; a <= 6; a++ {
		for b := 0; b <= 6; b++ {
			if pow(2, a)*pow(2, b) != pow(2, a+b) { // product rule
				ok = false
			}
			if pow(pow(2, a), b) != pow(2, a*b) { // power of a power
				ok = false
			}
		}
	}
	fmt.Println("product rule and power rule hold for 0..6:", ok)

	for _, x := range []float64{4294967296, 93000000, 0.00025, 0.0000042, 6e5 * 4e3} {
		m, e := sci(x)
		fmt.Printf("  %-14g = %.4g x 10^%d\n", x, m, e)
	}
}
