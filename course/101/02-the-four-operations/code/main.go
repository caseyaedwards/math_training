// The four operations: the area model, and division with a remainder.
package main

import "fmt"

// areaModel splits two 2-digit numbers by place value and adds the four rectangles.
func areaModel(a, b int) {
	aT, aO := a/10*10, a%10
	bT, bO := b/10*10, b%10
	parts := []int{aT * bT, aO * bT, aT * bO, aO * bO}
	sum := 0
	for _, p := range parts {
		sum += p
	}
	fmt.Printf("%d × %d: rectangles %v, total %d (check %d)\n", a, b, parts, sum, a*b)
}

// safeDiv recovers from the panic Go raises on integer division by zero.
func safeDiv(a, b int) (q int, err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("%v", r)
		}
	}()
	return a / b, nil
}

func main() {
	areaModel(23, 14)
	areaModel(34, 12)

	for _, p := range [][2]int{{17, 5}, {100, 7}, {96, 4}} {
		a, b := p[0], p[1]
		q, r := a/b, a%b
		fmt.Printf("%d = %d × %d + %d   (identity holds: %v)\n", a, b, q, r, a == b*q+r)
	}

	if _, err := safeDiv(5, 0); err != nil {
		fmt.Println("5 / 0:", err)
	}
	q, _ := safeDiv(0, 5)
	fmt.Println("0 / 5:", q)
}
