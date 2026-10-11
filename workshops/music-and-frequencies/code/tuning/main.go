// Command tuning prints the math of musical tuning: frequencies, ratios,
// equal temperament, cents, harmonics, and decibels.
//
// It prints:
//  1. Frequency and period of one octave of 12-tone equal temperament, A4 to A5.
//  2. Equal-tempered intervals versus simple (just) ratios, with the error in cents.
//  3. Why 3:2 sounds smooth: peaks of the two waves line up every 2 and 3 cycles.
//  4. Piano keys: key number to frequency, and why the keyboard is a log scale.
//  5. The harmonic series of A2 = 110 Hz and the nearest piano notes.
//  6. Decibels: another log scale.
//
// Standard library only. No arguments. Run: go run ./code/tuning
package main

import (
	"fmt"
	"math"
	"strings"
)

const a4 = 440.0

var semitone = math.Pow(2, 1.0/12)

var names = []string{"A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"}

// cents returns the size of the interval f1 -> f2 (1200 per octave).
func cents(f2, f1 float64) float64 { return 1200 * math.Log2(f2/f1) }

// keyFreq maps a piano key number (A0 = 1, A4 = 49, C8 = 88) to hertz.
func keyFreq(key int) float64 { return a4 * math.Pow(2, float64(key-49)/12) }

func keyName(key int) string {
	return fmt.Sprintf("%s%d", names[(key-1)%12], (key+8)/12)
}

// comma1 formats x with one decimal and thousands separators.
func comma1(x float64) string {
	s := fmt.Sprintf("%.1f", x)
	whole, frac := s[:len(s)-2], s[len(s)-2:]
	var b strings.Builder
	for i, c := range whole {
		if i > 0 && (len(whole)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(c)
	}
	return b.String() + frac
}

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func section(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 66))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 66))
}

