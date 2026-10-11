# Code: Ancient Greece

`main.go` runs four Greek methods with the Go standard library only:

* Archimedes: doubles polygon sides from 6 to 96 using only square roots and prints the half-perimeters that trap pi.
* Euclid: the Euclidean algorithm for gcd(1071, 462), one division per line.
* Eratosthenes: the sieve of primes up to 60.
* Euclid IX.20: products of the first primes plus 1, with the smallest prime factor of each.
* Root 2: fractions p/q that come ever closer to the square root of 2 while p*p - 2*q*q stays at 1 or -1.

## Run

```txt
cd code && go run main.go
```

## Expected Output

The Archimedes table ends with `96    3.14103    3.14271`, the gcd is 21, the sieve lists 17 primes up to 59, 30,031 has smallest prime factor 59, and the last fraction is 577/408. The full output is in the chapter [README](../README.md#code-corner).
