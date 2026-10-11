# Diagrams: Graph Theory Basics: Paths, Trees, BFS, DFS and Shortest Paths

Hand-authored SVG figures used by [the lesson](../README.md). Each file has a matching generator spec comment above its embed in the lesson.

* [dag-topo.svg](dag-topo.svg): Directed graph: config points to db and cache, both point to api, api points to web; below, a valid start order config, db, cache, api, web.
* [graph-bfs.svg](graph-bfs.svg): Six-node graph A to F laid out in BFS levels 0 to 3 from A; BFS tree edges solid, other edges dashed.
* [graph-dfs.svg](graph-dfs.svg): The six-vertex graph with DFS visit numbers: A 1, B 2, C 3, D 4, F 5, E 6; DFS tree edges form the single path A, B, C, D, F, E.
* [graph-dijkstra.svg](graph-dijkstra.svg): Weighted six-node graph; the shortest path from A to F through C, B and D with total weight 7 is highlighted.
* [graph-vocab.svg](graph-vocab.svg): Two copies of the six-vertex graph: the left highlights the path A, B, D, F; the right highlights the cycle B, C, D back to B.
* [trees.svg](trees.svg): Left: a tree with vertices r, a, b, c, d and 4 edges. Right: the same tree plus a dashed edge d to b, which closes the cycle r, a, d, b.
