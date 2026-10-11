// Command compound shows compound interest, the number e, doubling time,
// and half-life decay.
//
// It prints:
//  1. A = P(1 + r/n)^(nt) for n = 1, 12, 365, and continuous compounding.
//  2. (1 + 1/n)^n creeping up toward e = 2.71828...
//  3. Exact doubling time ln 2 / ln(1 + r) against the rules of 72, 70, and 69.3.
//  4. Half-life decay: carbon-14 and a cache score with a 60 s half-life.
//
// Standard library only. No arguments. Run: go run ./code/compound
package main

import (
	"fmt"
	"math"
	"strings"
)

// compound returns the balance after compounding n times per year.
func compound(principal, rate float64, n, years float64) float64 {
	return principal * math.Pow(1+rate/n, n*years)
}

// continuous returns P e^(rt).
func continuous(principal, rate, years float64) float64 {
	return principal * math.Exp(rate*years)
}

// comma formats x with thousands separators and the given decimals.
func comma(x float64, decimals int) string {
	s := fmt.Sprintf("%.*f", decimals, math.Abs(x))
	intPart, frac := s, ""
	if i := strings.IndexByte(s, '.'); i >= 0 {
		intPart, frac = s[:i], s[i:]
	}
	var b strings.Builder
	for i, c := range intPart {
		if i > 0 && (len(intPart)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(c)
	}
	sign := ""
	if x < 0 {
		sign = "-"
	}
	return sign + b.String() + frac
}

func section(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 64))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 64))
}

func bar(frac float64) string {
	return strings.Repeat("#", int(math.Round(frac*40)))
}

func main() {
	principal, rate, years := 10000.0, 0.05, 10.0

	section("1. Compound interest: $10,000 at 5% for 10 years")
	fmt.Printf("%-14s%6s%14s%18s\n", "compounding", "n", "balance", "gain vs yearly")
	yearly := compound(principal, rate, 1, years)
	for _, row := range []struct {
		label string
		n     float64
	}{{"yearly", 1}, {"monthly", 12}, {"daily", 365}} {
		a := compound(principal, rate, row.n, years)
		fmt.Printf("%-14s%6.0f%14s%18s\n", row.label, row.n, comma(a, 2), comma(a-yearly, 2))
	}
	a := continuous(principal, rate, years)
	fmt.Printf("%-14s%6s%14s%18s\n", "continuous", "inf", comma(a, 2), comma(a-yearly, 2))

	section("2. (1 + 1/n)^n approaches e")
	fmt.Printf("%12s  %-14s%12s\n", "n", "(1 + 1/n)^n", "gap to e")
	for _, n := range []float64{1, 2, 4, 12, 52, 365, 8760, 1000000} {
		v := math.Pow(1+1/n, n)
		fmt.Printf("%12s  %-14.8f%12.8f\n", comma(n, 0), v, math.E-v)
	}
	fmt.Printf("%12s  %-14.8f\n", "e", math.E)

	section("3. Doubling time: exact versus rules of thumb (years)")
	fmt.Printf("%6s%9s%8s%8s%8s%9s%9s\n", "rate", "exact", "72/r", "70/r", "69.3/r", "err 72", "err 70")
	for _, pct := range []float64{1, 2, 3, 5, 8, 10, 12, 15, 20, 30} {
		r := pct / 100
		exact := math.Ln2 / math.Log(1+r)
		r72, r70, r693 := 72/pct, 70/pct, 69.3/pct
		fmt.Printf("%5.0f%%%9.2f%8.2f%8.2f%8.2f%+8.1f%%%+8.1f%%\n", pct, exact, r72, r70, r693,
			(r72-exact)/exact*100, (r70-exact)/exact*100)
	}
	fmt.Println("continuous growth doubles in exactly ln 2 / r = 69.3 / (rate in %)")

	section("4. Half-life: the mirror image of doubling")
	halfLife := 5730.0 // carbon-14, years
	k := math.Ln2 / halfLife
	fmt.Printf("carbon-14: half-life %s years, decay constant k = %.3e per year\n", comma(halfLife, 0), k)
	for _, t := range []float64{0, 5730, 11460, 17190, 22920} {
		left := math.Exp(-k * t)
		fmt.Printf("  t = %6s yr  remaining %5.1f%%  %s\n", comma(t, 0), left*100, bar(left))
	}
	fmt.Println()
	fmt.Println("cache hit weight with a 60 s half-life (score = e^(-kt))")
	k = math.Ln2 / 60
	for _, t := range []float64{0, 30, 60, 120, 180, 300} {
		w := math.Exp(-k * t)
		fmt.Printf("  age %3.0f s  weight %5.3f  %s\n", t, w, bar(w))
	}
}
