// Triangle checks: the third angle, classification, and similarity.
package main

import (
	"fmt"
	"sort"
)

func thirdAngle(a, b float64) float64 { return 180 - a - b }

// bySides names a triangle from its side lengths.
func bySides(a, b, c float64) string {
	switch {
	case a == b && b == c:
		return "equilateral"
	case a == b || b == c || a == c:
		return "isosceles"
	default:
		return "scalene"
	}
}

// byAngles names a triangle from its three angles.
func byAngles(x, y, z float64) string {
	for _, v := range []float64{x, y, z} {
		if v == 90 {
			return "right"
		}
		if v > 90 {
			return "obtuse"
		}
	}
	return "acute"
}

// similar reports whether two triangles have proportional sides,
// and the scale factor from the first to the second.
func similar(p, q [3]float64) (bool, float64) {
	sort.Float64s(p[:])
	sort.Float64s(q[:])
	k := q[0] / p[0]
	for i := 1; i < 3; i++ {
		if q[i]/p[i] != k {
			return false, 0
		}
	}
	return true, k
}

func main() {
	fmt.Println("angles 50 and 60, third angle:", thirdAngle(50, 60))
	fmt.Println("sides 5, 5, 8:", bySides(5, 5, 8))
	fmt.Println("angles 30, 60, 90:", byAngles(30, 60, 90))
	fmt.Println("angles 20, 30, 130:", byAngles(20, 30, 130))
	ok, k := similar([3]float64{3, 4, 5}, [3]float64{10, 6, 8})
	fmt.Println("3-4-5 and 6-8-10 similar:", ok, "scale factor:", k)
	ok, _ = similar([3]float64{3, 4, 5}, [3]float64{6, 8, 11})
	fmt.Println("3-4-5 and 6-8-11 similar:", ok)
	// Shadow problem: h / 18 = 2 / 3.
	fmt.Println("tree height from shadows:", 18*2.0/3.0, "m")
}
