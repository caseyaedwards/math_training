// Algebraic geometry starter kit: Pythagorean triples from lines through a
// circle, conic types, Bezout checks, the chord-and-tangent group law on
// y^2 = x^3 - x + 1 over the rationals, and the same curve mod 29 with a toy
// Diffie-Hellman key exchange. Standard library only.
package main

import (
	"fmt"
	"math"
	"math/big"
)

// ---------- points on y^2 = x^3 + a x + b over the rationals ----------

// RPoint is a rational point. Inf marks the point at infinity (the zero).
type RPoint struct {
	X, Y *big.Rat
	Inf  bool
}

func r(n int64) *big.Rat { return big.NewRat(n, 1) }

// addQ adds two rational points with the chord-and-tangent rule.
func addQ(p, q RPoint, a *big.Rat) RPoint {
	if p.Inf {
		return q
	}
	if q.Inf {
		return p
	}
	var lam big.Rat
	if p.X.Cmp(q.X) == 0 {
		var s big.Rat
		if s.Add(p.Y, q.Y).Sign() == 0 {
			return RPoint{Inf: true} // vertical line: P + (-P) = 0
		}
		// tangent slope (3x^2 + a) / (2y)
		var num, den big.Rat
		num.Mul(p.X, p.X).Mul(&num, r(3)).Add(&num, a)
		den.Mul(p.Y, r(2))
		lam.Quo(&num, &den)
	} else {
		var num, den big.Rat
		num.Sub(q.Y, p.Y)
		den.Sub(q.X, p.X)
		lam.Quo(&num, &den)
	}
	x := new(big.Rat).Mul(&lam, &lam)
	x.Sub(x, p.X).Sub(x, q.X)
	y := new(big.Rat).Sub(p.X, x)
	y.Mul(y, &lam).Sub(y, p.Y)
	return RPoint{X: x, Y: y}
}

func (p RPoint) String() string {
	if p.Inf {
		return "O (infinity)"
	}
	return fmt.Sprintf("(%s, %s)", p.X.RatString(), p.Y.RatString())
}

// ---------- the same curve over the integers mod p ----------

// FPoint is a point mod p. Inf marks the point at infinity.
type FPoint struct {
	X, Y int
	Inf  bool
}

func mod(x, p int) int { return ((x % p) + p) % p }

// inv returns the inverse of x mod a prime p by Fermat: x^(p-2).
func inv(x, p int) int {
	res, b, e := 1, mod(x, p), p-2
	for e > 0 {
		if e&1 == 1 {
			res = res * b % p
		}
		b = b * b % p
		e >>= 1
	}
	return res
}

func addF(P, Q FPoint, a, p int) FPoint {
	if P.Inf {
		return Q
	}
	if Q.Inf {
		return P
	}
	if P.X == Q.X && mod(P.Y+Q.Y, p) == 0 {
		return FPoint{Inf: true}
	}
	var lam int
	if P == Q {
		lam = mod((3*P.X*P.X+a)*inv(2*P.Y, p), p)
	} else {
		lam = mod((Q.Y-P.Y)*inv(Q.X-P.X, p), p)
	}
	x := mod(lam*lam-P.X-Q.X, p)
	return FPoint{X: x, Y: mod(lam*(P.X-x)-P.Y, p)}
}

// mulF computes k*P by double-and-add: about log2(k) steps.
func mulF(k int, P FPoint, a, p int) FPoint {
	R := FPoint{Inf: true}
	for k > 0 {
		if k&1 == 1 {
			R = addF(R, P, a, p)
		}
		P = addF(P, P, a, p)
		k >>= 1
	}
	return R
}

func (p FPoint) String() string {
	if p.Inf {
		return "O"
	}
	return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}

