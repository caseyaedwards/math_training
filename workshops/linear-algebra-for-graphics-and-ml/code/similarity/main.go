// Command similarity shows dot product, length, angle, cosine similarity,
// and a tiny hand-made word embedding with nearest-neighbor search.
//
// It prints:
//  1. dot, length, and angle for a = (3, 1) and b = (1, 2)
//  2. cosine similarity ignores length, cares about direction
//  3. a hand-made 4-dimensional word embedding and its similarity matrix
//  4. nearest neighbors by cosine, plus king - man + woman
//
// The four embedding dimensions mean: royalty, gender (+ male, - female),
// animal, food. Real embeddings have hundreds of dimensions that no person chose.
//
// Run from the workshop folder: go run ./code/similarity
package main

import (
	"fmt"
	"math"
	"sort"
	"strings"
)

func dot(a, b []float64) float64 {
	s := 0.0
	for i := range a {
		s += a[i] * b[i]
	}
	return s
}

func length(a []float64) float64 { return math.Sqrt(dot(a, a)) }

func cosine(a, b []float64) float64 { return dot(a, b) / (length(a) * length(b)) }

func angleDeg(a, b []float64) float64 {
	c := math.Max(-1, math.Min(1, cosine(a, b))) // clamp against rounding drift
	return math.Acos(c) * 180 / math.Pi
}

// words keeps a fixed print order; Go maps have no order.
var words = []string{"king", "queen", "man", "woman", "cat", "dog", "pizza", "burger"}

var embed = map[string][]float64{
	//         royalty gender animal food
	"king":   {0.95, 0.50, 0.05, 0.00},
	"queen":  {0.95, -0.50, 0.05, 0.00},
	"man":    {0.10, 0.60, 0.10, 0.00},
	"woman":  {0.10, -0.60, 0.10, 0.00},
	"cat":    {0.05, 0.00, 0.95, 0.10},
	"dog":    {0.05, 0.05, 0.90, 0.15},
	"pizza":  {0.00, 0.00, 0.05, 0.95},
	"burger": {0.00, 0.05, 0.10, 0.90},
}

func section(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 64))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 64))
}

func fmtList(v []float64) string {
	parts := make([]string, len(v))
	for i, x := range v {
		parts[i] = fmt.Sprintf("%5.2f", x)
	}
	return "[" + strings.Join(parts, " ") + "]"
}

func partBasics() {
	section("1. Dot product, length, angle")
	a, b := []float64{3, 1}, []float64{1, 2}
	fmt.Println("a = (3, 1)   b = (1, 2)")
	fmt.Printf("a . b   = 3*1 + 1*2 = %.0f\n", dot(a, b))
	fmt.Printf("|a|     = sqrt(3^2 + 1^2) = sqrt(10) = %.4f\n", length(a))
	fmt.Printf("|b|     = sqrt(1^2 + 2^2) = sqrt(5)  = %.4f\n", length(b))
	fmt.Printf("cos(t)  = 5 / (sqrt(10) * sqrt(5)) = %.4f\n", cosine(a, b))
	fmt.Printf("t       = acos(%.4f) = %.2f degrees\n", cosine(a, b), angleDeg(a, b))
}

func partDirection() {
	section("2. Cosine looks at direction only")
	a := []float64{3, 1}
	others := []struct {
		label string
		b     []float64
	}{
		{"(6, 2)   same way, twice as long", []float64{6, 2}},
		{"(1, 2)   45 degrees off", []float64{1, 2}},
		{"(-1, 3)  perpendicular", []float64{-1, 3}},
		{"(-3, -1) opposite", []float64{-3, -1}},
	}
	fmt.Println("a = (3, 1)")
	for _, o := range others {
		c := cosine(a, o.b)
		if math.Abs(c) < 5e-10 {
			c = 0
		}
		fmt.Printf("  cos(a, %-34s) = %+.4f\n", o.label, c)
	}
}

// bar draws a text bar for a value in [-1, 1]; only the positive part gets #.
func bar(x float64) string {
	return strings.Repeat("#", int(math.Round(math.Max(0, x)*20)))
}

func partMatrix() {
	section("3. Hand-made 4-d embedding: cosine similarity matrix")
	fmt.Println("dims:       royalty gender animal food")
	for _, w := range words {
		fmt.Printf("  %-7s   %s\n", w, fmtList(embed[w]))
	}
	fmt.Println()
	fmt.Print("        ")
	for _, w := range words {
		fmt.Printf("%8s", w)
	}
	fmt.Println()
	for _, w := range words {
		fmt.Printf("%8s", w)
		for _, v := range words {
			fmt.Printf("%8.2f", cosine(embed[w], embed[v]))
		}
		fmt.Println()
	}
}

type scored struct {
	score float64
	word  string
}

// nearest ranks every stored word by cosine to vec and keeps the top k.
func nearest(vec []float64, k int, exclude ...string) []scored {
	skip := map[string]bool{}
	for _, e := range exclude {
		skip[e] = true
	}
	var out []scored
	for _, w := range words {
		if !skip[w] {
			out = append(out, scored{cosine(vec, embed[w]), w})
		}
	}
	sort.Slice(out, func(i, j int) bool { return out[i].score > out[j].score })
	return out[:k]
}

func partSearch() {
	section("4. Nearest neighbors by cosine (top 3, word itself excluded)")
	for _, q := range []string{"dog", "pizza", "king"} {
		fmt.Printf("\nquery: %s\n", q)
		for _, s := range nearest(embed[q], 3, q) {
			fmt.Printf("  %-7s %+.4f  %s\n", s.word, s.score, bar(s.score))
		}
	}
	fmt.Println("\nquery: king - man + woman")
	v := make([]float64, 4)
	for i := range v {
		v[i] = embed["king"][i] - embed["man"][i] + embed["woman"][i]
	}
	fmt.Printf("  vector = %s\n", fmtList(v))
	for _, s := range nearest(v, 3, "king", "man", "woman") {
		fmt.Printf("  %-7s %+.4f  %s\n", s.word, s.score, bar(s.score))
	}
}

func main() {
	partBasics()
	partDirection()
	partMatrix()
	partSearch()
}
