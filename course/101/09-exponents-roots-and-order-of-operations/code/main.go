// Exponents, roots and precedence. Go has no power operator.
package main

import (
	"fmt"
	"go/ast"
	"go/parser"
	"math"
	"strings"
)

// pow multiplies base by itself exp times. exp must be 0 or more.
func pow(base, exp int) int {
	result := 1
	for i := 0; i < exp; i++ {
		result *= base
	}
	return result
}

// show prints an expression tree, one node per line, children indented.
func show(e ast.Expr, depth int) {
	pad := strings.Repeat("    ", depth)
	switch n := e.(type) {
	case *ast.BinaryExpr:
		fmt.Println(pad + n.Op.String())
		show(n.X, depth+1)
		show(n.Y, depth+1)
	case *ast.ParenExpr:
		show(n.X, depth)
	case *ast.BasicLit:
		fmt.Println(pad + n.Value)
	}
}

func main() {
	for n := 0; n <= 5; n++ {
		fmt.Printf("2^%d = %-3d (-2)^%d = %d\n", n, pow(2, n), n, pow(-2, n))
	}
	fmt.Println("2^10 =", pow(2, 10), " 2^20 =", pow(2, 20))
	fmt.Println("2 ^ 3 in Go is XOR, not a power:", 2^3)
	fmt.Printf("sqrt(50) = %.4f\n", math.Sqrt(50))
	fmt.Println("-pow(3,2) =", -pow(3, 2), "  pow(-3,2) =", pow(-3, 2))

	fmt.Println("3 + 4*2*2 =", 3+4*2*2)
	fmt.Println("20 - 12/4*2 =", 20-12/4*2)
	for _, src := range []string{"3 + 4*2*2", "20 - 12/4*2"} {
		e, err := parser.ParseExpr(src)
		if err != nil {
			panic(err)
		}
		fmt.Println("tree for", src)
		show(e, 1)
	}
}
