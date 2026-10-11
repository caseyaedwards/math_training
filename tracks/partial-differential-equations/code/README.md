# Partial Differential Equations Code

Companion program for the [Partial Differential Equations Track](../README.md). It uses the Go standard library only.

[main.go](main.go) releases 20,000 random walkers, does one heat step by hand, solves the heat equation on a grid and compares with the exact answer, tests the stability limit, lists mode half-lives, checks a Fourier series solution against finite differences, splits a wave into two travellers, tunes a guitar string, and solves the Laplace equation by Jacobi iteration. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
