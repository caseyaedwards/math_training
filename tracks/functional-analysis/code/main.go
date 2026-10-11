// Functional analysis starter kit: functions as vectors, norms, inner
// products, projection, Gram-Schmidt, the parallelogram law, operator norms,
// the spectrum of the second derivative, and the kernel trick.
// Standard library only.
package main

import (
	"fmt"
	"math"
)

// integrate approximates the integral of f on [a,b] with the midpoint rule.
func integrate(f func(float64) float64, a, b float64) float64 {
	const n = 200000
	h := (b - a) / n
	sum := 0.0
	for i := 0; i < n; i++ {
		sum += f(a + (float64(i)+0.5)*h)
	}
	return sum * h
}

func inner(f, g func(float64) float64, a, b float64) float64 {
	v := integrate(func(x float64) float64 { return f(x) * g(x) }, a, b)
	if math.Abs(v) < 1e-9 {
		return 0 // hide rounding noise such as -0.000000
	}
	return v
}

func l2(f func(float64) float64, a, b float64) float64 {
	return math.Sqrt(inner(f, f, a, b))
}

func l1(f func(float64) float64, a, b float64) float64 {
	return integrate(func(x float64) float64 { return math.Abs(f(x)) }, a, b)
}

func sup(f func(float64) float64, a, b float64) float64 {
	m := 0.0
	for i := 0; i <= 100000; i++ {
		v := math.Abs(f(a + (b-a)*float64(i)/100000))
		if v > m {
			m = v
		}
	}
	return m
}

// poly is a polynomial stored as coefficients c[0] + c[1] x + c[2] x^2 + ...
type poly []float64

// dot is the exact inner product of two polynomials on [-1, 1].
func dot(p, q poly) float64 {
	s := 0.0
	for i, a := range p {
		for j, b := range q {
			if (i+j)%2 == 0 {
				s += a * b * 2 / float64(i+j+1)
			}
		}
	}
	return s
}

func (p poly) String() string {
	out := ""
	for i, c := range p {
		if math.Abs(c) < 1e-12 {
			continue
		}
		term := fmt.Sprintf("%.4f", c)
		if i == 1 {
			term += " x"
		} else if i > 1 {
			term += fmt.Sprintf(" x^%d", i)
		}
		if out != "" {
			out += " + "
		}
		out += term
	}
	return out
}

