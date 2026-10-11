// Ratios, proportions and rates.
package main

import (
	"fmt"
	"math"
	"math/big"
)

// solve returns x in a/b = x/d, exactly.
func solve(a, b, d int64) *big.Rat {
	return new(big.Rat).Mul(big.NewRat(a, b), big.NewRat(d, 1))
}

// split divides total in the ratio p : q.
func split(total, p, q int) (int, int) {
	part := total / (p + q)
	return p * part, q * part
}

func main() {
	fmt.Println("5/8 = x/40  ->  x =", solve(5, 8, 40).RatString())
	fmt.Println("14/21 = x/9 ->  x =", solve(14, 21, 9).RatString())

	web, db := split(25, 3, 2)
	fmt.Println("25 hosts at 3:2 ->", web, "web,", db, "db")

	fmt.Println("unit rate:", 1800/15, "req/s")
	fmt.Println("6 GB/min =", 6.0*1000/60, "MB/s")
	fmt.Println("90 km/h =", 90.0*1000/3600, "m/s")

	perPod := 0.75 * 250
	pods := 4000 / perPod
	fmt.Printf("pods needed: %.2f -> round up to %.0f\n", pods, math.Ceil(pods))
}
