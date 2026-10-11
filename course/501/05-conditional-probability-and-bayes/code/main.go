// Bayes' rule with exact fractions and with floats.
package main

import (
	"fmt"
	"math/big"
)

// bayes returns P(H | E) from the prior P(H), P(E | H) and P(E | not H).
func bayes(prior, eGivenH, eGivenNot *big.Rat) *big.Rat {
	one := big.NewRat(1, 1)
	jointH := new(big.Rat).Mul(prior, eGivenH)
	jointNot := new(big.Rat).Mul(new(big.Rat).Sub(one, prior), eGivenNot)
	total := new(big.Rat).Add(jointH, jointNot)
	return new(big.Rat).Quo(jointH, total)
}

func main() {
	r := big.NewRat
	fmt.Println("deploy alert:      P(bad | alert) =", bayes(r(1, 10), r(9, 10), r(2, 10)))
	fmt.Println("fewer false fires: P(bad | alert) =", bayes(r(1, 10), r(9, 10), r(5, 100)))

	slo, _ := bayes(r(1, 100), r(95, 100), r(5, 100)).Float64()
	fmt.Printf("rare SLO burn:     P(real | alert) = %.3f\n", slo)

	// Odds form, two independent alerts: odds 1:9 times 4.5 times 4.5.
	odds := 1.0 / 9.0 * 4.5 * 4.5
	fmt.Printf("two alerts:        P(bad | both)   = %.4f\n", odds/(1+odds))
}
