// Exponential functions: growth, decay, compounding toward e, and
// the total wait of an exponential backoff.
// Run: go run main.go
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println("Traffic: 1,000 rps growing 20% per month")
	for m := 0; m <= 6; m++ {
		fmt.Printf("  month %d: %8.1f rps\n", m, 1000*math.Pow(1.2, float64(m)))
	}

	fmt.Println("Caffeine: 200 mg, half-life 5 h")
	for _, t := range []float64{0, 5, 10, 12, 24} {
		fmt.Printf("  t=%4.1f h: %6.2f mg\n", t, 200*math.Pow(0.5, t/5))
	}

	fmt.Println("$1 at 100% for one year, compounded n times:")
	for _, n := range []float64{1, 2, 4, 12, 365, 8760, 1e6} {
		fmt.Printf("  n=%-8v %.6f\n", n, math.Pow(1+1/n, n))
	}
	fmt.Printf("  e      = %.6f\n", math.E)

	fmt.Println("Backoff waits 1, 2, 4, ... seconds:")
	total := 0
	for k := 0; k < 6; k++ {
		wait := 1 << k // 2^k using a bit shift
		total += wait
		fmt.Printf("  wait %2d s, total %2d s = 2^%d - 1\n", wait, total, k+1)
	}
}
