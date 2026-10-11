// Dynamical systems starter kit: iterate a map, test fixed points, watch the
// logistic map double its period, measure chaos, integrate the Lorenz system,
// draw the Mandelbrot set in ASCII, and simulate retries and an autoscaler.
// Standard library only.
package main

import (
	"fmt"
	"math"
	"strings"
)

// logistic is the map x -> r x (1 - x).
func logistic(r, x float64) float64 { return r * x * (1 - x) }

// settle runs the logistic map long enough to forget the start.
func settle(r, x float64, steps int) float64 {
	for i := 0; i < steps; i++ {
		x = logistic(r, x)
	}
	return x
}

// period returns the smallest p up to max with f^p(x) = x, or 0 if none.
func period(r, x float64, max int) int {
	start := x
	for p := 1; p <= max; p++ {
		x = logistic(r, x)
		if math.Abs(x-start) < 1e-9 {
			return p
		}
	}
	return 0
}

// lyapunov averages ln|f'(x)| along an orbit. Positive means chaos.
func lyapunov(r float64) float64 {
	x := settle(r, 0.2, 1000)
	sum := 0.0
	const n = 100000
	for i := 0; i < n; i++ {
		sum += math.Log(math.Abs(r * (1 - 2*x)))
		x = logistic(r, x)
	}
	return sum / n
}

// superstable finds r where the orbit of 1/2 returns to 1/2 after 2^k steps.
// The secant method starts from a guess.
func superstable(k int, guess float64) float64 {
	g := func(r float64) float64 {
		x := 0.5
		for i := 0; i < 1<<k; i++ {
			x = logistic(r, x)
		}
		return x - 0.5
	}
	r0, r1 := guess, guess+1e-7
	for i := 0; i < 100; i++ {
		f0, f1 := g(r0), g(r1)
		if f1 == f0 {
			break
		}
		r0, r1 = r1, r1-f1*(r1-r0)/(f1-f0)
		if math.Abs(r1-r0) < 1e-15 {
			break
		}
	}
	return r1
}

type vec [3]float64

// lorenz returns the velocity of the Lorenz system at s.
func lorenz(s vec) vec {
	const sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
	return vec{sigma * (s[1] - s[0]), s[0]*(rho-s[2]) - s[1], s[0]*s[1] - beta*s[2]}
}

// rk4 takes one fourth-order Runge-Kutta step of size h.
func rk4(s vec, h float64) vec {
	add := func(a, b vec, t float64) vec { return vec{a[0] + t*b[0], a[1] + t*b[1], a[2] + t*b[2]} }
	k1 := lorenz(s)
	k2 := lorenz(add(s, k1, h/2))
	k3 := lorenz(add(s, k2, h/2))
	k4 := lorenz(add(s, k3, h))
	var out vec
	for i := range out {
		out[i] = s[i] + h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i])
	}
	return out
}

// divergeTime integrates two Lorenz starts that differ by eps in x and
// returns the first time their x values differ by more than 1.
func divergeTime(eps float64) float64 {
	a, b := vec{1, 1, 1}, vec{1 + eps, 1, 1}
	for i := 0; i < 10000; i++ {
		if math.Abs(a[0]-b[0]) > 1 {
			return float64(i) * 0.01
		}
		a, b = rk4(a, 0.01), rk4(b, 0.01)
	}
	return math.Inf(1)
}

// autoscale runs x(n+1) = max(0, x(n) + k (target - x(n-d))) and returns
// the lowest and highest replica counts over steps 40 to 80.
func autoscale(k float64, d int) (lo, hi float64) {
	xs := make([]float64, d+1)
	for i := range xs {
		xs[i] = 40
	}
	lo, hi = math.Inf(1), math.Inf(-1)
	for n := 0; n < 80; n++ {
		last := xs[len(xs)-1]
		seen := xs[len(xs)-1-d]
		xs = append(xs, math.Max(0, last+k*(100-seen)))
		if n >= 40 {
			lo, hi = math.Min(lo, xs[len(xs)-1]), math.Max(hi, xs[len(xs)-1])
		}
	}
	return lo, hi
}

