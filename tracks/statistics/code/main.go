// Statistics starter kit: center, spread, percentiles, z-scores,
// confidence intervals, regression, EWMA anomalies and a bootstrap.
// Standard library only. The seed is fixed, so the output repeats.
package main

import (
	"fmt"
	"math"
	"math/rand/v2"
	"sort"
)

func mean(x []float64) float64 {
	s := 0.0
	for _, v := range x {
		s += v
	}
	return s / float64(len(x))
}

func median(x []float64) float64 {
	y := append([]float64(nil), x...)
	sort.Float64s(y)
	n := len(y)
	if n%2 == 1 {
		return y[n/2]
	}
	return (y[n/2-1] + y[n/2]) / 2
}

// stdev is the sample standard deviation (divide by n - 1).
func stdev(x []float64) float64 {
	m := mean(x)
	s := 0.0
	for _, v := range x {
		s += (v - m) * (v - m)
	}
	return math.Sqrt(s / float64(len(x)-1))
}

// percentile uses the nearest-rank method: the smallest value with at
// least p% of the data at or below it.
func percentile(x []float64, p float64) float64 {
	y := append([]float64(nil), x...)
	sort.Float64s(y)
	rank := int(math.Ceil(p / 100 * float64(len(y))))
	if rank < 1 {
		rank = 1
	}
	return y[rank-1]
}

func main() {
	lat := []float64{12, 15, 11, 90, 12}
	fmt.Println("== Center ==")
	fmt.Printf("latencies %v\n", lat)
	fmt.Printf("mean %.1f ms, median %.1f ms\n", mean(lat), median(lat))

	fmt.Println("\n== Spread ==")
	a := []float64{48, 49, 50, 51, 52}
	b := []float64{30, 40, 50, 60, 70}
	fmt.Printf("A: mean %.0f, sd %.2f\n", mean(a), stdev(a))
	fmt.Printf("B: mean %.0f, sd %.2f\n", mean(b), stdev(b))

	rng := rand.New(rand.NewPCG(11, 3))
	big := make([]float64, 5000)
	for i := range big {
		big[i] = math.Exp(math.Log(40) + 0.55*rng.NormFloat64()) // log-normal latency
	}
	fmt.Println("\n== Percentiles of 5,000 simulated latencies ==")
	for _, p := range []float64{50, 90, 99, 99.9} {
		fmt.Printf("p%-4g %6.1f ms\n", p, percentile(big, p))
	}
	fmt.Printf("mean  %6.1f ms (pulled up by the tail)\n", mean(big))

	fmt.Println("\n== z-scores (mean 200, sd 20) ==")
	for _, x := range []float64{180, 240, 260} {
		fmt.Printf("%.0f ms -> z = %+.1f\n", x, (x-200)/20)
	}

	fmt.Println("\n== 95% confidence interval ==")
	m, sd, n := 250.0, 30.0, 100.0
	se := sd / math.Sqrt(n)
	fmt.Printf("mean %.0f, sd %.0f, n %.0f -> %.2f to %.2f\n", m, sd, n, m-1.96*se, m+1.96*se)

	fmt.Println("\n== Least squares line ==")
	xs := []float64{1, 2, 3, 4, 5, 6, 7, 8}
	ys := []float64{2.1, 3.9, 5.2, 5.8, 8.1, 8.7, 11.2, 11.6}
	mx, my := mean(xs), mean(ys)
	sxy, sxx, syy := 0.0, 0.0, 0.0
	for i := range xs {
		sxy += (xs[i] - mx) * (ys[i] - my)
		sxx += (xs[i] - mx) * (xs[i] - mx)
		syy += (ys[i] - my) * (ys[i] - my)
	}
	slope := sxy / sxx
	fmt.Printf("y = %.3f + %.3f x, r = %.3f\n", my-slope*mx, slope, sxy/math.Sqrt(sxx*syy))

	fmt.Println("\n== EWMA anomaly detector ==")
	series := []float64{100, 102, 98, 101, 99, 103, 100, 97, 160, 101, 99}
	ew, dev := series[0], 3.0
	for t, v := range series {
		if t > 0 && math.Abs(v-ew) > 4*dev {
			fmt.Printf("t=%d value %.0f vs baseline %.1f: ANOMALY\n", t, v, ew)
			continue // keep the spike out of the baseline
		}
		dev = 0.9*dev + 0.1*math.Abs(v-ew)
		ew = 0.3*v + 0.7*ew
	}

	fmt.Println("\n== Bootstrap interval for p99 ==")
	sample := big[:1000]
	var boots []float64
	for k := 0; k < 2000; k++ {
		re := make([]float64, len(sample))
		for i := range re {
			re[i] = sample[rng.IntN(len(sample))]
		}
		boots = append(boots, percentile(re, 99))
	}
	fmt.Printf("p99 of sample %.1f ms, bootstrap 95%% interval %.1f to %.1f ms\n",
		percentile(sample, 99), percentile(boots, 2.5), percentile(boots, 97.5))
}
