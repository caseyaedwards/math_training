# Differential Geometry Code

Companion program for the [Differential Geometry Track](../README.md). It uses the Go standard library only.

[main.go](main.go) estimates curvature and torsion with finite differences, computes Gaussian curvature for a sphere cap, a cylinder and two saddles, measures the angles of a triangle on the sphere, compares a latitude route with a great circle, and works out the relativity correction for GPS clocks. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
