# Code: The Scientific Revolution and Calculus

`main.go` runs the four methods of [chapter 07](../README.md):

* Secant slopes of y = x² at x = 1 with a shrinking step h: 3, 2.5, 2.1, 2.01, 2.001, closing in on 2.
* Left-edge strip sums for the area under y = x² from 0 to 2: 2.1875 with eight strips, closing in on 8/3.
* A logarithm check: log 2 + log 3 = log 6 = 0.77815.
* Pascal's triangle, rows 0 to 7, and the problem of points (A needs 1, B needs 2: A gets 3/4).

Run it with Go (standard library only):

```txt
cd code && go run main.go
```

The chapter README shows the full expected output.
