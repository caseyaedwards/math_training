// Command sir solves the SIR epidemic model with Euler steps.
//
//	dS/dt = -beta * S * I / N
//	dI/dt =  beta * S * I / N - gamma * I
//	dR/dt =  gamma * I
//
// It prints the parameters, R0 = beta / gamma, the herd-immunity threshold
// 1 - 1/R0, the early doubling time, a table every 10 days, the peak, an
// ASCII plot of S, I, R, and a comparison of peaks for several R0 values.
//
// Standard library only. No arguments. Run: go run ./code/sir
package main

import (
	"fmt"
	"math"
	"strings"
)

const (
	popN  = 1000000.0 // population
	i0    = 10.0      // initially infected
	dt    = 0.1       // Euler step, days
	days  = 160
	steps = 10 // Euler steps per day (1 / dt)
)

type sample struct {
	day     int
	s, i, r float64
}

// simulate returns one sample per whole day.
func simulate(beta, gamma float64, nDays int) []sample {
	s, i, r := popN-i0, i0, 0.0
	out := []sample{{0, s, i, r}}
	for step := 1; step <= nDays*steps; step++ {
		newInf := beta * s * i / popN * dt
		newRec := gamma * i * dt
		s -= newInf
		i += newInf - newRec
		r += newRec
		if step%steps == 0 {
			out = append(out, sample{step / steps, s, i, r})
		}
	}
	return out
}

func peak(smp []sample) sample {
	best := smp[0]
	for _, x := range smp {
		if x.i > best.i {
			best = x
		}
	}
	return best
}

// comma formats x as a whole number with thousands separators.
func comma(x float64) string {
	s := fmt.Sprintf("%.0f", x)
	var b strings.Builder
	for i, c := range s {
		if i > 0 && (len(s)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(c)
	}
	return b.String()
}

// asciiPlot draws S, I, R as fractions of N; one column per 2 days.
func asciiPlot(smp []sample) {
	const width, height = 80, 20
	grid := make([][]byte, height)
	for r := range grid {
		grid[r] = []byte(strings.Repeat(" ", width))
	}
	for col := 0; col < width; col++ {
		day := col * 2
		if day >= len(smp) {
			break
		}
		x := smp[day]
		for _, p := range []struct {
			frac float64
			mark byte
		}{{x.r / popN, 'R'}, {x.s / popN, 'S'}, {x.i / popN, 'I'}} {
			row := height - 1 - int(math.Round(p.frac*(height-1)))
			grid[row][col] = p.mark
		}
	}
	fmt.Println("fraction of population")
	for idx, line := range grid {
		level := 1 - float64(idx)/(height-1)
		label := "     |"
		if idx%4 == 0 || idx == height-1 {
			label = fmt.Sprintf("%4.2f |", level)
		}
		fmt.Println(strings.TrimRight(label+string(line), " "))
	}
	fmt.Println("     +" + strings.Repeat("-", width))
	ticks := ""
	for d := 0; d < width*2; d += 20 {
		ticks += fmt.Sprintf("%-10d", d)
	}
	fmt.Println(strings.TrimRight("  day "+ticks, " "))
	fmt.Println("  S = susceptible, I = infected, R = recovered (one column = 2 days)")
}

func main() {
	beta, gamma := 0.3, 0.1
	r0 := beta / gamma
	fmt.Println("SIR model, Euler steps")
	fmt.Printf("  N = 1,000,000  I0 = %.0f  beta = %.1f/day  gamma = %.1f/day  dt = %.1f day\n", i0, beta, gamma, dt)
	fmt.Printf("  R0 = beta / gamma = %.2f\n", r0)
	fmt.Printf("  mean infectious period = 1 / gamma = %.0f days\n", 1/gamma)
	fmt.Printf("  herd-immunity threshold = 1 - 1/R0 = %.1f%%\n", (1-1/r0)*100)
	g := beta - gamma
	fmt.Printf("  early growth rate beta - gamma = %.2f/day, doubling time ln 2 / %.2f = %.1f days\n",
		g, g, math.Ln2/g)

	smp := simulate(beta, gamma, days)
	pk := peak(smp)
	fmt.Println()
	fmt.Printf("%5s%12s%12s%12s\n", "day", "S", "I", "R")
	for k := 0; k < len(smp); k += 10 {
		x := smp[k]
		fmt.Printf("%5d%12s%12s%12s\n", x.day, comma(x.s), comma(x.i), comma(x.r))
	}
	fmt.Println()
	fmt.Printf("peak: day %d, %s infected at once (%.1f%%), S at peak = %.1f%% of N\n",
		pk.day, comma(pk.i), pk.i/popN*100, pk.s/popN*100)
	fmt.Printf("final: %.1f%% of the population was ever infected\n", smp[len(smp)-1].r/popN*100)
	fmt.Println()
	asciiPlot(smp)

	fmt.Println()
	fmt.Println("Effect of R0 (gamma fixed at 0.1/day)")
	fmt.Printf("%5s%7s%10s%10s%15s%11s\n", "R0", "beta", "peak day", "peak I %", "ever infected", "herd thr.")
	for _, r0 := range []float64{1.5, 2.0, 2.5, 3.0, 4.0} {
		b := r0 * gamma
		s := simulate(b, gamma, 400)
		p := peak(s)
		fmt.Printf("%5.1f%7.2f%10d%9.1f%%%14.1f%%%10.1f%%\n", r0, b, p.day, p.i/popN*100,
			s[len(s)-1].r/popN*100, (1-1/r0)*100)
	}
}
