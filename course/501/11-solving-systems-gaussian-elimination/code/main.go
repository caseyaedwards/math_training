// Gaussian elimination with exact fractions (math/big.Rat), then back substitution.
package main

import (
	"fmt"
	"math/big"
)

func show(m [][]*big.Rat) {
	for _, row := range m {
		for j, x := range row {
			if j == len(row)-1 {
				fmt.Print(" |")
			}
			fmt.Printf(" %5s", x.RatString())
		}
		fmt.Println()
	}
	fmt.Println()
}

// solve reduces m (n rows, n+1 columns) and returns the solution.
// It assumes exactly one solution exists.
func solve(m [][]*big.Rat) []*big.Rat {
	n := len(m)
	for col := 0; col < n; col++ {
		p := col
		for m[p][col].Sign() == 0 { // find a row with a nonzero pivot
			p++
		}
		m[col], m[p] = m[p], m[col]
		for r := col + 1; r < n; r++ {
			f := new(big.Rat).Quo(m[r][col], m[col][col])
			for c := col; c <= n; c++ {
				m[r][c].Sub(m[r][c], new(big.Rat).Mul(f, m[col][c]))
			}
		}
	}
	show(m)
	x := make([]*big.Rat, n)
	for r := n - 1; r >= 0; r-- { // back substitution, bottom row first
		s := new(big.Rat).Set(m[r][n])
		for c := r + 1; c < n; c++ {
			s.Sub(s, new(big.Rat).Mul(m[r][c], x[c]))
		}
		x[r] = s.Quo(s, m[r][r])
	}
	return x
}

func matrix(rows [][]int64) [][]*big.Rat {
	m := make([][]*big.Rat, len(rows))
	for i, row := range rows {
		for _, v := range row {
			m[i] = append(m[i], big.NewRat(v, 1))
		}
	}
	return m
}

func main() {
	m := matrix([][]int64{{1, 1, 1, 6}, {2, 1, -1, 1}, {1, -1, 2, 5}})
	show(m)
	fmt.Println("x, y, z =", ratStrings(solve(m)))
	fmt.Println("capacity a, b =", ratStrings(solve(matrix([][]int64{{2, 4, 20}, {4, 4, 28}}))))
}

func ratStrings(xs []*big.Rat) []string {
	out := make([]string, len(xs))
	for i, x := range xs {
		out[i] = x.RatString()
	}
	return out
}
