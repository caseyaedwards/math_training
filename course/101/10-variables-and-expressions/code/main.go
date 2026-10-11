// Variables and expressions: a function is an expression with a named input.
package main

import "fmt"

func main() {
	f := func(x int) int { return 4*(x+3) - 2*x } // before simplifying
	g := func(x int) int { return 2*x + 12 }      // after simplifying

	same := true
	for x := -100; x <= 100; x++ {
		if f(x) != g(x) {
			same = false
		}
	}
	fmt.Println("4(x+3) - 2x == 2x + 12 for x in -100..100:", same)

	h := func(x int) int { return 3 * (x + 1) }
	k := func(x int) int { return 3*x + 1 }
	fmt.Println("3(x+1) vs 3x+1 at x=0:", h(0), "vs", k(0))

	expr := func(x int) int { return 3*x + 2 }
	for x := -2; x <= 2; x++ {
		fmt.Printf("x = %2d  ->  3x + 2 = %2d\n", x, expr(x))
	}

	memory := func(n int) int { return 16*n + 8 }
	fmt.Println("cluster memory, 5 workers:", memory(5), "GB")
	cost := func(g float64) float64 { return 0.10*g + 20 }
	fmt.Printf("storage cost, 500 GB: $%.2f\n", cost(500))
}
