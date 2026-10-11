# Code: Medieval and Renaissance Europe

`main.go` replays methods from [Chapter 06](../README.md):

* Fibonacci's rabbits, month by month, with young and adult pairs, in the modern convention and in Fibonacci's own (377 pairs after a year).
* Ratios of neighboring Fibonacci numbers next to the golden ratio.
* Lattice (gelosia) multiplication of any two digit strings, checked against `math/big`.
* Cardano's formula for $x^3 + 6x = 20$ and Bombelli's complex cube roots for $x^3 = 15x + 4$.

Run it (Go standard library only):

```txt
cd code && go run main.go
```

Expected output includes:

```txt
  [1 2 3 5 8 13 21 34 55 89 144 233 377]
  47 x 36 = 1692 (check: true)
  cbrt(20.392305) - cbrt(0.392305) = 2.000000000000
  sum of the two cube roots = (4.000000+0.000000i)
```