func main() {
	section("1. One octave of 12-tone equal temperament (A4 = 440 Hz)")
	fmt.Printf("semitone ratio 2^(1/12) = %.6f\n", semitone)
	fmt.Printf("%3s  %-5s%10s%11s  bar (log spacing)\n", "n", "note", "freq Hz", "period ms")
	for n := 0; n <= 12; n++ {
		f := a4 * math.Pow(semitone, float64(n))
		fmt.Printf("%3d  %-5s%10.2f%11.3f  %s\n", n, keyName(49+n), f, 1000/f, strings.Repeat("#", n*4+1))
	}

	section("2. Equal temperament versus simple ratios")
	intervals := []struct {
		name     string
		n        int
		num, den int
	}{
		{"unison", 0, 1, 1}, {"minor second", 1, 16, 15}, {"major second", 2, 9, 8},
		{"minor third", 3, 6, 5}, {"major third", 4, 5, 4}, {"perfect fourth", 5, 4, 3},
		{"tritone", 6, 45, 32}, {"perfect fifth", 7, 3, 2}, {"minor sixth", 8, 8, 5},
		{"major sixth", 9, 5, 3}, {"minor seventh", 10, 9, 5}, {"major seventh", 11, 15, 8},
		{"octave", 12, 2, 1},
	}
	fmt.Printf("%-16s%6s%10s%7s%9s%10s%9s%11s\n", "interval", "semis", "2^(n/12)", "just", "ratio",
		"ET cents", "just c", "ET - just")
	for _, iv := range intervals {
		et := math.Pow(2, float64(iv.n)/12)
		ratio := float64(iv.num) / float64(iv.den)
		frac := fmt.Sprint(iv.num)
		if iv.den != 1 {
			frac = fmt.Sprintf("%d/%d", iv.num, iv.den)
		}
		jc := cents(ratio, 1)
		fmt.Printf("%-16s%6d%10.5f%7s%9.5f%10d%9.2f%+11.2f\n", iv.name, iv.n, et, frac, ratio,
			iv.n*100, jc, float64(iv.n*100)-jc)
	}
	fmt.Println()
	fifth, third := math.Pow(2, 7.0/12), math.Pow(2, 4.0/12)
	fmt.Printf("fifth:       2^(7/12) = %.6f   3/2 = 1.5   gap = %.3f cents\n", fifth, cents(1.5, fifth))
	fmt.Printf("major third: 2^(4/12) = %.6f   5/4 = 1.25  gap = %.3f cents\n", third, cents(third, 1.25))
	e5 := a4 * fifth
	fmt.Printf("A4 = 440 Hz: just E5 = 660.00 Hz, equal-tempered E5 = %.2f Hz, difference %.2f Hz\n", e5, 660-e5)

	section("3. Why 3:2 sounds smooth: peaks line up")
	fmt.Println("A4 = 440 Hz and E5 = 660 Hz. A peak happens at t = k / f.")
	peaks := func(f float64, count int) string {
		var p []string
		for k := 0; k < count; k++ {
			p = append(p, fmt.Sprintf("%.3f", float64(k)/f*1000))
		}
		return strings.Join(p, ", ")
	}
	fmt.Println("  A4 peaks (ms): " + peaks(440, 5))
	fmt.Println("  E5 peaks (ms): " + peaks(660, 7))
	fmt.Printf("  shared peaks every 1 / gcd(440, 660) = 1/%d s = %.3f ms (2 A cycles = 3 E cycles)\n",
		gcd(440, 660), 1000/float64(gcd(440, 660)))
	fmt.Println("  ASCII view of 0 to 9.09 ms (^ = peak, one column = 0.152 ms):")
	const width = 60 // 60 columns span 1/110 s
	pers := []int{}
	for _, w := range []struct {
		label string
		f     int
	}{{"A4 440", 440}, {"E5 660", 660}} {
		per := width * 110 / w.f // columns per cycle: 15 for A, 10 for E
		pers = append(pers, per)
		var b strings.Builder
		for c := 0; c < width; c++ {
			if c%per == 0 {
				b.WriteByte('^')
			} else {
				b.WriteByte('-')
			}
		}
		fmt.Printf("  %s |%s|\n", w.label, b.String())
	}
	both := pers[0] * pers[1] / gcd(pers[0], pers[1])
	var b strings.Builder
	for c := 0; c < width; c++ {
		if c%both == 0 {
			b.WriteByte('*')
		} else {
			b.WriteByte(' ')
		}
	}
	fmt.Printf("  shared |%s|\n", b.String())

	section("4. Piano keys: frequency = 440 * 2^((key - 49) / 12)")
	fmt.Printf("%4s  %-5s%9s  log2(f / 27.5)  position bar\n", "key", "note", "freq Hz")
	for _, key := range []int{1, 13, 25, 37, 40, 49, 52, 56, 61, 73, 85, 88} {
		f := keyFreq(key)
		oct := math.Log2(f / 27.5)
		line := fmt.Sprintf("%4d  %-5s%9.2f  %14.3f  %s", key, keyName(key), f, oct,
			strings.Repeat("#", int(math.Round(oct*8))))
		fmt.Println(strings.TrimRight(line, " "))
	}
	fmt.Println("Each octave adds 12 keys and doubles the frequency: equal steps in log2(f).")
	lo, hi := keyFreq(1), keyFreq(88)
	fmt.Printf("Range: %.1f Hz to %s Hz, a factor of %.0f, %.2f octaves\n", lo, comma1(hi), hi/lo, math.Log2(hi/lo))

	section("5. Harmonics of A2 = 110 Hz (integer multiples)")
	fmt.Printf("%8s%9s  %-12s%9s%11s\n", "harmonic", "freq Hz", "nearest key", "key Hz", "cents off")
	for h := 1; h <= 10; h++ {
		f := 110 * float64(h)
		key := int(math.Round(49 + 12*math.Log2(f/a4)))
		kf := keyFreq(key)
		fmt.Printf("%8d%9.0f  %-12s%9.2f%+11.2f\n", h, f, keyName(key), kf, cents(f, kf))
	}

	section("6. Decibels: also a log scale")
	fmt.Println("sound pressure level change = 20 * log10(p2 / p1) dB")
	for _, r := range []float64{2, 10, 100, 1000} {
		fmt.Printf("  pressure x%-5.0f -> %6.2f dB\n", r, 20*math.Log10(r))
	}
	fmt.Println("power ratio change = 10 * log10(P2 / P1) dB")
	for _, r := range []float64{2, 10, 100} {
		fmt.Printf("  power x%-5.0f    -> %6.2f dB\n", r, 10*math.Log10(r))
	}
}
