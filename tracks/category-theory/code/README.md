# Category Theory Code

Companion program for the [Category Theory Track](../README.md). It uses the Go standard library only and needs Go 1.21 or newer for generics and the `slices` package.

[main.go](main.go) composes funcs and checks the identity and associativity laws, builds a pipe of `grep`, `sort` and `uniq`, checks the functor laws for slices and options, walks the naturality square for `First` (and catches a generic func that breaks it), builds products and coproducts, counts arrows between small finite sets by brute force, and chains steps that fail with a monad. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

Go cannot compare two funcs for equality. The program checks every law on sample inputs, which is evidence, not proof. The proofs live in the track README.

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
