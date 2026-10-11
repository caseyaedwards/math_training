// Game theory starter kit: pure Nash equilibria by best-response search,
// 2x2 mixed equilibria, zero-sum minimax, an iterated prisoner's dilemma
// tournament, Braess paradox, sealed-bid auctions and Nim.
// Standard library only.
package main

import (
	"fmt"
	"math/rand"
	"sort"
)

// Game is a two-player bimatrix game. A[i][j] is the row player's payoff
// and B[i][j] is the column player's payoff when row plays i and column j.
type Game struct {
	Name       string
	Rows, Cols []string
	A, B       [][]float64
}

// pureNash returns every cell where each player is already playing a best
// response to the other: no one gains by switching alone.
func pureNash(g Game) [][2]int {
	var out [][2]int
	for i := range g.Rows {
		for j := range g.Cols {
			rowBest, colBest := true, true
			for k := range g.Rows {
				if g.A[k][j] > g.A[i][j] {
					rowBest = false
				}
			}
			for k := range g.Cols {
				if g.B[i][k] > g.B[i][j] {
					colBest = false
				}
			}
			if rowBest && colBest {
				out = append(out, [2]int{i, j})
			}
		}
	}
	return out
}

// dominant returns the index of a strictly dominant row strategy, or -1.
func dominant(g Game) int {
	for i := range g.Rows {
		ok := true
		for k := range g.Rows {
			if k == i {
				continue
			}
			for j := range g.Cols {
				if g.A[i][j] <= g.A[k][j] {
					ok = false
				}
			}
		}
		if ok {
			return i
		}
	}
	return -1
}

// mixed2x2 finds the interior mixed equilibrium of a 2x2 game.
// p is the chance row plays row 0, chosen to make the column player
// indifferent. q is the chance column plays column 0, chosen to make the
// row player indifferent.
func mixed2x2(g Game) (p, q float64) {
	a, b := g.A, g.B
	q = (a[1][1] - a[0][1]) / (a[0][0] - a[0][1] - a[1][0] + a[1][1])
	p = (b[1][1] - b[1][0]) / (b[0][0] - b[0][1] - b[1][0] + b[1][1])
	return p, q
}

// minimax2x2 solves a 2x2 zero-sum game with payoffs M to the row player.
// It reports the pure safety levels and the mixed solution.
func minimax2x2(m [2][2]float64) (maximin, minimax, p, q, v float64) {
	maximin = max(min(m[0][0], m[0][1]), min(m[1][0], m[1][1]))
	minimax = min(max(m[0][0], m[1][0]), max(m[0][1], m[1][1]))
	d := m[0][0] - m[0][1] - m[1][0] + m[1][1]
	p = (m[1][1] - m[1][0]) / d
	q = (m[1][1] - m[0][1]) / d
	v = (m[0][0]*m[1][1] - m[0][1]*m[1][0]) / d
	return
}

// ---------- Iterated prisoner's dilemma ----------

// Strategy picks C (true) or D (false) from both move histories.
type Strategy struct {
	Name string
	Move func(mine, theirs []bool, r *rand.Rand) bool
}

func pdPayoff(me, them bool) int {
	switch {
	case me && them:
		return 3 // both cooperate: reward
	case me && !them:
		return 0 // sucker
	case !me && them:
		return 5 // temptation
	default:
		return 1 // both defect: punishment
	}
}

var strategies = []Strategy{
	{"tit-for-tat", func(m, t []bool, r *rand.Rand) bool {
		return len(t) == 0 || t[len(t)-1]
	}},
	{"grim-trigger", func(m, t []bool, r *rand.Rand) bool {
		for _, c := range t {
			if !c {
				return false
			}
		}
		return true
	}},
	{"always-cooperate", func(m, t []bool, r *rand.Rand) bool { return true }},
	{"always-defect", func(m, t []bool, r *rand.Rand) bool { return false }},
	{"random", func(m, t []bool, r *rand.Rand) bool { return r.Intn(2) == 0 }},
}

func match(a, b Strategy, rounds int, seed int64) (int, int) {
	r := rand.New(rand.NewSource(seed))
	var ha, hb []bool
	sa, sb := 0, 0
	for i := 0; i < rounds; i++ {
		ma := a.Move(ha, hb, r)
		mb := b.Move(hb, ha, r)
		sa += pdPayoff(ma, mb)
		sb += pdPayoff(mb, ma)
		ha, hb = append(ha, ma), append(hb, mb)
	}
	return sa, sb
}

