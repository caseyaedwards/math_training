# Images

* [counter-secant.svg](counter-secant.svg): a counter scraped every 15 s drawn as a staircase, with the secant from t = 60 to t = 120 whose slope is the 68 req/s that rate() reports.
* [secant-to-tangent.svg](secant-to-tangent.svg): secant lines through t = 60 with h = 60, 15 and 5 closing in on the tangent of slope 62.
* [counter-reset.svg](counter-reset.svg): raw scraped values falling at the restart, the reset-aware running total, and the true count, from 150 s to 300 s.
* [rate-area.svg](rate-area.svg): the rate r(t) = 50 + 0.2t with 20 left Riemann rectangles; the area under the line is the 24,000 total requests.
* [telescoping-sum.svg](telescoping-sum.svg): the counter as a staircase with 60-second rises, and the same rises stacked into one column of 24,000.
* [riemann-three-ways.svg](riemann-three-ways.svg): left, right and trapezoid sums of the rate with five 60-second slices: 22,200, 25,800 and 24,000.
* [falling-object.svg](falling-object.svg): height h(t) = 100 - 4.9t² with Euler points at dt = 0.5 s, and velocity v(t) = -9.8t with the area that equals the drop by t = 2 s.
* [euler-steps.svg](euler-steps.svg): Euler steps with dt = 1 s against the exact height curve, with the 19.6 m error at t = 4 s marked.
* [euler-error.svg](euler-error.svg): Euler height error at t = 4 s against step size, a straight line error = 19.6 × dt.
* [littles-law-area.svg](littles-law-area.svg): six requests as bars and as a count-in-system step plot, both covering 11 request-seconds.
* [mm1-queue.svg](mm1-queue.svg): a schematic M/M/1 queue: arrivals at rate lambda, a waiting line, one server at rate mu, departures.
* [latency-hockey-stick.svg](latency-hockey-stick.svg): M/M/1 average latency W = 1 / (mu - lambda) against utilization for mu = 100 req/s, computed from the formula, with 50%, 80%, 90% and 95% marked.
