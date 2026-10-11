# Chapter 09 Code: Turing Machines and Entropy

[main.go](main.go) is a small Turing machine simulator plus a Shannon entropy calculator. Go standard library only.

It does three things:

* Runs the binary increment machine from the chapter diagram on 1011 (printing each step) and on 111.
* Runs the two-state busy beaver on a blank tape.
* Prints the entropy in bits of a fair coin, a 90/10 coin, a fair die, eight equal outcomes, and the distribution 1/2, 1/4, 1/8, 1/8.

Run it:

```txt
go run main.go
```

Key lines of the expected output:

```txt
  1011 + 1 = 1100 in 3 steps
Two-state busy beaver: tape 1111, 4 ones, 6 steps
  fair coin         1.000
  coin 90/10        0.469
  fair die          2.585
  8 equal outcomes  3.000
  1/2 1/4 1/8 1/8   1.750
```

The full output is in the chapter [Code Corner](../README.md#code-corner).
