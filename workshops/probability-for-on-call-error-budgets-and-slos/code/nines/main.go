// Command nines turns availability targets ("nines") into allowed downtime
// and error budgets.
//
// It prints:
//  1. Allowed downtime per day, per 30-day window, and per 365-day year.
//  2. A text-mode "nines ladder": log-scale bars of downtime per year.
//  3. The error budget in requests for a sample monthly traffic volume.
//
// Run from the workshop folder: go run ./code/nines
package main

import (
	"fmt"
	"math"
	"strings"
)

var slos = []float64{99.0, 99.5, 99.9, 99.95, 99.99, 99.999}

const (
	daySec   = 24 * 60 * 60 // 86,400 seconds
	monthSec = 30 * daySec  // 2,592,000 seconds (30-day window)
	yearSec  = 365 * daySec // 31,536,000 seconds
)

// budget returns the error budget as a fraction: 1 - SLO.
func budget(sloPercent float64) float64 { return 1 - sloPercent/100 }

// human formats a duration in seconds with the largest sensible unit.
func human(s float64) string {
	switch {
	case s >= daySec:
		return fmt.Sprintf("%.2f d", s/daySec)
	case s >= 3600:
		return fmt.Sprintf("%.2f h", s/3600)
	case s >= 60:
		return fmt.Sprintf("%.2f min", s/60)
	}
	return fmt.Sprintf("%.2f s", s)
}

// comma formats an integer with thousands separators.
func comma(n int64) string {
	s := fmt.Sprintf("%d", n)
	var b strings.Builder
	for i, c := range s {
		if i > 0 && (len(s)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(c)
	}
	return b.String()
}

func table() {
	fmt.Println("1. Allowed downtime per window (budget = 1 - SLO)")
	fmt.Println()
	header := fmt.Sprintf("%8s  %8s  %10s  %10s  %10s", "SLO", "budget", "per day", "per 30 d", "per year")
	fmt.Println(header)
	fmt.Println(strings.Repeat("-", len(header)))
	for _, slo := range slos {
		b := budget(slo)
		fmt.Printf("%7g%%  %8.5f  %10s  %10s  %10s\n", slo, b,
			human(b*daySec), human(b*monthSec), human(b*yearSec))
	}
	fmt.Println()
}

func ladder() {
	fmt.Println("2. Nines ladder: downtime per year, log scale (each '#' = x1.25)")
	fmt.Println()
	for _, slo := range slos {
		minutes := budget(slo) * yearSec / 60
		n := int(math.Max(1, math.Round(math.Log(minutes)/math.Log(1.25))))
		whole := int64(minutes)
		tenth := int64(math.Round(minutes*10)) % 10
		fmt.Printf("%7g%%  %9s min  %s\n", slo, fmt.Sprintf("%s.%d", comma(whole), tenth), strings.Repeat("#", n))
	}
	fmt.Println()
	fmt.Println("Each extra nine divides the downtime by 10.")
	fmt.Println()
}

func requests(monthly int64) {
	fmt.Printf("3. Error budget in requests for %s requests per 30 days\n\n", comma(monthly))
	for _, slo := range slos {
		allowed := int64(math.Round(budget(slo) * float64(monthly)))
		fmt.Printf("%7g%%  %12s failed requests allowed\n", slo, comma(allowed))
	}
	fmt.Println()
}

func main() {
	table()
	ladder()
	requests(50_000_000)
}
