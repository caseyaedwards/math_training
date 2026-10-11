# Images

All data-driven images come from the seeded Go programs in `../code`.

* `skewed-latency-histogram.svg`: histogram of 1,005 latencies in 25 ms bins, with the median (81.5 ms), the mean (109.5 ms), and the p99 (353.1 ms) marked.
* `one-slow-request.svg`: two number lines showing the mean jump from 100.8 to 396.9 ms and the median move from 86.9 to 88.6 ms after one 30,000 ms request.
* `nearest-rank.svg`: ten sorted latencies as bars with ranks, the p50 (rank 5) and the p90 (rank 9) in orange.
* `bucket-interpolation.svg`: cumulative counts joined by straight lines, with rank 95 read off at 325 ms inside the 200 to 400 ms bucket.
* `bucket-choice.svg`: the p99 estimate under four bucket layouts against the exact p99.
* `p99-averaging-trap.svg`: the p99 of two hosts, the plain and traffic-weighted averages of those p99s, and the true merged p99.
* `summing-buckets.svg`: per-host cumulative bucket counts and their column sums.
* `variance-squares.svg`: five points around a mean of 14, the distance to each, and the squares whose average is the variance.
* `three-sigma-shapes.svg`: mean plus or minus 3 standard deviations on a normal curve and on a lognormal latency curve.
* `ewma-band.svg`: a 200-point time series with a spike and a level shift, its EWMA, the 3-sigma band, and the three alerting points.
* `ewma-weights.svg`: the weight of a point by age for alpha 0.1 and alpha 0.3.
* `mad-vs-sd.svg`: the masking example on two number lines, with the wide mean and sd band and the narrow median and MAD band.
