# Workshops

Each workshop takes one real problem, names the math it needs, and builds a working program that shows the math in action.
The course teaches the idea. The workshop puts it to work.

## How a Workshop Works

Every workshop folder has the same shape:

```txt
workshops/<slug>/
  README.md     the real problem, the math, a guided build, worked numbers, exercises
  img/          SVG diagrams for the workshop
  code/         runnable Go programs, standard library only, one folder per program
```

Work through a workshop in this order:

1. Read **The Real Problem** and **The Math You Need**. Follow a link back into the course if a term looks unfamiliar.
2. Study the pictures in **Picture It**.
3. Do the **Guided Build** step by step. Run each program from the workshop folder, for example `go run ./code/toyrsa`, and compare your terminal with the output in the README.
4. Check the **Worked Numbers** by hand, then try the exercises in **Try It** before you open the answers.
5. Read **Where This Shows Up at Work** and change one number in the code to see what moves.

## The Workshops

| Workshop | The Math It Uses | Course Level Needed | Time |
|---|---|---|---|
| [Number Theory for Cryptography](number-theory-for-cryptography/README.md) | Modular arithmetic, gcd and the extended Euclidean algorithm, modular inverse, fast exponentiation, toy RSA, Diffie-Hellman, hashing into buckets | [301](../course/301/README.md), with [601](../course/601/README.md) number theory as a bonus | 2 to 3 hours |
| [Probability for On-Call: Error Budgets and SLOs](probability-for-on-call-error-budgets-and-slos/README.md) | Percentages, nines to minutes of downtime, error budgets, burn rates, independent events, series and parallel availability, the complement rule | [201](../course/201/README.md), with the probability unit of [501](../course/501/README.md) | 90 minutes |
| [Statistics for Monitoring and Anomaly Detection](statistics-for-monitoring-and-anomaly-detection/README.md) | Mean, median, percentiles, histograms, standard deviation, z-scores, EWMA, median absolute deviation | [501](../course/501/README.md), starting from [101](../course/101/README.md) arithmetic | 2 hours |
| [Linear Algebra for Graphics and ML](linear-algebra-for-graphics-and-ml/README.md) | Vectors, 2D transform matrices, matrix multiplication, dot product, cosine similarity, embeddings, least-squares regression | [501](../course/501/README.md), starting from [201](../course/201/README.md) and [301](../course/301/README.md) trig | 2 to 3 hours |
| [Graph Theory for Networks and Dependencies](graph-theory-for-networks-and-dependencies/README.md) | Directed graphs, topological sort, cycle detection, BFS, Dijkstra shortest paths, reachability and blast radius | [501](../course/501/README.md) graph theory unit | 2 hours |
| [Calculus of Rates in Physics and Queues](calculus-of-rates-in-physics-and-queues/README.md) | Slopes and derivatives, rate() of counters, integrals as sums, the Fundamental Theorem of Calculus, Euler steps, Little's law, M/M/1 queues | [401](../course/401/README.md), with the queue parts open from [201](../course/201/README.md) | 2 to 3 hours |
| [Exponential Growth in Interest, Epidemics, and Load](exponential-growth-in-interest-epidemics-and-load/README.md) | Compound interest, the number e, logarithms, doubling time and the rule of 72, the SIR model, exponential backoff with jitter, log scales | [301](../course/301/README.md), with [401](../course/401/README.md) for the SIR rates | 2 hours |
| [Music and Frequencies](music-and-frequencies/README.md) | Ratios, sine waves, logarithms, equal temperament and cents, harmonics, Fourier series and a hand-made DFT | [301](../course/301/README.md) | 90 minutes to 2 hours |
| [Maps and Projections](maps-and-projections/README.md) | Spherical coordinates, 3D vectors, haversine great-circle distance, bearings, the Mercator projection and its scale factor | [301](../course/301/README.md) trigonometry | 90 minutes to 2 hours |
| [Games and Probability](games-and-probability/README.md) | Sample spaces, expected value, the law of large numbers, conditional probability (Monty Hall), the birthday problem, simulation | [501](../course/501/README.md) probability unit, starting from [101](../course/101/README.md) | 90 minutes to 2 hours |

## Suggested Order

Pick by need, not by number. These paths work well:

* **On-call first:** [Error Budgets and SLOs](probability-for-on-call-error-budgets-and-slos/README.md), then [Monitoring and Anomaly Detection](statistics-for-monitoring-and-anomaly-detection/README.md), then [Rates and Queues](calculus-of-rates-in-physics-and-queues/README.md).
* **Infrastructure plumbing:** [Graphs and Dependencies](graph-theory-for-networks-and-dependencies/README.md), then [Cryptography](number-theory-for-cryptography/README.md), then [Exponential Growth](exponential-growth-in-interest-epidemics-and-load/README.md) for backoff and capacity planning.
* **Just for fun:** [Games and Probability](games-and-probability/README.md), [Music and Frequencies](music-and-frequencies/README.md), and [Maps and Projections](maps-and-projections/README.md).

## Running the Code

* Every program is Go with only the standard library. Each workshop folder has its own `go.mod`. From the workshop folder, run `go run ./code/<name>`. Inside a program folder, `go run .` also works.
* Each `code/README.md` records the Go version used for the output shown. Go 1.22 or newer works.
* Every program is deterministic. Random simulations use a fixed seed, so your output matches the README line for line.

## Where to Go Next

* Back to the [course](../course/README.md) for the full theory behind each idea.
* Into a [track](../tracks/README.md) to follow one field further.
* To the [resources](../resources/README.md) for free textbooks and classic university pages.
