// counter-rate shows derivatives and integrals on a Prometheus-style counter.
//
// The true request count is c(t) = 50t + 0.1t^2 (requests after t seconds), so
// the true rate is c'(t) = 50 + 0.2t requests per second. A scraper samples
// the counter every 15 s. The process restarts at t = 200 s and the counter
// resets to zero.
//
// Run from the workshop folder: go run ./code/counter-rate
package main

import (
	"fmt"
	"math"
	"strings"
)

const (
	step    = 15  // scrape interval in seconds
	end     = 300 // last sample time
	restart = 200 // process restart time (counter resets to 0)
)

// c is the true cumulative request count since t = 0.
func c(t float64) float64 { return 50*t + 0.1*t*t }

// r is the true instantaneous rate, the derivative c'(t).
func r(t float64) float64 { return 50 + 0.2*t }

// scraped is what the scraper sees: an integer counter that resets at restart.
func scraped(t int) int {
	v := int(math.Floor(c(float64(t))))
	if t <= restart {
		return v
	}
	return v - int(math.Floor(c(restart)))
}

// comma formats an integer with thousands separators.
func comma(n int) string {
	s := fmt.Sprint(n)
	neg := strings.HasPrefix(s, "-")
	s = strings.TrimPrefix(s, "-")
	var b strings.Builder
	for i, ch := range s {
		if i > 0 && (len(s)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(ch)
	}
	if neg {
		return "-" + b.String()
	}
	return b.String()
}

// commaf formats a float with one decimal and thousands separators.
func commaf(x float64) string {
	whole := math.Floor(x)
	return fmt.Sprintf("%s.%d", comma(int(whole)), int(math.Round((x-whole)*10)))
}

func part1() {
	fmt.Println("=== Part 1: the derivative is the limit of the difference quotient ===")
	t := 60.0
	fmt.Printf("c(t) = 50t + 0.1t^2, exact c'(%g) = 50 + 0.2*%g = %g req/s\n", t, t, r(t))
	fmt.Printf("%8s  %22s  %8s\n", "h (s)", "[c(t+h) - c(t)] / h", "error")
	for _, h := range []float64{60, 15, 5, 1, 0.1, 0.01} {
		q := (c(t+h) - c(t)) / h
		fmt.Printf("%8g  %22.4f  %8.4f\n", h, q, q-r(t))
	}
	fmt.Println()
}

func part2() ([]int, []int, []int) {
	fmt.Println("=== Part 2: scrape every 15 s, per-interval rate, reset handling ===")
	var times, vals, fixed []int
	for t := 0; t <= end; t += step {
		times = append(times, t)
		vals = append(vals, scraped(t))
	}
	fmt.Printf("%4s %7s %10s %12s %7s  bar (1 # = 5 req/s)\n", "t", "value", "raw delta", "fixed delta", "rate/s")
	for i, t := range times {
		v := vals[i]
		if i == 0 {
			fmt.Printf("%4d %7d\n", t, v)
			continue
		}
		raw := v - vals[i-1]
		d := raw
		note := ""
		if raw < 0 { // counter went down: assume it restarted from 0
			d = v
			note = "  <- reset detected"
		}
		fixed = append(fixed, d)
		rate := float64(d) / step
		bar := strings.Repeat("#", int(math.Round(rate/5)))
		fmt.Printf("%4d %7d %10d %12d %7.2f  %s%s\n", t, v, raw, d, rate, bar, note)
	}
	fmt.Println()
	return times, vals, fixed
}

func part3(times, vals []int) {
	fmt.Println("=== Part 3: rate(counter[1m]) = slope of the secant over the last 60 s ===")
	index := func(t int) int {
		for i, x := range times {
			if x == t {
				return i
			}
		}
		return -1
	}
	for _, e := range []int{120, 240} {
		s := e - 60
		i, j := index(s), index(e)
		inc := 0
		for k := i + 1; k <= j; k++ {
			d := vals[k] - vals[k-1]
			if d < 0 {
				d = vals[k]
			}
			inc += d
		}
		trueAvg := (c(float64(e)) - c(float64(s))) / 60
		mid := (s + e) / 2
		fmt.Printf("window [%d, %d]: increase = %s, rate = %s/60 = %.2f req/s\n", s, e, comma(inc), comma(inc), float64(inc)/60)
		fmt.Printf("    true average slope = %.2f, c'(%d) at the midpoint = %g, c'(%d) at the end = %g\n",
			trueAvg, mid, r(float64(mid)), e, r(float64(e)))
	}
	fmt.Println()
}

func part4(fixed []int) {
	fmt.Println("=== Part 4: integrate the rate back to a total (Fundamental Theorem of Calculus) ===")
	trueTotal := c(end) - c(0)
	sum := 0
	for _, d := range fixed {
		sum += d
	}
	lastScrape := restart - restart%step
	lost := int(math.Floor(c(restart))) - int(math.Floor(c(float64(lastScrape))))
	fmt.Printf("true total requests c(%d) - c(0)            = %s\n", end, comma(int(trueTotal)))
	fmt.Printf("increase() = sum of fixed deltas             = %s\n", comma(sum))
	fmt.Printf("requests lost between scrape at %d and restart at %d = %s\n", lastScrape, restart, comma(lost))
	fmt.Println()

	var left, right, trap, tel float64
	for t := 0.0; t < end; t += step {
		left += r(t) * step
		right += r(t+step) * step
		trap += (r(t) + r(t+step)) / 2 * step
		tel += c(t+step) - c(t)
	}
	exact := 50.0*end + 0.1*end*end
	fmt.Printf("Riemann sums of the true rate r(t) = 50 + 0.2t over [0, %d] with dt = %d s\n", end, step)
	fmt.Printf("  left  endpoints : %9s\n", commaf(left))
	fmt.Printf("  right endpoints : %9s\n", commaf(right))
	fmt.Printf("  trapezoid       : %9s\n", commaf(trap))
	fmt.Printf("  exact integral  : %9s\n", commaf(exact))
	fmt.Println()
	fmt.Println("Telescoping check without a reset: sum of (c(t_k) - c(t_k-1)) = c(300) - c(0)")
	fmt.Printf("  sum of 20 deltas = %s, c(300) - c(0) = %s\n", commaf(tel), commaf(trueTotal))
}

func main() {
	part1()
	times, vals, fixed := part2()
	part3(times, vals)
	part4(fixed)
}
