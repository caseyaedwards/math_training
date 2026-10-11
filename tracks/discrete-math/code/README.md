# Discrete Math Code Corner

A single Go program for the [Discrete Math track](../README.md). It checks an induction formula, compares two recurrences with their closed forms (Towers of Hanoi and Fibonacci), counts binary search steps, and tests the Königsberg bridges for an Euler walk.

## Run It

```txt
cd tracks/discrete-math/code
go run main.go
```

Standard library only. Go prints maps with sorted keys, so the output is stable.

## Output

```txt
sum formula holds for n = 1..1000: true | sum to 100 = 5050
hanoi(1) = 1, 2^1 - 1 = 1
hanoi(2) = 3, 2^2 - 1 = 3
hanoi(3) = 7, 2^3 - 1 = 7
hanoi(5) = 31, 2^5 - 1 = 31
hanoi(10) = 1023, 2^10 - 1 = 1023
F(0) = 0, Binet = 0
F(10) = 55, Binet = 55
F(20) = 6765, Binet = 6765
F(30) = 832040, Binet = 832040
binary search over 1000 items: at most 10 comparisons
binary search over 1000000 items: at most 20 comparisons
binary search over 1000000000 items: at most 30 comparisons
Konigsberg degrees map[A:5 B:3 C:3 D:3], sum 14 = 2 x 7 edges, odd vertices 4
Euler walk over every bridge exists: false
```

## Things to Try

1. Checking 1,000 cases is evidence, not proof. Read rung 5 of the track for the proof that covers every $n$.
2. Print Binet's formula for $n = 80$ and compare with the loop. Floating point starts to drift around $n = 71$, a good reminder of why exact integer recurrences matter.
3. Remove one bridge from `edges` so that exactly two land masses have odd degree, and confirm an Euler walk now exists.
