# Code

Four small Go programs, one folder each, standard library only. Tested with Go 1.27.2. The `go.mod` file in the workshop folder lets `go run ./code/<name>` work from there.

Run each program from the workshop folder:

```txt
go run ./code/compound
go run ./code/capacity
go run ./code/sir
go run ./code/backoff
```

Or step into a folder and run `go run .` (or `go run main.go`).

| Program | What it prints |
|---|---|
| `compound/main.go` | Compound interest for n = 1, 12, 365 and continuous; (1 + 1/n)^n approaching e; exact doubling time versus the rules of 72, 70, and 69.3; half-life decay for carbon-14 and a cache score with a 60 s half-life. |
| `capacity/main.go` | Month-by-month load at 8% growth with a capacity bar chart; months to double, to reach 70% of capacity, and to reach capacity; the same for other growth rates; equal log10 steps; a growth rate recovered from two readings. |
| `sir/main.go` | SIR parameters, R0, the herd-immunity threshold, a table every 10 days, the peak, an ASCII plot of S, I, and R, and a comparison across R0 values. |
| `backoff/main.go` | The backoff ceiling per attempt, then for no jitter, full jitter, and equal jitter: total calls, the most retries in one 10 ms slot, the finish time, and an ASCII histogram of retries per 100 ms. Seeded with `rand.NewPCG(42, 42)`, which gives the same output on every run. |

All programs take no arguments and finish in well under a second. To experiment, change the constants at the top of a file (for example `growth` in `capacity/main.go` or `capacity` in `backoff/main.go`) and run it again.
