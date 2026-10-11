// Area formulas, and pi estimated by counting grid squares inside a circle.
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println("rectangle 8 x 5: area", 8*5, "perimeter", 2*(8+5))
	fmt.Println("triangle b=10 h=6: area", 0.5*10*6)
	fmt.Println("trapezoid 6, 10, h=4: area", 0.5*(6+10)*4)
	r := 3.0
	fmt.Printf("circle r=3: C = %.2f, A = %.2f\n", 2*math.Pi*r, math.Pi*r*r)
	fmt.Printf("track 100 by 60 with round ends: perimeter %.2f\n", 200+math.Pi*60)

	// Count unit squares whose centers lie inside a circle of radius n.
	// Area / n^2 approaches pi as n grows: area really is pi r^2.
	for _, n := range []int{10, 100, 1000} {
		count := 0
		for x := -n; x < n; x++ {
			for y := -n; y < n; y++ {
				cx, cy := float64(x)+0.5, float64(y)+0.5
				if cx*cx+cy*cy <= float64(n*n) {
					count++
				}
			}
		}
		fmt.Printf("radius %4d: %8d squares, squares / r^2 = %.5f\n", n, count, float64(count)/float64(n*n))
	}
	fmt.Printf("pi                                      = %.5f\n", math.Pi)
}
