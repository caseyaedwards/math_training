# Code

Three Go programs, standard library only. Each lives in its own folder as a single `main.go` with `package main`. The `go.mod` file in the workshop folder (no dependencies) lets Go find them by path. Run them from the workshop folder:

```txt
go run ./code/deploy-order
go run ./code/dijkstra
go run ./code/blast-radius
```

Or step into a program folder and run `go run .` or `go run main.go`.

Tested with:

```txt
go version go1.27.2 darwin/arm64
```

The programs use the built-in `min` function and need Go 1.21 or newer. All output is deterministic and each program finishes in well under a second.

## What Each Program Prints

* [deploy-order/main.go](deploy-order/main.go): the adjacency list and adjacency matrix of a nine-service dependency graph, the Kahn algorithm queue state at every step, the start order and stop order, then the same run after adding the bad edge db needs web (Kahn stalls after three services) and the cycle found by a three-color DFS.
* [dijkstra/main.go](dijkstra/main.go): the Dijkstra frontier table (tentative latency to every region after each finish step) from us-east, the final latency and route to each region with a text bar chart, BFS hop counts, and the fewest-hops versus lowest-latency route to ap-south.
* [blast-radius/main.go](blast-radius/main.go): the in-degree and out-degree table with a fan-in bar, the blast radius of every service by reverse BFS, a step-by-step BFS trace for db, and the articulation points (single points of failure) with the pieces left after removing each one.
