# Code

Three Go programs, standard library only, one folder each. Tested with Go 1.27.2. Any Go 1.22 or newer runs them (they use `math/rand/v2`). Run them from the workshop folder, which holds a small `go.mod`:

```sh
go run ./code/nines
go run ./code/burnrate
go run ./code/availability
```

Each one takes no arguments, finishes in well under a second, and prints the same output every time. Randomness uses a fixed seed: `rand.New(rand.NewPCG(42, 42))`.

## nines

Prints a table of allowed downtime per day, per 30-day window, and per 365-day year for SLOs from 99% to 99.999%, a text-mode nines ladder on a log scale, and the error budget in failed requests for 50,000,000 requests per 30 days.

## burnrate

For a 99.9% SLO over 30 days, prints the budget in minutes and requests, burn rates for several error rates, the multiwindow, multi-burn-rate alert table with the budget each alert consumes, time to exhaustion, and a text-mode burn-down for a month with one 14.4x incident.

## availability

Prints series availability for a three-part chain, parallel availability for one to five 99% replicas, a seeded simulation of 1,000,000 minutes that checks $1 - q^N$, a correlated-failure case with a shared availability zone, and the chance of at least one page in a week, checked by simulating 20,000 weeks.
