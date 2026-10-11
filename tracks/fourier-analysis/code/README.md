# Fourier Analysis Code

Companion program for the [Fourier Analysis Track](../README.md). It uses the Go standard library only.

[main.go](main.go) computes square wave coefficients and the Gibbs overshoot, does a DFT by hand, checks a radix-2 FFT against the direct DFT, finds the daily and weekly cycles in synthetic request rates, compresses that series by keeping its largest frequencies, convolves two ways, filters out a hum, shows aliasing, and runs a Haar transform. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
