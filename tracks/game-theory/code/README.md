# Game Theory Code

Companion program for the [Game Theory Track](../README.md). It uses the Go standard library only.

[main.go](main.go) searches 2x2 games for pure Nash equilibria by checking best responses, solves the mixed equilibrium of the retry game, solves a zero-sum defender game by minimax, runs a seeded round-robin tournament of the repeated prisoner's dilemma, computes Braess paradox and the Pigou price of anarchy, simulates first-price and second-price auctions, and finds winning Nim moves with XOR, checked against brute force. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

Every random number comes from a fixed seed. The output is the same on every run. The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).

Ideas to try:

* Add a strategy to the tournament, such as tit-for-two-tats (defect only after two defections in a row), and see how the ranking changes.
* Change the retry payoffs and watch the mixed equilibrium move.
* Raise the number of bidders and compare the simulated revenue to $100 (n - 1)/(n + 1)$.
