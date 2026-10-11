// The unit circle and radians: conversions, (cos, sin) coordinates,
// wrapping angles, arc length and the angular speed of a disk.
// Run: go run main.go
package main

import (
	"fmt"
	"math"
)

func toRad(d float64) float64 { return d * math.Pi / 180 }
func toDeg(r float64) float64 { return r * 180 / math.Pi }

// wrap reduces any angle in degrees to [0, 360), like a clock or a modulo.
func wrap(d float64) float64 {
	m := math.Mod(d, 360)
	if m < 0 {
		m += 360
	}
	return m
}

func main() {
	fmt.Printf("1 radian = %.4f degrees\n", toDeg(1))
	fmt.Printf("150 degrees = %.4f rad = 5π/6 = %.4f\n", toRad(150), 5*math.Pi/6)

	fmt.Println(" deg   (cos, sin)")
	for d := 0.0; d < 360; d += 45 {
		c, s := math.Cos(toRad(d)), math.Sin(toRad(d))
		// Round tiny floating-point noise like 6e-17 to 0 for display.
		if math.Abs(c) < 1e-12 {
			c = 0
		}
		if math.Abs(s) < 1e-12 {
			s = 0
		}
		fmt.Printf("%4.0f   (%7.4f, %7.4f)\n", d, c, s)
	}

	for _, d := range []float64{420, -90, 1000} {
		fmt.Printf("angle %5.0f wraps to %3.0f\n", d, wrap(d))
	}

	fmt.Printf("arc: r = 10 cm, θ = 1.5 rad -> s = %.1f cm\n", 10*1.5)

	rpm := 7200.0
	omega := rpm * 2 * math.Pi / 60 // radians per second
	fmt.Printf("7200 rpm disk: ω = %.1f rad/s, rim speed at 4.5 cm = %.1f m/s\n", omega, omega*0.045)
}
