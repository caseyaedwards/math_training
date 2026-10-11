// Partial differential equations starter kit: random walkers, the heat
// equation by finite differences, the stability limit, decaying modes, a
// Fourier series solution, the wave equation, guitar harmonics, and the
// Laplace equation by Jacobi iteration.
// Standard library only.
package main

import (
	"fmt"
	"math"
	"math/rand/v2"
)

// heatStep does one explicit finite-difference step of u_t = u_xx with the
// end values held fixed. r = dt / dx^2.
func heatStep(u []float64, r float64) []float64 {
	next := make([]float64, len(u))
	next[0], next[len(u)-1] = u[0], u[len(u)-1]
	for i := 1; i < len(u)-1; i++ {
		next[i] = u[i] + r*(u[i+1]-2*u[i]+u[i-1])
	}
	return next
}

func maxAbs(u []float64) float64 {
	m := 0.0
	for _, v := range u {
		m = math.Max(m, math.Abs(v))
	}
	return m
}

// pulseSeries is the Fourier series solution of the heat equation on [0,1]
// for a start of 1 on [0.25, 0.75] and 0 elsewhere, ends held at 0.
func pulseSeries(x, t float64, terms int) float64 {
	s := 0.0
	for n := 1; n <= terms; n++ {
		k := float64(n) * math.Pi
		bn := 2 / k * (math.Cos(k/4) - math.Cos(3*k/4))
		s += bn * math.Sin(k*x) * math.Exp(-k*k*t)
	}
	return s
}

