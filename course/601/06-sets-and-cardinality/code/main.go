// List the positive rationals by diagonals, then beat a list of strings with the diagonal flip.
package main

import "fmt"

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func main() {
	var out []string
	for s := 2; len(out) < 15; s++ { // s = p + q, one diagonal at a time
		for p := 1; p < s && len(out) < 15; p++ {
			q := s - p
			if gcd(p, q) == 1 { // skip repeats like 2/4
				out = append(out, fmt.Sprintf("%d/%d", p, q))
			}
		}
	}
	fmt.Println("first 15 rationals:", out)

	rows := []string{"0110100", "1011001", "0001110", "1110010", "0100111", "1010101", "0011000"}
	flip := make([]byte, len(rows))
	for i, r := range rows {
		if r[i] == '0' {
			flip[i] = '1'
		} else {
			flip[i] = '0'
		}
	}
	fmt.Println("flipped diagonal:", string(flip))
	for i, r := range rows {
		fmt.Printf("  differs from row %d at place %d: %c vs %c\n", i+1, i+1, flip[i], r[i])
	}
}
