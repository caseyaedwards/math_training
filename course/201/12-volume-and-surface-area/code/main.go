// Volume and surface area formulas, plus what scaling does to each.
package main

import (
	"fmt"
	"math"
)

func boxVolume(l, w, h float64) float64 { return l * w * h }
func boxSurface(l, w, h float64) float64 {
	return 2 * (l*w + l*h + w*h)
}
func cylinderVolume(r, h float64) float64  { return math.Pi * r * r * h }
func cylinderSurface(r, h float64) float64 { return 2*math.Pi*r*r + 2*math.Pi*r*h }
func coneVolume(r, h float64) float64      { return cylinderVolume(r, h) / 3 }
func sphereVolume(r float64) float64       { return 4.0 / 3.0 * math.Pi * r * r * r }
func sphereSurface(r float64) float64      { return 4 * math.Pi * r * r }

func main() {
	fmt.Println("box 4 x 2 x 3: V =", boxVolume(4, 2, 3), " SA =", boxSurface(4, 2, 3))
	fmt.Printf("cylinder r=3 h=10: V = %.2f  SA = %.2f\n", cylinderVolume(3, 10), cylinderSurface(3, 10))
	fmt.Printf("cone r=3 h=4: V = %.2f\n", coneVolume(3, 4))
	fmt.Printf("sphere r=3: V = %.2f  SA = %.2f\n", sphereVolume(3), sphereSurface(3))

	fmt.Println("scale a 4 x 2 x 3 box by k:")
	for _, k := range []float64{1, 2, 3} {
		v := boxVolume(4*k, 2*k, 3*k)
		s := boxSurface(4*k, 2*k, 3*k)
		fmt.Printf("  k=%g  SA = %4g (x%g)  V = %4g (x%g)\n", k, s, s/52, v, v/24)
	}
}
