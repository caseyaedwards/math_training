// Indian and Chinese methods in Go: Sulba root 2, Sunzi remainders,
// fangcheng elimination, Zu Chongzhi fractions, and Madhava's series.
// Run: go run main.go
package main

import (
	"fmt"
	"math"
	"math/big"
)

// sunzi searches upward for the smallest x that leaves the given
// remainders. Brute force, like trying every key until one fits.
func sunzi(mods, rems []int) int {
	for x := 1; ; x++ {
		ok := true
		for i, m := range mods {
			if x%m != rems[i] {
				ok = false
				break
			}
		}
		if ok {
			return x
		}
	}
}

// fangcheng solves a 3x3 system the Nine Chapters way: clear a column by
// multiplying a row by the pivot and subtracting, so every entry stays a
// whole number. Fractions appear only at the very end.
func fangcheng(m [3][4]int64) [3]*big.Rat {
	for i := 0; i < 3; i++ {
		for j := i + 1; j < 3; j++ {
			p, q := m[i][i], m[j][i]
			for k := 0; k < 4; k++ {
				m[j][k] = p*m[j][k] - q*m[i][k]
			}
		}
	}
	fmt.Println("  board after elimination (whole numbers only):")
	for _, row := range m {
		fmt.Printf("    %4d %4d %4d | %4d\n", row[0], row[1], row[2], row[3])
	}
	var x [3]*big.Rat
	for i := 2; i >= 0; i-- {
		sum := big.NewRat(m[i][3], 1)
		for k := i + 1; k < 3; k++ {
			t := new(big.Rat).Mul(big.NewRat(m[i][k], 1), x[k])
			sum.Sub(sum, t)
		}
		x[i] = sum.Quo(sum, big.NewRat(m[i][i], 1))
	}
	return x
}

// madhava returns 4 times the first n terms of 1 - 1/3 + 1/5 - ...,
// and the same sum with his end correction (p/2)/(p*p+1), p = 2n.
func madhava(n int) (plain, corrected float64) {
	s, sign := 0.0, 1.0
	for k := 0; k < n; k++ {
		s += sign / float64(2*k+1)
		sign = -sign
	}
	p := float64(2 * n)
	return 4 * s, 4 * (s + sign*(p/2)/(p*p+1))
}

func main() {
	fmt.Println("Sulba Sutras: 1 + 1/3 + 1/(3*4) - 1/(3*4*34)")
	r := 1 + 1.0/3 + 1.0/12 - 1.0/408
	fmt.Printf("  %.7f vs root 2 = %.7f, error %.1e\n\n", r, math.Sqrt2, r-math.Sqrt2)

	fmt.Println("Sunzi: remainder 2 by 3, 3 by 5, 2 by 7")
	x := sunzi([]int{3, 5, 7}, []int{2, 3, 2})
	fmt.Printf("  smallest answer %d, then every 105 more: %d, %d\n\n", x, x+105, x+210)

	fmt.Println("Nine Chapters 8.1: grain bundles (top, medium, low)")
	sol := fangcheng([3][4]int64{{3, 2, 1, 39}, {2, 3, 1, 34}, {1, 2, 3, 26}})
	for i, name := range []string{"top", "medium", "low"} {
		f, _ := sol[i].Float64()
		fmt.Printf("  %-6s = %-5s dou = %.2f\n", name, sol[i].RatString(), f)
	}
	fmt.Println()

	fmt.Println("Pi as a fraction: value and error")
	for _, fr := range []struct {
		who  string
		n, d float64
	}{{"Aryabhata 62832/20000", 62832, 20000},
		{"Zu Chongzhi 22/7", 22, 7}, {"Zu Chongzhi 355/113", 355, 113}} {
		v := fr.n / fr.d
		fmt.Printf("  %-22s %.7f  error %+.1e\n", fr.who, v, v-math.Pi)
	}
	fmt.Println()

	fmt.Println("Madhava: n terms, plain and with his end correction")
	for _, n := range []int{1, 2, 5, 10, 16, 50} {
		p, c := madhava(n)
		fmt.Printf("  n=%2d  plain %.9f (error %+.1e)  corrected %.9f (error %+.1e)\n",
			n, p, p-math.Pi, c, c-math.Pi)
	}
}
