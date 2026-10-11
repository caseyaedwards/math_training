// Decimals and percents: floats, exact decimals, and error budgets.
package main

import (
	"fmt"
	"math/big"
)

func main() {
	// Constants in Go are exact, so 0.1 + 0.2 prints 0.3.
	fmt.Println("constants: ", 0.1+0.2)
	// float64 variables are binary and cannot hold 0.1 exactly.
	a, b := 0.1, 0.2
	fmt.Println("variables: ", a+b)

	x, _ := new(big.Rat).SetString("0.1")
	y, _ := new(big.Rat).SetString("0.2")
	fmt.Println("big.Rat:   ", new(big.Rat).Add(x, y).FloatString(1))

	fmt.Printf("3/8 = %.3f = %.1f%%\n", 3.0/8, 3.0/8*100)
	fmt.Println("15% of 80 =", 0.15*80)

	change := func(old, new float64) float64 { return (new - old) / old * 100 }
	fmt.Printf("200 -> 250 ms: %+.0f%%\n", change(200, 250))
	fmt.Printf("250 -> 200 ms: %+.0f%%\n", change(250, 200))

	minutes := 30.0 * 24 * 60
	for _, slo := range []float64{99.9, 99.95, 99.99} {
		fmt.Printf("SLO %.2f%%: budget %.1f min per 30 days\n", slo, (100-slo)/100*minutes)
	}
}
