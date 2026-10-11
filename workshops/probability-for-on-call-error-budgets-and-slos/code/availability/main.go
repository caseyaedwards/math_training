// Command availability compares series and parallel availability formulas
// with a seeded simulation.
//
// It prints:
//  1. Series availability (every component needed): the product.
//  2. Parallel availability (any one replica is enough).
//  3. A simulation of N flaky replicas that checks the formula.
//  4. A correlated-failure case: replicas that share one availability zone.
//  5. The chance of at least one page in a week (complement rule), checked
//     by simulation.
//
// Run from the workshop folder: go run ./code/availability
package main

import (
	"fmt"
	"math"
	"math/rand/v2"
	"strings"
)

const seed = 42

func newRNG() *rand.Rand { return rand.New(rand.NewPCG(seed, seed)) }

// series: all components must be up, so multiply availabilities.
func series(avail ...float64) float64 {
	out := 1.0
	for _, a := range avail {
		out *= a
	}
	return out
}

// parallel: any one component is enough, so 1 - product of failure chances.
func parallel(avail ...float64) float64 {
	down := 1.0
	for _, a := range avail {
		down *= 1 - a
	}
	return 1 - down
}

// comma formats an integer with thousands separators.
func comma(n int64) string {
	s := fmt.Sprintf("%d", n)
	var b strings.Builder
	for i, c := range s {
		if i > 0 && (len(s)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(c)
	}
	return b.String()
}

func part1() {
	fmt.Println("1. Series: load balancer -> app -> database")
	lb, app, db := 0.9999, 0.999, 0.9995
	t := series(lb, app, db)
	fmt.Printf("   %g x %g x %g = %.6f  (%.4f%%)\n", lb, app, db, t, t*100)
	fmt.Println("   The chain is worse than its weakest link (99.9%).")
	fmt.Println()
}

func part2() {
	fmt.Println("2. Parallel: N replicas, each up 99% of the time")
	for n := 1; n <= 5; n++ {
		reps := make([]float64, n)
		for i := range reps {
			reps[i] = 0.99
		}
		t := parallel(reps...)
		fmt.Printf("   N=%d  1 - 0.01^%d = %.10f   down %10.4f min/yr\n", n, n, t, (1-t)*365*24*60)
	}
	fmt.Println()
}

func part3(trials int) {
	fmt.Printf("3. Simulation: replicas each down 5%% of minutes, %s minutes, seed %d\n", comma(int64(trials)), seed)
	rng := newRNG()
	q := 0.05
	allDown := map[int]int{1: 0, 2: 0, 3: 0}
	for i := 0; i < trials; i++ {
		d1 := rng.Float64() < q
		d2 := rng.Float64() < q
		d3 := rng.Float64() < q
		if d1 {
			allDown[1]++
			if d2 {
				allDown[2]++
				if d3 {
					allDown[3]++
				}
			}
		}
	}
	fmt.Printf("   %2s  %10s  %10s  %14s\n", "N", "formula", "simulated", "outage minutes")
	for n := 1; n <= 3; n++ {
		formula := 1 - math.Pow(q, float64(n))
		sim := 1 - float64(allDown[n])/float64(trials)
		fmt.Printf("   %2d  %10.6f  %10.6f  %14s\n", n, formula, sim, comma(int64(allDown[n])))
	}
	fmt.Println()
}

func part4(trials int) {
	fmt.Println("4. Correlated failure: two replicas in one availability zone")
	fmt.Println("   zone down 1% of minutes (takes both out), each replica also down 5% on its own")
	rng := newRNG()
	zoneQ, nodeQ := 0.01, 0.05
	marginal := (1 - zoneQ) * (1 - nodeQ)
	naive := parallel(marginal, marginal)
	truth := (1 - zoneQ) * parallel(1-nodeQ, 1-nodeQ)
	down := 0
	for i := 0; i < trials; i++ {
		zone := rng.Float64() < zoneQ
		n1 := rng.Float64() < nodeQ
		n2 := rng.Float64() < nodeQ
		if zone || (n1 && n2) {
			down++
		}
	}
	fmt.Printf("   one replica alone        = 0.99 x 0.95          = %.6f\n", marginal)
	fmt.Printf("   naive independent pair   = 1 - (1 - %.4f)^2   = %.6f\n", marginal, naive)
	fmt.Printf("   true pair (zone x pair)  = 0.99 x (1 - 0.05^2)  = %.6f\n", truth)
	fmt.Printf("   %-24s = %-20s = %.6f\n", "simulated pair", comma(int64(trials))+" minutes", 1-float64(down)/float64(trials))
	fmt.Printf("   naive downtime %.4f%%  vs true %.4f%%  (%.1fx worse)\n",
		(1-naive)*100, (1-truth)*100, (1-truth)/(1-naive))
	fmt.Println()
}

func part5(weeks int) {
	fmt.Println("5. Chance of at least one page in a week (168 hours)")
	const hours = 168
	for _, p := range []float64{0.001, 0.005, 0.01, 0.02} {
		fmt.Printf("   p per hour %-6g -> 1 - (1 - p)^168 = %.4f\n", p, 1-math.Pow(1-p, hours))
	}
	p := 0.01
	rng := newRNG()
	paged := 0
	for w := 0; w < weeks; w++ {
		for h := 0; h < hours; h++ {
			if rng.Float64() < p {
				paged++
				break
			}
		}
	}
	fmt.Printf("   simulation, p = %g, %s weeks: %.4f\n", p, comma(int64(weeks)), float64(paged)/float64(weeks))
	fmt.Println()
}

func main() {
	part1()
	part2()
	part3(1_000_000)
	part4(1_000_000)
	part5(20_000)
}
