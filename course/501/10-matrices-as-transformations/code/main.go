// 2x2 matrices acting on vectors, and composition by multiplication.
package main

import "fmt"

type mat [2][2]int
type vec [2]int

// apply computes M v as x*(column 1) + y*(column 2).
func (m mat) apply(v vec) vec {
	return vec{m[0][0]*v[0] + m[0][1]*v[1], m[1][0]*v[0] + m[1][1]*v[1]}
}

// mul returns m*n, which means: apply n first, then m.
func (m mat) mul(n mat) mat {
	var out mat
	for i := 0; i < 2; i++ {
		for j := 0; j < 2; j++ {
			out[i][j] = m[i][0]*n[0][j] + m[i][1]*n[1][j]
		}
	}
	return out
}

func main() {
	A := mat{{2, 1}, {0, 1}}
	fmt.Println("A i       =", A.apply(vec{1, 0}), "(column 1)")
	fmt.Println("A j       =", A.apply(vec{0, 1}), "(column 2)")
	fmt.Println("A (3, 2)  =", A.apply(vec{3, 2}))

	R := mat{{0, -1}, {1, 0}} // rotate 90 degrees
	S := mat{{2, 0}, {0, 1}}  // stretch x by 2
	fmt.Println("S*R       =", S.mul(R), "(rotate, then stretch)")
	fmt.Println("R*S       =", R.mul(S), "(stretch, then rotate)")
	fmt.Println("R*R       =", R.mul(R), "(rotate 180)")
}
