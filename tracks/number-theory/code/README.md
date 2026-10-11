# Number Theory Code Corner

A single Go program that runs the main tools of the [Number Theory track](../README.md): the sieve, the Euclidean algorithm, the extended Euclidean algorithm (Bezout coefficients), fast modular exponentiation, and a toy RSA round trip.

## Run It

```txt
cd tracks/number-theory/code
go run main.go
```

Standard library only. Go 1.21 or newer works.

## Output

```txt
primes up to 100 (25): [2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97]
gcd(84, 36) = 12
Bezout: 240*(-9) + 46*(47) = 2
7^100 mod 5 = 1
Fermat check 3^12 mod 13 = 1
RSA: n=3233 phi=3120 e=17 d=2753
RSA: message 65 -> ciphertext 2790 -> decrypted 65
```

## Things to Try

1. Change `sieve(100)` to `sieve(1000000)` and print only `len(p)`. The answer is 78,498.
2. Replace `powMod` with a loop that multiplies `exp` times. Time both with an exponent of 10,000,000.
3. Pick new toy primes for RSA, for example 101 and 113, and a new `e` with `gcd(e, phi) = 1`.
