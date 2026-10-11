// Partial derivatives, gradient descent, and a double Riemann sum.
package main

import "fmt"

// latency in ms as a function of load (req/s) and replica count.
func latency(load, replicas float64) float64 { return 10 + 0.5*load/replicas }

func main() {
	h := 1e-4
	load, reps := 1000.0, 10.0
	dLoad := (latency(load+h, reps) - latency(load-h, reps)) / (2 * h)
	dReps := (latency(load, reps+h) - latency(load, reps-h)) / (2 * h)
	fmt.Printf("latency %.1f ms; d/dload = %.4f ms per req/s; d/dreplicas = %.4f ms per replica\n",
		latency(load, reps), dLoad, dReps)

	// Gradient descent on f(x, y) = x^2 + 4y^2, gradient (2x, 8y), step 0.2.
	x, y := 2.6, 1.0
	for step := 0; step <= 12; step++ {
		if step%3 == 0 {
			fmt.Printf("  step %2d: (%8.5f, %8.5f)  f = %.6f\n", step, x, y, x*x+4*y*y)
		}
		x, y = x-0.2*2*x, y-0.2*8*y
	}

	// Double Riemann sum of f(x, y) = x + y over [0, 3] x [0, 2] with midpoints.
	for _, n := range []int{2, 6, 100} {
		dx, dy := 3/float64(n), 2/float64(n)
		total := 0.0
		for i := 0; i < n; i++ {
			for j := 0; j < n; j++ {
				xm, ym := (float64(i)+0.5)*dx, (float64(j)+0.5)*dy
				total += (xm + ym) * dx * dy
			}
		}
		fmt.Printf("  %3d x %-3d cells: volume = %.6f\n", n, n, total)
	}
}
