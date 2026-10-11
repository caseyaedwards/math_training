// Command main checks every number in the Stochastic Processes and
// Queueing track: random walks, a two-state Markov chain, Poisson
// arrivals, M/M/1 formulas and a simulation, Erlang C, Kingman and
// fan-out tail latency. It uses the Go standard library only.
package main

import (
	"fmt"
	"math"
	"math/rand/v2"
	"sort"
)

// rng is seeded so the output is the same on every run.
var rng = rand.New(rand.NewPCG(2026, 10))

// expo draws an exponential gap with the given rate.
func expo(rate float64) float64 {
	return rng.ExpFloat64() / rate
}

func randomWalks() {
	fmt.Println("== Random walk: +1 or -1 per step ==")
	pos := 0
	path := []int{0}
	for i := 0; i < 20; i++ {
		if rng.IntN(2) == 0 {
			pos++
		} else {
			pos--
		}
		path = append(path, pos)
	}
	fmt.Println("one 20-step walk:", path)
	const walks, steps = 10000, 100
	sum, sumSq := 0.0, 0.0
	for w := 0; w < walks; w++ {
		x := 0
		for s := 0; s < steps; s++ {
			if rng.IntN(2) == 0 {
				x++
			} else {
				x--
			}
		}
		sum += float64(x)
		sumSq += float64(x * x)
	}
	fmt.Printf("%d walks of %d steps: mean end %.2f, typical distance (RMS) %.2f, sqrt(n) = %.2f\n\n",
		walks, steps, sum/walks, math.Sqrt(sumSq/walks), math.Sqrt(steps))
}

func markovChain() {
	fmt.Println("== Markov chain: server Up/Down, fail 0.1, repair 0.6 ==")
	up := 1.0
	for step := 0; step <= 8; step++ {
		fmt.Printf("step %d: P(Up) = %.4f\n", step, up)
		up = up*0.9 + (1-up)*0.6
	}
	fmt.Printf("steady state P(Up) = 0.6 / (0.1 + 0.6) = %.4f\n\n", 0.6/0.7)
}

func poisson() {
	fmt.Println("== Poisson arrivals, rate 5 per second ==")
	const n = 100000
	total, long := 0.0, 0
	for i := 0; i < n; i++ {
		g := expo(5)
		total += g
		if g > 0.4 {
			long++
		}
	}
	fmt.Printf("mean gap %.4f s (theory 0.2000), P(gap > 0.4 s) %.4f (theory e^-2 = %.4f)\n",
		total/n, float64(long)/n, math.Exp(-2))
	lt := 5.0
	for k := 0; k <= 10; k++ {
		p := math.Exp(-lt) * math.Pow(lt, float64(k)) / math.Gamma(float64(k+1))
		fmt.Printf("P(%2d arrivals in 1 s) = %.4f\n", k, p)
	}
	fmt.Println()
}

func mm1Table() {
	fmt.Println("== M/M/1 with service rate 100 per second (mean service 10 ms) ==")
	fmt.Println("  rho   L (in system)   W mean (ms)   p99 (ms)   slowdown 1/(1-rho)")
	mu := 100.0
	for _, rho := range []float64{0.5, 0.7, 0.8, 0.9, 0.95, 0.99} {
		lam := rho * mu
		L := rho / (1 - rho)
		W := 1 / (mu - lam)
		p99 := math.Log(100) / (mu - lam)
		fmt.Printf("  %.2f  %10.2f   %11.1f   %8.1f   %8.1f\n", rho, L, W*1000, p99*1000, 1/(1-rho))
	}
	fmt.Println("queue length P(n) = (1 - rho) rho^n:")
	for _, rho := range []float64{0.5, 0.9} {
		fmt.Printf("  rho %.1f:", rho)
		for k := 0; k < 10; k++ {
			fmt.Printf(" %.3f", (1-rho)*math.Pow(rho, float64(k)))
		}
		fmt.Println()
	}
	fmt.Println()
}

