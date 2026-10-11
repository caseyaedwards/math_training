// Trust, but verify: sweep many inputs and compare the
// original inequality with the solved form.
package main

import "fmt"

func main() {
	original := func(x float64) bool { return -2*x+1 < 5 }
	solved := func(x float64) bool { return x > -2 }

	mismatches := 0
	for tenth := -50; tenth <= 50; tenth++ {
		x := float64(tenth) / 10
		if original(x) != solved(x) {
			mismatches++
			fmt.Println("mismatch at", x)
		}
	}
	fmt.Println("checked 101 points from -5 to 5, mismatches:", mismatches)

	// The latency budget: 30 + 0.2x <= 200.
	// Work in tenths of a millisecond to stay in whole numbers.
	maxReq := 0
	for x := 0; x <= 2000; x++ {
		if 300+2*x <= 2000 {
			maxReq = x
		}
	}
	fmt.Println("largest concurrency inside the SLO:", maxReq)
}
