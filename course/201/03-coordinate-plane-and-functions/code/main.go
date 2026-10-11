// A map is a function with a finite domain: each key has exactly one value.
package main

import "fmt"

type pair struct{ x, y int }

// isFunction reports whether no input appears with two different outputs.
func isFunction(pairs []pair) bool {
	seen := map[int]int{}
	for _, p := range pairs {
		if y, ok := seen[p.x]; ok && y != p.y {
			return false
		}
		seen[p.x] = p.y
	}
	return true
}

func quadrant(x, y int) string {
	switch {
	case x == 0 || y == 0:
		return "on an axis"
	case x > 0 && y > 0:
		return "I"
	case x < 0 && y > 0:
		return "II"
	case x < 0 && y < 0:
		return "III"
	default:
		return "IV"
	}
}

func main() {
	f := func(x int) int { return 2*x + 1 }
	for x := -3; x <= 3; x++ {
		fmt.Printf("f(%d) = %d\n", x, f(x))
	}
	fmt.Println("{(1,2),(2,3),(1,5)} is a function:", isFunction([]pair{{1, 2}, {2, 3}, {1, 5}}))
	fmt.Println("{(1,4),(2,4),(3,4)} is a function:", isFunction([]pair{{1, 4}, {2, 4}, {3, 4}}))
	for _, p := range []pair{{3, 2}, {-4, 1}, {-2, -3}, {4, -2}, {0, 3}} {
		fmt.Printf("(%d, %d) -> %s\n", p.x, p.y, quadrant(p.x, p.y))
	}
}
