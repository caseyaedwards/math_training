// Command main replays three methods from medieval and Renaissance
// Europe: Fibonacci's rabbits, lattice (gelosia) multiplication, and
// Cardano's formula for a cubic, plus Bombelli's complex-number check.
package main

import (
	"fmt"
	"math"
	"math/big"
	"math/cmplx"
	"strings"
)

// rabbits simulates the puzzle month by month. Each month every adult
// pair breeds one young pair, and last month's young pairs grow up.
func rabbits(young, adult, months int) {
	for m := 1; m <= months; m++ {
		fmt.Printf("  month %2d: %3d young + %3d adult = %3d total\n",
			m, young, adult, young+adult)
		young, adult = adult, adult+young
	}
}

// lattice multiplies two digit strings with the gelosia grid and
// returns the product as a string. Cell (i, j) holds the two-digit
// product of digit i of a and digit j of b. Diagonals are summed
// from the bottom right, carrying left.
func lattice(a, b string) string {
	n, m := len(a), len(b)
	diag := make([]int, n+m) // diag[k] collects one place value
	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			p := int(a[i]-'0') * int(b[j]-'0')
			// place value of the units half of this cell
			k := (n - 1 - i) + (m - 1 - j)
			diag[k] += p % 10
			diag[k+1] += p / 10
		}
	}
	carry := 0
	digits := make([]byte, n+m)
	for k := 0; k < n+m; k++ {
		s := diag[k] + carry
		digits[n+m-1-k] = byte('0' + s%10)
		carry = s / 10
	}
	out := strings.TrimLeft(string(digits), "0")
	if out == "" {
		return "0"
	}
	return out
}

func main() {
	fmt.Println("== Fibonacci's rabbits, modern start (one young pair) ==")
	rabbits(1, 0, 8)
	fmt.Println("== Liber Abaci start (one adult pair): start, then each month-end ==")
	young, adult := 0, 1
	counts := []int{adult}
	for m := 1; m <= 12; m++ {
		young, adult = adult, adult+young
		counts = append(counts, young+adult)
	}
	fmt.Println(" ", counts)
	fmt.Println("== Ratios of neighbors ==")
	a, b := 1, 1
	for i := 0; i < 10; i++ {
		fmt.Printf("  %3d/%-3d = %.6f\n", b, a, float64(b)/float64(a))
		a, b = b, a+b
	}
	fmt.Printf("  phi     = %.6f\n", (1+math.Sqrt(5))/2)

	fmt.Println("== Lattice multiplication ==")
	pairs := [][2]string{{"47", "36"}, {"1202", "349"}, {"987654321", "123456789"}}
	for _, p := range pairs {
		x, _ := new(big.Int).SetString(p[0], 10)
		y, _ := new(big.Int).SetString(p[1], 10)
		want := new(big.Int).Mul(x, y).String()
		got := lattice(p[0], p[1])
		fmt.Printf("  %s x %s = %s (check: %v)\n", p[0], p[1], got, got == want)
	}

	fmt.Println("== Cardano: x^3 + 6x = 20 ==")
	p, q := 6.0, 20.0
	r := math.Sqrt(q*q/4 + p*p*p/27) // sqrt(100 + 8) = sqrt(108)
	x := math.Cbrt(r+q/2) - math.Cbrt(r-q/2)
	fmt.Printf("  sqrt(108) = %.6f\n", r)
	fmt.Printf("  cbrt(%.6f) - cbrt(%.6f) = %.12f\n", r+q/2, r-q/2, x)
	fmt.Printf("  check: x^3 + 6x = %.12f\n", x*x*x+6*x)

	fmt.Println("== Bombelli: x^3 = 15x + 4 ==")
	u := cmplx.Pow(complex(2, 11), 1.0/3) // principal cube root of 2 + 11i
	v := cmplx.Pow(complex(2, -11), 1.0/3)
	fmt.Printf("  cube root of 2+11i = %.6f\n", u)
	fmt.Printf("  sum of the two cube roots = %.6f\n", u+v)
}
