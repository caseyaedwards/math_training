// Mean and variance of a distribution given as value -> probability.
package main

import (
	"fmt"
	"math"
	"math/big"
)

type outcome struct {
	value int64
	prob  *big.Rat
}

func meanVar(pmf []outcome) (*big.Rat, *big.Rat) {
	mu, sq := new(big.Rat), new(big.Rat)
	for _, o := range pmf {
		x := new(big.Rat).SetInt64(o.value)
		mu.Add(mu, new(big.Rat).Mul(x, o.prob))
		sq.Add(sq, new(big.Rat).Mul(new(big.Rat).Mul(x, x), o.prob))
	}
	variance := new(big.Rat).Sub(sq, new(big.Rat).Mul(mu, mu)) // E[X^2] - mu^2
	return mu, variance
}

func main() {
	var die, low, high, latency []outcome
	for k := int64(1); k <= 6; k++ {
		die = append(die, outcome{k, big.NewRat(1, 6)})
	}
	for _, v := range []int64{4, 5, 6} {
		low = append(low, outcome{v, big.NewRat(1, 3)})
	}
	for _, v := range []int64{1, 5, 9} {
		high = append(high, outcome{v, big.NewRat(1, 3)})
	}
	latency = []outcome{{20, big.NewRat(9, 10)}, {200, big.NewRat(1, 10)}}

	for _, c := range []struct {
		name string
		pmf  []outcome
	}{{"one die", die}, {"{4,5,6}", low}, {"{1,5,9}", high}, {"latency ms", latency}} {
		mu, v := meanVar(c.pmf)
		vf, _ := v.Float64()
		fmt.Printf("%-10s mean %-4s variance %-5s sd %.3f\n", c.name, mu.RatString(), v.RatString(), math.Sqrt(vf))
	}
}
