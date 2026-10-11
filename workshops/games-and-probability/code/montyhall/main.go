// Command montyhall runs the Monty Hall problem: exact tree enumeration
// plus a 100,000-game simulation.
//
// Rules: three doors, one car, two goats. You pick a door. The host,
// who knows where the car is, opens a different door with a goat
// behind it (choosing at random when two goat doors are available),
// then offers a switch.
//
// Prints:
//
//  1. Every branch of the probability tree with exact fractions
//  2. A seeded simulation of 100,000 games for stay and for switch
//  3. A 100-door version that makes the intuition obvious
//
// Run from the workshop folder: go run ./code/montyhall
package main

import (
	"fmt"
	"math"
	"math/big"
	"math/rand/v2"
	"strings"
)

const (
	seed  = 42
	games = 100_000
)

func banner(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 62))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 62))
}

func winLose(ok bool) string {
	if ok {
		return "WIN"
	}
	return "lose"
}

func exactTree() {
	banner("1. Exact probability tree (you always pick door 1)")
	stay, sw := new(big.Rat), new(big.Rat)
	fmt.Printf("  %4s %11s %10s %6s %7s\n", "car", "host opens", "P(branch)", "stay", "switch")
	for car := 1; car <= 3; car++ {
		var goats []int
		for _, d := range []int{2, 3} {
			if d != car {
				goats = append(goats, d)
			}
		}
		for _, opened := range goats {
			p := big.NewRat(1, int64(3*len(goats)))
			other := 5 - opened // the closed door that is not door 1: 2+3 = 5
			stayWins := car == 1
			switchWins := other == car
			if stayWins {
				stay.Add(stay, p)
			}
			if switchWins {
				sw.Add(sw, p)
			}
			fmt.Printf("  %4d %11d %10s %6s %7s\n", car, opened, p.RatString(), winLose(stayWins), winLose(switchWins))
		}
	}
	fmt.Printf("  P(win | stay)   = %s\n", stay.RatString())
	fmt.Printf("  P(win | switch) = %s\n", sw.RatString())
}

// play runs one game and reports whether the player wins the car.
func play(rng *rand.Rand, switchDoor bool, doors int) bool {
	car := rng.IntN(doors)
	pick := rng.IntN(doors)
	if !switchDoor {
		return pick == car
	}
	// The host opens every other door except one, never the car.
	// The closed door left is the car when the pick missed it,
	// otherwise a goat door. Switching wins exactly when the
	// first pick was wrong.
	return pick != car
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

func simulate() {
	banner(fmt.Sprintf("2. Simulation: %s games each, seed %d", comma(games), seed))
	rng := rand.New(rand.NewPCG(seed, 0))
	stayWins, switchWins := 0, 0
	for i := 0; i < games; i++ {
		if play(rng, false, 3) {
			stayWins++
		}
	}
	for i := 0; i < games; i++ {
		if play(rng, true, 3) {
			switchWins++
		}
	}
	for _, r := range []struct {
		name string
		w    int
	}{{"stay", stayWins}, {"switch", switchWins}} {
		f := float64(r.w) / games
		fmt.Printf("  %-7s wins %6s / %s = %.4f  %s\n", r.name, comma(r.w), comma(games), f,
			strings.Repeat("#", int(math.Round(f*50))))
	}
	fmt.Printf("  theory: stay 1/3 = %.4f, switch 2/3 = %.4f\n", 1.0/3, 2.0/3)

	fmt.Println()
	fmt.Println("  Running win rate for switch (fresh run, seed 42):")
	rng = rand.New(rand.NewPCG(seed, 0))
	wins := 0
	for n := 1; n <= 10_000; n++ {
		if play(rng, true, 3) {
			wins++
		}
		if n == 10 || n == 100 || n == 1_000 || n == 10_000 {
			fmt.Printf("    after %6s games: %.4f\n", comma(n), float64(wins)/float64(n))
		}
	}
}

func hundredDoors() {
	banner("3. Same game with 100 doors (host opens 98 goat doors)")
	rng := rand.New(rand.NewPCG(seed, 0))
	stay, sw := 0, 0
	for i := 0; i < games; i++ {
		if play(rng, false, 100) {
			stay++
		}
	}
	for i := 0; i < games; i++ {
		if play(rng, true, 100) {
			sw++
		}
	}
	fmt.Printf("  stay   win rate: %.4f  (theory 1/100 = 0.0100)\n", float64(stay)/games)
	fmt.Printf("  switch win rate: %.4f  (theory 99/100 = 0.9900)\n", float64(sw)/games)
}

func main() {
	exactTree()
	simulate()
	hundredDoors()
}
