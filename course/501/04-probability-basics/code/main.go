// Exact probability by counting cells, then a seeded simulation to compare.
package main

import (
	"fmt"
	"math/big"
	"math/rand/v2"
)

func main() {
	hits, sevens := 0, 0
	for a := 1; a <= 6; a++ {
		for b := 1; b <= 6; b++ {
			if a == 6 || b == 6 {
				hits++
			}
			if a+b == 7 {
				sevens++
			}
		}
	}
	fmt.Println("P(sum = 7)          =", big.NewRat(int64(sevens), 36))
	exact := big.NewRat(int64(hits), 36)
	f, _ := exact.Float64()
	fmt.Printf("P(at least one six) = %s = %.4f\n", exact, f)

	r := rand.New(rand.NewPCG(1, 2)) // fixed seed: same output every run
	trials, sim := 100000, 0
	for i := 0; i < trials; i++ {
		if r.IntN(6) == 5 || r.IntN(6) == 5 { // IntN(6) gives 0..5, and 5 means a six
			sim++
		}
	}
	fmt.Printf("simulated           = %.4f\n", float64(sim)/float64(trials))

	fmt.Printf("series 0.999*0.999  = %.6f\n", 0.999*0.999)
	fmt.Printf("3 replicas parallel = %.6f\n", 1-0.01*0.01*0.01)
}
