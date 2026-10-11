# Graph Theory Code

Companion program for the [Graph Theory Track](../README.md). It uses the Go standard library only.

[main.go](main.go) checks the handshake lemma, runs Kahn's topological sort (and catches a circular dependency), then runs BFS and Dijkstra on the graph from the shortest-path diagram. Run it with `go run main.go` in this folder.

```txt
go run main.go
```

The expected output is printed in the Code Corner section of the [track README](../README.md#code-corner).
