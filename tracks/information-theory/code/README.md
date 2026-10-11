# Information Theory Code

Companion program for the [Information Theory Track](../README.md). It uses the Go standard library only.

[main.go](main.go) computes entropies, builds the Huffman code, measures KL divergence and channel capacity, encodes and repairs a Hamming (7,4) codeword, and compresses a repetitive log next to random bytes. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