// tournament plays every strategy against every other one, and itself,
// once. A self-match counts once.
func tournament(pool []Strategy, rounds int) {
	total := map[string]int{}
	seed := int64(1)
	for i := range pool {
		for j := i; j < len(pool); j++ {
			sa, sb := match(pool[i], pool[j], rounds, seed)
			seed++
			total[pool[i].Name] += sa
			if i != j {
				total[pool[j].Name] += sb
			}
		}
	}
	names := make([]string, 0, len(total))
	for n := range total {
		names = append(names, n)
	}
	sort.Slice(names, func(x, y int) bool {
		if total[names[x]] != total[names[y]] {
			return total[names[x]] > total[names[y]]
		}
		return names[x] < names[y]
	})
	for k, n := range names {
		fmt.Printf("  %d. %-17s %5d points\n", k+1, n, total[n])
	}
}

// ---------- Nim ----------

func nimSum(heaps []int) int {
	s := 0
	for _, h := range heaps {
		s ^= h
	}
	return s
}

// winningMove returns the heap index and the new size, or -1 when the
// position is already lost for the player to move.
func winningMove(heaps []int) (int, int) {
	s := nimSum(heaps)
	if s == 0 {
		return -1, 0
	}
	for i, h := range heaps {
		if h^s < h {
			return i, h ^ s
		}
	}
	return -1, 0
}

// bruteLoses reports whether the player to move loses with perfect play,
// by plain recursion over every move. It checks the XOR rule.
func bruteLoses(a, b, c int, memo map[[3]int]bool) bool {
	k := [3]int{a, b, c}
	if v, ok := memo[k]; ok {
		return v
	}
	lose := true
	for n := 1; n <= a && lose; n++ {
		if bruteLoses(a-n, b, c, memo) {
			lose = false
		}
	}
	for n := 1; n <= b && lose; n++ {
		if bruteLoses(a, b-n, c, memo) {
			lose = false
		}
	}
	for n := 1; n <= c && lose; n++ {
		if bruteLoses(a, b, c-n, memo) {
			lose = false
		}
	}
	memo[k] = lose
	return lose
}

// ---------- Auctions ----------

// auctions simulates sealed-bid auctions with values uniform on [0, 100).
// Second-price bidders bid their value. First-price bidders shade to
// (n-1)/n of their value, the equilibrium bid for this setting.
func auctions(n, trials int, reserve float64, seed int64) (first, second float64) {
	r := rand.New(rand.NewSource(seed))
	vals := make([]float64, n)
	for t := 0; t < trials; t++ {
		for i := range vals {
			vals[i] = 100 * r.Float64()
		}
		sort.Float64s(vals)
		top, next := vals[n-1], vals[n-2]
		first += top * float64(n-1) / float64(n)
		if top >= reserve {
			second += max(next, reserve)
		}
	}
	return first / float64(trials), second / float64(trials)
}

func secondPricePayoff(value, bid, rival float64) float64 {
	if bid > rival {
		return value - rival
	}
	return 0
}

