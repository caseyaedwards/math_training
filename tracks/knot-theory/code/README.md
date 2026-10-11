# Knot Theory Code

Companion program for the [Knot Theory Track](../README.md). It uses the Go standard library only.

[main.go](main.go) reads knots as planar diagram (PD) codes, the format used by the Knot Atlas. For the trefoil, its mirror image and the figure-eight knot it computes the writhe, the Kauffman bracket (by summing over all smoothing states), the Jones polynomial and the number of Fox 3- and 5-colorings. It then multiplies Jones polynomials to tell the granny knot from the square knot. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
