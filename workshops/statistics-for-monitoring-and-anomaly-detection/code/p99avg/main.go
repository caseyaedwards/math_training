// Command p99avg shows why averaging p99 across hosts is wrong, and why
// summing histogram buckets works.
//
// Two hosts serve one service. Host A takes most of the traffic and is fast.
// Host B takes a little traffic and is slow. It prints:
//  1. Each host p99, the plain average of the p99s, the traffic-weighted
//     average, and the true p99 of all requests merged.
//  2. Per-host bucket counts, their sum, and histogram_quantile on the sum.
//
// Run from the workshop folder: go run ./code/p99avg
package main

import (
	"fmt"
	"math"
	"math/rand/v2"
	"slices"
	"strings"
)

const seed = 42

var (
	inf     = math.Inf(1)
	buckets = []float64{25, 50, 100, 200, 400, 800, 1600, 3200, inf}
)

func lognormal(rng *rand.Rand, median, sigma float64, n int) []float64 {
	out := make([]float64, n)
	for i := range out {
		out[i] = math.Exp(math.Log(median) + sigma*rng.NormFloat64())
	}
	return out
}

func hosts() (a, b []float64) {
	rng := rand.New(rand.NewPCG(seed, seed))
	return lognormal(rng, 40, 0.4, 9000), lognormal(rng, 150, 0.6, 1000)
}

func nearestRank(data []float64, p float64) float64 {
	s := slices.Clone(data)
	slices.Sort(s)
	rank := int(math.Max(1, math.Ceil(p/100*float64(len(s)))))
	return s[rank-1]
}

func bucketCounts(data []float64) []int {
	out := make([]int, len(buckets))
	for i, b := range buckets {
		for _, x := range data {
			if x <= b {
				out[i]++
			}
		}
	}
	return out
}

func histogramQuantile(q float64, cum []int, explain bool) float64 {
	total := cum[len(cum)-1]
	rank := q * float64(total)
	i := 0
	for float64(cum[i]) < rank {
		i++
	}
	if math.IsInf(buckets[i], 1) {
		return buckets[len(buckets)-2]
	}
	lower, below := 0.0, 0
	if i > 0 {
		lower, below = buckets[i-1], cum[i-1]
	}
	in := cum[i] - below
	pos := (rank - float64(below)) / float64(in)
	est := lower + (buckets[i]-lower)*pos
	if explain {
		fmt.Printf("   rank      = %g x %d = %.2f\n", q, total, rank)
		fmt.Printf("   bucket    = (%g, %g] holds ranks %d..%d\n", lower, buckets[i], below+1, cum[i])
		fmt.Printf("   position  = (%.2f - %d) / %d = %.4f\n", rank, below, in, pos)
		fmt.Printf("   estimate  = %g + (%g - %g) x %.4f = %.1f ms\n", lower, buckets[i], lower, pos, est)
	}
	return est
}

func bar(ms float64) string { return strings.Repeat("#", int(math.Round(ms/8))) }

func part1(a, b []float64) {
	fmt.Println("1. p99 per host versus the true p99")
	all := append(slices.Clone(a), b...)
	pa, pb, merged := nearestRank(a, 99), nearestRank(b, 99), nearestRank(all, 99)
	plain := (pa + pb) / 2
	weighted := (pa*float64(len(a)) + pb*float64(len(b))) / float64(len(all))
	rows := []struct {
		label string
		v     float64
	}{
		{"host A p99 (9,000 req)", pa},
		{"host B p99 (1,000 req)", pb},
		{"average of p99s", plain},
		{"traffic-weighted avg", weighted},
		{"TRUE merged p99", merged},
	}
	for _, r := range rows {
		fmt.Printf("   %-24s %7.1f ms  %s\n", r.label, r.v, bar(r.v))
	}
	fmt.Printf("   average of p99s is off by %+.1f ms (%+.0f%%)\n", plain-merged, (plain/merged-1)*100)
	fmt.Printf("   weighted average is off by %+.1f ms (%+.0f%%)\n", weighted-merged, (weighted/merged-1)*100)
	above, fromB := 0, 0
	for _, x := range a {
		if x > merged {
			above++
		}
	}
	for _, x := range b {
		if x > merged {
			above++
			fromB++
		}
	}
	fmt.Printf("   requests above the true p99: %.2f%%, of which %d come from host B\n",
		float64(above)/float64(len(all))*100, fromB)
	fmt.Printf("   host B p90 = %.1f ms\n\n", nearestRank(b, 90))
}

func part2(a, b []float64) {
	fmt.Println("2. Sum the buckets, then take the quantile")
	ca, cb := bucketCounts(a), bucketCounts(b)
	total := make([]int, len(ca))
	fmt.Printf("   %-6s%8s%8s%8s\n", "le", "host A", "host B", "sum")
	for i := range ca {
		total[i] = ca[i] + cb[i]
		l := "+Inf"
		if !math.IsInf(buckets[i], 1) {
			l = fmt.Sprintf("%g", buckets[i])
		}
		fmt.Printf("   %-6s%8d%8d%8d\n", l, ca[i], cb[i], total[i])
	}
	fmt.Println()
	est := histogramQuantile(0.99, total, true)
	estA, estB := histogramQuantile(0.99, ca, false), histogramQuantile(0.99, cb, false)
	fmt.Printf("   histogram_quantile on summed buckets: %.1f ms\n", est)
	fmt.Printf("   average of per-host estimates:        %.1f ms\n", (estA+estB)/2)
	fmt.Printf("   exact merged p99:                     %.1f ms\n\n", nearestRank(append(slices.Clone(a), b...), 99))
}

func main() {
	a, b := hosts()
	part1(a, b)
	part2(a, b)
}
