# Chapter 02 Code: Scribe Lab

A single Go program (standard library only) that explores the methods of [Chapter 02](../README.md):

- Approximates the square root of 2 by averaging, with exact fractions (`math/big`), and prints each step in base 60 and in decimal.
- Decodes the YBC 7289 value 1;24,51,10 and checks the diagonal 30 x 1;24,51,10 = 42;25,35.
- Multiplies 13 x 24 by Egyptian doubling and prints the table with the used rows marked `\`.
- Splits fractions into unit fractions with the greedy method.

## Run

```txt
cd code && go run main.go
```

## Expected Output

```txt
Square root of 2 by averaging (start with a 1 by 2 rectangle):
  step 1: 3/2            = 1;30,0,0,0        = 1.500000000
  step 2: 17/12          = 1;25,0,0,0        = 1.416666667
  step 3: 577/408        = 1;24,51,10,35     = 1.414215686
  step 4: 665857/470832  = 1;24,51,10,7      = 1.414213562

YBC 7289 value 1;24,51,10 = 1.414212963
its square                = 1.999998305
30 x 1;24,51,10           = 42;25,35,0

Egyptian multiplication 13 x 24:
  \    1     24
       2     48
  \    4     96
  \    8    192
  total = 312

Greedy unit fractions:
  2/5 = 1/3 + 1/15
  2/7 = 1/4 + 1/28
  2/13 = 1/7 + 1/91
  3/7 = 1/3 + 1/11 + 1/231
  5/6 = 1/2 + 1/3
```
