// queue-sim covers Little's law and the M/M/1 queue: formulas, a latency
// table, and a simulation.
//
// Service rate mu = 100 requests per second (mean service time 10 ms).
// The simulation is a seeded discrete-event loop with two event types:
// arrival and departure. It integrates the number in system over time to
// measure L directly, and records the time in system of each request to
// measure W.
//
// Run from the workshop folder: go run ./code/queue-sim
package main

import (
	"fmt"
	"math"
	"math/rand"
	"strings"
)

const mu = 100.0 // requests per second one server completes

func littlesLaw() {
	fmt.Println("=== Little's law: L = lambda * W ===")
	cases := []struct {
		name string
		lam  string
		l    float64
		w    float64
	}{
		{"requests in flight at an API", "200", 200, 0.250},
		{"busy worker threads", "1,200", 1200, 0.080},
	}
	for _, k := range cases {
		fmt.Printf("%-30s lambda = %5s req/s, W = %4.0f ms -> L = %g\n", k.name, k.lam, k.w*1000, math.Round(k.l*k.w*1e9)/1e9)
	}
	fmt.Println()
}

func mm1Table() {
	fmt.Printf("=== M/M/1 formulas with mu = %g req/s ===\n", mu)
	fmt.Printf("%5s %7s %8s %8s %6s  W bar (1 # = 20 ms)\n", "rho", "lambda", "W (ms)", "Wq (ms)", "L")
	for _, rho := range []float64{0.5, 0.8, 0.9, 0.95, 0.99} {
		lam := rho * mu
		w := 1 / (mu - lam)
		wq := rho / (mu - lam)
		l := rho / (1 - rho)
		bar := strings.Repeat("#", int(math.Round(w*1000/20)))
		fmt.Printf("%5.2f %7g %8.0f %8.0f %6.0f  %s\n", rho, math.Round(lam*1e9)/1e9, w*1000, wq*1000, l, bar)
	}
	fmt.Println()
}

// simulate runs a single-server FIFO queue until n requests finish.
// It returns the mean time in system, the time-average number in system,
// and the simulated clock at the end.
func simulate(lam, mu float64, n int, rng *rand.Rand) (meanW, avgL, clockEnd float64) {
	exp := func(rate float64) float64 { return rng.ExpFloat64() / rate }
	clock := 0.0
	nextArrival := exp(lam)
	nextDeparture := math.Inf(1)
	var waiting []float64 // arrival times of requests in system; front is in service
	area := 0.0           // integral of N(t) dt
	totalW := 0.0
	done := 0
	for done < n {
		t := math.Min(nextArrival, nextDeparture)
		area += float64(len(waiting)) * (t - clock)
		clock = t
		if nextArrival <= nextDeparture {
			waiting = append(waiting, clock)
			if len(waiting) == 1 {
				nextDeparture = clock + exp(mu)
			}
			nextArrival = clock + exp(lam)
		} else {
			arrived := waiting[0]
			waiting = waiting[1:]
			totalW += clock - arrived
			done++
			if len(waiting) > 0 {
				nextDeparture = clock + exp(mu)
			} else {
				nextDeparture = math.Inf(1)
			}
		}
	}
	return totalW / float64(done), area / clock, clock
}

func main() {
	littlesLaw()
	mm1Table()
	rng := rand.New(rand.NewSource(42))
	n := 200000
	fmt.Println("=== Discrete-event simulation, 200,000 requests per run, seed 42 ===")
	fmt.Printf("%5s %10s %8s %10s %7s %13s\n", "rho", "W formula", "W sim", "L formula", "L sim", "lambda*W sim")
	for _, rho := range []float64{0.5, 0.8, 0.9} {
		lam := rho * mu
		wSim, lSim, tEnd := simulate(lam, mu, n, rng)
		lamObs := float64(n) / tEnd
		fmt.Printf("%5.2f %8.1fms %6.1fms %10.2f %7.2f %13.2f\n",
			rho, 1000/(mu-lam), wSim*1000, rho/(1-rho), lSim, lamObs*wSim)
	}
}
