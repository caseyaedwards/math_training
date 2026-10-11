# Topology Code

Companion program for the [Topology Track](../README.md). It uses the Go standard library only.

[main.go](main.go) computes $V - E + F$ from face lists (including a torus glued from a 3 by 3 grid), measures winding numbers, counts holes in letter bitmaps with a flood fill, and watches noisy circle points merge into one ring as the radius grows. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