func main() {
	fmt.Println("== A function sampled at 5 points is a vector ==")
	f := func(x float64) float64 { return x }
	g := func(x float64) float64 { return 1 - x*x }
	for _, x := range []float64{0, 0.25, 0.5, 0.75, 1} {
		fmt.Printf("x = %.2f  f = %.4f  g = %.4f  f+g = %.4f  2f = %.4f\n", x, f(x), g(x), f(x)+g(x), 2*f(x))
	}

	fmt.Println()
	fmt.Println("== Three norms of f(x) = x on [0,1] ==")
	fmt.Printf("L1  (area under |f|)        %.6f   exact 1/2\n", l1(f, 0, 1))
	fmt.Printf("L2  (root of area of f^2)   %.6f   exact 1/sqrt(3) = %.6f\n", l2(f, 0, 1), 1/math.Sqrt(3))
	fmt.Printf("sup (tallest point)         %.6f   exact 1\n", sup(f, 0, 1))

	fmt.Println()
	fmt.Println("== x^n: small in L2, never small in sup ==")
	for _, n := range []int{1, 5, 20, 100} {
		pn := func(x float64) float64 { return math.Pow(x, float64(n)) }
		fmt.Printf("n = %3d  sup %.4f  L2 %.4f  exact 1/sqrt(2n+1) = %.4f\n", n, sup(pn, 0, 1), l2(pn, 0, 1), 1/math.Sqrt(float64(2*n+1)))
	}

	fmt.Println()
	fmt.Println("== Inner products on [0, 2 pi] ==")
	twoPi := 2 * math.Pi
	sin2 := func(x float64) float64 { return math.Sin(2 * x) }
	fmt.Printf("<sin, cos>     = %+.6f\n", inner(math.Sin, math.Cos, 0, twoPi))
	fmt.Printf("<sin, sin 2x>  = %+.6f\n", inner(math.Sin, sin2, 0, twoPi))
	fmt.Printf("<sin, sin>     = %+.6f   exact pi = %.6f\n", inner(math.Sin, math.Sin, 0, twoPi), math.Pi)

	fmt.Println()
	fmt.Println("== Project f(x) = x on [-pi, pi] onto sin(nx) ==")
	coef := make([]float64, 9)
	for k := 1; k <= 8; k++ {
		kk := float64(k)
		coef[k] = inner(f, func(t float64) float64 { return math.Sin(kk * t) }, -math.Pi, math.Pi) / math.Pi
	}
	for n := 1; n <= 4; n++ {
		fmt.Printf("b%d = %+.4f   exact 2(-1)^(n+1)/n = %+.4f\n", n, coef[n], 2*math.Pow(-1, float64(n+1))/float64(n))
	}
	for _, n := range []int{1, 2, 4, 8} {
		sq := func(x float64) float64 {
			e := f(x)
			for k := 1; k <= n; k++ {
				e -= coef[k] * math.Sin(float64(k)*x)
			}
			return e * e
		}
		fmt.Printf("terms %d  L2 error %.4f\n", n, math.Sqrt(integrate(sq, -math.Pi, math.Pi)))
	}

	fmt.Println()
	fmt.Println("== Gram-Schmidt on 1, x, x^2 over [-1, 1] ==")
	basis := []poly{{1}, {0, 1}, {0, 0, 1}}
	var ortho []poly
	for _, v := range basis {
		w := append(poly{}, v...)
		for _, e := range ortho {
			c := dot(v, e) / dot(e, e)
			for len(w) < len(e) {
				w = append(w, 0)
			}
			for i := range e {
				w[i] -= c * e[i]
			}
		}
		ortho = append(ortho, w)
		fmt.Printf("e%d = %s\n", len(ortho)-1, w)
	}
	fmt.Printf("<e0, e2> = %.4f  <e1, e2> = %.4f\n", dot(ortho[0], ortho[2]), dot(ortho[1], ortho[2]))

	fmt.Println()
	fmt.Println("== Parallelogram law with f = 1, g = x on [0,1] ==")
	one := func(x float64) float64 { return 1 }
	sum := func(x float64) float64 { return 1 + x }
	diff := func(x float64) float64 { return 1 - x }
	lhs2 := math.Pow(l2(sum, 0, 1), 2) + math.Pow(l2(diff, 0, 1), 2)
	rhs2 := 2*math.Pow(l2(one, 0, 1), 2) + 2*math.Pow(l2(f, 0, 1), 2)
	lhsS := math.Pow(sup(sum, 0, 1), 2) + math.Pow(sup(diff, 0, 1), 2)
	rhsS := 2*math.Pow(sup(one, 0, 1), 2) + 2*math.Pow(sup(f, 0, 1), 2)
	fmt.Printf("L2 norm:  %.4f vs %.4f  holds: comes from an inner product\n", lhs2, rhs2)
	fmt.Printf("sup norm: %.4f vs %.4f  fails: no inner product behind it\n", lhsS, rhsS)

	fmt.Println()
	fmt.Println("== Operator norm of A = [[2,1],[1,2]] by power iteration ==")
	v := [2]float64{1, 0}
	for i := 1; i <= 20; i++ {
		w := [2]float64{2*v[0] + v[1], v[0] + 2*v[1]}
		n := math.Hypot(w[0], w[1])
		v = [2]float64{w[0] / n, w[1] / n}
		if i == 1 || i == 5 || i == 20 {
			fmt.Printf("step %2d  stretch %.6f  direction (%.4f, %.4f)\n", i, n, v[0], v[1])
		}
	}

	fmt.Println()
	fmt.Println("== Differentiation is unbounded: f_n = sin(nx) on [0, 2 pi] ==")
	for _, n := range []int{1, 2, 10, 100} {
		k := float64(n)
		fn := func(x float64) float64 { return math.Sin(k * x) }
		dfn := func(x float64) float64 { return k * math.Cos(k*x) }
		a, b := l2(fn, 0, twoPi), l2(dfn, 0, twoPi)
		fmt.Printf("n = %3d  ||f|| = %.4f  ||f'|| = %8.4f  ratio %6.1f\n", n, a, b, b/a)
	}

	fmt.Println()
	fmt.Println("== Spectrum of -d^2/dx^2 on [0,1] with ends fixed (100 grid points) ==")
	const N = 100
	h := 1.0 / (N + 1)
	for k := 1; k <= 4; k++ {
		u := make([]float64, N)
		for i := range u {
			u[i] = math.Sin(float64(k) * math.Pi * float64(i+1) * h)
		}
		num, den := 0.0, 0.0
		for i := range u {
			left, right := 0.0, 0.0
			if i > 0 {
				left = u[i-1]
			}
			if i < N-1 {
				right = u[i+1]
			}
			au := (2*u[i] - left - right) / (h * h)
			num += u[i] * au
			den += u[i] * u[i]
		}
		kp := float64(k) * math.Pi
		fmt.Printf("mode %d  eigenvalue %9.4f  continuous (k pi)^2 = %9.4f\n", k, num/den, kp*kp)
	}

	fmt.Println()
	fmt.Println("== Kernel trick: (xy + 1)^2 equals phi(x).phi(y), phi(x) = (x^2, sqrt2 x, 1) ==")
	phi := func(x float64) [3]float64 { return [3]float64{x * x, math.Sqrt2 * x, 1} }
	for _, p := range [][2]float64{{1, 2}, {-1.5, 0.5}, {3, -2}} {
		x, y := p[0], p[1]
		k := math.Pow(x*y+1, 2)
		a, b := phi(x), phi(y)
		d := a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
		fmt.Printf("x = %+.1f y = %+.1f  kernel %7.4f  feature dot %7.4f\n", x, y, k, d)
	}

	fmt.Println()
	fmt.Println("== Measuring a quantum-style state psi = 0.6 e1 + 0.8 e2 ==")
	c1, c2 := 0.6, 0.8
	fmt.Printf("||psi||^2 = %.2f   P(e1) = %.2f   P(e2) = %.2f\n", c1*c1+c2*c2, c1*c1, c2*c2)
}
