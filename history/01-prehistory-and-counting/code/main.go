// Ishango rows, pebble matching, and counting bases: a tiny lab for Chapter 01.
// Run: go run main.go
package main

import (
	"fmt"
	"strings"
)

// isPrime reports whether n has no divisors other than 1 and itself.
func isPrime(n int) bool {
	if n < 2 {
		return false
	}
	for d := 2; d*d <= n; d++ {
		if n%d == 0 {
			return false
		}
	}
	return true
}

// digits writes n in the given base, most significant digit first.
func digits(n, base int) []int {
	if n == 0 {
		return []int{0}
	}
	var out []int
	for n > 0 {
		out = append([]int{n % base}, out...)
		n /= base
	}
	return out
}

// tally draws n as groups of five: four strokes and a slash.
func tally(n int) string {
	var sb strings.Builder
	for ; n >= 5; n -= 5 {
		sb.WriteString("||||/ ")
	}
	sb.WriteString(strings.Repeat("|", n))
	return sb.String()
}

// match pairs each returning sheep with one pebble from the bag.
// It never counts: it only removes one pebble per sheep.
func match(pebbles, sheepBack int) (left, extra int) {
	for ; sheepBack > 0; sheepBack-- {
		if pebbles == 0 {
			extra++
			continue
		}
		pebbles--
	}
	return pebbles, extra
}

func main() {
	rows := []struct {
		name   string
		groups []int
	}{
		{"A", []int{11, 13, 17, 19}},
		{"B", []int{3, 6, 4, 8, 10, 5, 5, 7}},
		{"C", []int{11, 21, 19, 9}},
	}
	fmt.Println("Ishango bone rows:")
	for _, r := range rows {
		sum := 0
		var primes []string
		for _, g := range r.groups {
			sum += g
			if isPrime(g) {
				primes = append(primes, fmt.Sprint(g))
			}
		}
		fmt.Printf("  Row %s: %v sum %d, primes: %s\n", r.name, r.groups, sum, strings.Join(primes, " "))
	}

	fmt.Println()
	fmt.Println("Shepherd at dusk (7 pebbles in the bag):")
	for _, back := range []int{7, 6, 8} {
		left, extra := match(7, back)
		fmt.Printf("  %d sheep return: pebbles left %d, unmatched sheep %d\n", back, left, extra)
	}

	fmt.Println()
	fmt.Println("47 sheep written in different bases (digits, biggest place first):")
	for _, b := range []int{5, 10, 20, 60} {
		fmt.Printf("  base %2d: %v\n", b, digits(47, b))
	}

	fmt.Println()
	fmt.Println("Tally of 23 in groups of five:")
	fmt.Println("  " + tally(23))
}
