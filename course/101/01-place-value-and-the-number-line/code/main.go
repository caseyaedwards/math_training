// Place value: peel digits off a number with / and %.
package main

import (
	"fmt"
	"strconv"
)

// expand returns [digit, place] pairs, biggest place first.
func expand(n, base int) [][2]int {
	var parts [][2]int
	place := 1
	for n > 0 {
		parts = append([][2]int{{n % base, place}}, parts...)
		n /= base
		place *= base
	}
	return parts
}

// roundTo rounds n to the nearest multiple of unit. Halfway rounds up.
func roundTo(n, unit int) int {
	return (n + unit/2) / unit * unit
}

func main() {
	fmt.Println("3507 in base 10:", expand(3507, 10))
	fmt.Println("13 in base 2:   ", expand(13, 2))
	fmt.Println("3748 to nearest 100:", roundTo(3748, 100))
	fmt.Println("3748 to nearest 10: ", roundTo(3748, 10))
	fmt.Println("tens in 3507:", 3507/10, "remainder", 3507%10)
	fmt.Println("470 * 10 =", 470*10, " 470 / 10 =", 470/10)

	v, _ := strconv.ParseInt("1011", 2, 64)
	fmt.Println("binary 1011 =", v)
	fmt.Println("255 in base 2 =", strconv.FormatInt(255, 2), " in base 16 =", strconv.FormatInt(255, 16))
}
