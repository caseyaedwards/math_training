// Babylonian square roots in base 60, Egyptian doubling, and Egyptian
// unit fractions: a small lab for Chapter 02.
// Run: go run main.go
package main

import (
	"fmt"
	"math/big"
	"strings"
)

// sexagesimal writes a positive fraction in base 60 as "whole;d1,d2,...",
// keeping `places` digits after the semicolon (cut off, not rounded).
func sexagesimal(x *big.Rat, places int) string {
	num := new(big.Int).Set(x.Num())
	den := x.Denom()
	whole, rem := new(big.Int).QuoRem(num, den, new(big.Int))
	var parts []string
	sixty := big.NewInt(60)
	for i := 0; i < places; i++ {
		rem.Mul(rem, sixty)
		d := new(big.Int)
		d.QuoRem(rem, den, rem)
		parts = append(parts, d.String())
	}
	return whole.String() + ";" + strings.Join(parts, ",")
}

// fromSexagesimal turns base-60 digits (whole part first) into a fraction.
func fromSexagesimal(digits ...int64) *big.Rat {
	sum := new(big.Rat)
	scale := big.NewRat(1, 1)
	for _, d := range digits {
		sum.Add(sum, new(big.Rat).Mul(big.NewRat(d, 1), scale))
		scale.Quo(scale, big.NewRat(60, 1))
	}
	return sum
}

// egyptianMultiply multiplies a by b using only doubling and adding,
// and prints the scribe's table with a backslash on the rows used.
func egyptianMultiply(a, b int) int {
	count, value, total := 1, b, 0
	type row struct{ count, value int }
	var rows []row
	for count <= a {
		rows = append(rows, row{count, value})
		count, value = count*2, value*2
	}
	left := a
	marked := make([]bool, len(rows))
	for i := len(rows) - 1; i >= 0; i-- {
		if rows[i].count <= left {
			left -= rows[i].count
			total += rows[i].value
			marked[i] = true
		}
	}
	for i, r := range rows {
		mark := " "
		if marked[i] {
			mark = "\\"
		}
		fmt.Printf("  %s %4d %6d\n", mark, r.count, r.value)
	}
	return total
}

// greedy splits num/den into distinct unit fractions by always taking
// the largest unit fraction that still fits.
func greedy(num, den int64) []string {
	x := big.NewRat(num, den)
	var out []string
	for x.Sign() > 0 {
		n := new(big.Int).Set(x.Num())
		d := new(big.Int).Set(x.Denom())
		// smallest n' with 1/n' <= x is ceil(d/n)
		q, r := new(big.Int).QuoRem(d, n, new(big.Int))
		if r.Sign() != 0 {
			q.Add(q, big.NewInt(1))
		}
		out = append(out, "1/"+q.String())
		x.Sub(x, new(big.Rat).SetFrac(big.NewInt(1), q))
	}
	return out
}

func main() {
	fmt.Println("Square root of 2 by averaging (start with a 1 by 2 rectangle):")
	two := big.NewRat(2, 1)
	side := big.NewRat(1, 1)
	for step := 1; step <= 4; step++ {
		other := new(big.Rat).Quo(two, side)
		side = new(big.Rat).Add(side, other)
		side.Quo(side, big.NewRat(2, 1))
		f, _ := side.Float64()
		fmt.Printf("  step %d: %-14s = %-17s = %.9f\n", step, side.RatString(), sexagesimal(side, 4), f)
	}

	ybc := fromSexagesimal(1, 24, 51, 10)
	yf, _ := ybc.Float64()
	fmt.Println()
	fmt.Printf("YBC 7289 value 1;24,51,10 = %.9f\n", yf)
	fmt.Printf("its square                = %.9f\n", yf*yf)
	diag := new(big.Rat).Mul(big.NewRat(30, 1), ybc)
	fmt.Printf("30 x 1;24,51,10           = %s\n", sexagesimal(diag, 3))

	fmt.Println()
	fmt.Println("Egyptian multiplication 13 x 24:")
	fmt.Println("  total =", egyptianMultiply(13, 24))

	fmt.Println()
	fmt.Println("Greedy unit fractions:")
	for _, p := range [][2]int64{{2, 5}, {2, 7}, {2, 13}, {3, 7}, {5, 6}} {
		fmt.Printf("  %d/%d = %s\n", p[0], p[1], strings.Join(greedy(p[0], p[1]), " + "))
	}
}
