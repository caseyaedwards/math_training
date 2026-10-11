# Code

Three Go programs, standard library only, one folder each. They need no arguments, print the same output on every run, and finish in well under one second. Tested with Go 1.27.2. The `go.mod` file in the workshop folder (Go 1.22 or later) lets `go run ./code/<name>` work from there.

> **For learning only.** The RSA and Diffie-Hellman code uses tiny primes and no padding. Never use it to protect real data. Use Go `crypto/tls`, `crypto/rsa`, and `crypto/ecdh`.

Run each program from the workshop folder (the one holding `go.mod`):

```txt
go run ./code/toyrsa
go run ./code/diffiehellman
go run ./code/hashbuckets
```

Or from inside a program folder: `go run main.go`.

## toyrsa

Prints seven labelled sections:

* Modular arithmetic: the Go `%` sign trap and a `mod` helper.
* Euclid: the Euclidean and extended Euclidean algorithm as a table for (3120, 17).
* Inverse: the modular inverse 2753, checked against `big.Int.ModInverse`.
* Fast power: a square-and-multiply trace for 65^17 mod 3233, checked against `big.Int.Exp`, with the full 31-digit power shown.
* Totient: values of Euler phi and a check of Euler theorem.
* RSA: key generation, then encryption and decryption of 65 and of the text `HI`.
* Signatures: a valid signature, a tampered one that fails, and a trial-division factoring of 3233 that shows why the key is a toy.

## diffiehellman

Prints every power of g = 5 mod p = 23 as an ASCII bar chart (5 is a generator), the public values Alice and Bob send (8 and 19), the shared secret both compute (2), and what an eavesdropper sees, including a brute-force discrete log that works only because p is tiny.

## hashbuckets

Hashes 10,000 keys with `crypto/sha256` (stable on every machine, unlike Go map order or `hash/maphash`), shows the spread under `% 4` as a bar chart, counts the keys that move from 4 to 5 buckets with `hash % N` (7,973) and with a consistent-hash ring of 100 virtual nodes per node (1,892), and prints a summary table for 2 to 3, 4 to 5, 8 to 9, and 16 to 17 nodes.
