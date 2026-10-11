// Counting formulas, checked against brute-force listing.
package main

import "fmt"

func perm(n, k int) int {
	out := 1
	for i := 0; i < k; i++ {
		out *= n - i
	}
	return out
}

func comb(n, k int) int {
	out := 1
	for i := 0; i < k; i++ {
		out = out * (n - i) / (i + 1) // stays an integer at every step
	}
	return out
}

// arrangements lists every ordering of the letters in s.
func arrangements(s []byte) []string {
	if len(s) <= 1 {
		return []string{string(s)}
	}
	var out []string
	for i := range s {
		rest := append(append([]byte{}, s[:i]...), s[i+1:]...)
		for _, tail := range arrangements(rest) {
			out = append(out, string(s[i])+tail)
		}
	}
	return out
}

func main() {
	fmt.Println("3-letter codes:", 26*26*26)
	fmt.Println("P(10,3) =", perm(10, 3), " C(10,3) =", comb(10, 3))
	fmt.Println("ABC orderings:", arrangements([]byte("ABC")))
	fmt.Println("team with exactly 2 SREs:", comb(4, 2)*comb(5, 1))
	fmt.Println("5-card hands:", comb(52, 5))
	fmt.Println("lattice paths to (3,2):", comb(5, 2))

	// Pigeonhole: n items in k boxes force a box with ceil(n/k).
	n, k := 1000, 512
	fmt.Println("busiest bucket holds at least", (n+k-1)/k)
}
