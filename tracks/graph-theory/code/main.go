// Graph theory starter kit: handshake check, topological sort, BFS hops
// and Dijkstra shortest paths. Standard library only.
package main

import (
	"container/heap"
	"fmt"
	"sort"
)

// Edge is a weighted undirected edge.
type Edge struct {
	A, B string
	W    int
}

// handshake returns the degree sum and the edge count.
func handshake(edges []Edge) (int, int) {
	deg := map[string]int{}
	for _, e := range edges {
		deg[e.A]++
		deg[e.B]++
	}
	sum := 0
	for _, d := range deg {
		sum += d
	}
	return sum, len(edges)
}

// topoSort runs Kahn's algorithm. deps[x] lists what x needs first.
func topoSort(deps map[string][]string) ([]string, bool) {
	indeg := map[string]int{}
	users := map[string][]string{}
	for n, ds := range deps {
		indeg[n] += 0
		for _, d := range ds {
			indeg[d] += 0
			indeg[n]++
			users[d] = append(users[d], n)
		}
	}
	var ready []string
	for n, k := range indeg {
		if k == 0 {
			ready = append(ready, n)
		}
	}
	var order []string
	for len(ready) > 0 {
		sort.Strings(ready) // deterministic output
		n := ready[0]
		ready = ready[1:]
		order = append(order, n)
		for _, m := range users[n] {
			indeg[m]--
			if indeg[m] == 0 {
				ready = append(ready, m)
			}
		}
	}
	return order, len(order) == len(indeg)
}

type item struct {
	node string
	dist int
}
type pq []item

func (q pq) Len() int            { return len(q) }
func (q pq) Less(i, j int) bool  { return q[i].dist < q[j].dist }
func (q pq) Swap(i, j int)       { q[i], q[j] = q[j], q[i] }
func (q *pq) Push(x interface{}) { *q = append(*q, x.(item)) }
func (q *pq) Pop() interface{} {
	old := *q
	it := old[len(old)-1]
	*q = old[:len(old)-1]
	return it
}

// dijkstra returns shortest distances and predecessors from src.
func dijkstra(edges []Edge, src string) (map[string]int, map[string]string) {
	adj := map[string][]Edge{}
	for _, e := range edges {
		adj[e.A] = append(adj[e.A], e)
		adj[e.B] = append(adj[e.B], Edge{e.B, e.A, e.W})
	}
	dist := map[string]int{src: 0}
	prev := map[string]string{}
	q := &pq{{src, 0}}
	for q.Len() > 0 {
		it := heap.Pop(q).(item)
		if it.dist > dist[it.node] {
			continue
		}
		for _, e := range adj[it.node] {
			nd := it.dist + e.W
			if old, ok := dist[e.B]; !ok || nd < old {
				dist[e.B] = nd
				prev[e.B] = it.node
				heap.Push(q, item{e.B, nd})
			}
		}
	}
	return dist, prev
}

// bfsHops counts hops from src, ignoring weights.
func bfsHops(edges []Edge, src string) map[string]int {
	adj := map[string][]string{}
	for _, e := range edges {
		adj[e.A] = append(adj[e.A], e.B)
		adj[e.B] = append(adj[e.B], e.A)
	}
	hops := map[string]int{src: 0}
	queue := []string{src}
	for len(queue) > 0 {
		n := queue[0]
		queue = queue[1:]
		for _, m := range adj[n] {
			if _, seen := hops[m]; !seen {
				hops[m] = hops[n] + 1
				queue = append(queue, m)
			}
		}
	}
	return hops
}

func main() {
	// The latency graph from the shortest-path diagram.
	g := []Edge{{"S", "A", 4}, {"S", "B", 1}, {"B", "A", 2}, {"A", "C", 5},
		{"B", "D", 8}, {"C", "T", 3}, {"D", "T", 1}, {"C", "D", 2}}

	sum, e := handshake(g)
	fmt.Printf("handshake: degree sum %d = 2 x %d edges\n", sum, e)

	deps := map[string][]string{"build": {"fetch"}, "test": {"build"}, "deploy": {"test", "approve"}}
	order, ok := topoSort(deps)
	fmt.Println("deploy order:", order, "acyclic:", ok)

	deps["fetch"] = []string{"deploy"} // add a circular dependency
	_, ok = topoSort(deps)
	fmt.Println("after adding fetch -> deploy, acyclic:", ok)

	hops := bfsHops(g, "S")
	dist, prev := dijkstra(g, "S")
	names := []string{"S", "A", "B", "C", "D", "T"}
	for _, n := range names {
		fmt.Printf("%s: %d hops, %2d ms\n", n, hops[n], dist[n])
	}
	path := []string{"T"}
	for n := "T"; n != "S"; n = prev[n] {
		path = append([]string{prev[n]}, path...)
	}
	fmt.Println("fastest route:", path)
}
