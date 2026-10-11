# Optimization Code

Companion program for the [Optimization Track](../README.md). It uses the Go standard library only.

[main.go](main.go) finds the cheapest replica count, runs gradient descent with four step sizes, checks the Lagrange fence, solves a linear program with a small simplex method and prints its shadow prices, prices an instance mix by its corners, solves an integer program by branch and bound, packs pods onto nodes with first fit and first fit decreasing, and backtracks through a maintenance schedule. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
