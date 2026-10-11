# Functional Analysis Code

Companion program for the [Functional Analysis Track](../README.md). It uses the Go standard library only.

[main.go](main.go) treats functions as vectors, computes three norms, compares L2 and sup convergence, checks orthogonality, projects f(x) = x onto sines, runs Gram-Schmidt, tests the parallelogram law, finds an operator norm by power iteration, shows that differentiation is unbounded, computes eigenvalues of the second derivative on a grid, and checks the kernel trick. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
