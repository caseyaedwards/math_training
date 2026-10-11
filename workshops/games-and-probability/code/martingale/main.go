// Command martingale shows why the martingale betting system fails,
// and the gambler's ruin.
//
// Martingale: bet $1 on red. After a loss, double the bet. After a win,
// pocket $1 and restart at $1. It looks like a sure profit until a
// losing streak outruns the bankroll.
//
// Prints:
//
//  1. The bet ladder for a $255 bankroll (eight doublings deep)
//  2. Exact math for one cycle and for a 100-cycle session
//  3. A seeded simulation of 10,000 sessions with an ASCII histogram
//  4. Gambler's ruin: chance to double $50 to $100 with $1 bets,
//     exact formula versus simulation, fair coin versus roulette
//
// Run from the workshop folder: go run ./code/martingale
package main

import (
	"fmt"
	"math"
	"math/rand/v2"
	"strings"
)

const (
	seed         = 42
	pRed         = 18.0 / 38 // American roulette: 18 red of 38 pockets
	bankroll     = 255       // covers bets 1+2+4+...+128 = 255
	targetCycles = 100       // stop after winning $100
	sessions     = 10_000
)

func banner(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 62))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 62))
}

func comma(n int) string {
	s := fmt.Sprint(n)
	var b strings.Builder
	for i, ch := range s {
		if i > 0 && (len(s)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(ch)
	}
	return b.String()
}

func ladder() {
	banner("1. The doubling ladder with a $255 bankroll")
	total, bet := 0, 1
	fmt.Printf("  %6s %5s %12s\n", "loss #", "bet", "lost so far")
	for k := 1; k <= 8; k++ {
		total += bet
		fmt.Printf("  %6d %5d %12d\n", k, bet, total)
		bet *= 2
	}
	fmt.Printf("  next bet is $%d, but only $%d is left -> bust\n", bet, bankroll-total)
}

func exact() {
	banner("2. Exact math (p = P(red) = 18/38)")
	q := 1 - pRed
	pBust := math.Pow(q, 8)
	ev := (1-pBust)*1 + pBust*(-bankroll)
	fmt.Printf("  P(lose 8 in a row) = (20/38)^8 = %.6f\n", pBust)
	fmt.Printf("  one cycle: win $1 with prob %.6f, lose $255 with prob %.6f\n", 1-pBust, pBust)
	fmt.Printf("  E[one cycle] = %.6f*1 - %.6f*255 = %+.4f dollars\n", 1-pBust, pBust, ev)
	pSession := math.Pow(1-pBust, targetCycles)
	fmt.Printf("  P(win all %d cycles, +$100) = %.4f\n", targetCycles, pSession)
	fmt.Printf("  P(bust first)                = %.4f\n", 1-pSession)
}

// session plays martingale until +$100 or the next bet is unaffordable.
func session(rng *rand.Rand) int {
	money, goal, bet := bankroll, bankroll+targetCycles, 1
	for money < goal {
		if bet > money {
			break
		}
		if rng.Float64() < pRed {
			money += bet
			bet = 1
		} else {
			money -= bet
			bet *= 2
		}
	}
	return money - bankroll
}

func simulate() {
	banner(fmt.Sprintf("3. Simulation: %s sessions, seed %d", comma(sessions), seed))
	rng := rand.New(rand.NewPCG(seed, 0))
	results := make([]int, sessions)
	wins, sum := 0, 0
	for i := range results {
		results[i] = session(rng)
		sum += results[i]
		if results[i] > 0 {
			wins++
		}
	}
	fmt.Printf("  sessions ending +$100: %s (%.1f%%)\n", comma(wins), 100*float64(wins)/sessions)
	fmt.Printf("  sessions ending in a loss: %s (%.1f%%)\n", comma(sessions-wins), 100*float64(sessions-wins)/sessions)
	fmt.Printf("  average result per session: %+.2f dollars\n", float64(sum)/sessions)
	fmt.Println()
	fmt.Println("  histogram of session results (each # = 100 sessions):")
	// A bust after k winning cycles leaves k - 255 dollars, so every
	// losing session lands between -255 and -156.
	edges := [][2]int{{-255, -206}, {-205, -156}, {-155, 99}, {100, 100}}
	for _, e := range edges {
		c := 0
		for _, r := range results {
			if e[0] <= r && r <= e[1] {
				c++
			}
		}
		label := fmt.Sprintf("%+d to %+d", e[0], e[1])
		if e[0] == e[1] {
			label = fmt.Sprintf("%+d", e[0])
		}
		fmt.Printf("  %14s: %6s  %s\n", label, comma(c), strings.Repeat("#", int(math.Round(float64(c)/100))))
	}
}

// ruinExact is P(reach n before 0) starting at i with +1/-1 steps, P(+1) = p.
func ruinExact(i, n int, p float64) float64 {
	if p == 0.5 {
		return float64(i) / float64(n)
	}
	r := (1 - p) / p
	return (1 - math.Pow(r, float64(i))) / (1 - math.Pow(r, float64(n)))
}

func ruinSim(rng *rand.Rand, i, n int, p float64, trials int) float64 {
	hits := 0
	for t := 0; t < trials; t++ {
		x := i
		for 0 < x && x < n {
			if rng.Float64() < p {
				x++
			} else {
				x--
			}
		}
		if x == n {
			hits++
		}
	}
	return float64(hits) / float64(trials)
}

func gamblersRuin() {
	banner("4. Gambler's ruin: start $50, stop at $100 or $0, bet $1")
	rng := rand.New(rand.NewPCG(seed, 0))
	for _, c := range []struct {
		name   string
		p      float64
		trials int
	}{{"fair coin  p = 0.5000", 0.5, 1_000}, {"roulette red p = 0.4737", pRed, 2_000}} {
		fmt.Printf("  %s: exact %.4f, simulated %.4f (%s trials)\n",
			c.name, ruinExact(50, 100, c.p), ruinSim(rng, 50, 100, c.p, c.trials), comma(c.trials))
	}
	e := ruinExact(50, 100, pRed)
	fmt.Printf("  p is only %.4f below 1/2, yet the chance drops to 1 in %.0f.\n", 0.5-pRed, 1/e)
}

func main() {
	ladder()
	exact()
	simulate()
	gamblersRuin()
}
