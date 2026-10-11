# Real Analysis Code

Companion program for the [Real Analysis Track](../README.md). It uses the Go standard library only.

[main.go](main.go) finds $N$ for several values of $\varepsilon$, compares a convergent and a divergent series, closes in on $\sqrt{2}$ with nested intervals, squeezes Riemann sums onto $1/3$, and shows why $x^n$ fails to converge uniformly. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
