# Images

* `clock-mod-12.svg`: a twelve-position clock with an arrow from 9 forward five hours to 2, showing (9 + 5) % 12 = 2.
* `number-line-wrap.svg`: the integers -12 to 35 cut into rows of twelve, so congruent numbers line up in columns (14 under 2, -4 under 8).
* `euclid-rectangle.svg`: a 30 by 12 rectangle tiled by squares, showing gcd(30, 12) = 6.
* `back-substitution.svg`: extended Euclid by hand for 7 mod 40, Euclid down on the left and substitution up on the right, ending at the inverse 23.
* `inverse-tables.svg`: multiplication tables mod 7 and mod 8 with the 1s highlighted; rows without a 1 have no inverse.
* `exponent-ladder.svg`: naive multiplication (16 steps) next to square-and-multiply (1, 2, 4, 8, 16, 17) for the exponent 17.
* `square-and-multiply.svg`: the five square-and-multiply steps for 65^17 mod 3233, one box per binary digit of 17.
* `totient-grid.svg`: phi(12) = 4 as highlighted circles, and phi(15) = 8 as a 3 by 5 grid with multiples of 3 and 5 crossed out.
* `euler-cycle.svg`: powers of 2 and 7 mod 15 looping back to 1, with k = 8 = phi(15) a full lap.
* `rsa-keygen.svg`: toy RSA key generation from p = 61 and q = 53 to n, phi, e and d, colored public or secret.
* `rsa-flow.svg`: toy RSA with n = 3233, encrypt 65 to 2790 and back, sign digest 123 to 2746 and verify.
* `diffie-hellman.svg`: toy Diffie-Hellman with p = 23 and g = 5, the public wire Eve sees, and the shared secret 2.
* `dh-powers-scatter.svg`: a scatter plot of 5^k mod 23 for k = 1 to 22, showing no pattern to exploit.
* `mod-vs-ring.svg`: a table of hashes 0 to 19 under % 4 and % 5 showing 80% of keys move, and a consistent-hash ring where a new node takes one arc.
* `moved-fraction-bars.svg`: grouped bars of keys moved by hash % N versus a consistent-hash ring for 2 to 3, 4 to 5, 8 to 9, and 16 to 17 nodes.
