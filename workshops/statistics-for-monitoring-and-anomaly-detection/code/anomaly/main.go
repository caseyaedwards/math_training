// Command anomaly covers variance, z-scores, EWMA bands, and the median
// absolute deviation (MAD) for anomaly detection.
//
// It prints:
//  1. Variance and standard deviation by hand for five latencies.
//  2. The 3-sigma rule on normal data versus skewed (lognormal) data.
//  3. Masking: two big outliers inflate the standard deviation and hide
//     from the z-score, while the MAD-based score catches them.
//  4. An EWMA plus EWM-variance band on a seeded time series with a spike
//     at t = 100 and a level shift at t = 150, listing which points alert.
//  5. A rolling median and MAD detector on the same series.
//
// Run from the workshop folder: go run ./code/anomaly
// Optional: go run ./code/anomaly -csv prints t,x,ewma,sd,alert rows only.
package main

import (
	"flag"
	"fmt"
	"math"
	"math/rand/v2"
	"slices"
	"strings"
)

const (
	seed   = 42
	alpha  = 0.1
	k      = 3.0 // band width in standard deviations
	warmup = 30  // points used to seed the EWMA, never alerted on
)

func newRNG() *rand.Rand { return rand.New(rand.NewPCG(seed, seed)) }

func mean(xs []float64) float64 {
	s := 0.0
	for _, x := range xs {
		s += x
	}
	return s / float64(len(xs))
}

// pvar is the population variance: mean squared distance from the mean.
func pvar(xs []float64) float64 {
	m, s := mean(xs), 0.0
	for _, x := range xs {
		s += (x - m) * (x - m)
	}
	return s / float64(len(xs))
}

func median(xs []float64) float64 {
	s := slices.Clone(xs)
	slices.Sort(s)
	n := len(s)
	if n%2 == 1 {
		return s[n/2]
	}
	return (s[n/2-1] + s[n/2]) / 2
}

// mad returns the median and the median absolute deviation.
func mad(xs []float64) (float64, float64) {
	med := median(xs)
	dev := make([]float64, len(xs))
	for i, x := range xs {
		dev[i] = math.Abs(x - med)
	}
	return med, median(dev)
}

// robustZ is the modified z-score of Iglewicz and Hoaglin.
func robustZ(x, med, m float64) float64 { return 0.6745 * (x - med) / m }

// series: 200 points around 100 with noise sd 4, a spike at 100, a shift at 150.
func series() []float64 {
	rng := newRNG()
	out := make([]float64, 200)
	for t := range out {
		x := 100 + 4*rng.NormFloat64()
		if t == 100 {
			x += 40
		}
		if t >= 150 {
			x += 25
		}
		out[t] = x
	}
	return out
}

type row struct {
	t           int
	x, mean, sd float64
	alert       bool
}

// ewmaBand checks each point against the band from the previous step, then updates.
func ewmaBand(xs []float64) []row {
	m, v := mean(xs[:warmup]), pvar(xs[:warmup])
	var rows []row
	for t := warmup; t < len(xs); t++ {
		x := xs[t]
		sd := math.Sqrt(v)
		rows = append(rows, row{t, x, m, sd, math.Abs(x-m) > k*sd})
		diff := x - m // update after the check
		incr := alpha * diff
		m += incr
		v = (1 - alpha) * (v + diff*incr)
	}
	return rows
}

func part1() {
	fmt.Println("1. Variance and standard deviation by hand")
	xs := []float64{12, 15, 11, 14, 18}
	mu := mean(xs)
	fmt.Printf("   data  %v   mean = 70 / 5 = %g\n", xs, mu)
	fmt.Printf("   %4s %9s %8s\n", "x", "x - mean", "squared")
	ss := 0.0
	for _, x := range xs {
		fmt.Printf("   %4g %9g %8g\n", x, x-mu, (x-mu)*(x-mu))
		ss += (x - mu) * (x - mu)
	}
	n := float64(len(xs))
	fmt.Printf("   sum of squares = %g\n", ss)
	fmt.Printf("   population variance = %g / %g = %g   sd = %.3f\n", ss, n, ss/n, math.Sqrt(ss/n))
	fmt.Printf("   sample variance     = %g / %g = %g   sd = %.3f\n\n", ss, n-1, ss/(n-1), math.Sqrt(ss/(n-1)))
}

