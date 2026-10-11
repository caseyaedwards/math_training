// Category theory starter kit in Go: composition, identity, a Unix-style
// pipeline, functors, a natural transformation, products, coproducts,
// counting arrows between finite sets, and a monad taster.
// Standard library only.
//
// Go cannot compare two funcs for equality, so every law below is checked
// on sample inputs. That is evidence, not proof. The proofs are in the README.
package main

import (
	"errors"
	"fmt"
	"slices"
	"strconv"
	"strings"
)

// ---------- Composition and identity ----------

// Compose returns g after f: first run f, then run g.
func Compose[A, B, C any](f func(A) B, g func(B) C) func(A) C {
	return func(a A) C { return g(f(a)) }
}

// Identity returns its input unchanged.
func Identity[A any](a A) A { return a }

// ---------- A Unix-style pipeline ----------

// Stage is one command in a pipe: lines in, lines out.
type Stage func([]string) []string

func grep(word string) Stage {
	return func(in []string) []string {
		var out []string
		for _, s := range in {
			if strings.Contains(s, word) {
				out = append(out, s)
			}
		}
		return out
	}
}

func sortLines(in []string) []string {
	out := slices.Clone(in)
	slices.Sort(out)
	return out
}

func uniq(in []string) []string {
	var out []string
	for i, s := range in {
		if i == 0 || s != in[i-1] {
			out = append(out, s)
		}
	}
	return out
}

// Pipe composes stages left to right, like a | b | c.
func Pipe(stages ...Stage) Stage {
	return func(in []string) []string {
		for _, s := range stages {
			in = s(in)
		}
		return in
	}
}

// ---------- Functors: slices and Option ----------

// Map lifts f: A -> B to []A -> []B.
func Map[A, B any](xs []A, f func(A) B) []B {
	out := make([]B, 0, len(xs))
	for _, x := range xs {
		out = append(out, f(x))
	}
	return out
}

// Option holds zero or one value.
type Option[T any] struct {
	val T
	ok  bool
}

func Some[T any](v T) Option[T] { return Option[T]{val: v, ok: true} }
func None[T any]() Option[T]    { return Option[T]{} }

func (o Option[T]) String() string {
	if !o.ok {
		return "None"
	}
	return fmt.Sprintf("Some(%#v)", o.val)
}

// MapOpt lifts f: A -> B to Option[A] -> Option[B].
func MapOpt[A, B any](o Option[A], f func(A) B) Option[B] {
	if !o.ok {
		return None[B]()
	}
	return Some(f(o.val))
}

// ---------- Natural transformation ----------

// First works the same way for every T: it never looks inside the values.
func First[T any](xs []T) Option[T] {
	if len(xs) == 0 {
		return None[T]()
	}
	return Some(xs[0])
}

// Sneaky peeks at the type, which breaks naturality.
func Sneaky[T any](xs []T) Option[T] {
	if _, isInts := any(xs).([]int); isInts {
		return None[T]()
	}
	return First(xs)
}

// ---------- Products and coproducts ----------

// Pair is the product of A and B.
type Pair[A, B any] struct {
	Fst A
	Snd B
}

// Fanout builds the unique arrow X -> A x B from f: X -> A and g: X -> B.
func Fanout[X, A, B any](f func(X) A, g func(X) B) func(X) Pair[A, B] {
	return func(x X) Pair[A, B] { return Pair[A, B]{f(x), g(x)} }
}

// Either is the coproduct of A and B: exactly one side is filled.
type Either[A, B any] struct {
	left   A
	right  B
	isLeft bool
}

func Left[A, B any](a A) Either[A, B]  { return Either[A, B]{left: a, isLeft: true} }
func Right[A, B any](b B) Either[A, B] { return Either[A, B]{right: b} }

// Case builds the unique arrow A + B -> X from f: A -> X and g: B -> X.
func Case[A, B, X any](f func(A) X, g func(B) X) func(Either[A, B]) X {
	return func(e Either[A, B]) X {
		if e.isLeft {
			return f(e.left)
		}
		return g(e.right)
	}
}

