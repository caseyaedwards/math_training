// Related rates checked by brute force: move time forward a tiny step and measure.
package main

import (
	"fmt"
	"math"
)

func main() {
	dt := 1e-6

	// Ladder: 10 m long, base x(t) = 6 + t metres, top y = sqrt(100 - x^2).
	y := func(t float64) float64 { x := 6 + t; return math.Sqrt(100 - x*x) }
	fmt.Printf("ladder top speed at x = 6: measured %.4f m/s, formula -(x/y)(dx/dt) = %.4f m/s\n",
		(y(dt)-y(0))/dt, -6.0/8.0*1)

	// Cone: V = pi h^3 / 12, filled at 2 m^3/min. Find h(t) by stepping V and inverting.
	h := func(V float64) float64 { return math.Cbrt(12 * V / math.Pi) }
	V4 := math.Pi * 64 / 12 // volume when h = 4
	fmt.Printf("cone level speed at h = 4:  measured %.4f m/min, formula 2/(4 pi) = %.4f m/min\n",
		(h(V4+2*dt)-h(V4))/dt, 2/(4*math.Pi))

	// Ripple: r(t) = 5 + 2t cm, area A = pi r^2.
	A := func(t float64) float64 { r := 5 + 2*t; return math.Pi * r * r }
	fmt.Printf("ripple area rate at r = 5:  measured %.4f cm^2/s, formula 2 pi r dr/dt = %.4f\n",
		(A(dt)-A(0))/dt, 2*math.Pi*5*2)

	// Full mesh: n(t) = 20 + 3t nodes, links L = n(n-1)/2.
	Lk := func(t float64) float64 { n := 20 + 3*t; return n * (n - 1) / 2 }
	fmt.Printf("mesh link rate at n = 20:   measured %.4f links/h, formula ((2n-1)/2)(dn/dt) = %.4f\n",
		(Lk(dt)-Lk(0))/dt, (2*20.0-1)/2*3)
}
