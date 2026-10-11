# Code: Islamic Golden Age

`main.go` replays two methods from [Chapter 05](../README.md):

* Al-Khwarizmi's recipe for $x^2 + bx = c$ (halve, square, add, take the root, subtract the half), printed step by step for three equations.
* Omar Khayyam's cubic $x^3 + 4x = 16$, solved by bisection and checked against his parabola $y = x^2/2$ and circle with center $(2, 0)$ and radius 2.

Run it (Go standard library only):

```txt
cd code && go run main.go
```

Expected output ends with:

```txt
  bisection root: 2.000000000
  parabola point: (2.000000, 2.000000)
  distance to circle center (2, 0): 2.000000 (radius 2)
  geometric answer: x = 2, check 2^3 + 4 x 2 = 16
```
