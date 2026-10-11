# Coding Theory Code

Companion program for the [Coding Theory Track](../README.md). It uses the Go standard library only.

[main.go](main.go) computes repetition-code error rates, parity and checksum results, Hamming distances, the Hamming (7,4) generator and parity-check matrices with an exhaustive single-error test, CRC long division step by step, finite field inverses, Reed-Solomon erasure recovery over GF(7), a RAID 5 rebuild, storage durability for six schemes, a peeling decoder and a random fountain experiment. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The fountain experiment uses a fixed random seed, which keeps the output identical on every run. The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
