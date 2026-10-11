// Angle bookkeeping: complements, supplements, the eight angles
// at a transversal, and the angle between clock hands.
package main

import "fmt"

func complement(a float64) float64 { return 90 - a }
func supplement(a float64) float64 { return 180 - a }

// transversal returns angles 1..8 given angle 2 (upper right at the top line).
// Numbering: 1 upper left, 2 upper right, 3 lower left, 4 lower right,
// then 5..8 in the same places at the bottom line.
func transversal(angle2 float64) [9]float64 {
	var a [9]float64
	acute, other := angle2, supplement(angle2)
	a[2], a[3], a[6], a[7] = acute, acute, acute, acute
	a[1], a[4], a[5], a[8] = other, other, other, other
	return a
}

// clockAngle gives the smaller angle between the hands at h:m.
func clockAngle(h, m int) float64 {
	minute := 6 * float64(m)                  // 360 / 60 degrees per minute
	hour := 30*float64(h%12) + 0.5*float64(m) // 360 / 12 per hour, plus drift
	d := hour - minute
	if d < 0 {
		d = -d
	}
	if d > 180 {
		d = 360 - d
	}
	return d
}

func main() {
	fmt.Println("complement of 35:", complement(35))
	fmt.Println("supplement of 35:", supplement(35))
	a := transversal(60)
	for i := 1; i <= 8; i++ {
		fmt.Printf("angle %d = %g\n", i, a[i])
	}
	fmt.Println("clock at 3:00 :", clockAngle(3, 0))
	fmt.Println("clock at 2:30 :", clockAngle(2, 30))
}
