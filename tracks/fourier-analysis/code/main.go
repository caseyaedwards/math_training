// Fourier analysis starter kit: square wave coefficients and the Gibbs
// overshoot, a DFT by hand, a radix-2 FFT, seasonality in a request-rate
// metric, convolution, a low-pass filter, aliasing, a Haar wavelet, and
// compression by keeping the largest coefficients.
// Standard library only.
package main

import (
	"fmt"
	"math"
	"math/cmplx"
	"math/rand/v2"
	"sort"
)

// dft is the direct O(N^2) discrete Fourier transform.
func dft(x []complex128) []complex128 {
	n := len(x)
	out := make([]complex128, n)
	for k := 0; k < n; k++ {
		var s complex128
		for t := 0; t < n; t++ {
			angle := -2 * math.Pi * float64(k*t) / float64(n)
			s += x[t] * cmplx.Rect(1, angle)
		}
		out[k] = s
	}
	return out
}

// fft is the recursive radix-2 Cooley-Tukey FFT. len(x) must be a power of 2.
func fft(x []complex128) []complex128 {
	n := len(x)
	if n == 1 {
		return []complex128{x[0]}
	}
	even := make([]complex128, n/2)
	odd := make([]complex128, n/2)
	for i := 0; i < n/2; i++ {
		even[i] = x[2*i]
		odd[i] = x[2*i+1]
	}
	e, o := fft(even), fft(odd)
	out := make([]complex128, n)
	for k := 0; k < n/2; k++ {
		tw := cmplx.Rect(1, -2*math.Pi*float64(k)/float64(n)) * o[k]
		out[k] = e[k] + tw
		out[k+n/2] = e[k] - tw
	}
	return out
}

// idft inverts dft.
func idft(x []complex128) []complex128 {
	n := len(x)
	out := make([]complex128, n)
	for t := 0; t < n; t++ {
		var s complex128
		for k := 0; k < n; k++ {
			s += x[k] * cmplx.Rect(1, 2*math.Pi*float64(k*t)/float64(n))
		}
		out[t] = s / complex(float64(n), 0)
	}
	return out
}

// tidy turns tiny rounding noise such as -0.0000 into a plain 0.
func tidy(v float64) float64 {
	if math.Abs(v) < 5e-5 {
		return 0
	}
	return v
}

func toComplex(x []float64) []complex128 {
	c := make([]complex128, len(x))
	for i, v := range x {
		c[i] = complex(v, 0)
	}
	return c
}

func square(t float64) float64 {
	if math.Mod(t, 2*math.Pi) < math.Pi {
		return 1
	}
	return -1
}

func squarePartial(t float64, terms int) float64 {
	s := 0.0
	for k := 0; k < terms; k++ {
		n := float64(2*k + 1)
		s += 4 / (math.Pi * n) * math.Sin(n*t)
	}
	return s
}

