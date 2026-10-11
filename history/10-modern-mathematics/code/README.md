# Chapter 10 Code: RSA, Map Coloring, and the Mandelbrot Set

[main.go](main.go) explores four ideas from the chapter. Go standard library only.

* Builds the toy RSA key from p = 61 and q = 53 with `math/big`, encrypts 65 to 2790, and decrypts it back.
* Shows square-and-multiply step by step for 65^17 mod 3233.
* Counts proper colorings of the wheel map (center, ring of five, outer region) with two, three, and four colors.
* Prints an ASCII Mandelbrot set for real parts -2.2 to 0.8 and imaginary parts -1.2 to 1.2.

Run it:

```txt
go run main.go
```

Key lines of the expected output:

```txt
Toy RSA: n = 3233, phi = 3120, e = 17, d = 2753
  encrypt 65 -> 2790, decrypt 2790 -> 65
  answer: 2790
  2 colors:    0 colorings  first: []
  3 colors:    0 colorings  first: []
  4 colors:  120 colorings  first: [1 2 3 2 3 4 1]
```

The full output, including the Mandelbrot picture, is in the chapter [Code Corner](../README.md#code-corner).
