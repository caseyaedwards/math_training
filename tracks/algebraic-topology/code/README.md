# Algebraic Topology Code

Companion program for the [Algebraic Topology Track](../README.md). It uses the Go standard library only.

[main.go](main.go) computes Euler characteristics, finds Betti numbers of simplicial complexes from boundary matrices (rank mod 2), counts winding numbers, finds a Brouwer fixed point by bisection, and runs a Vietoris-Rips persistence scan on a noisy ring of 12 points. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
