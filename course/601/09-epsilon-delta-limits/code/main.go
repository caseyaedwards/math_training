// Spot-check a proposed delta on a fine grid of inputs. Evidence, not proof.
package main

import "fmt"

// check samples x in (a - d, a + d) and reports the worst output error.
func check(f func(float64) float64, a, L, d float64) float64 {
	worst := 0.0
	const steps = 200000
	for i := 1; i < steps; i++ {
		x := a - d + 2*d*float64(i)/steps
		if x == a {
			continue
		}
		e := f(x) - L
		if e < 0 {
			e = -e
		}
		if e > worst {
			worst = e
		}
	}
	return worst
}

func main() {
	sq := func(x float64) float64 { return x * x }
	good := func(eps float64) float64 { return min(1, eps/5) }
	naive := func(eps float64) float64 { return eps / 2 }
	for _, eps := range []float64{4, 1, 0.1, 0.001} {
		g, n := good(eps), naive(eps)
		fmt.Printf("eps = %-6g delta=min(1,eps/5)=%-7g worst=%.6f ok=%-5v | delta=eps/2=%-7g worst=%.6f ok=%v\n",
			eps, g, check(sq, 2, 4, g), check(sq, 2, 4, g) < eps,
			n, check(sq, 2, 4, n), check(sq, 2, 4, n) < eps)
	}
}
