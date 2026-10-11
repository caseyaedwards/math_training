# Code: The 18th and 19th Centuries: Rigor

`main.go` runs four small programs for [chapter 08](../README.md):

* Euler's bridge test: degrees of each land mass and whether a walk crosses every bridge once. Königsberg gives A=5, B=3, C=3, D=3: four odd nodes, no walk. An eighth bridge from B to C leaves two odd nodes, and a walk exists.
* Gauss's sum 1 + 2 + ... + 100 three ways: a loop, 50 x 101, and n(n + 1)/2. All give 5,050.
* Cantor's zigzag listing of the positive fractions: 1/1, 1/2, 2/1, 3/1, 1/3, 1/4, 2/3, 3/2, 4/1, 5/1, 1/5.
* Cantor's diagonal on six binary rows: diagonal 010100, flipped 101011.

Run it with Go (standard library only):

```txt
cd code && go run main.go
```

The chapter README shows the full expected output.
