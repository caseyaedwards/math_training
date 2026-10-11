# Logic and Set Theory Code Corner

A single Go program for the [Logic and Set Theory track](../README.md). It prints a truth table for an implication and its contrapositive, checks a De Morgan law on every row, lists a power set with bitmasks, and runs Cantor's diagonal trick on a small list.

## Run It

```txt
cd tracks/logic-and-set-theory/code
go run main.go
```

Standard library only.

## Output

```txt
p q | p->q | !q->!p
T T |  T   |   T
T F |  F   |   F
F T |  T   |   T
F F |  T   |   T
De Morgan holds on all 4 rows: true
power set has 8 subsets: {} {a} {b} {a,b} {c} {a,c} {b,c} {a,b,c}
diagonal-flipped string 1100 is in the list: false
```

## Things to Try

1. Add a column for the converse, `q -> p`, and find the rows where it differs from `p -> q`.
2. Check the other De Morgan law: `!(p || q) == (!p && !q)`.
3. Add a fourth element to `elems` and confirm the power set has 16 subsets.
4. Change the rows in the diagonal demo. The flipped string never appears, no matter what you list.
