// Discrete math toolkit: check an induction formula, solve recurrences
// (Towers of Hanoi, Fibonacci), count binary search steps, and find
// an Euler path condition on a small graph.
// Run with: go run main.go
package main

import (
	"fmt"
	"math"
)

// hanoi returns the number of moves to shift n disks, using the recurrence
// T(n) = 2T(n-1) + 1 with T(0) = 0.
func hanoi(n int) int {
	if n == 0 {
		return 0
	}
	return 2*hanoi(n-1) + 1
}

func main() {
	// 1. Induction claim: 1 + 2 + ... + n = n(n+1)/2. Check n = 1..1000.
	sum, ok := 0, true
	for n := 1; n <= 1000; n++ {
		sum += n
		if sum != n*(n+1)/2 {
			ok = false
		}
	}
	fmt.Println("sum formula holds for n = 1..1000:", ok, "| sum to 100 =", 100*101/2)

	// 2. Recurrence vs closed form for Hanoi: T(n) = 2^n - 1.
	for _, n := range []int{1, 2, 3, 5, 10} {
		fmt.Printf("hanoi(%d) = %d, 2^%d - 1 = %d\n", n, hanoi(n), n, (1<<n)-1)
	}

	// 3. Fibonacci by iteration vs Binet's closed form.
	phi := (1 + math.Sqrt(5)) / 2
	a, b := 0, 1
	for n := 0; n <= 30; n++ {
		if n%10 == 0 {
			binet := math.Round(math.Pow(phi, float64(n)) / math.Sqrt(5))
			fmt.Printf("F(%d) = %d, Binet = %.0f\n", n, a, binet)
		}
		a, b = b, a+b
	}

	// 4. Worst-case binary search comparisons: smallest k with 2^k >= n + 1.
	for _, n := range []int{1000, 1000000, 1000000000} {
		k := 0
		for (1 << k) < n+1 {
			k++
		}
		fmt.Printf("binary search over %d items: at most %d comparisons\n", n, k)
	}

	// 5. Handshake lemma and Euler paths on the Konigsberg bridge multigraph.
	// Land masses A, B, C, D; seven bridges as edges.
	edges := [][2]string{{"A", "B"}, {"A", "B"}, {"A", "C"}, {"A", "C"}, {"A", "D"}, {"B", "D"}, {"C", "D"}}
	deg := map[string]int{}
	for _, e := range edges {
		deg[e[0]]++
		deg[e[1]]++
	}
	total, odd := 0, 0
	for _, v := range []string{"A", "B", "C", "D"} {
		total += deg[v]
		if deg[v]%2 == 1 {
			odd++
		}
	}
	fmt.Printf("Konigsberg degrees %v, sum %d = 2 x %d edges, odd vertices %d\n", deg, total, len(edges), odd)
	fmt.Println("Euler walk over every bridge exists:", odd == 0 || odd == 2)
}
