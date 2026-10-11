// Information theory starter kit: entropy, Huffman codes, KL divergence,
// channel capacity, a Hamming (7,4) code and a compression experiment.
// Standard library only.
package main

import (
	"bytes"
	"compress/flate"
	"container/heap"
	"fmt"
	"math"
	"math/rand/v2"
	"strings"
)

// entropy returns H(p) in bits.
func entropy(p []float64) float64 {
	h := 0.0
	for _, x := range p {
		if x > 0 {
			h -= x * math.Log2(x)
		}
	}
	return h
}

// textEntropy returns bits per character, using character frequencies.
func textEntropy(s string) float64 {
	count := map[rune]int{}
	for _, r := range s {
		count[r]++
	}
	n := float64(len([]rune(s)))
	var p []float64
	for _, c := range count {
		p = append(p, float64(c)/n)
	}
	return entropy(p)
}

type node struct {
	weight float64
	sym    string // non-empty for leaves
	left   *node
	right  *node
}
type nodeHeap []*node

func (h nodeHeap) Len() int { return len(h) }
func (h nodeHeap) Less(i, j int) bool {
	if h[i].weight != h[j].weight {
		return h[i].weight < h[j].weight
	}
	return h[i].sym < h[j].sym
}
func (h nodeHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *nodeHeap) Push(x interface{}) { *h = append(*h, x.(*node)) }
func (h *nodeHeap) Pop() interface{} {
	old := *h
	n := old[len(old)-1]
	*h = old[:len(old)-1]
	return n
}

// huffman builds a prefix code from symbol probabilities.
func huffman(p map[string]float64) map[string]string {
	h := &nodeHeap{}
	for s, w := range p {
		heap.Push(h, &node{weight: w, sym: s})
	}
	for h.Len() > 1 {
		a := heap.Pop(h).(*node)
		b := heap.Pop(h).(*node)
		heap.Push(h, &node{weight: a.weight + b.weight, sym: "~" + a.sym + b.sym, left: a, right: b})
	}
	codes := map[string]string{}
	var walk func(n *node, prefix string)
	walk = func(n *node, prefix string) {
		if n.left == nil {
			codes[n.sym] = prefix
			return
		}
		walk(n.left, prefix+"0")
		walk(n.right, prefix+"1")
	}
	walk(heap.Pop(h).(*node), "")
	return codes
}

// hammingEncode turns 4 data bits into 7 bits: p1 p2 d1 p3 d2 d3 d4
// (classic positions 1..7, parity bits at positions 1, 2, 4).
func hammingEncode(d [4]int) [7]int {
	var c [7]int
	c[2], c[4], c[5], c[6] = d[0], d[1], d[2], d[3]
	c[0] = c[2] ^ c[4] ^ c[6]
	c[1] = c[2] ^ c[5] ^ c[6]
	c[3] = c[4] ^ c[5] ^ c[6]
	return c
}

// hammingFix finds and flips a single wrong bit. It returns the position
// (1..7) it fixed, or 0 when every parity check passes.
func hammingFix(c *[7]int) int {
	s1 := c[0] ^ c[2] ^ c[4] ^ c[6]
	s2 := c[1] ^ c[2] ^ c[5] ^ c[6]
	s4 := c[3] ^ c[4] ^ c[5] ^ c[6]
	pos := s1 + 2*s2 + 4*s4
	if pos > 0 {
		c[pos-1] ^= 1
	}
	return pos
}

func deflateSize(b []byte) int {
	var buf bytes.Buffer
	w, _ := flate.NewWriter(&buf, flate.BestCompression)
	w.Write(b)
	w.Close()
	return buf.Len()
}

func main() {
	fmt.Println("== Entropy ==")
	fmt.Printf("fair coin           %.3f bits\n", entropy([]float64{0.5, 0.5}))
	fmt.Printf("90/10 coin          %.3f bits\n", entropy([]float64{0.9, 0.1}))
	fmt.Printf("fair 8-sided die    %.3f bits\n", entropy([]float64{.125, .125, .125, .125, .125, .125, .125, .125}))
	p := []float64{0.5, 0.25, 0.125, 0.125}
	fmt.Printf("skewed A,B,C,D      %.3f bits\n", entropy(p))

	fmt.Println("\n== Huffman code for A 0.5, B 0.25, C 0.125, D 0.125 ==")
	codes := huffman(map[string]float64{"A": 0.5, "B": 0.25, "C": 0.125, "D": 0.125})
	syms := []string{"A", "B", "C", "D"}
	avg := 0.0
	for i, s := range syms {
		fmt.Printf("%s -> %s\n", s, codes[s])
		avg += p[i] * float64(len(codes[s]))
	}
	fmt.Printf("average length %.3f bits = entropy %.3f bits\n", avg, entropy(p))

	fmt.Println("\n== Cross-entropy and KL divergence ==")
	q := []float64{0.25, 0.25, 0.25, 0.25}
	cross := 0.0
	for i := range p {
		cross -= p[i] * math.Log2(q[i])
	}
	fmt.Printf("H(p, q) = %.3f bits, KL(p||q) = %.3f bits\n", cross, cross-entropy(p))

	fmt.Println("\n== Binary symmetric channel ==")
	for _, f := range []float64{0, 0.01, 0.1, 0.5} {
		fmt.Printf("flip %.2f -> capacity %.3f bits per use\n", f, 1-entropy([]float64{f, 1 - f}))
	}

	fmt.Println("\n== Hamming (7,4) ==")
	data := [4]int{1, 0, 1, 1}
	code := hammingEncode(data)
	fmt.Println("data   ", data, "-> codeword", code)
	code[4] ^= 1 // noise flips position 5
	fmt.Println("noisy  ", code)
	pos := hammingFix(&code)
	fmt.Println("fixed  ", code, "repaired position", pos)

	fmt.Println("\n== Compression versus entropy ==")
	logLine := "GET /healthz 200 1ms\n"
	repetitive := []byte(strings.Repeat(logLine, 500))
	r := rand.New(rand.NewPCG(1, 2))
	noise := make([]byte, len(repetitive))
	for i := range noise {
		noise[i] = byte(r.IntN(256))
	}
	fmt.Printf("health-check log: %5d bytes -> %4d bytes deflated\n", len(repetitive), deflateSize(repetitive))
	fmt.Printf("random bytes:     %5d bytes -> %4d bytes deflated\n", len(noise), deflateSize(noise))
	fmt.Printf("letter entropy of %q: %.3f bits per char\n", "mississippi", textEntropy("mississippi"))

	fmt.Println("\n== Password entropy ==")
	type pw struct {
		name   string
		length int
		alpha  float64
	}
	list := []pw{{"8 lowercase", 8, 26}, {"8 mixed+digits", 8, 62}, {"4 diceware words", 4, 7776}, {"12 mixed+digits", 12, 62}}
	for _, x := range list {
		fmt.Printf("%-17s %5.1f bits\n", x.name, float64(x.length)*math.Log2(x.alpha))
	}
}
