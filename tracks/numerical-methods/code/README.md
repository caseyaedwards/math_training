# Numerical Methods Code

Companion program for the [Numerical Methods Track](../README.md). It uses the Go standard library only.

[main.go](main.go) shows the classic float surprises, measures machine epsilon, repairs a long sum with Kahan summation, fixes a cancellation by rewriting the formula, races bisection against Newton, integrates with trapezoids and Simpson, and finds the step size where Euler explodes. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
