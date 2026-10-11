// Differential equations starter kit: Euler and RK4 steppers, logistic
// growth, Newton cooling, a draining queue and a damped spring.
// Standard library only.
package main

import (
	"fmt"
	"math"
)

// F is the right-hand side of y' = F(t, y) for a system of equations.
type F func(t float64, y []float64) []float64

func axpy(y []float64, h float64, k []float64) []float64 {
	out := make([]float64, len(y))
	for i := range y {
		out[i] = y[i] + h*k[i]
	}
	return out
}

func euler(f F, y []float64, t, h float64, n int) []float64 {
	for i := 0; i < n; i++ {
		y = axpy(y, h, f(t, y))
		t += h
	}
	return y
}

func rk4(f F, y []float64, t, h float64, n int) []float64 {
	for i := 0; i < n; i++ {
		k1 := f(t, y)
		k2 := f(t+h/2, axpy(y, h/2, k1))
		k3 := f(t+h/2, axpy(y, h/2, k2))
		k4 := f(t+h, axpy(y, h, k3))
		for j := range y {
			y[j] += h / 6 * (k1[j] + 2*k2[j] + 2*k3[j] + k4[j])
		}
		t += h
	}
	return y
}

func main() {
	grow := func(t float64, y []float64) []float64 { return []float64{y[0]} }
	fmt.Println("== y' = y, y(0) = 1: estimate y(1) = e ==")
	for _, n := range []int{2, 10, 100} {
		h := 1 / float64(n)
		fmt.Printf("h = %-5g Euler %.6f   RK4 %.10f\n", h, euler(grow, []float64{1}, 0, h, n)[0], rk4(grow, []float64{1}, 0, h, n)[0])
	}
	fmt.Printf("exact          %.10f\n", math.E)

	fmt.Println("\n== Logistic y' = y(1 - y), y(0) = 0.1 ==")
	logi := func(t float64, y []float64) []float64 { return []float64{y[0] * (1 - y[0])} }
	for _, T := range []float64{0, 2, 4, 6, 8} {
		got := rk4(logi, []float64{0.1}, 0, 0.01, int(math.Round(T/0.01)))[0]
		fmt.Printf("t = %.0f  y = %.4f  exact %.4f\n", T, got, 1/(1+9*math.Exp(-T)))
	}

	fmt.Println("\n== Newton cooling: server at 90 C in a 20 C room, k = 0.1/min ==")
	for _, T := range []float64{0, 10, 20, 30} {
		fmt.Printf("t = %2.0f min  T = %.1f C\n", T, 20+70*math.Exp(-0.1*T))
	}
	fmt.Printf("time to reach 30 C: %.1f min\n", math.Log(70.0/10)/0.1)

	fmt.Println("\n== Queue: backlog 5,000, arrivals 900/s, service 1,000/s ==")
	backlog, lambda, mu := 5000.0, 900.0, 1000.0
	fmt.Printf("dQ/dt = %.0f - %.0f = %.0f per second, drains in %.0f s\n", lambda, mu, lambda-mu, backlog/(mu-lambda))

	fmt.Println("\n== Damped spring y'' + c y' + y = 0 ==")
	for _, c := range []float64{0.4, 2, 5} {
		disc := c*c - 4
		kind := "critically damped"
		if disc < 0 {
			kind = "underdamped (oscillates)"
		} else if disc > 0 {
			kind = "overdamped"
		}
		spring := func(t float64, y []float64) []float64 { return []float64{y[1], -c*y[1] - y[0]} }
		y := rk4(spring, []float64{1, 0}, 0, 0.01, 300)
		fmt.Printf("c = %-3g c^2 - 4 = %5.2f  %-25s y(3) = %+.4f\n", c, disc, kind, y[0])
	}
}