func main() {
	fmt.Println("== Rational points on x^2 + y^2 = 1 from slopes t = m/n ==")
	for _, mn := range [][2]int{{1, 2}, {2, 3}, {1, 4}, {3, 4}, {4, 5}} {
		m, n := mn[0], mn[1]
		a, b, c := n*n-m*m, 2*m*n, n*n+m*m
		fmt.Printf("t = %d/%d -> (%d/%d, %d/%d) -> %d^2 + %d^2 = %d^2 (%d = %d)\n",
			m, n, a, c, b, c, a, b, c, a*a+b*b, c*c)
	}

	fmt.Println("\n== Conic type from B^2 - 4AC ==")
	for _, cn := range []struct {
		name    string
		A, B, C float64
	}{{"x^2/4 + y^2 = 1", 0.25, 0, 1}, {"y = x^2", 1, 0, 0}, {"x^2 - y^2 = 1", 1, 0, -1}, {"xy = 1", 0, 1, 0}} {
		d := cn.B*cn.B - 4*cn.A*cn.C
		kind := "parabola"
		if d < 0 {
			kind = "ellipse"
		} else if d > 0 {
			kind = "hyperbola"
		}
		fmt.Printf("%-16s B^2 - 4AC = %5.2f -> %s\n", cn.name, d, kind)
	}

	fmt.Println("\n== Bezout checks ==")
	s := 2 / math.Sqrt(5)
	count := 0
	for _, sx := range []float64{-1, 1} {
		for _, sy := range []float64{-1, 1} {
			x, y := sx*s, sy*s
			e1, e2 := x*x/4+y*y-1, x*x+y*y/4-1
			if math.Abs(e1) < 1e-12 && math.Abs(e2) < 1e-12 {
				count++
			}
		}
	}
	fmt.Printf("x^2/4 + y^2 = 1 and x^2 + y^2/4 = 1: %d common points at (+-%.3f, +-%.3f)\n", count, s, s)
	fmt.Printf("y = x^3 - x and y = 0.3x: x = 0 and x = +-%.3f, so 3 points\n", math.Sqrt(1.3))
	for _, c := range []float64{0.5, 1, 1.5} {
		fmt.Printf("x^2 + y^2 = 1 and y = %.1f: x^2 = %+.2f\n", c, 1-c*c)
	}

	fmt.Println("\n== y^2 = x^3 - x + 1 over the rationals ==")
	a := r(-1)
	P := RPoint{X: r(0), Y: r(1)}
	Q := RPoint{X: r(1), Y: r(1)}
	fmt.Println("P =", P, " Q =", Q)
	fmt.Println("P + Q =", addQ(P, Q, a))
	fmt.Println("2Q    =", addQ(Q, Q, a))
	fmt.Println("P + (-P) =", addQ(P, RPoint{X: r(0), Y: r(-1)}, a))
	R := P
	for k := 2; k <= 6; k++ {
		R = addQ(R, P, a)
		fmt.Printf("%dP = %v\n", k, R)
	}

	fmt.Println("\n== The same curve mod 29 ==")
	const p, A, B = 29, -1, 1
	n := 1 // the point at infinity
	for x := 0; x < p; x++ {
		for y := 0; y < p; y++ {
			if mod(y*y-(x*x*x+A*x+B), p) == 0 {
				n++
			}
		}
	}
	fmt.Printf("points: %d, Hasse bound: |%d - %d| = %d <= 2 sqrt(29) = %.2f\n", n, n, p+1, n-(p+1), 2*math.Sqrt(p))
	G := FPoint{X: 0, Y: 1}
	fmt.Print("multiples of G = (0, 1):")
	for k := 1; k <= 6; k++ {
		fmt.Printf(" %v", mulF(k, G, A, p))
	}
	fmt.Println()
	order := 1
	for X := G; !X.Inf; X = addF(X, G, A, p) {
		order++
	}
	fmt.Printf("order of G: %d (37G = %v)\n", order, mulF(37, G, A, p))

	alice, bob := 7, 11
	pa, pb := mulF(alice, G, A, p), mulF(bob, G, A, p)
	fmt.Printf("toy ECDH: Alice sends %dG = %v, Bob sends %dG = %v\n", alice, pa, bob, pb)
	fmt.Printf("Alice computes %d * %v = %v\n", alice, pb, mulF(alice, pb, A, p))
	fmt.Printf("Bob computes   %d * %v = %v\n", bob, pa, mulF(bob, pa, A, p))
}
