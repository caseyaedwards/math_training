// Chapter 09: a tiny Turing machine simulator and Shannon entropy.
package main

import (
	"fmt"
	"math"
	"strings"
)

// rule says what to do on reading a symbol in a state.
type rule struct {
	write byte
	move  int // -1 left, 0 stay, +1 right
	next  string
}

// machine maps "state,symbol" to a rule. Missing entries never fire.
type machine map[string]rule

// run executes m on tape from position head in state start until it
// reaches "halt". It prints every step and returns the final tape.
func run(m machine, tape string, head int, start string, show bool) (string, int) {
	cells := map[int]byte{}
	for i := 0; i < len(tape); i++ {
		cells[i] = tape[i]
	}
	state, steps := start, 0
	for state != "halt" {
		sym, ok := cells[head]
		if !ok {
			sym = '_' // blank cell
		}
		r := m[state+","+string(sym)]
		if show {
			fmt.Printf("  step %d: state %-5s head %d reads %c -> write %c, move %+d, next %s\n",
				steps+1, state, head, sym, r.write, r.move, r.next)
		}
		cells[head] = r.write
		head += r.move
		state = r.next
		steps++
	}
	lo, hi := 0, 0
	for k := range cells {
		lo, hi = min(lo, k), max(hi, k)
	}
	var b strings.Builder
	for i := lo; i <= hi; i++ {
		c, ok := cells[i]
		if !ok {
			c = '_'
		}
		b.WriteByte(c)
	}
	return b.String(), steps
}

// entropy returns the Shannon entropy in bits: -sum p log2 p.
func entropy(p []float64) float64 {
	h := 0.0
	for _, x := range p {
		if x > 0 {
			h -= x * math.Log2(x)
		}
	}
	return h
}

func main() {
	increment := machine{
		"carry,1": {'0', -1, "carry"}, // 1 + carry = 0, carry moves left
		"carry,0": {'1', 0, "halt"},   // 0 + carry = 1, done
		"carry,_": {'1', 0, "halt"},   // ran off the left end: new digit
	}
	fmt.Println("Binary increment machine")
	for _, in := range []string{"1011", "111"} {
		out, n := run(increment, in, len(in)-1, "carry", in == "1011")
		fmt.Printf("  %s + 1 = %s in %d steps\n", in, strings.Trim(out, "_"), n)
	}

	beaver := machine{
		"A,_": {'1', +1, "B"}, "A,1": {'1', -1, "B"},
		"B,_": {'1', -1, "A"}, "B,1": {'1', +1, "halt"},
	}
	out, n := run(beaver, "", 0, "A", false)
	fmt.Printf("\nTwo-state busy beaver: tape %s, %d ones, %d steps\n",
		out, strings.Count(out, "1"), n)

	fmt.Println("\nShannon entropy (bits per outcome)")
	cases := []struct {
		name string
		p    []float64
	}{
		{"fair coin", []float64{0.5, 0.5}},
		{"coin 90/10", []float64{0.9, 0.1}},
		{"fair die", []float64{1, 1, 1, 1, 1, 1}},
		{"8 equal outcomes", []float64{1, 1, 1, 1, 1, 1, 1, 1}},
		{"1/2 1/4 1/8 1/8", []float64{4, 2, 1, 1}},
	}
	for _, c := range cases {
		sum := 0.0
		for _, x := range c.p {
			sum += x
		}
		for i := range c.p {
			c.p[i] /= sum // turn weights into probabilities
		}
		fmt.Printf("  %-17s %.3f\n", c.name, entropy(c.p))
	}
}
