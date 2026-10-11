// Measure theory starter kit: coin sorting, Riemann versus Lebesgue sums,
// covering the rationals, the Cantor set, simple functions climbing to an
// integral, a bump that escapes to infinity, and probability as area.
// Standard library only.
package main

import (
	"fmt"
	"math"
	"math/rand/v2"
	"sort"
)

// coins shows that adding in any order gives the same total.
func coins() {
	pocket := []int{25, 1, 10, 5, 25, 1, 1, 10, 25, 5, 1, 10}
	inOrder := 0
	for _, c := range pocket {
		inOrder += c
	}
	count := map[int]int{}
	for _, c := range pocket {
		count[c]++
	}
	values := []int{}
	for v := range count {
		values = append(values, v)
	}
	sort.Sort(sort.Reverse(sort.IntSlice(values)))
	sorted := 0
	fmt.Printf("Riemann (one coin at a time): total %d cents\n", inOrder)
	fmt.Print("Lebesgue (sort by value):    ")
	for i, v := range values {
		if i > 0 {
			fmt.Print(" + ")
		}
		fmt.Printf("%dx%d", v, count[v])
		sorted += v * count[v]
	}
	fmt.Printf(" = %d cents\n", sorted)
}

// riemannMid approximates the integral of f on [0,1] with n vertical strips.
func riemannMid(f func(float64) float64, n int) float64 {
	sum := 0.0
	h := 1.0 / float64(n)
	for i := 0; i < n; i++ {
		sum += f((float64(i)+0.5)*h) * h
	}
	return sum
}

// lebesgueLayers approximates the integral of x^2 on [0,1] with n horizontal
// layers. Layer at height t has width = length of {x : x^2 > t} = 1 - sqrt(t).
func lebesgueLayers(n int) float64 {
	sum := 0.0
	h := 1.0 / float64(n)
	for k := 0; k < n; k++ {
		t := (float64(k) + 0.5) * h
		sum += (1 - math.Sqrt(t)) * h
	}
	return sum
}

// simpleIntegral integrates the simple function that rounds x^2 down to a
// multiple of 2^-n. The set where k/2^n <= x^2 < (k+1)/2^n has length
// sqrt((k+1)/2^n) - sqrt(k/2^n).
func simpleIntegral(n int) float64 {
	m := 1 << n
	sum := 0.0
	for k := 0; k < m; k++ {
		a := float64(k) / float64(m)
		b := float64(k+1) / float64(m)
		sum += a * (math.Sqrt(b) - math.Sqrt(a))
	}
	return sum
}

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func main() {
	fmt.Println("== Coin sorting ==")
	coins()

	sq := func(x float64) float64 { return x * x }
	fmt.Println()
	fmt.Println("== Integral of x^2 on [0,1], exact 1/3 = 0.333333 ==")
	for _, n := range []int{4, 10, 100, 1000} {
		fmt.Printf("n = %4d  vertical strips %.6f  horizontal layers %.6f\n",
			n, riemannMid(sq, n), lebesgueLayers(n))
	}

	fmt.Println()
	fmt.Println("== Simple functions climb to the integral (monotone convergence) ==")
	for _, n := range []int{1, 2, 3, 4, 6, 8, 12} {
		fmt.Printf("levels 1/%-5d integral %.6f\n", 1<<n, simpleIntegral(n))
	}

	fmt.Println()
	fmt.Println("== Covering the rationals in [0,1] ==")
	eps := 0.01
	seen := map[[2]int]bool{}
	total := 0.0
	k := 0
	for q := 1; q <= 20; q++ {
		for p := 0; p <= q; p++ {
			g := gcd(p, q)
			key := [2]int{p / g, q / g}
			if seen[key] {
				continue
			}
			seen[key] = true
			k++
			total += eps / math.Pow(2, float64(k))
		}
	}
	fmt.Printf("rationals with denominator <= 20: %d\n", k)
	fmt.Printf("interval k has length eps/2^k, eps = %.2f\n", eps)
	fmt.Printf("total length of all %d intervals: %.6f, never more than eps\n", k, total)

	fmt.Println()
	fmt.Println("== Cantor set ==")
	for _, n := range []int{0, 1, 2, 3, 5, 10, 20} {
		pieces := math.Pow(2, float64(n))
		left := math.Pow(2.0/3.0, float64(n))
		fmt.Printf("step %2d: %8.0f pieces, length left %.6f, removed %.6f\n", n, pieces, left, 1-left)
	}

	fmt.Println()
	fmt.Println("== Escaping bump f_n = n on (0, 1/n) ==")
	for _, n := range []int{1, 2, 3, 4, 10, 100} {
		at := 0.0
		if 0.3 < 1.0/float64(n) {
			at = float64(n)
		}
		fmt.Printf("n = %3d  integral %.1f  f_n(0.3) = %.0f\n", n, float64(n)*(1.0/float64(n)), at)
	}
	fmt.Println("limit function is 0 everywhere, integral 0, yet every integral is 1")

	fmt.Println()
	fmt.Println("== Dominated convergence: x^n on [0,1] ==")
	for _, n := range []int{1, 2, 5, 10, 100} {
		pn := func(x float64) float64 { return math.Pow(x, float64(n)) }
		fmt.Printf("n = %3d  integral %.6f  exact 1/(n+1) = %.6f\n", n, riemannMid(pn, 100000), 1/float64(n+1))
	}

	fmt.Println()
	fmt.Println("== Probability as area (100000 darts in the unit square) ==")
	rng := rand.New(rand.NewPCG(1, 2))
	const darts = 100000
	below, inCircle := 0, 0
	for i := 0; i < darts; i++ {
		x, y := rng.Float64(), rng.Float64()
		if x+y < 1 {
			below++
		}
		if x*x+y*y < 1 {
			inCircle++
		}
	}
	fmt.Printf("P(x + y < 1)      ~ %.4f   exact area 0.5\n", float64(below)/darts)
	fmt.Printf("P(x^2 + y^2 < 1)  ~ %.4f   exact area pi/4 = %.4f\n", float64(inCircle)/darts, math.Pi/4)
	hit := 0
	for i := 0; i < darts; i++ {
		if rng.Float64() == 0.5 {
			hit++
		}
	}
	fmt.Printf("P(x = 0.5 exactly) ~ %d hits in %d darts: a point has measure 0\n", hit, darts)
}
