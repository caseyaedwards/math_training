# Code: India and China

`main.go` runs five methods from the chapter with the Go standard library only:

* Sulba Sutras: the value 1 + 1/3 + 1/12 - 1/408 for root 2 and its error.
* Sunzi: a brute-force search for the number that leaves 2 by 3, 3 by 5, and 2 by 7.
* Nine Chapters 8.1: fangcheng elimination of a 3 by 3 system, whole numbers until the last step, exact fractions with `math/big`.
* Pi fractions: Aryabhata 62,832/20,000 and Zu Chongzhi 22/7 and 355/113, with their errors.
* Madhava: the series 4(1 - 1/3 + 1/5 - ...) with and without his end correction.

## Run

```txt
cd code && go run main.go
```

## Expected Output

The Sunzi answer is 23, the fangcheng answers are 37/4, 17/4, and 11/4 dou, 355/113 has an error of about 2.7e-07, and after 16 terms the plain Madhava sum is 3.079153394 while the corrected sum is 3.141592419. The full output is in the chapter [README](../README.md#code-corner).
