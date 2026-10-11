# Code

Three Go programs, standard library only, one folder each. Tested with Go 1.27.2. Any Go 1.22 or newer runs them (they use `math/rand/v2` and `slices`). Run them from the workshop folder, which holds a small `go.mod`:

```sh
go run ./code/percentiles
go run ./code/p99avg
go run ./code/anomaly
go run ./code/anomaly -csv   # optional: t,x,ewma,sd,alert rows for plotting
```

Each one takes no required arguments, finishes in well under a second, and prints the same output every time. Randomness uses a fixed seed: `rand.New(rand.NewPCG(42, 42))`. Each program is self-contained, therefore `p99avg` repeats a few helpers from `percentiles`.

## percentiles

Prints the mean, p50, p90, p95, p99, p99.9, and max for 1,000 lognormal latencies plus five outliers, a text-mode histogram, the effect of one 30,000 ms request on the mean and the median, Prometheus-style cumulative buckets with the `histogram_quantile` interpolation step by step, and the p99 estimate under four bucket layouts.

## p99avg

Prints the p99 of a busy fast host and a quiet slow host, the plain and traffic-weighted averages of those p99s, the true merged p99 with text bars, then per-host bucket counts, their sum, and `histogram_quantile` on the sum.

## anomaly

Prints variance and standard deviation by hand, the share of points outside a 3-sigma band for normal and lognormal data, a masking example with z-scores and modified z-scores, an EWMA plus EWM-variance band on a seeded series with a spike and a level shift (alerting points, a table around each event, and a text plot), and a rolling median and MAD detector on the same series.
