# Images

* `linear-vs-log.svg`: load 10,000 * 1.08^t on a linear y-axis (a bending curve) beside the same data on a log y-axis (a straight line), with the 50,000 rps capacity line.
* `doubling-ladder.svg`: 1.08^t over 40 years with the doublings to 2, 4, 8, and 16 marked every nine years.
* `compound-staircase.svg`: one dollar at 100% for one year, compounded yearly (one jump), monthly (12 steps), and continuously (a smooth curve to e).
* `e-convergence.svg`: the values of (1 + 1/n)^n for n = 1 to 365 on a log x-axis, rising toward the dashed line at e = 2.71828.
* `rule-of-72-error.svg`: percent error of the rules of 72 and 70 against the exact doubling time, for rates from 1% to 30%.
* `half-life.svg`: decay with a 60 s half-life (1/2, 1/4, 1/8, 1/16 marked) beside a hard 120 s TTL step.
* `sir-flow.svg`: the three SIR boxes with arrows for new infections and recoveries.
* `euler-steps.svg`: Euler steps with dt = 0.5 for dy/dt = y against the exact curve e^t.
* `sir-curves.svg`: S, I, and R fractions for the SIR model with beta = 0.3 and gamma = 0.1, marking the infection peak on day 62 where S = 1/R0.
* `backoff-ceiling.svg`: the backoff ceiling per attempt (base 100 ms, cap 5,000 ms) with the full jitter and equal jitter ranges.
* `backoff-jitter.svg`: retries per 10 ms slot for 100 clients from the Go simulation, without jitter (tall synchronized spikes) and with full jitter (low, spread-out bars).
