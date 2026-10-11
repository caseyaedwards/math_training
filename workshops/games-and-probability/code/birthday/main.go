// Command birthday covers the birthday problem: exact formula,
// simulation, and hash collisions.
//
// Prints:
//
//  1. Exact P(at least one shared birthday) for groups of size n,
//     with an ASCII bar chart
//  2. The smallest group with P >= 50% (the famous 23)
//  3. A seeded simulation that checks the formula
//  4. Hash collisions: the same math for a b-bit hash, with the
//     square-root rule of thumb and a 16-bit simulation
//
// Run from the workshop folder: go run ./code/birthday
package main

import (
	"fmt"
	"math"
	"math/rand/v2"
	"sort"
	"strings"
)

const (
	seed   = 42
	days   = 365
	trials = 20_000
)

func banner(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 62))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 62))
}

// pShared is the exact probability that at least two of n items share a slot of d.
func pShared(n, d int) float64 {
	pDistinct := 1.0
	for k := 0; k < n; k++ {
		pDistinct *= float64(d-k) / float64(d)
	}
	return 1 - pDistinct
}

func comma(n int64) string {
	s := fmt.Sprint(n)
	var b strings.Builder
	for i, ch := range s {
		if i > 0 && (len(s)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(ch)
	}
	return b.String()
}

func exactTable() {
	banner("1. Exact: P(shared) = 1 - (365/365)(364/365)...((365-n+1)/365)")
	for _, n := range []int{5, 10, 15, 20, 23, 30, 40, 50, 57, 70} {
		p := pShared(n, days)
		fmt.Printf("  n = %2d: %.4f  %s\n", n, p, strings.Repeat("#", int(math.Round(p*50))))
	}
}

func threshold() {
	banner("2. Smallest group with at least a 50% chance")
	n := 1
	for pShared(n, days) < 0.5 {
		n++
	}
	fmt.Printf("  n = %d: %.4f\n", n-1, pShared(n-1, days))
	fmt.Printf("  n = %d: %.4f  <- first n at or above 0.5\n", n, pShared(n, days))
	fmt.Printf("  pairs among %d people: C(%d,2) = %d\n", n, n, n*(n-1)/2)
	fmt.Printf("  approximation 1 - exp(-n(n-1)/(2*365)) = %.4f\n",
		1-math.Exp(-float64(n*(n-1))/(2*days)))
}

func simulate() {
	banner(fmt.Sprintf("3. Simulation: %s random groups per n, seed %d", comma(trials), seed))
	rng := rand.New(rand.NewPCG(seed, 0))
	fmt.Printf("  %3s %10s %8s\n", "n", "simulated", "exact")
	for _, n := range []int{10, 23, 30, 50} {
		hits := 0
		for t := 0; t < trials; t++ {
			var seen [days]bool
			for i := 0; i < n; i++ {
				d := rng.IntN(days)
				if seen[d] {
					hits++
					break
				}
				seen[d] = true
			}
		}
		fmt.Printf("  %3d %10.4f %8.4f\n", n, float64(hits)/trials, pShared(n, days))
	}
}

func hashCollisions() {
	banner("4. Hash collisions: the birthday problem with 2^b slots")
	fmt.Println("  keys for a 50% collision chance ~ 1.1774 * sqrt(2^b)")
	for _, b := range []int{16, 32, 64, 128} {
		n50 := 1.1774 * math.Sqrt(math.Pow(2, float64(b)))
		shown := fmt.Sprintf("%.2e", n50)
		if n50 < 1e12 {
			shown = comma(int64(math.Round(n50)))
		}
		fmt.Printf("  %3d-bit hash: about %s keys\n", b, shown)
	}
	fmt.Println()
	rng := rand.New(rand.NewPCG(seed, 0))
	const slots = 1 << 16
	const runs = 2_000
	firsts := make([]int, 0, runs)
	for r := 0; r < runs; r++ {
		seen := map[int]bool{}
		for {
			v := rng.IntN(slots)
			if seen[v] {
				firsts = append(firsts, len(seen)+1)
				break
			}
			seen[v] = true
		}
	}
	sum := 0
	for _, f := range firsts {
		sum += f
	}
	sort.Ints(firsts)
	fmt.Printf("  16-bit simulation, %s runs: keys inserted until the first collision\n", comma(runs))
	fmt.Printf("    mean   = %.1f   (theory sqrt(pi/2 * 2^16) = %.1f)\n",
		float64(sum)/runs, math.Sqrt(math.Pi/2*slots))
	fmt.Printf("    median = %d     (theory about 1.1774 * 256 = %.0f)\n", firsts[runs/2], 1.1774*256)
	fmt.Printf("    exact P(collision) with 302 keys in 2^16 slots = %.4f\n", pShared(302, slots))
}

func main() {
	exactTable()
	threshold()
	simulate()
	hashCollisions()
}