func main() {
	games := []Game{
		{"coffee shops", []string{"High", "Low"}, []string{"High", "Low"},
			[][]float64{{6, 2}, {8, 4}}, [][]float64{{6, 8}, {2, 4}}},
		{"prisoner's dilemma", []string{"Cooperate", "Defect"}, []string{"Cooperate", "Defect"},
			[][]float64{{3, 0}, {5, 1}}, [][]float64{{3, 5}, {0, 1}}},
		{"log format", []string{"JSON", "Plain"}, []string{"JSON", "Plain"},
			[][]float64{{3, 0}, {0, 2}}, [][]float64{{3, 0}, {0, 2}}},
		{"retry or back off", []string{"Retry", "Back off"}, []string{"Retry", "Back off"},
			[][]float64{{0, 3}, {1, 2}}, [][]float64{{0, 1}, {3, 2}}},
	}
	fmt.Println("== Pure Nash equilibria (best-response search) ==")
	for _, g := range games {
		fmt.Printf("%-19s", g.Name+":")
		for _, c := range pureNash(g) {
			i, j := c[0], c[1]
			fmt.Printf(" (%s, %s) pays %g, %g;", g.Rows[i], g.Cols[j], g.A[i][j], g.B[i][j])
		}
		if d := dominant(g); d >= 0 {
			fmt.Printf(" dominant: %s", g.Rows[d])
		}
		fmt.Println()
	}

	fmt.Println("\n== Mixed equilibrium of retry or back off ==")
	p, q := mixed2x2(games[3])
	fmt.Printf("row retries with p = %.2f, column retries with q = %.2f\n", p, q)
	retry := q*games[3].A[0][0] + (1-q)*games[3].A[0][1]
	back := q*games[3].A[1][0] + (1-q)*games[3].A[1][1]
	fmt.Printf("expected payoff: retry %.2f, back off %.2f (equal, so no regret)\n", retry, back)
	collide := p * q
	fmt.Printf("chance both retry and collide: %.2f\n", collide)

	fmt.Println("\n== Zero-sum: defender versus attacker ==")
	m := [2][2]float64{{3, -2}, {-1, 2}}
	lo, hi, dp, aq, v := minimax2x2(m)
	fmt.Printf("pure: defender guarantees %g, attacker holds defender to %g\n", lo, hi)
	fmt.Printf("mixed: defender watches login with p = %.3f\n", dp)
	fmt.Printf("       attacker hits login with q = %.3f\n", aq)
	fmt.Printf("value of the game = %.3f\n", v)

	fmt.Println("\n== Iterated prisoner's dilemma, 200 rounds, round robin ==")
	tournament(strategies, 200)
	ta, tb := match(strategies[0], strategies[3], 200, 99)
	fmt.Printf("head to head, tit-for-tat %d vs always-defect %d\n", ta, tb)

	fmt.Println("\n== Braess paradox, 4,000 drivers ==")
	n := 4000.0
	before := (n/2)/100 + 45
	after := n/100 + 0 + n/100
	fmt.Printf("without shortcut: 2,000 per route, trip = %.0f minutes\n", before)
	fmt.Printf("with shortcut:    all take it,   trip = %.0f minutes\n", after)
	// Pigou: one link costs 1, the other costs x (fraction of traffic).
	selfish := 1.0
	best := 2.0
	bestX := 0.0
	for i := 0; i <= 1000; i++ {
		x := float64(i) / 1000
		c := x*x + (1-x)*1
		if c < best {
			best, bestX = c, x
		}
	}
	fmt.Printf("Pigou: selfish cost %.2f, best cost %.2f at x = %.2f, price of anarchy %.3f\n",
		selfish, best, bestX, selfish/best)

	fmt.Println("\n== Sealed-bid auctions, values uniform on 0 to 100 ==")
	for _, nb := range []int{2, 5} {
		f, s := auctions(nb, 200000, 0, 42)
		exact := 100 * float64(nb-1) / float64(nb+1)
		fmt.Printf("%d bidders: first-price %.2f, second-price %.2f, theory %.2f\n", nb, f, s, exact)
	}
	_, sr := auctions(2, 200000, 50, 42)
	fmt.Printf("2 bidders, second-price with reserve 50: %.2f, theory %.2f\n", sr, 100*5.0/12)
	fmt.Println("second-price payoff for value 70:")
	for _, rival := range []float64{50, 90} {
		fmt.Printf("  rival bids %g:", rival)
		for _, bid := range []float64{40, 60, 70, 80, 100} {
			fmt.Printf(" bid %g -> %g;", bid, secondPricePayoff(70, bid, rival))
		}
		fmt.Println()
	}

	fmt.Println("\n== Nim ==")
	for _, h := range [][]int{{3, 4, 5}, {1, 4, 5}, {7, 9, 12}} {
		s := nimSum(h)
		i, to := winningMove(h)
		if i < 0 {
			fmt.Printf("heaps %v: nim-sum %d, player to move loses\n", h, s)
			continue
		}
		fmt.Printf("heaps %v: nim-sum %d, win by cutting heap %d from %d to %d\n", h, s, i+1, h[i], to)
	}
	memo := map[[3]int]bool{}
	agree, total := 0, 0
	for a := 0; a <= 7; a++ {
		for b := 0; b <= 7; b++ {
			for c := 0; c <= 7; c++ {
				total++
				if bruteLoses(a, b, c, memo) == (a^b^c == 0) {
					agree++
				}
			}
		}
	}
	fmt.Printf("brute force agrees with the XOR rule on %d of %d positions\n", agree, total)
}
