// Command capacity plans capacity for exponentially growing load and shows
// why a log axis turns exponential growth into a straight line.
//
// Scenario: a service serves 10,000 requests per second today and traffic
// grows 8% month over month. The fleet tops out at 50,000 rps.
//
// It prints:
//  1. Month-by-month load with an ASCII bar chart and the capacity line.
//  2. Exact months to double, to reach 70% of capacity, and to reach capacity.
//  3. The same questions for other growth rates.
//  4. Equal steps in log10(load) every month.
//  5. The growth rate recovered from two dashboard readings.
//
// Standard library only. No arguments. Run: go run ./code/capacity
package main

import (
	"fmt"
	"math"
	"strings"
)

const (
	startRPS    = 10000.0
	capacityRPS = 50000.0
	growth      = 0.08
)

// monthsUntil solves start * (1 + g)^t = target for t.
func monthsUntil(target, start, g float64) float64 {
	return math.Log(target/start) / math.Log(1+g)
}

// comma formats x with thousands separators and the given decimals.
func comma(x float64, decimals int) string {
	s := fmt.Sprintf("%.*f", decimals, x)
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
	return b.String() + frac
}

func main() {
	fmt.Printf("Load model: L(t) = 10,000 * (1 + %.2f)^t   (t in months)\n", growth)
	fmt.Printf("Capacity: %s rps\n", comma(capacityRPS, 0))
	fmt.Println()
	fmt.Println("1. Month by month (# = 1,000 rps, | = capacity)")
	capCol := int(capacityRPS / 1000)
	for month := 0; month <= 24; month += 2 {
		load := startRPS * math.Pow(1+growth, float64(month))
		n := int(math.Round(load / 1000))
		var bar, flag string
		if n <= capCol {
			bar = fmt.Sprintf("%-*s|", capCol, strings.Repeat("#", n))
		} else {
			bar = strings.Repeat("#", n)
			flag = "  OVER"
		}
		fmt.Printf("  month %2d  %8s rps  %s%s\n", month, comma(load, 0), bar, flag)
	}

	fmt.Println()
	fmt.Println("2. Exact answers with logs")
	t2 := monthsUntil(2*startRPS, startRPS, growth)
	t70 := monthsUntil(0.7*capacityRPS, startRPS, growth)
	tcap := monthsUntil(capacityRPS, startRPS, growth)
	fmt.Printf("  doubles (20,000 rps):       t = ln 2 / ln 1.08   = %5.2f months\n", t2)
	fmt.Printf("  70%% of capacity (35,000):   t = ln 3.5 / ln 1.08 = %5.2f months\n", t70)
	fmt.Printf("  full capacity (50,000):     t = ln 5 / ln 1.08   = %5.2f months\n", tcap)
	fmt.Printf("  rule of 72 check: 72 / 8 = %.2f months to double\n", 72.0/8)

	fmt.Println()
	fmt.Println("3. Months from 10,000 rps at other growth rates")
	fmt.Printf("  %12s%9s%9s%10s\n", "growth/month", "double", "70% cap", "capacity")
	for _, pct := range []float64{2, 4, 5, 8, 10, 15} {
		g := pct / 100
		fmt.Printf("  %11.0f%%%9.1f%9.1f%10.1f\n", pct,
			monthsUntil(2*startRPS, startRPS, g),
			monthsUntil(35000, startRPS, g),
			monthsUntil(capacityRPS, startRPS, g))
	}

	fmt.Println()
	fmt.Println("4. Log scale: log10(load) climbs by the same amount every month")
	step := math.Log10(1 + growth)
	fmt.Printf("  log10(1.08) = %.5f per month\n", step)
	prev := 0.0
	for month := 0; month <= 6; month++ {
		load := startRPS * math.Pow(1+growth, float64(month))
		lg := math.Log10(load)
		diff := ""
		if month > 0 {
			diff = fmt.Sprintf("  +%.5f", lg-prev)
		}
		fmt.Printf("  month %d  load %9s  log10 %.5f%s\n", month, comma(load, 1), lg, diff)
		prev = lg
	}

	fmt.Println()
	fmt.Println("5. Recover the growth rate from two dashboard readings")
	jan, jul, months := 12400.0, 19700.0, 6.0
	g := math.Pow(jul/jan, 1/months) - 1
	fmt.Printf("  January %s rps, July %s rps, %.0f months apart\n", comma(jan, 0), comma(jul, 0), months)
	fmt.Printf("  g = (%s / %s)^(1/%.0f) - 1 = %.2f%% per month\n", comma(jul, 0), comma(jan, 0), months, g*100)
	fmt.Printf("  months from July to %s rps: %.1f\n", comma(capacityRPS, 0), monthsUntil(capacityRPS, jul, g))
}
