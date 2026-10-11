# Galois Theory Code

Companion program for the [Galois Theory Track](../README.md). It uses the Go standard library only.

[main.go](main.go) solves a quadratic and the Bombelli cubic by formula with `complex128`, shuffles the roots to show which expressions stay put, checks that the four symmetries of the field with root 2 and root 3 respect multiplication, follows z to z² around the fifth roots of unity, computes the derived series of S3, S4 and S5 by brute force, finds the real and complex roots of x⁵ - 4x + 2, and tests which numbers and regular polygons a ruler and compass reach. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