func main() {
	fmt.Println("== Press cos again and again, start 1 ==")
	x := 1.0
	for n := 1; n <= 40; n++ {
		x = math.Cos(x)
		if n <= 5 || n == 10 || n == 20 || n == 40 {
			fmt.Printf("n=%-3d x=%.6f\n", n, x)
		}
	}
	fmt.Printf("slope at the fixed point: -sin(x*) = %.4f, and |slope| < 1: stable\n", -math.Sin(x))

	fmt.Println("\n== Logistic map: fixed point x* = 1 - 1/r, slope 2 - r ==")
	for _, r := range []float64{2.8, 3.2, 3.5, 3.9} {
		slope := 2 - r
		verdict := "stable"
		if math.Abs(slope) > 1 {
			verdict = "unstable"
		}
		x := settle(r, 0.2, 2000)
		p := period(r, x, 64)
		var vals []string
		for i := 0; i < 4; i++ {
			vals = append(vals, fmt.Sprintf("%.4f", x))
			x = logistic(r, x)
		}
		ps := fmt.Sprint(p)
		if p == 0 {
			ps = "none up to 64"
		}
		fmt.Printf("r=%.1f x*=%.4f slope %+.1f %-8s | settles to %s | period %s\n",
			r, 1-1/r, slope, verdict, strings.Join(vals, " "), ps)
	}

	fmt.Println("\n== Feigenbaum constant from superstable r values ==")
	rs := []float64{2, 1 + math.Sqrt(5)}
	for k := 2; k <= 8; k++ {
		n := len(rs)
		rs = append(rs, superstable(k, rs[n-1]+(rs[n-1]-rs[n-2])/4.669))
	}
	for i := 2; i < len(rs); i++ {
		fmt.Printf("period %-4d r=%.7f  gap ratio %.4f\n", 1<<i, rs[i], (rs[i-1]-rs[i-2])/(rs[i]-rs[i-1]))
	}

	fmt.Println("\n== Lyapunov exponents (positive = chaos) ==")
	for _, r := range []float64{2.8, 3.2, 3.5, 3.9, 4.0} {
		fmt.Printf("r=%.1f  lambda=%+.4f\n", r, lyapunov(r))
	}
	fmt.Printf("ln 2 = %.4f (the exact value at r=4)\n", math.Ln2)

	fmt.Println("\n== Two orbits at r=3.9, starts 0.2 and 0.2+1e-10 ==")
	a, b := 0.2, 0.2+1e-10
	for n := 0; n <= 45; n++ {
		if n%5 == 0 {
			fmt.Printf("n=%-2d a=%.6f b=%.6f gap=%.2e\n", n, a, b, math.Abs(a-b))
		}
		a, b = logistic(3.9, a), logistic(3.9, b)
	}

	fmt.Println("\n== Retry storm: L(n+1) = 100 + g L(n), start 100 ==")
	for _, g := range []float64{0.5, 0.9, 1.1} {
		L := 100.0
		for n := 0; n < 20; n++ {
			L = 100 + g*L
		}
		limit := "no limit, grows forever"
		if g < 1 {
			limit = fmt.Sprintf("limit %.0f", 100/(1-g))
		}
		fmt.Printf("g=%.1f  load after 20 steps %7.0f  %s\n", g, L, limit)
	}

	fmt.Println("\n== Autoscaler: x(n+1) = x(n) + k (100 - x(n-d)), floor 0 ==")
	for _, c := range []struct {
		k float64
		d int
	}{{0.5, 0}, {1.5, 0}, {0.5, 2}, {0.6, 2}, {0.8, 2}} {
		lo, hi := autoscale(c.k, c.d)
		fmt.Printf("k=%.1f d=%d  steps 40-80 range %6.1f to %6.1f\n", c.k, c.d, lo, hi)
	}
	for d := 0; d <= 3; d++ {
		fmt.Printf("delay %d: swings grow once k > %.3f\n", d, 2*math.Sin(math.Pi/float64(2*(2*d+1))))
	}

	fmt.Println("\n== Lorenz system, RK4, step 0.01, start (1,1,1) ==")
	s := vec{1, 1, 1}
	for i := 0; i <= 2000; i++ {
		if i%500 == 0 {
			fmt.Printf("t=%5.1f  x=%8.3f y=%8.3f z=%8.3f\n", float64(i)*0.01, s[0], s[1], s[2])
		}
		s = rk4(s, 0.01)
	}
	for _, eps := range []float64{1e-5, 1e-8, 1e-11} {
		fmt.Printf("start gap %.0e in x -> forecasts split (gap > 1) at t=%.2f\n", eps, divergeTime(eps))
	}

	fmt.Println("\n== Mandelbrot set, re -2.1..0.6, im -1.1..1.1 ==")
	for row := 0; row < 21; row++ {
		im := 1.1 - float64(row)*0.11
		var line strings.Builder
		for col := 0; col < 60; col++ {
			re := -2.1 + float64(col)*0.045
			zr, zi := 0.0, 0.0
			n := 0
			for n < 100 && zr*zr+zi*zi <= 4 {
				zr, zi = zr*zr-zi*zi+re, 2*zr*zi+im
				n++
			}
			switch {
			case n == 100:
				line.WriteByte('#')
			case n > 8:
				line.WriteByte('+')
			case n > 4:
				line.WriteByte('.')
			default:
				line.WriteByte(' ')
			}
		}
		fmt.Println(strings.TrimRight(line.String(), " "))
	}

	fmt.Println("\n== Koch curve ==")
	for lv := 0; lv <= 5; lv++ {
		fmt.Printf("level %d: segments %4d, length %.4f\n", lv, int(math.Pow(4, float64(lv))), math.Pow(4.0/3.0, float64(lv)))
	}
	fmt.Printf("dimension log4/log3 = %.4f\n", math.Log(4)/math.Log(3))
}