// ---------- Counting arrows between finite sets ----------

// allFuncs lists every function from {0..m-1} to {0..n-1} as a slice of outputs.
func allFuncs(m, n int) [][]int {
	result := [][]int{{}}
	for i := 0; i < m; i++ {
		var next [][]int
		for _, f := range result {
			for v := 0; v < n; v++ {
				next = append(next, append(slices.Clone(f), v))
			}
		}
		result = next
	}
	return result
}

func key(f []int) string { return fmt.Sprint(f) }

// ---------- Monad taster ----------

// Bind runs f only when o holds a value.
func Bind[A, B any](o Option[A], f func(A) Option[B]) Option[B] {
	if !o.ok {
		return None[B]()
	}
	return f(o.val)
}

func parse(s string) (int, error) { return strconv.Atoi(s) }

func half(n int) (int, error) {
	if n%2 != 0 {
		return 0, fmt.Errorf("%d is odd", n)
	}
	return n / 2, nil
}

func positive(n int) (int, error) {
	if n <= 0 {
		return 0, errors.New("not positive")
	}
	return n, nil
}

// Then chains two (value, error) steps: the Kleisli composition.
func Then[A, B, C any](f func(A) (B, error), g func(B) (C, error)) func(A) (C, error) {
	return func(a A) (C, error) {
		b, err := f(a)
		if err != nil {
			var zero C
			return zero, err
		}
		return g(b)
	}
}

