// 2D vectors: add, scale, length, dot product, angle, projection.
package main

import (
	"fmt"
	"math"
)

type vec struct{ x, y float64 }

func (a vec) add(b vec) vec       { return vec{a.x + b.x, a.y + b.y} }
func (a vec) scale(k float64) vec { return vec{k * a.x, k * a.y} }
func (a vec) dot(b vec) float64   { return a.x*b.x + a.y*b.y }
func (a vec) length() float64     { return math.Sqrt(a.dot(a)) }
func (a vec) angleTo(b vec) float64 {
	return math.Acos(a.dot(b)/(a.length()*b.length())) * 180 / math.Pi
}

func main() {
	u, v := vec{3, 1}, vec{1, 3}
	fmt.Println("u + v =", u.add(v))
	fmt.Println("2v    =", v.scale(2))
	fmt.Println("|(3,4)| =", vec{3, 4}.length())

	a, b := vec{4, 1}, vec{2, 3}
	fmt.Println("a . b =", a.dot(b))
	fmt.Printf("angle  = %.1f degrees\n", a.angleTo(b))
	fmt.Printf("shadow of b on a: length %.3f, vector (%.3f, %.3f)\n",
		a.dot(b)/a.length(), a.scale(a.dot(b)/a.dot(a)).x, a.scale(a.dot(b)/a.dot(a)).y)
	fmt.Println("(2,3) . (-3,2) =", vec{2, 3}.dot(vec{-3, 2}), "-> perpendicular")
}
