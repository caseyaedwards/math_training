// Differential geometry starter kit: curvature of plane and space curves,
// Gaussian curvature by finite differences, a spherical triangle, great
// circle distances and the relativity correction for GPS clocks.
// Standard library only.
package main

import (
	"fmt"
	"math"
)

type vec [3]float64

func sub(a, b vec) vec           { return vec{a[0] - b[0], a[1] - b[1], a[2] - b[2]} }
func scale(a vec, s float64) vec { return vec{a[0] * s, a[1] * s, a[2] * s} }
func dot(a, b vec) float64       { return a[0]*b[0] + a[1]*b[1] + a[2]*b[2] }
func norm(a vec) float64         { return math.Sqrt(dot(a, a)) }
func cross(a, b vec) vec {
	return vec{a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]}
}

// derivs returns numerical first, second and third derivatives of a curve.
func derivs(r func(float64) vec, t float64) (vec, vec, vec) {
	h := 1e-3
	p2, p1, m1, m2 := r(t+2*h), r(t+h), r(t-h), r(t-2*h)
	d1 := scale(sub(p1, m1), 1/(2*h))
	d2 := scale(sub(sub(p1, r(t)), sub(r(t), m1)), 1/(h*h))
	d3 := scale(sub(sub(p2, scale(p1, 2)), sub(m2, scale(m1, 2))), 1/(2*h*h*h))
	return d1, d2, d3
}

// curvature and torsion of a space curve: |r' x r”| / |r'|^3 and
// (r' x r”) . r”' / |r' x r”|^2.
func curvature(r func(float64) vec, t float64) (float64, float64) {
	d1, d2, d3 := derivs(r, t)
	c := cross(d1, d2)
	return norm(c) / math.Pow(norm(d1), 3), dot(c, d3) / dot(c, c)
}

// gaussK estimates the Gaussian curvature of the graph z = f(x, y) at (0, 0):
// K = (fxx fyy - fxy^2) / (1 + fx^2 + fy^2)^2.
func gaussK(f func(x, y float64) float64) float64 {
	h := 1e-4
	fx := (f(h, 0) - f(-h, 0)) / (2 * h)
	fy := (f(0, h) - f(0, -h)) / (2 * h)
	fxx := (f(h, 0) - 2*f(0, 0) + f(-h, 0)) / (h * h)
	fyy := (f(0, h) - 2*f(0, 0) + f(0, -h)) / (h * h)
	fxy := (f(h, h) - f(h, -h) - f(-h, h) + f(-h, -h)) / (4 * h * h)
	return (fxx*fyy - fxy*fxy) / math.Pow(1+fx*fx+fy*fy, 2)
}

func sphere(latDeg, lonDeg float64) vec {
	la, lo := latDeg*math.Pi/180, lonDeg*math.Pi/180
	return vec{math.Cos(la) * math.Cos(lo), math.Cos(la) * math.Sin(lo), math.Sin(la)}
}

// angleAt returns the angle of a spherical triangle at vertex a.
func angleAt(a, b, c vec) float64 {
	tb := sub(b, scale(a, dot(a, b))) // direction toward b in the tangent plane at a
	tc := sub(c, scale(a, dot(a, c)))
	return math.Acos(dot(tb, tc) / (norm(tb) * norm(tc)))
}

func main() {
	fmt.Println("== Curvature of y = x^2 ==")
	parab := func(t float64) vec { return vec{t, t * t, 0} }
	for _, x := range []float64{0, 0.5, 1} {
		k, _ := curvature(parab, x)
		fmt.Printf("x = %.1f: kappa = %.4f, radius = %.4f\n", x, k, 1/k)
	}

	fmt.Println("\n== Helix (cos t, sin t, 0.25 t) ==")
	helix := func(t float64) vec { return vec{math.Cos(t), math.Sin(t), 0.25 * t} }
	k, tau := curvature(helix, 1.0)
	fmt.Printf("kappa = %.4f (formula %.4f), torsion = %.4f (formula %.4f)\n", k, 1/1.0625, tau, 0.25/1.0625)

	fmt.Println("\n== Gaussian curvature at the origin ==")
	surfaces := []struct {
		name string
		f    func(x, y float64) float64
	}{
		{"unit sphere cap", func(x, y float64) float64 { return 1 - math.Sqrt(1-x*x-y*y) }},
		{"sphere of radius 2", func(x, y float64) float64 { return 2 - math.Sqrt(4-x*x-y*y) }},
		{"cylinder", func(x, y float64) float64 { return 1 - math.Sqrt(1-x*x) }},
		{"saddle (x^2-y^2)/2", func(x, y float64) float64 { return (x*x - y*y) / 2 }},
		{"saddle x^2-y^2", func(x, y float64) float64 { return x*x - y*y }},
	}
	for _, s := range surfaces {
		fmt.Printf("%-20s K = %+.4f\n", s.name, gaussK(s.f))
	}

	fmt.Println("\n== A triangle on the unit sphere ==")
	n, a, b := sphere(90, 0), sphere(0, 0), sphere(0, 90)
	sum := angleAt(n, a, b) + angleAt(a, b, n) + angleAt(b, n, a)
	fmt.Printf("angle sum = %.1f degrees, excess = %.4f rad, area/R^2 = %.4f\n", sum*180/math.Pi, sum-math.Pi, 4*math.Pi/8)

	fmt.Println("\n== From 60N 0E to 60N 90E on Earth (R = 6371 km) ==")
	const R = 6371.0
	p, q := sphere(60, 0), sphere(60, 90)
	gc := math.Acos(dot(p, q)) * R
	lat := math.Cos(60*math.Pi/180) * (math.Pi / 2) * R
	fmt.Printf("along the latitude: %.0f km\ngreat circle:       %.0f km (saves %.0f km)\n", lat, gc, lat-gc)

	fmt.Println("\n== GPS clock drift per day ==")
	const (
		GM = 3.986004418e14 // m^3/s^2
		c  = 299792458.0    // m/s
		rE = 6.371e6        // m
		rS = 2.6561e7       // GPS orbit radius, m
		dy = 86400.0
	)
	grav := GM / (c * c) * (1/rE - 1/rS) * dy * 1e6
	v := math.Sqrt(GM / rS)
	speed := -v * v / (2 * c * c) * dy * 1e6
	net := grav + speed
	fmt.Printf("orbital speed %.0f m/s\n", v)
	fmt.Printf("gravity: %+.1f us, speed: %+.1f us, net: %+.1f us per day\n", grav, speed, net)
	fmt.Printf("uncorrected position error: %.1f km per day\n", net*1e-6*c/1000)
}
