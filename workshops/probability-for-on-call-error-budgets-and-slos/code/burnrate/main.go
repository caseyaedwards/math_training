// Command burnrate covers error budget burn rate, the multiwindow alert
// thresholds, and time to exhaustion for a 99.9% SLO over 30 days.
//
// It prints:
//  1. The error budget in minutes and in requests.
//  2. Burn rate from an observed error rate.
//  3. The multiwindow, multi-burn-rate alert table from the Google SRE
//     Workbook, with the budget each alert consumes before it fires.
//  4. Time to exhaustion at several burn rates.
//  5. A 30-day budget burn-down as a text chart, with an incident on day 10.
//
// Run from the workshop folder: go run ./code/burnrate
package main

import (
	"fmt"
	"math"
	"strings"
)

const (
	slo      = 0.999
	periodH  = 30 * 24 // 720 hours in the SLO window
	reqPerS  = 100     // sample traffic
	budgetFr = 1 - slo
)

// burnRate says how many times faster than steady spend the budget burns.
func burnRate(errorRate float64) float64 { return errorRate / budgetFr }

// consumed is the fraction of the whole-period budget spent in windowH hours.
func consumed(rate, windowH float64) float64 { return rate * windowH / periodH }

// hoursLeft is the time until the remaining budget fraction reaches zero.
func hoursLeft(rate, remaining float64) float64 { return remaining * periodH / rate }

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

func part1() {
	fmt.Println("1. Error budget for SLO 99.9% over 30 days")
	minutes := periodH * 60
	reqs := periodH * 3600 * reqPerS
	fmt.Printf("   window          = %d h = 43,200 min\n", periodH)
	fmt.Printf("   budget fraction = 1 - %g = %.3f\n", slo, budgetFr)
	fmt.Printf("   budget minutes  = 43,200 x 0.001 = %.1f min\n", float64(minutes)*budgetFr)
	fmt.Printf("   requests        = %s at %d req/s\n", comma(int64(reqs)), reqPerS)
	fmt.Printf("   budget requests = %s failed requests\n", comma(int64(math.Round(float64(reqs)*budgetFr))))
	fmt.Println()
}

func part2() {
	fmt.Println("2. Burn rate = observed error rate / (1 - SLO)")
	for _, e := range []float64{0.0005, 0.001, 0.002, 0.006, 0.0144, 0.05} {
		fmt.Printf("   error rate %5.2f%%  ->  burn rate %5.1fx\n", e*100, burnRate(e))
	}
	fmt.Println()
}

func part3() {
	fmt.Println("3. Multiwindow, multi-burn-rate alerts (SRE Workbook, SLO 99.9%, 30 d)")
	type row struct {
		action      string
		rate, longH float64
		short       string
	}
	rows := []row{{"page", 14.4, 1, "5m"}, {"page", 6, 6, "30m"}, {"ticket", 1, 72, "6h"}}
	fmt.Printf("   %-7s%6s%7s%8s%10s%10s\n", "action", "burn", "long", "short", "err rate", "consumed")
	for _, r := range rows {
		fmt.Printf("   %-7s%5.1fx%6gh%8s%9.2f%%%9.1f%%\n", r.action, r.rate, r.longH, r.short,
			r.rate*budgetFr*100, consumed(r.rate, r.longH)*100)
	}
	fmt.Println()
	fmt.Println("   consumed = burn x long window / 720 h")
	fmt.Println("   14.4 x 1 / 720 = 0.02   6 x 6 / 720 = 0.05   1 x 72 / 720 = 0.10")
	fmt.Println()
}

func part4() {
	fmt.Println("4. Time to exhaustion = remaining x 720 h / burn rate")
	fmt.Printf("   %6s  %18s  %10s\n", "burn", "full budget", "40% left")
	for _, r := range []float64{0.5, 1, 2, 6, 14.4, 36} {
		full := hoursLeft(r, 1)
		fmt.Printf("   %5gx  %8.2f h (%4.1f d)  %8.2f h\n", r, full, full/24, hoursLeft(r, 0.4))
	}
	fmt.Println()
}

func part5() {
	fmt.Println("5. Burn-down: 0.5x steady, 14.4x incident for 6 h starting day 10")
	remaining := 1.0
	points := make([]float64, 0, periodH+1)
	for hour := 0; hour <= periodH; hour++ {
		points = append(points, remaining)
		rate := 0.5
		if hour >= 240 && hour < 246 {
			rate = 14.4
		}
		remaining -= rate / periodH
	}
	for day := 0; day <= 30; day += 2 {
		r := points[day*24]
		fmt.Printf("   day %2d  %5.1f%%  %s\n", day, r*100, strings.Repeat("#", int(math.Round(r*50))))
	}
	fmt.Printf("   incident cost: 14.4 x 6 / 720 = %.1f%% of the budget\n", 14.4*6/720*100)
	fmt.Println()
}

func main() {
	part1()
	part2()
	part3()
	part4()
	part5()
}
