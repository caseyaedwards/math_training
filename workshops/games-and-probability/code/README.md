# Code

Four Go programs, standard library only, one folder each. They need no arguments, use a fixed seed (`rand.NewPCG(42, 0)` from `math/rand/v2`; the pasted output comes from Go 1.27.2), and finish in about a second each. Tested with Go 1.27.2. The `go.mod` file in the workshop folder (Go 1.22 or later) lets `go run ./code/<name>` work from there.

Run each program from the workshop folder (the one holding `go.mod`):

```txt
go run ./code/dice
go run ./code/montyhall
go run ./code/birthday
go run ./code/martingale
```

Or from inside a program folder: `go run main.go`.

## dice

Prints the 36-outcome grid of two-dice sums with the 7-diagonal marked, the distribution of the sum as a bar chart, expected values for one die (3.5), a carnival game (-\$0.3333 per play), and a 6-of-49 lottery ticket (-\$1.3506 per \$2 ticket), then the running average of 10,000 seeded rolls as a table and an ASCII plot. The optional flag `-trace` prints `n,average` for every roll instead; that data draws `img/running-average.svg`.

## montyhall

Prints the exact Monty Hall tree with fractions (stay 1/3, switch 2/3), a 100,000-game simulation for each strategy (stay 0.3344, switch 0.6669), the running switch win rate, and a 100-door version (switch 0.9905).

## birthday

Prints exact shared-birthday probabilities with a bar chart, the 50% threshold at 23 people, a 20,000-group simulation per group size, and the hash-collision version: keys needed for a 50% collision chance with 16-, 32-, 64-, and 128-bit hashes, plus a 16-bit simulation of the first collision.

## martingale

Prints the doubling ladder for a \$255 bankroll, the exact expected value of one martingale cycle on roulette red (-\$0.5073), a 10,000-session simulation with a histogram of results, and the gambler's ruin formula against simulation for a fair coin and for roulette red.
