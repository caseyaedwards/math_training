// Logarithms: base 2 for computing, change of base, doubling time,
// and counting binary-search steps.
// Run: go run main.go
package main

import (
	"fmt"
	"math"
	"math/bits"
	"sort"
)

// logb computes log base b of x with the change-of-base formula.
func logb(b, x float64) float64 { return math.Log(x) / math.Log(b) }

func main() {
	fmt.Println("log2 32      =", math.Log2(32))
	fmt.Println("log10 0.001  =", math.Log10(0.001))
	fmt.Printf("log3 20      = %.4f (the x with 3^x = 20)\n", logb(3, 20))

	// Bits needed to give n distinct IDs: ceil(log2 n).
	for _, n := range []float64{256, 5000, 1e6, 1e9} {
		fmt.Printf("IDs %-8v need %2.0f bits (log2 = %.2f)\n", n, math.Ceil(math.Log2(n)), math.Log2(n))
	}
	// The same thing with integer bit tricks: bits.Len gives the bit length.
	fmt.Println("bits.Len(4999) =", bits.Len(4999), "(IDs 0..4999 fit in 13 bits)")

	// Doubling time at 20% per month and the rule of 70.
	fmt.Printf("doubling at 20%%/month: %.2f months (rule of 70 says %.1f)\n",
		math.Log(2)/math.Log(1.2), 70.0/20)

	// Count binary-search probes on a sorted slice of one million keys.
	keys := make([]int, 1_000_000)
	for i := range keys {
		keys[i] = 2 * i
	}
	probes := 0
	target := 1_234_566
	idx := sort.Search(len(keys), func(i int) bool { probes++; return keys[i] >= target })
	fmt.Printf("found %d at index %d after %d probes (log2 1e6 = %.1f)\n",
		keys[idx], idx, probes, math.Log2(1e6))
}