func main() {
	inc := func(x int) int { return x + 1 }
	dbl := func(x int) int { return 2 * x }

	fmt.Println("== Composition ==")
	fmt.Println("dbl after inc, at 3:", Compose(inc, dbl)(3))
	fmt.Println("inc after dbl, at 3:", Compose(dbl, inc)(3))
	idOK, assocOK := true, true
	sq := func(x int) int { return x * x }
	for x := -5; x <= 5; x++ {
		if Compose(Identity[int], inc)(x) != inc(x) || Compose(inc, Identity[int])(x) != inc(x) {
			idOK = false
		}
		if Compose(Compose(inc, dbl), sq)(x) != Compose(inc, Compose(dbl, sq))(x) {
			assocOK = false
		}
	}
	fmt.Println("identity laws hold on -5..5:", idOK)
	fmt.Println("associativity holds on -5..5:", assocOK)

	fmt.Println()
	fmt.Println("== Pipes are composition ==")
	logs := []string{"ERROR disk full", "INFO ok", "ERROR timeout", "ERROR disk full", "WARN slow"}
	p1 := Pipe(Pipe(grep("ERROR"), sortLines), uniq)
	p2 := Pipe(grep("ERROR"), Pipe(sortLines, uniq))
	fmt.Printf("grep ERROR | sort | uniq -> %q\n", p1(logs))
	fmt.Println("(a|b)|c equals a|(b|c):", slices.Equal(p1(logs), p2(logs)))

	fmt.Println()
	fmt.Println("== Functors ==")
	xs := []int{1, 2, 3}
	fmt.Println("Map(dbl) over", xs, "->", Map(xs, dbl))
	lhs := Map(xs, Compose(inc, dbl))
	rhs := Map(Map(xs, inc), dbl)
	fmt.Println("Map(dbl after inc) =", lhs, " Map(dbl) after Map(inc) =", rhs)
	fmt.Println("Map(id) leaves", xs, "as", Map(xs, Identity[int]))
	fmt.Println("MapOpt(dbl) on Some(5):", MapOpt(Some(5), dbl), " on None:", MapOpt(None[int](), dbl))

	fmt.Println()
	fmt.Println("== Natural transformation First: []T -> Option[T] ==")
	itoa := strconv.Itoa
	for _, in := range [][]int{{7, 8, 9}, {42}, {}} {
		down := First(Map(in, itoa))
		across := MapOpt(First(in), itoa)
		fmt.Printf("%-8v First(Map) = %-10v Map(First) = %-10v square commutes: %v\n",
			fmt.Sprint(in), down, across, down == across)
	}
	in := []int{7, 8, 9}
	fmt.Printf("Sneaky on %v: Sneaky(Map) = %v, Map(Sneaky) = %v -> not natural\n",
		in, Sneaky(Map(in, itoa)), MapOpt(Sneaky(in), itoa))

	fmt.Println()
	fmt.Println("== Product and coproduct ==")
	both := Fanout(strconv.Itoa, func(n int) bool { return n%2 == 0 })
	pr := both(6)
	fmt.Printf("Fanout(itoa, isEven)(6) = {%q %v}; Fst = %q, Snd = %v\n", pr.Fst, pr.Snd, pr.Fst, pr.Snd)
	describe := Case(func(n int) string { return "number " + strconv.Itoa(n) },
		func(e error) string { return "error: " + e.Error() })
	fmt.Println(describe(Left[int, error](42)))
	fmt.Println(describe(Right[int](errors.New("timeout"))))

	fmt.Println()
	fmt.Println("== Counting arrows between finite sets ==")
	fmt.Println("functions 2 -> 3:", len(allFuncs(2, 3)), " functions 3 -> 2:", len(allFuncs(3, 2)))
	fmt.Println("functions to a 1-element set from a 4-element set:", len(allFuncs(4, 1)))
	fmt.Println("functions from the empty set to a 5-element set:", len(allFuncs(0, 5)))
	// Product: pairs (f: X->A, g: X->B) with |X|=2, |A|=2, |B|=3 match functions X -> A x B.
	seen := map[string]bool{}
	pairs := 0
	for _, f := range allFuncs(2, 2) {
		for _, g := range allFuncs(2, 3) {
			h := []int{f[0]*3 + g[0], f[1]*3 + g[1]} // encode (a, b) as 3a + b
			seen[key(h)] = true
			pairs++
		}
	}
	fmt.Printf("product:   %d pairs (f, g) -> %d distinct X -> AxB, of %d total\n",
		pairs, len(seen), len(allFuncs(2, 6)))
	// Coproduct: pairs (f: A->X, g: B->X) with |A|=2, |B|=3, |X|=2 match functions A+B -> X.
	seen = map[string]bool{}
	pairs = 0
	for _, f := range allFuncs(2, 2) {
		for _, g := range allFuncs(3, 2) {
			seen[key(append(slices.Clone(f), g...))] = true
			pairs++
		}
	}
	fmt.Printf("coproduct: %d pairs (f, g) -> %d distinct A+B -> X, of %d total\n",
		pairs, len(seen), len(allFuncs(5, 2)))
	fmt.Printf("currying:  functions AxB -> C = %d, functions A -> (B -> C) = %d\n",
		len(allFuncs(2*3, 2)), len(allFuncs(2, len(allFuncs(3, 2)))))

	fmt.Println()
	fmt.Println("== Monad taster ==")
	step := Then(Then(parse, positive), half)
	for _, s := range []string{"42", "7", "-4", "abc"} {
		v, err := step(s)
		if err != nil {
			fmt.Printf("%-5q -> error: %v\n", s, err)
			continue
		}
		fmt.Printf("%-5q -> %d\n", s, v)
	}
	safeHalf := func(n int) Option[int] {
		if n%2 != 0 {
			return None[int]()
		}
		return Some(n / 2)
	}
	fmt.Println("Some(40) >>= half >>= half >>= half:", Bind(Bind(Bind(Some(40), safeHalf), safeHalf), safeHalf))
	fmt.Println("one more half on 5:", Bind(Some(5), safeHalf))
	leftID := Bind(Some(10), safeHalf) == safeHalf(10)
	rightID := Bind(Some(10), Some[int]) == Some(10)
	assoc := Bind(Bind(Some(40), safeHalf), safeHalf) ==
		Bind(Some(40), func(n int) Option[int] { return Bind(safeHalf(n), safeHalf) })
	fmt.Println("monad laws on samples: left identity", leftID, "right identity", rightID, "associativity", assoc)
}
