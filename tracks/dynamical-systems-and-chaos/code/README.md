# Dynamical Systems and Chaos Code

Companion program for the [Dynamical Systems and Chaos Track](../README.md). It uses the Go standard library only.

[main.go](main.go) presses `cos` 40 times, applies the slope test to the logistic map and detects the period of each orbit, estimates the Feigenbaum constant from superstable parameter values, measures Lyapunov exponents, follows two logistic orbits that start 0.0000000001 apart, simulates a retry storm and a delayed autoscaler, integrates the Lorenz system with RK4 at step 0.01, draws the Mandelbrot set in ASCII, and grows the Koch curve. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