func mm1Simulate() {
	fmt.Println("== M/M/1 simulation: arrivals 80/s, service 100/s, 1,000,000 requests ==")
	const n = 1000000
	lam, mu := 80.0, 100.0
	resp := make([]float64, n)
	wait, busyArea := 0.0, 0.0
	for i := 0; i < n; i++ {
		s := expo(mu)
		resp[i] = wait + s
		busyArea += resp[i]
		a := expo(lam)
		// Lindley recursion: next wait = max(0, this wait + service - gap).
		wait = math.Max(0, wait+s-a)
	}
	mean := busyArea / n
	sort.Float64s(resp)
	fmt.Printf("mean response %.1f ms (theory 50.0), p99 %.1f ms (theory %.1f)\n",
		mean*1000, resp[n*99/100]*1000, math.Log(100)/(mu-lam)*1000)
	fmt.Printf("Little: L = lambda W = 80 x %.4f = %.2f requests in system (theory 4.00)\n\n",
		mean, 80*mean)
}

// erlangC returns the probability that an arrival waits in an M/M/c queue
// with offered load a = lambda/mu, using the Erlang B recursion.
func erlangC(c int, a float64) float64 {
	b := 1.0
	for k := 1; k <= c; k++ {
		b = a * b / (float64(k) + a*b)
	}
	return float64(c) * b / (float64(c) - a*(1-b))
}

func pooling() {
	fmt.Println("== Pooling: total load 8 per second ==")
	// Two separate M/M/1 queues, each lambda 4, mu 5.
	w1 := 1 / (5.0 - 4.0)
	fmt.Printf("two separate queues, 1 server each (mu 5): P(wait) %.3f, Wq %.3f s, W %.3f s\n",
		0.8, 0.8*w1, w1)
	cw := erlangC(2, 8.0/5.0)
	wq := cw / (2*5.0 - 8.0)
	fmt.Printf("one shared queue, 2 servers (mu 5):       P(wait) %.3f, Wq %.3f s, W %.3f s\n",
		cw, wq, wq+1/5.0)
	fmt.Printf("one queue, 1 fast server (mu 10):          P(wait) %.3f, Wq %.3f s, W %.3f s\n\n",
		0.8, 0.8/(10.0-8.0), 1/(10.0-8.0))

	fmt.Println("== Erlang C capacity plan: 90 req/s, each worker 10 req/s ==")
	lam, mu := 90.0, 10.0
	for c := 10; c <= 14; c++ {
		p := erlangC(c, lam/mu)
		wq := p / (float64(c)*mu - lam)
		fmt.Printf("c = %2d  rho %.3f  P(wait) %.3f  mean wait %6.1f ms\n",
			c, lam/(float64(c)*mu), p, wq*1000)
	}
	fmt.Println("P(wait) versus rho at the same utilization:")
	for _, c := range []int{1, 2, 4, 8, 16} {
		fmt.Printf("  c = %2d:", c)
		for _, rho := range []float64{0.5, 0.8, 0.9} {
			fmt.Printf("  rho %.1f -> %.3f", rho, erlangC(c, rho*float64(c)))
		}
		fmt.Println()
	}
	fmt.Println()
}

func kingman() {
	fmt.Println("== Kingman G/G/1 wait: rho 0.9, mean service 10 ms, ca^2 = 1 ==")
	rho, tau, ca2 := 0.9, 10.0, 1.0
	for _, cs2 := range []float64{0, 0.25, 1, 4} {
		wq := rho / (1 - rho) * (ca2 + cs2) / 2 * tau
		fmt.Printf("service cs^2 = %.2f -> mean wait %.1f ms\n", cs2, wq)
	}
	fmt.Println()
}

func fanOut() {
	fmt.Println("== Fan-out: each backend is slow 1% of the time ==")
	for _, n := range []int{1, 10, 50, 100, 200} {
		fmt.Printf("fan-out %3d -> P(request sees a slow backend) %.3f\n", n, 1-math.Pow(0.99, float64(n)))
	}
}

func main() {
	randomWalks()
	markovChain()
	poisson()
	mm1Table()
	mm1Simulate()
	pooling()
	kingman()
	fanOut()
}
