// Determinants of 2x2 and 3x3 matrices, and the product rule det(AB) = det(A) det(B).
package main

import "fmt"

func det2(m [2][2]int) int { return m[0][0]*m[1][1] - m[0][1]*m[1][0] }

// det3 expands along the top row (cofactor expansion).
func det3(m [3][3]int) int {
	minor := func(col int) [2][2]int {
		var out [2][2]int
		for i := 1; i < 3; i++ {
			k := 0
			for j := 0; j < 3; j++ {
				if j != col {
					out[i-1][k] = m[i][j]
					k++
				}
			}
		}
		return out
	}
	return m[0][0]*det2(minor(0)) - m[0][1]*det2(minor(1)) + m[0][2]*det2(minor(2))
}

func mul2(a, b [2][2]int) [2][2]int {
	var out [2][2]int
	for i := 0; i < 2; i++ {
		for j := 0; j < 2; j++ {
			out[i][j] = a[i][0]*b[0][j] + a[i][1]*b[1][j]
		}
	}
	return out
}

func main() {
	fmt.Println("det [[3,1],[1,2]] =", det2([2][2]int{{3, 1}, {1, 2}}))
	fmt.Println("det [[1,2],[3,4]] =", det2([2][2]int{{1, 2}, {3, 4}}))
	fmt.Println("det [[2,4],[1,2]] =", det2([2][2]int{{2, 4}, {1, 2}}), "(columns on one line)")
	fmt.Println("det [[0,1],[1,0]] =", det2([2][2]int{{0, 1}, {1, 0}}), "(a flip)")
	fmt.Println("det of 3x3 example =", det3([3][3]int{{1, 2, 3}, {0, 1, 4}, {5, 6, 0}}))

	A, B := [2][2]int{{3, 1}, {1, 2}}, [2][2]int{{2, 0}, {1, -1}}
	fmt.Println("det(AB) =", det2(mul2(A, B)), " det(A)*det(B) =", det2(A)*det2(B))
}
