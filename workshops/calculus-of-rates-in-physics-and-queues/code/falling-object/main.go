// falling-object integrates acceleration to velocity to height.
//
// A ball drops from rest at 100 m. With a(t) = -9.8 m/s^2:
//
//	v(t) = -9.8t        h(t) = 100 - 4.9t^2
//
// The program prints the exact motion, the impact time and speed, then runs
// explicit Euler integration with shrinking dt and shows the error shrink.
//
// Run from the workshop folder: go run ./code/falling-object
package main

import (
	"fmt"
	"math"
	"strings"
)

const (
	g  = -9.8  // acceleration in m/s^2
	h0 = 100.0 // starting height in m
)

func exact(t float64) (h, v float64) {
	return h0 + 0.5*g*t*t, g*t + 0.0 // + 0.0 turns -0 into 0
}

// euler moves with the old velocity, then updates the velocity.
func euler(dt, tEnd float64) (h, v float64) {
	h, v = h0, 0.0
	n := int(math.Round(tEnd / dt))
	for i := 0; i < n; i++ {
		h += v * dt
		v += g * dt
	}
	return h, v
}

func main() {
	tHit := math.Sqrt(2 * h0 / -g)
	fmt.Println("=== Exact motion: h(t) = 100 - 4.9 t^2, v(t) = -9.8 t ===")
	fmt.Printf("%6s %8s %9s  height bar (1 # = 4 m)\n", "t (s)", "h (m)", "v (m/s)")
	for i := 0; i <= 9; i++ {
		t := float64(i) * 0.5
		h, v := exact(t)
		fmt.Printf("%6.1f %8.2f %9.2f  %s\n", t, h, v, strings.Repeat("#", int(math.Round(h/4))))
	}
	_, v := exact(tHit)
	fmt.Printf("impact: t = sqrt(100 / 4.9) = %.4f s, speed = 9.8 * t = %.2f m/s\n", tHit, -v)
	fmt.Println()

	fmt.Println("=== Euler integration vs exact at t = 4 s (exact h = 21.6 m) ===")
	h4, _ := exact(4)
	fmt.Printf("%8s %6s %10s %10s %11s\n", "dt (s)", "steps", "Euler h", "error (m)", "error / dt")
	for _, dt := range []float64{1, 0.5, 0.1, 0.01, 0.001} {
		he, _ := euler(dt, 4)
		err := he - h4
		fmt.Printf("%8g %6d %10.4f %10.4f %11.3f\n", dt, int(math.Round(4/dt)), he, err, err/dt)
	}
	fmt.Println("error / dt stays at 19.6: halve dt and the error halves (first-order method)")
	fmt.Println()

	fmt.Println("=== Impact time found by stepping until h <= 0 ===")
	for _, dt := range []float64{0.5, 0.1, 0.01, 0.001} {
		h, v, t := h0, 0.0, 0.0
		for h > 0 {
			h += v * dt
			v += g * dt
			t += dt
		}
		fmt.Printf("dt = %-6g first step with h <= 0 at t = %.4f s (exact %.4f)\n", dt, t, tHit)
	}
}