func part2(n int) {
	fmt.Printf("2. The 3-sigma rule on %d,%03d points\n", n/1000, n%1000)
	rng := newRNG()
	normal := make([]float64, n)
	skewed := make([]float64, n)
	for i := range normal {
		normal[i] = 100 + 20*rng.NormFloat64()
	}
	for i := range skewed {
		skewed[i] = math.Exp(math.Log(80) + 0.6*rng.NormFloat64())
	}
	for _, c := range []struct {
		name string
		xs   []float64
	}{{"normal", normal}, {"lognormal", skewed}} {
		mu, sd := mean(c.xs), math.Sqrt(pvar(c.xs))
		hi, lo := 0, 0
		for _, x := range c.xs {
			if x > mu+k*sd {
				hi++
			}
			if x < mu-k*sd {
				lo++
			}
		}
		fmt.Printf("   %-10s mean %6.1f  sd %5.1f  band [%6.1f, %6.1f]  above %.3f%%  below %.3f%%\n",
			c.name, mu, sd, mu-k*sd, mu+k*sd, float64(hi)/float64(n)*100, float64(lo)/float64(n)*100)
	}
	fmt.Println("   normal theory: 0.135% above and 0.135% below")
	fmt.Println()
}

func part3() {
	fmt.Println("3. Masking: outliers inflate the sd and hide from the z-score")
	xs := []float64{100, 102, 98, 101, 99, 103, 97, 100, 500, 520}
	mu, sd := mean(xs), math.Sqrt(pvar(xs))
	med, m := mad(xs)
	fmt.Printf("   data   %v\n", xs)
	fmt.Printf("   mean %.1f  sd %.1f   median %g  MAD %g\n", mu, sd, med, m)
	fmt.Printf("   %5s %7s %9s\n", "x", "z", "robust z")
	for _, x := range xs {
		z, rz := (x-mu)/sd, robustZ(x, med, m)
		flag := ""
		if math.Abs(z) > 3 {
			flag += "z>3 "
		}
		if math.Abs(rz) > 3.5 {
			flag += "rz>3.5"
		}
		fmt.Printf("   %5g %7.2f %9.1f  %s\n", x, z, rz, flag)
	}
	fmt.Println()
}

func part4(xs []float64) {
	fmt.Printf("4. EWMA band: alpha %g, band = mean +/- %g sd, warm-up %d points\n", alpha, k, warmup)
	rows := ewmaBand(xs)
	var alerts []int
	show := map[int]bool{}
	for _, r := range rows {
		if r.alert {
			alerts = append(alerts, r.t)
			show[r.t] = true
		}
	}
	for t := 98; t < 104; t++ {
		show[t] = true
	}
	for t := 148; t < 158; t++ {
		show[t] = true
	}
	fmt.Printf("   alerts at t = %v\n\n", alerts)
	fmt.Printf("   %4s %7s %7s %7s %7s\n", "t", "x", "ewma", "low", "high")
	last := -1
	for _, r := range rows {
		if !show[r.t] {
			continue
		}
		if last >= 0 && r.t != last+1 {
			fmt.Println("    ...")
		}
		mark := ""
		if r.alert {
			mark = "  ALERT"
		}
		fmt.Printf("   %4d %7.1f %7.1f %7.1f %7.1f%s\n", r.t, r.x, r.mean, r.mean-k*r.sd, r.mean+k*r.sd, mark)
		last = r.t
	}
	fmt.Println()
	fmt.Println("   text plot, one row per 5 points: # bar = highest value in the row,")
	fmt.Println("   | = ewma at the end of the row, ! = an alert in the row, each char = 2 units from 80")
	pos := func(v float64) int { return max(0, min(39, int(math.Round((v-80)/2)))) }
	for start := warmup; start < 200; start += 5 {
		chunk := rows[start-warmup : start-warmup+5]
		hi, flag := chunk[0].x, " "
		for _, r := range chunk {
			hi = math.Max(hi, r.x)
			if r.alert {
				flag = "!"
			}
		}
		line := []byte(strings.Repeat(" ", 40))
		for i := 0; i <= pos(hi); i++ {
			line[i] = '#'
		}
		line[pos(chunk[4].mean)] = '|'
		fmt.Printf("   t %3d %s %s %6.1f\n", start, flag, line, hi)
	}
	fmt.Println()
}

func part5(xs []float64) {
	const window, cut = 30, 3.5
	fmt.Printf("5. Rolling median and MAD: window %d, alert when |robust z| > %g\n", window, cut)
	var hits []int
	for t := window; t < len(xs); t++ {
		med, m := mad(xs[t-window : t])
		if math.Abs(robustZ(xs[t], med, m)) > cut {
			hits = append(hits, t)
		}
	}
	fmt.Printf("   alerts at t = %v\n\n", hits)
}

func main() {
	csv := flag.Bool("csv", false, "print t,x,ewma,sd,alert rows for the EWMA band and exit")
	flag.Parse()
	data := series()
	if *csv {
		for _, r := range ewmaBand(data) {
			fmt.Printf("%d,%.4f,%.4f,%.4f,%t\n", r.t, r.x, r.mean, r.sd, r.alert)
		}
		return
	}
	part1()
	part2(100_000)
	part3()
	part4(data)
	part5(data)
}
