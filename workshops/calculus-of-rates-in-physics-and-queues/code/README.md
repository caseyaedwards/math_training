# Code

Three Go programs, standard library only. Each lives in its own folder as a single `main.go` with `package main`. The `go.mod` file in the workshop folder (no dependencies) lets Go find them by path. Run them from the workshop folder:

```txt
go run ./code/counter-rate
go run ./code/falling-object
go run ./code/queue-sim
```

Or step into a program folder and run `go run .` or `go run main.go`.

Tested with:

```txt
go version go1.27.2 darwin/arm64
```

Any Go 1.21 or newer works. Output is deterministic: the queue simulation seeds its random source with `rand.New(rand.NewSource(42))`. All three finish in under a second.

## What Each Program Prints

* [counter-rate/main.go](counter-rate/main.go): the difference quotient of c(t) = 50t + 0.1t² at t = 60 for shrinking h, a 15-second scrape table with a counter reset at t = 200 and the reset fix, rate() over two one-minute windows compared with the true slope, and increase() and Riemann sums (left, right, trapezoid) compared with the exact integral.
* [falling-object/main.go](falling-object/main.go): exact height and velocity of an object dropped from 100 m with a text bar chart of height, the impact time and speed, Euler integration errors at t = 4 s for five step sizes, and the impact time found by Euler stepping.
* [queue-sim/main.go](queue-sim/main.go): two Little's law examples, the M/M/1 table of latency, wait and queue length at 50% to 99% utilization with a text bar chart, and a seeded discrete-event simulation at 50%, 80% and 90% utilization compared with the formulas.