func main() {
	fmt.Println("== Square wave: sine coefficients b_n ==")
	for n := 1; n <= 7; n++ {
		const m = 100000
		s := 0.0
		for i := 0; i < m; i++ {
			t := (float64(i) + 0.5) * 2 * math.Pi / m
			s += square(t) * math.Sin(float64(n)*t)
		}
		bn := s * (2 * math.Pi / m) / math.Pi
		exact := 0.0
		if n%2 == 1 {
			exact = 4 / (math.Pi * float64(n))
		}
		fmt.Printf("b%d = %.4f   exact %.4f\n", n, tidy(bn), exact)
	}

	fmt.Println()
	fmt.Println("== Partial sums and the Gibbs overshoot ==")
	for _, terms := range []int{1, 3, 10, 50, 200} {
		peak := 0.0
		for i := 1; i < 20000; i++ {
			v := squarePartial(math.Pi*float64(i)/20000, terms)
			if v > peak {
				peak = v
			}
		}
		fmt.Printf("%3d odd terms: peak %.4f (target 1)\n", terms, peak)
	}

	fmt.Println()
	fmt.Println("== DFT of [1, 0, -1, 0] by hand ==")
	X := dft(toComplex([]float64{1, 0, -1, 0}))
	for k, v := range X {
		fmt.Printf("X[%d] = %+.1f %+.1fi\n", k, tidy(real(v)), tidy(imag(v)))
	}

	fmt.Println()
	fmt.Println("== FFT agrees with the direct DFT ==")
	rng := rand.New(rand.NewPCG(7, 11))
	sig := make([]float64, 1024)
	for i := range sig {
		sig[i] = rng.NormFloat64()
	}
	a, b := dft(toComplex(sig)), fft(toComplex(sig))
	maxDiff := 0.0
	for i := range a {
		maxDiff = math.Max(maxDiff, cmplx.Abs(a[i]-b[i]))
	}
	fmt.Printf("N = 1024, largest difference %.1e\n", maxDiff)
	for _, n := range []int{1024, 1 << 20} {
		lg := math.Log2(float64(n))
		fmt.Printf("N = %7d: direct N^2 = %.2e steps, FFT N log2 N = %.2e steps, %6.0fx fewer\n",
			n, float64(n)*float64(n), float64(n)*lg, float64(n)/lg)
	}

	fmt.Println()
	fmt.Println("== Seasonality: 4 weeks of hourly request rates ==")
	const hours = 4 * 7 * 24
	rate := make([]float64, hours)
	for t := range rate {
		ft := float64(t)
		rate[t] = 1000 + 300*math.Sin(2*math.Pi*ft/24) + 100*math.Sin(2*math.Pi*ft/168) + 50*rng.NormFloat64()
	}
	R := dft(toComplex(rate))
	type peak struct {
		k   int
		amp float64
	}
	var peaks []peak
	for k := 1; k < hours/2; k++ {
		peaks = append(peaks, peak{k, 2 * cmplx.Abs(R[k]) / hours})
	}
	sort.Slice(peaks, func(i, j int) bool { return peaks[i].amp > peaks[j].amp })
	fmt.Printf("mean level %.1f requests per hour\n", real(R[0])/hours)
	for _, p := range peaks[:3] {
		fmt.Printf("bin %3d: period %6.1f hours, amplitude %6.1f\n", p.k, float64(hours)/float64(p.k), p.amp)
	}

	fmt.Println()
	fmt.Println("== Compression: keep only the largest coefficients ==")
	energy := 0.0
	for _, v := range rate {
		energy += (v - real(R[0])/hours) * (v - real(R[0])/hours)
	}
	for _, keep := range []int{1, 2, 10, 50} {
		kept := make([]complex128, hours)
		kept[0] = R[0]
		for _, p := range peaks[:keep] {
			kept[p.k] = R[p.k]
			kept[hours-p.k] = R[hours-p.k]
		}
		back := idft(kept)
		errSq := 0.0
		for i := range rate {
			d := rate[i] - real(back[i])
			errSq += d * d
		}
		fmt.Printf("keep %2d of %d frequencies: %5.1f%% of the variation explained\n", keep, hours/2, 100*(1-errSq/energy))
	}

	fmt.Println()
	fmt.Println("== Convolution: a moving average ==")
	x := []float64{1, 2, 3}
	h := []float64{0.5, 0.5}
	conv := make([]float64, len(x)+len(h)-1)
	for i := range x {
		for j := range h {
			conv[i+j] += x[i] * h[j]
		}
	}
	fmt.Printf("[1 2 3] * [0.5 0.5] = %v\n", conv)
	xp := toComplex([]float64{1, 2, 3, 0})
	hp := toComplex([]float64{0.5, 0.5, 0, 0})
	Xp, Hp := dft(xp), dft(hp)
	prod := make([]complex128, 4)
	for i := range prod {
		prod[i] = Xp[i] * Hp[i]
	}
	back := idft(prod)
	fmt.Printf("via DFT: multiply spectra, invert: [%.1f %.1f %.1f %.1f]\n", real(back[0]), real(back[1]), real(back[2]), real(back[3]))

	fmt.Println()
	fmt.Println("== Low-pass filter: 3 Hz signal plus 40 Hz hum, 256 samples per second ==")
	const fs = 256
	clean := make([]float64, fs)
	noisy := make([]float64, fs)
	for i := range noisy {
		t := float64(i) / fs
		clean[i] = math.Sin(2 * math.Pi * 3 * t)
		noisy[i] = clean[i] + 0.5*math.Sin(2*math.Pi*40*t)
	}
	S := fft(toComplex(noisy))
	for k := range S {
		freq := k
		if k > fs/2 {
			freq = fs - k
		}
		if freq > 10 {
			S[k] = 0
		}
	}
	filtered := idft(S)
	before, after := 0.0, 0.0
	for i := range clean {
		before = math.Max(before, math.Abs(noisy[i]-clean[i]))
		after = math.Max(after, math.Abs(real(filtered[i])-clean[i]))
	}
	fmt.Printf("largest error before filter %.3f, after %.1e\n", before, after)

	fmt.Println()
	fmt.Println("== Aliasing: a 9 Hz wave sampled 10 times per second ==")
	for i := 0; i < 5; i++ {
		t := float64(i) / 10
		fmt.Printf("t = %.1f s  sin(2 pi 9 t) = %+.4f   -sin(2 pi 1 t) = %+.4f\n", t, tidy(math.Sin(2*math.Pi*9*t)), tidy(-math.Sin(2*math.Pi*1*t)))
	}
	f, sr := 1.0/45, 1.0/60
	alias := math.Abs(f - sr*math.Round(f/sr))
	fmt.Printf("45 s oscillation scraped every 60 s looks like a %.0f s oscillation\n", 1/alias)

	fmt.Println()
	fmt.Println("== Haar wavelet: averages and details ==")
	cur := []float64{4, 6, 10, 12, 8, 6, 5, 5}
	fmt.Printf("signal   %v\n", cur)
	for len(cur) > 1 {
		avg := make([]float64, len(cur)/2)
		det := make([]float64, len(cur)/2)
		for i := range avg {
			avg[i] = (cur[2*i] + cur[2*i+1]) / 2
			det[i] = (cur[2*i] - cur[2*i+1]) / 2
		}
		fmt.Printf("averages %v  details %v\n", avg, det)
		cur = avg
	}
}
