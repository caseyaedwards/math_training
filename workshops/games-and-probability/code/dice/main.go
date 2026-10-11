// Command dice covers dice sample spaces, expected value, and the law
// of large numbers.
//
// Prints:
//
//  1. The 36-outcome sample space for two dice as a 6 x 6 grid of sums
//  2. The distribution of the sum as an ASCII bar chart
//  3. Expected value of one die, a carnival game, and a lottery ticket
//  4. The law of large numbers: a seeded running average of die rolls,
//     as a table and as an ASCII plot
//
// Flag -trace prints "n,average" for every roll (used to draw the SVG).
//
// Run from the workshop folder: go run ./code/dice
package main

import (
	"flag"
	"fmt"
	"math"
	"math/big"
	"math/rand/v2"
	"strings"
)

const (
	seed  = 42
	rolls = 10_000
)

func banner(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 62))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 62))
}

func money(x float64) string {
	if x < 0 {
		return fmt.Sprintf("-$%.4f", -x)
	}
	return fmt.Sprintf("$%.4f", x)
}

// comb returns n choose k.
func comb(n, k int64) int64 { return new(big.Int).Binomial(n, k).Int64() }

func comma(n int64) string {
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

func sampleSpace() {
	banner("1. Two dice: 36 equally likely outcomes (cell = sum)")
	head := []string{}
	for b := 1; b <= 6; b++ {
		head = append(head, fmt.Sprintf("%3d", b))
	}
	fmt.Println("       die 2: " + strings.Join(head, " "))
	for a := 1; a <= 6; a++ {
		cells := []string{}
		for b := 1; b <= 6; b++ {
			if a+b == 7 {
				cells = append(cells, "[7]")
			} else {
				cells = append(cells, fmt.Sprintf("%3d", a+b))
			}
		}
		fmt.Printf("  die 1 = %d:  %s\n", a, strings.Join(cells, " "))
	}
	fmt.Println("  [7] marks the six cells on the 7-diagonal")
}

func sumDistribution() {
	banner("2. Distribution of the sum of two dice")
	counts := map[int]int{}
	for a := 1; a <= 6; a++ {
		for b := 1; b <= 6; b++ {
			counts[a+b]++
		}
	}
	for s := 2; s <= 12; s++ {
		c := counts[s]
		fmt.Printf("  sum %2d: %d/36 = %.3f  %s\n", s, c, float64(c)/36, strings.Repeat("#", c*4))
	}
	fmt.Println("  most likely sum: 7 with probability 6/36 = 1/6")
}

func expectedValues() {
	banner("3. Expected value")
	fmt.Printf("  one fair die: (1+2+3+4+5+6)/6 = 21/6 = %.1f\n", 21.0/6)

	fmt.Println()
	fmt.Println("  Carnival game: pay $2, roll one die, a 6 pays a $10 prize")
	win := 10.0 / 6
	fmt.Printf("    E[prize] = (1/6)(10) + (5/6)(0) = 10/6 = %s\n", money(win))
	fmt.Printf("    E[net]   = 10/6 - 2 = -2/6 = %s per play\n", money(win-2))

	fmt.Println()
	fmt.Println("  Lottery: pay $2, pick 6 of 49 numbers")
	total := comb(49, 6)
	prizes := map[int64]float64{6: 5_000_000, 5: 1_000, 4: 100, 3: 10}
	fmt.Printf("    total tickets C(49,6) = %s\n", comma(total))
	fmt.Printf("    %5s %10s %14s %12s %13s\n", "match", "ways", "probability", "prize", "contribution")
	ePrize := 0.0
	for _, k := range []int64{6, 5, 4, 3} {
		ways := comb(6, k) * comb(43, 6-k)
		p := float64(ways) / float64(total)
		contrib := p * prizes[k]
		ePrize += contrib
		fmt.Printf("    %5d %10s %14.8f %12s %13.4f\n", k, comma(ways), p, comma(int64(prizes[k])), contrib)
	}
	fmt.Printf("    E[prize] = %s\n", money(ePrize))
	fmt.Printf("    E[net]   = %s per $2 ticket (%.1f%% of the stake)\n", money(ePrize-2), 100*(ePrize-2)/2)
}

func lawOfLargeNumbers(trace bool) {
	rng := rand.New(rand.NewPCG(seed, 0))
	checkpoints := map[int]bool{1: true, 2: true, 5: true, 10: true, 20: true, 50: true, 100: true,
		200: true, 500: true, 1_000: true, 2_000: true, 5_000: true, 10_000: true}
	type row struct {
		n   int
		avg float64
	}
	var rows []row
	total := 0
	for n := 1; n <= rolls; n++ {
		total += rng.IntN(6) + 1
		avg := float64(total) / float64(n)
		if trace {
			fmt.Printf("%d,%.6f\n", n, avg)
		}
		if checkpoints[n] {
			rows = append(rows, row{n, avg})
		}
	}
	if trace {
		return
	}
	banner(fmt.Sprintf("4. Law of large numbers: %s rolls, seed %d", comma(rolls), seed))
	fmt.Printf("  %7s %8s %13s\n", "rolls", "average", "gap from 3.5")
	for _, r := range rows {
		fmt.Printf("  %7s %8.4f %+13.4f\n", comma(int64(r.n)), r.avg, r.avg-3.5)
	}

	fmt.Println()
	fmt.Println("  ASCII plot: running average (each row = one checkpoint)")
	lo, hi, width := 2.5, 4.5, 40
	col := int(math.Round((3.5 - lo) / (hi - lo) * float64(width)))
	fmt.Printf("  %7s %-*s3.5%*s\n", "", col, "2.5", width-col-2, "4.5")
	for _, r := range rows {
		line := []byte(strings.Repeat(" ", width+1))
		line[col] = '|'
		pos := int(math.Round((r.avg - lo) / (hi - lo) * float64(width)))
		switch {
		case pos > width:
			line[width] = '>'
		case pos < 0:
			line[0] = '<'
		default:
			line[pos] = '*'
		}
		fmt.Printf("  %7s %s\n", comma(int64(r.n)), string(line))
	}
	fmt.Println("  (* = running average, | = 3.5, > = off the chart)")
}

func main() {
	trace := flag.Bool("trace", false, "print n,average for every roll and exit")
	flag.Parse()
	if *trace {
		lawOfLargeNumbers(true)
		return
	}
	sampleSpace()
	sumDistribution()
	expectedValues()
	lawOfLargeNumbers(false)
}
