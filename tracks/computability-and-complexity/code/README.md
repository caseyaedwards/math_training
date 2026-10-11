# Computability and Complexity Code

Companion program for the [Computability and Complexity Track](../README.md). It uses the Go standard library only.

[main.go](main.go) runs a DFA, simulates an NFA, races a backtracking regex engine against a DFA and the Go `regexp` package, checks parentheses with a stack, runs a Turing machine that adds 1, puts a step budget on a Collatz run, prints growth rates, and compares brute force with certificates and shortcuts for subset sum, 3-SAT, vertex cover and scheduling. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner). The backtracking section counts 201,326,590 steps at n = 25. Each extra character doubles that count.
