// Command percentiles compares mean, median, and percentiles on a skewed
// latency sample, and reproduces the Prometheus histogram_quantile estimate.
//
// It prints:
//  1. Summary statistics for 1,000 seeded lognormal latencies plus five outliers.
//  2. A text-mode histogram of the sample.
//  3. How one slow request moves the mean but not the median.
//  4. Prometheus-style cumulative buckets and the histogram_quantile estimate,
//     with the linear interpolation shown step by step.
//  5. How the bucket layout changes the p99 estimate.
//
// Run from the workshop folder: go run ./code/percentiles
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
	outliers = []float64{1200, 1800, 2500, 4000, 6000}
	inf      = math.Inf(1)
	buckets  = []float64{25, 50, 100, 200, 400, 800, 1600, 3200, inf}
)

// latencies returns 1,000 lognormal latencies in ms (median near 80 ms)
// followed by five slow outliers.
func latencies() []float64 {
	rng := rand.New(rand.NewPCG(seed, seed))
	data := make([]float64, 0, 1005)
	for i := 0; i < 1000; i++ {
		data = append(data, math.Exp(math.Log(80)+0.6*rng.NormFloat64()))
	}
	return append(data, outliers...)
}

// nearestRank returns the value at rank ceil(p/100 * n), counting from 1.
func nearestRank(data []float64, p float64) float64 {
	s := slices.Clone(data)
	slices.Sort(s)
	rank := int(math.Max(1, math.Ceil(p/100*float64(len(s)))))
	return s[rank-1]
}

func mean(data []float64) float64 {
	sum := 0.0
	for _, x := range data {
		sum += x
	}
	return sum / float64(len(data))
}

// bucketCounts returns cumulative counts per upper bound, like Prometheus le buckets.
func bucketCounts(data, bounds []float64) []int {
	out := make([]int, len(bounds))
	for i, b := range bounds {
		for _, x := range data {
			if x <= b {
				out[i]++
			}
		}
	}
	return out
}

// histogramQuantile follows Prometheus: find the bucket, interpolate linearly.
func histogramQuantile(q float64, bounds []float64, cum []int, explain bool) float64 {
	total := cum[len(cum)-1]
	rank := q * float64(total)
	i := 0
	for float64(cum[i]) < rank {
		i++
	}
	if math.IsInf(bounds[i], 1) {
		return bounds[len(bounds)-2] // the highest finite bound
	}
	lower, below := 0.0, 0
	if i > 0 {
		lower, below = bounds[i-1], cum[i-1]
	}
	in := cum[i] - below
	pos := (rank - float64(below)) / float64(in)
	est := lower + (bounds[i]-lower)*pos
	if explain {
		fmt.Printf("   rank      = %g x %d = %.2f\n", q, total, rank)
		fmt.Printf("   bucket    = (%g, %g] holds ranks %d..%d\n", lower, bounds[i], below+1, cum[i])
		fmt.Printf("   position  = (%.2f - %d) / %d = %.4f\n", rank, below, in, pos)
		fmt.Printf("   estimate  = %g + (%g - %g) x %.4f = %.1f ms\n", lower, bounds[i], lower, pos, est)
	}
	return est
}

func label(b float64) string {
	if math.IsInf(b, 1) {
		return "+Inf"
	}
	return fmt.Sprintf("%g", b)
}

func part1(data []float64) {
	fmt.Printf("1. Summary of 1,005 latencies (ms), seed %d\n", seed)
	fmt.Printf("   mean   %8.1f\n", mean(data))
	for _, p := range []float64{50, 90, 95, 99, 99.9} {
		fmt.Printf("   p%-5g %8.1f\n", p, nearestRank(data, p))
	}
	fmt.Printf("   max    %8.1f\n", slices.Max(data))
	fmt.Printf("   mean without the 5 outliers: %.1f\n\n", mean(data[:1000]))
}

func part2(data []float64) {
	fmt.Println("2. Histogram, 25 ms bins (each # = 5 requests)")
	for lo := 0.0; lo < 400; lo += 25 {
		n := 0
		for _, x := range data {
			if x >= lo && x < lo+25 {
				n++
			}
		}
		fmt.Printf("   %4g-%-4g %4d %s\n", lo, lo+25, n, strings.Repeat("#", int(math.Round(float64(n)/5))))
	}
	n := 0
	for _, x := range data {
		if x >= 400 {
			n++
		}
	}
	fmt.Printf("   400+      %4d %s\n\n", n, strings.Repeat("#", int(math.Round(float64(n)/5))))
}

func part3(data []float64) {
	fmt.Println("3. One slow request")
	first := slices.Clone(data[:100])
	slow := append(slices.Clone(first), 30000)
	fmt.Printf("   100 requests:               mean %7.1f  median %6.1f\n", mean(first), nearestRank(first, 50))
	fmt.Printf("   plus one 30,000 ms timeout: mean %7.1f  median %6.1f\n", mean(slow), nearestRank(slow, 50))
	fmt.Printf("   mean moves by %.1f ms = (30,000 - %.1f) / 101\n", mean(slow)-mean(first), mean(first))
	fmt.Printf("   median moves by %.1f ms\n\n", nearestRank(slow, 50)-nearestRank(first, 50))
}

func part4(data []float64) {
	fmt.Println("4. Prometheus histogram and histogram_quantile")
	cum := bucketCounts(data, buckets)
	for i, b := range buckets {
		fmt.Printf("   le=%-5s cumulative %5d\n", label(b), cum[i])
	}
	fmt.Println()
	fmt.Println("   p99 by linear interpolation:")
	histogramQuantile(0.99, buckets, cum, true)
	fmt.Println()
	fmt.Printf("   %5s  %18s  %18s\n", "q", "histogram_quantile", "exact nearest-rank")
	for _, q := range []float64{0.5, 0.9, 0.99} {
		fmt.Printf("   %5g  %15.1f ms  %15.1f ms\n", q,
			histogramQuantile(q, buckets, cum, false), nearestRank(data, q*100))
	}
	fmt.Println()
}

func part5(data []float64) {
	fmt.Printf("5. Bucket choice and the p99 estimate (exact p99 = %.1f ms)\n", nearestRank(data, 99))
	var expo, linear []float64
	for k := 0; k < 30; k++ {
		expo = append(expo, math.Round(10*math.Pow(1.25, float64(k))*10)/10)
	}
	for b := 50.0; b <= 1000; b += 50 {
		linear = append(linear, b)
	}
	layouts := []struct {
		name   string
		bounds []float64
	}{
		{"coarse 100/500/1000", []float64{100, 500, 1000, inf}},
		{"doubling 25..3200", buckets},
		{"x1.25 from 10 ms", append(expo, inf)},
		{"linear 50 ms steps", append(linear, inf)},
	}
	for _, l := range layouts {
		est := histogramQuantile(0.99, l.bounds, bucketCounts(data, l.bounds), false)
		fmt.Printf("   %-22s %3d buckets  p99 ~ %6.1f ms\n", l.name, len(l.bounds), est)
	}
	fmt.Println()
}

func main() {
	d := latencies()
	part1(d)
	part2(d)
	part3(d)
	part4(d)
	part5(d)
}
