// Eigenvalues of a 2x2 matrix, power iteration, and a Markov chain steady state.
package main

import (
	"fmt"
	"math"
)

type mat [2][2]float64
type vec [2]float64

func (m mat) apply(v vec) vec {
	return vec{m[0][0]*v[0] + m[0][1]*v[1], m[1][0]*v[0] + m[1][1]*v[1]}
}

// eigenvalues solves l^2 - (trace) l + det = 0 with the quadratic formula.
func eigenvalues(m mat) (float64, float64) {
	tr := m[0][0] + m[1][1]
	det := m[0][0]*m[1][1] - m[0][1]*m[1][0]
	disc := tr*tr - 4*det
	if disc < 0 {
		return math.NaN(), math.NaN() // no real eigenvalues: every vector turns
	}
	return (tr + math.Sqrt(disc)) / 2, (tr - math.Sqrt(disc)) / 2
}

func main() {
	A := mat{{2, 1}, {1, 2}}
	l1, l2 := eigenvalues(A)
	fmt.Println("eigenvalues of [[2,1],[1,2]]:", l1, l2)
	fmt.Println("A(1,1)  =", A.apply(vec{1, 1}), " A(1,-1) =", A.apply(vec{1, -1}))
	l1, l2 = eigenvalues(mat{{4, 1}, {2, 3}})
	fmt.Println("eigenvalues of [[4,1],[2,3]]:", l1, l2)
	l1, _ = eigenvalues(mat{{0, -1}, {1, 0}})
	fmt.Println("rotation by 90 degrees:", l1)

	// Power iteration: apply A again and again, rescale to length 1.
	v := vec{1, 0}
	for k := 0; k <= 4; k++ {
		fmt.Printf("step %d: direction %.1f degrees\n", k, math.Atan2(v[1], v[0])*180/math.Pi)
		v = A.apply(v)
		n := math.Hypot(v[0], v[1])
		v = vec{v[0] / n, v[1] / n}
	}

	// Markov chain: columns are "from UP" and "from DOWN".
	P := mat{{0.9, 0.5}, {0.1, 0.5}}
	s := vec{0, 1} // start fully down
	for i := 0; i < 50; i++ {
		s = P.apply(s)
	}
	fmt.Printf("steady state: up %.4f, down %.4f\n", s[0], s[1])
}
