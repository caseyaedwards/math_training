# Algebraic Geometry Code

Companion program for the [Algebraic Geometry Track](../README.md). It uses the Go standard library only.

[main.go](main.go) generates Pythagorean triples from slopes, classifies conics by the discriminant, checks the Bezout examples, adds points on $y^2 = x^3 - x + 1$ with exact fractions from `math/big`, counts the same curve mod 29, and runs a toy elliptic curve Diffie-Hellman key exchange. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
