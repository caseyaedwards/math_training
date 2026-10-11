// The four common distributions, standard library only.
package main

import (
	"fmt"
	"math"
)

func comb(n, k int) float64 {
	out := 1.0
	for i := 0; i < k; i++ {
		out = out * float64(n-i) / float64(i+1)
	}
	return out
}

func binomial(k, n int, p float64) float64 {
	return comb(n, k) * math.Pow(p, float64(k)) * math.Pow(1-p, float64(n-k))
}

func poisson(k int, lambda float64) float64 {
	fact := 1.0
	for i := 2; i <= k; i++ {
		fact *= float64(i)
	}
	return math.Exp(-lambda) * math.Pow(lambda, float64(k)) / fact
}

// normalAbove returns P(X > x) for a normal with mean mu and sd sigma.
func normalAbove(x, mu, sigma float64) float64 {
	z := (x - mu) / sigma
	return 0.5 * math.Erfc(z/math.Sqrt2)
}

func main() {
	fmt.Printf("Binomial(10, 0.3): P(X=3) = %.4f\n", binomial(3, 10, 0.3))
	fmt.Printf("Poisson(3):        P(X=0) = %.4f  P(X=5) = %.4f\n", poisson(0, 3), poisson(5, 3))
	fmt.Printf("Normal(200, 20):   P(X>240) = %.4f\n", normalAbove(240, 200, 20))
	fmt.Printf("Exponential(1):    P(T>2) = %.4f\n", math.Exp(-2))
	fmt.Printf("500 disks at 1%%:   binomial P(0) = %.5f  Poisson P(0) = %.5f\n",
		binomial(0, 500, 0.01), poisson(0, 5))
}