func main() {
	fmt.Println("== Random walkers: spread grows like sqrt(time) ==")
	rng := rand.New(rand.NewPCG(3, 5))
	const walkers = 20000
	pos := make([]int, walkers)
	step := 0
	for _, t := range []int{25, 100, 400} {
		for ; step < t; step++ {
			for i := range pos {
				if rng.IntN(2) == 0 {
					pos[i]--
				} else {
					pos[i]++
				}
			}
		}
		sum := 0.0
		for _, p := range pos {
			sum += float64(p * p)
		}
		fmt.Printf("after %3d steps: spread %.2f   sqrt(steps) = %.0f\n", t, math.Sqrt(sum/walkers), math.Sqrt(float64(t)))
	}

	fmt.Println()
	fmt.Println("== One heat step by hand, r = 0.25 ==")
	u := []float64{0, 0, 100, 0, 0}
	fmt.Printf("before %v\n", u)
	fmt.Printf("after  %v\n", heatStep(u, 0.25))

	fmt.Println()
	fmt.Println("== Heat equation on [0,1], start sin(pi x), ends at 0 ==")
	const n = 20
	dx := 1.0 / n
	r := 0.4
	dt := r * dx * dx
	u = make([]float64, n+1)
	for i := range u {
		u[i] = math.Sin(math.Pi * float64(i) * dx)
	}
	steps := int(math.Round(0.1 / dt))
	for s := 0; s < steps; s++ {
		u = heatStep(u, r)
	}
	exact := math.Exp(-math.Pi * math.Pi * 0.1)
	fmt.Printf("dx = %.2f, dt = %.4f, %d steps to t = 0.1\n", dx, dt, steps)
	fmt.Printf("u(0.5, 0.1): grid %.4f   exact e^(-pi^2 t) = %.4f\n", u[n/2], exact)

	fmt.Println()
	fmt.Println("== Stability: r = dt/dx^2 must stay at or below 1/2 ==")
	for _, rr := range []float64{0.4, 0.5, 0.6} {
		v := make([]float64, n+1)
		v[n/2] = 1
		for s := 0; s < 200; s++ {
			v = heatStep(v, rr)
		}
		fmt.Printf("r = %.1f: largest |u| after 200 steps = %.3g\n", rr, maxAbs(v))
	}

	fmt.Println()
	fmt.Println("== Modes decay at different speeds (alpha = 1, L = 1) ==")
	for k := 1; k <= 4; k++ {
		rate := math.Pow(float64(k)*math.Pi, 2)
		fmt.Printf("mode sin(%d pi x): decay rate %7.2f, half-life %.4f\n", k, rate, math.Ln2/rate)
	}

	fmt.Println()
	fmt.Println("== Square pulse: Fourier series versus finite differences ==")
	const m = 200
	h := 1.0 / m
	w := make([]float64, m+1)
	for i := range w {
		x := float64(i) * h
		if x > 0.25 && x < 0.75 {
			w[i] = 1
		} else if x == 0.25 || x == 0.75 {
			w[i] = 0.5
		}
	}
	rr := 0.25
	k := rr * h * h
	t := 0.0
	for _, target := range []float64{0.001, 0.01, 0.05} {
		for t < target-1e-12 {
			w = heatStep(w, rr)
			t += k
		}
		fmt.Printf("t = %.3f  u(0.5): series %.4f  grid %.4f   u(0.25): series %.4f  grid %.4f\n",
			target, pulseSeries(0.5, target, 400), w[m/2], pulseSeries(0.25, target, 400), w[m/4])
	}

	fmt.Println()
	fmt.Println("== Wave equation: a bump splits into two halves ==")
	const nw = 400
	cdx := 1.0 / nw
	prev := make([]float64, nw+1)
	for i := range prev {
		x := float64(i) * cdx
		prev[i] = math.Exp(-math.Pow((x-0.5)/0.03, 2))
	}
	// first step with zero starting velocity, Courant number 1
	cur := make([]float64, nw+1)
	for i := 1; i < nw; i++ {
		cur[i] = prev[i] + 0.5*(prev[i+1]-2*prev[i]+prev[i-1])
	}
	stepsW := nw / 4 // t = 0.25 with dt = dx and c = 1
	for s := 1; s < stepsW; s++ {
		next := make([]float64, nw+1)
		for i := 1; i < nw; i++ {
			next[i] = 2*cur[i] - prev[i] + (cur[i+1] - 2*cur[i] + cur[i-1])
		}
		prev, cur = cur, next
	}
	bestL, bestR := 0, nw/2
	for i := 0; i <= nw/2; i++ {
		if cur[i] > cur[bestL] {
			bestL = i
		}
	}
	for i := nw / 2; i <= nw; i++ {
		if cur[i] > cur[bestR] {
			bestR = i
		}
	}
	fmt.Printf("start: one bump at x = 0.50, height 1.000\n")
	fmt.Printf("t = 0.25: bumps at x = %.2f and x = %.2f, heights %.3f and %.3f\n",
		float64(bestL)*cdx, float64(bestR)*cdx, cur[bestL], cur[bestR])

	fmt.Println()
	fmt.Println("== Guitar string: L = 0.65 m, base note 110 Hz ==")
	L, f1 := 0.65, 110.0
	c := 2 * L * f1
	fmt.Printf("wave speed c = 2 L f1 = %.0f m/s\n", c)
	for k := 1; k <= 4; k++ {
		fmt.Printf("harmonic %d: %3.0f Hz, wavelength %.3f m\n", k, float64(k)*c/(2*L), 2*L/float64(k))
	}

	fmt.Println()
	fmt.Println("== Laplace equation: plate with top edge at 100, other edges at 0 ==")
	for _, size := range []int{3, 9, 49} {
		g := make([][]float64, size+2)
		for i := range g {
			g[i] = make([]float64, size+2)
		}
		for j := range g[0] {
			g[0][j] = 100
		}
		g[0][0], g[0][size+1] = 0, 0
		iters := 0
		for {
			iters++
			change := 0.0
			ng := make([][]float64, size+2)
			for i := range g {
				ng[i] = append([]float64{}, g[i]...)
			}
			for i := 1; i <= size; i++ {
				for j := 1; j <= size; j++ {
					ng[i][j] = (g[i-1][j] + g[i+1][j] + g[i][j-1] + g[i][j+1]) / 4
					change = math.Max(change, math.Abs(ng[i][j]-g[i][j]))
				}
			}
			g = ng
			if change < 1e-8 {
				break
			}
		}
		mid := (size + 1) / 2
		fmt.Printf("%2dx%-2d interior: center %.4f after %5d Jacobi sweeps\n", size, size, g[mid][mid], iters)
	}
}
