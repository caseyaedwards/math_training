// Command fourier builds Fourier intuition in plain Go: square waves, a
// naive DFT, seasonality in a metric, and aliasing.
//
// It prints:
//  1. A square wave built from odd sine harmonics: partial sums with 1, 3, 5,
//     and 25 terms, as numbers and as ASCII plots.
//  2. A naive discrete Fourier transform (DFT) that finds 440, 660, and
//     1,320 Hz hidden in a noisy mixed signal.
//  3. Seasonality: an hourly metric over 14 days with daily and weekly cycles.
//  4. Aliasing: a 60 s periodic job scraped every 50 s looks like a 300 s cycle.
//
// Standard library only. No arguments. Seeded: rand.NewPCG(42, 42).
// Run: go run ./code/fourier
package main

import (
	"fmt"
	"math"
	"math/cmplx"
	"math/rand/v2"
	"sort"
	"strings"
)

// squarePartial returns (4/pi) * sum of sin((2k-1)x)/(2k-1) for k = 1..terms.
func squarePartial(x float64, terms int) float64 {
	sum := 0.0
	for k := 1; k <= terms; k++ {
		h := float64(2*k - 1)
		sum += math.Sin(h*x) / h
	}
	return 4 / math.Pi * sum
}

// dftAmplitudes is a naive O(N^2) DFT. It returns |X[k]| * 2 / N for
// k = 0..N/2, which equals the amplitude of a sine at bin k.
func dftAmplitudes(x []float64) []float64 {
	n := len(x)
	out := make([]float64, n/2+1)
	for k := range out {
		var total complex128
		for t, v := range x {
			angle := -2 * math.Pi * float64(k) * float64(t) / float64(n)
			total += complex(v, 0) * cmplx.Exp(complex(0, angle))
		}
		out[k] = cmplx.Abs(total) * 2 / float64(n)
	}
	return out
}

// ranked returns bin indices from start upward, sorted by amplitude, largest first.
func ranked(amp []float64, start int) []int {
	idx := []int{}
	for k := start; k < len(amp); k++ {
		idx = append(idx, k)
	}
	sort.Slice(idx, func(i, j int) bool { return amp[idx[i]] > amp[idx[j]] })
	return idx
}

// asciiCurve plots values in a small text grid from +1.4 down to -1.4.
func asciiCurve(values []float64) {
	const height, lo, hi = 11, -1.4, 1.4
	rows := make([][]byte, height)
	for r := range rows {
		rows[r] = []byte(strings.Repeat(" ", len(values)))
	}
	for c, v := range values {
		r := int(math.Round((hi - v) / (hi - lo) * (height - 1)))
		r = max(0, min(height-1, r))
		rows[r][c] = '*'
	}
	zero := int(math.Round(hi / (hi - lo) * (height - 1)))
	for r, row := range rows {
		if r == zero {
			for c := range row {
				if row[c] == ' ' {
					row[c] = '-'
				}
			}
		}
		label := fmt.Sprintf("%+5.2f", hi-float64(r)*(hi-lo)/(height-1))
		fmt.Println(strings.TrimRight(fmt.Sprintf("  %s |%s", label, row), " "))
	}
}

func section(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 66))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 66))
}

