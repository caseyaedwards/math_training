# Chapter 01 Code: Counting Lab

A single Go program (standard library only) that explores the methods of [Chapter 01](../README.md):

- Sums the three rows of the Ishango bone and flags the prime groups.
- Runs the shepherd pebble check: one pebble removed per returning sheep, then reports leftovers on both sides.
- Writes 47 in bases 5, 10, 20, and 60.
- Draws a tally of 23 in slashed groups of five.

## Run

```txt
cd code && go run main.go
```

## Expected Output

```txt
Ishango bone rows:
  Row A: [11 13 17 19] sum 60, primes: 11 13 17 19
  Row B: [3 6 4 8 10 5 5 7] sum 48, primes: 3 5 5 7
  Row C: [11 21 19 9] sum 60, primes: 11 19

Shepherd at dusk (7 pebbles in the bag):
  7 sheep return: pebbles left 0, unmatched sheep 0
  6 sheep return: pebbles left 1, unmatched sheep 0
  8 sheep return: pebbles left 0, unmatched sheep 1

47 sheep written in different bases (digits, biggest place first):
  base  5: [1 4 2]
  base 10: [4 7]
  base 20: [2 7]
  base 60: [47]

Tally of 23 in groups of five:
  ||||/ ||||/ ||||/ ||||/ |||
```
