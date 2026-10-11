// Probability starter kit: exact answers next to simulations.
// Standard library only. The seed is fixed, so the output repeats.
package main

import (
	"fmt"
	"math"
	"math/rand/v2"
)

var rng = rand.New(rand.NewPCG(2024, 7))

// montyHall plays the game many times and returns the win rate.
func montyHall(switchDoor bool, trials int) float64 {
	wins := 0
	for i := 0; i < trials; i++ {
		car, pick := rng.IntN(3), rng.IntN(3)
		opened := 0
		for opened == pick || opened == car {
			opened++
		}
		if switchDoor {
			pick = 3 - pick - opened // the one door left
		}
		if pick == car {
			wins++
		}
	}
	return float64(wins) / float64(trials)
}

// birthday returns the exact chance that n people share a birthday.
func birthday(n int) float64 {
	allDiff := 1.0
	for i := 0; i < n; i++ {
		allDiff *= float64(365-i) / 365
	}
	return 1 - allDiff
}

func main() {
	fmt.Println("== Two dice: P(sum = 7) ==")
	count := 0
	for a := 1; a <= 6; a++ {
		for b := 1; b <= 6; b++ {
			if a+b == 7 {
				count++
			}
		}
	}
	fmt.Printf("exact %d/36 = %.4f\n", count, float64(count)/36)

	fmt.Println("\n== Monty Hall, 100,000 games each ==")
	fmt.Printf("stay   %.3f  (exact 1/3)\n", montyHall(false, 100000))
	fmt.Printf("switch %.3f  (exact 2/3)\n", montyHall(true, 100000))

	fmt.Println("\n== Birthday problem ==")
	for _, n := range []int{10, 23, 50} {
		fmt.Printf("%2d people: %.3f\n", n, birthday(n))
	}

	fmt.Println("\n== Bayes: alert fires, is it real? ==")
	pInc, hit, falseAlarm := 0.01, 0.99, 0.05
	pAlert := hit*pInc + falseAlarm*(1-pInc)
	fmt.Printf("P(alert) = %.4f, P(incident | alert) = %.4f\n", pAlert, hit*pInc/pAlert)

	fmt.Println("\n== Redundancy: replicas down with p = 0.01 each ==")
	for k := 1; k <= 3; k++ {
		fmt.Printf("%d replicas all down: %.0e\n", k, math.Pow(0.01, float64(k)))
	}

	fmt.Println("\n== Retries: attempts until success, p(success) = 0.8 ==")
	total, runs := 0, 100000
	for i := 0; i < runs; i++ {
		tries := 1
		for rng.Float64() >= 0.8 {
			tries++
		}
		total += tries
	}
	fmt.Printf("average %.3f attempts (exact 1/0.8 = 1.25)\n", float64(total)/float64(runs))

	fmt.Println("\n== Markov chain UP/DOWN, stepped 200 minutes ==")
	up, down := 1.0, 0.0
	for i := 0; i < 200; i++ {
		up, down = up*0.99+down*0.50, up*0.01+down*0.50
	}
	fmt.Printf("UP %.4f, DOWN %.4f (exact DOWN = 0.01/0.51 = %.4f)\n", up, down, 0.01/0.51)

	fmt.Println("\n== Poisson arrivals at 2 per second for 1 hour ==")
	t, n := 0.0, 0
	for {
		t += rng.ExpFloat64() / 2 // exponential gap with mean 0.5 s
		if t > 3600 {
			break
		}
		n++
	}
	fmt.Printf("%d arrivals (expected 7200, give or take about 85)\n", n)
}