func comma(n int) string {
	s := fmt.Sprint(n)
	var b strings.Builder
	for i, c := range s {
		if i > 0 && (len(s)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(c)
	}
	return b.String()
}

func main() {
	rng := rand.New(rand.NewPCG(42, 42))

	section("1. Square wave = sum of odd harmonics")
	fmt.Println("f_K(x) = (4/pi) * [sin x + sin 3x / 3 + sin 5x / 5 + ...], K terms")
	xs := []float64{math.Pi / 2, math.Pi / 4, math.Pi / 10, math.Pi / 40}
	fmt.Printf("%6s%12s%12s%12s%12s\n", "terms", "x=pi/2", "x=pi/4", "x=pi/10", "x=pi/40")
	for _, terms := range []int{1, 3, 5, 25, 250} {
		fmt.Printf("%6d", terms)
		for _, x := range xs {
			fmt.Printf("%12.4f", squarePartial(x, terms))
		}
		fmt.Println()
	}
	fmt.Printf("%6s%12.4f%12.4f%12.4f%12.4f\n", "target", 1.0, 1.0, 1.0, 1.0)
	for _, terms := range []int{1, 3, 5, 25} {
		fmt.Println()
		fmt.Printf("  %d term(s), x from 0 to 2*pi:\n", terms)
		vals := make([]float64, 65)
		for c := range vals {
			vals[c] = squarePartial(2*math.Pi*float64(c)/64, terms)
		}
		asciiCurve(vals)
	}
	peak := 0.0
	for c := 1; c < 1000; c++ {
		peak = math.Max(peak, squarePartial(math.Pi*float64(c)/2000, 25))
	}
	fmt.Printf("\n  overshoot near the jump with 25 terms: max = %.4f (Gibbs: about 9%% of the jump size 2)\n", peak)

	section("2. Naive DFT finds the notes in a mixed signal")
	rate, n := 8000, 800
	fmt.Printf("sample rate %s Hz, N = %d samples (%d ms), bin width %d Hz, Nyquist %s Hz\n",
		comma(rate), n, n*1000/rate, rate/n, comma(rate/2))
	fmt.Println("signal = 1.0 sin(2 pi 440 t) + 0.5 sin(2 pi 660 t) + 0.3 sin(2 pi 1320 t) + noise(0.2)")
	samples := make([]float64, n)
	for t := range samples {
		ts := float64(t) / float64(rate)
		samples[t] = math.Sin(2*math.Pi*440*ts) + 0.5*math.Sin(2*math.Pi*660*ts) +
			0.3*math.Sin(2*math.Pi*1320*ts) + 0.2*rng.NormFloat64()
	}
	amp := dftAmplitudes(samples)
	order := ranked(amp, 0)
	top := append([]int{}, order[:3]...)
	sort.Ints(top)
	fmt.Println("strongest three bins:")
	for _, k := range top {
		fmt.Printf("  bin %3d  %7s Hz  amplitude %.3f\n", k, comma(k*rate/n), amp[k])
	}
	k := order[3]
	fmt.Printf("largest remaining bin (noise): bin %d, %s Hz, amplitude %.3f\n", k, comma(k*rate/n), amp[k])
	fmt.Println("spectrum 0 to 1,500 Hz in 50 Hz groups (# = 0.05 amplitude):")
	const group = 5 // bins per row
	for start := 0; start < 150; start += group {
		m := 0.0
		for _, a := range amp[start : start+group] {
			m = math.Max(m, a)
		}
		line := fmt.Sprintf("  %5d-%-5d Hz %s", start*rate/n, (start+group)*rate/n-1,
			strings.Repeat("#", int(math.Round(m/0.05))))
		fmt.Println(strings.TrimRight(line, " "))
	}

	section("3. Seasonality in a metric: hourly samples over 14 days")
	hours := 24 * 14
	metric := make([]float64, hours)
	for h := range metric {
		fh := float64(h)
		metric[h] = 1000 + 300*math.Sin(2*math.Pi*fh/24) + 150*math.Sin(2*math.Pi*fh/168) + 60*rng.NormFloat64()
	}
	amp = dftAmplitudes(metric)
	order = ranked(amp, 1)
	fmt.Printf("N = %d hourly points; bin k means k cycles per %d hours\n", hours, hours)
	fmt.Printf("bin 0 (the mean level): %.1f\n", amp[0]/2)
	top = append([]int{}, order[:2]...)
	sort.Ints(top)
	for _, k := range top {
		fmt.Printf("  bin %3d  period %6.1f h  amplitude %6.1f\n", k, float64(hours)/float64(k), amp[k])
	}
	k = order[2]
	fmt.Printf("largest remaining bin (noise): bin %d, period %.1f h, amplitude %.1f\n",
		k, float64(hours)/float64(k), amp[k])

	section("4. Aliasing: a 60 s job scraped every 50 s")
	fmt.Println("true signal cos(2 pi t / 60), sampled at t = 0, 50, 100, ...")
	fmt.Printf("%6s%12s%17s\n", "t s", "true value", "cos(2 pi t/300)")
	for i := 0; i < 8; i++ {
		t := 50 * float64(i)
		fmt.Printf("%6.0f%12.3f%17.3f\n", t, math.Cos(2*math.Pi*t/60), math.Cos(2*math.Pi*t/300))
	}
	fTrue, fS := 1.0/60, 1.0/50
	alias := math.Abs(fTrue - fS)
	fmt.Printf("sample rate %.4f Hz, Nyquist %.4f Hz < signal %.4f Hz\n", fS, fS/2, fTrue)
	fmt.Printf("alias frequency |1/60 - 1/50| = %.5f Hz -> period %.0f s\n", alias, 1/alias)
}
