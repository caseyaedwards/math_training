# Stochastic Processes and Queueing Code

Companion program for the [Stochastic Processes and Queueing Track](../README.md). It uses the Go standard library only.

[main.go](main.go) simulates random walks, steps a two-state Markov chain to its steady state, generates Poisson arrivals, tabulates M/M/1 formulas, simulates one million requests through an M/M/1 queue, computes Erlang C for pooling and capacity planning, and evaluates the Kingman and fan-out formulas. The random seed is fixed, which makes every run print the same numbers. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
