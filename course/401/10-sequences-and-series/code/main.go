// Partial sums: which series settle down and which run away.
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println("        n    sum 1/2^k    sum 1/k    sum 1/k^2   sum (-1)^(k+1)/k")
	var geo, harm, sq, alt float64
	next := 1
	for k := 1; k <= 1000000; k++ {
		fk := float64(k)
		geo += math.Pow(0.5, fk)
		harm += 1 / fk
		sq += 1 / (fk * fk)
		if k%2 == 1 {
			alt += 1 / fk
		} else {
			alt -= 1 / fk
		}
		if k == next {
			fmt.Printf("%9d  %11.6f  %9.4f  %11.6f  %11.6f\n", k, geo, harm, sq, alt)
			next *= 10
		}
	}
	fmt.Printf("  targets:  %11.6f  %9s  %11.6f  %11.6f\n", 1.0, "none", math.Pi*math.Pi/6, math.Ln2)

	fmt.Println("Exponential backoff, base 1 s, doubling, capped at 30 s:")
	wait, total := 1.0, 0.0
	for retry := 1; retry <= 8; retry++ {
		total += wait
		fmt.Printf("  retry %d after waiting %4.0f s, total %5.0f s\n", retry, wait, total)
		wait = math.Min(wait*2, 30)
	}
}
