// BFS, DFS and Dijkstra on the six-vertex graph from the lesson.
package main

import (
	"container/heap"
	"fmt"
	"sort"
)

var W = map[string]map[string]int{
	"A": {"B": 4, "C": 1},
	"B": {"A": 4, "C": 2, "D": 1},
	"C": {"A": 1, "B": 2, "D": 5, "E": 2},
	"D": {"B": 1, "C": 5, "F": 3},
	"E": {"C": 2, "F": 6},
	"F": {"D": 3, "E": 6},
}

func neighbors(v string) []string {
	var out []string
	for w := range W[v] {
		out = append(out, w)
	}
	sort.Strings(out) // alphabetical, to match the lesson
	return out
}

func bfs(start string) []string {
	seen := map[string]bool{start: true}
	queue, order := []string{start}, []string{}
	for len(queue) > 0 {
		v := queue[0]
		queue = queue[1:]
		order = append(order, v)
		for _, w := range neighbors(v) {
			if !seen[w] {
				seen[w] = true
				queue = append(queue, w)
			}
		}
	}
	return order
}

func dfs(v string, seen map[string]bool, order *[]string) {
	seen[v] = true
	*order = append(*order, v)
	for _, w := range neighbors(v) {
		if !seen[w] {
			dfs(w, seen, order)
		}
	}
}

type item struct {
	dist int
	v    string
}
type pq []item

func (q pq) Len() int { return len(q) }
func (q pq) Less(i, j int) bool {
	return q[i].dist < q[j].dist || (q[i].dist == q[j].dist && q[i].v < q[j].v)
}
func (q pq) Swap(i, j int)       { q[i], q[j] = q[j], q[i] }
func (q *pq) Push(x interface{}) { *q = append(*q, x.(item)) }
func (q *pq) Pop() interface{} {
	old := *q
	it := old[len(old)-1]
	*q = old[:len(old)-1]
	return it
}

func dijkstra(start string) (map[string]int, map[string]string) {
	dist, prev := map[string]int{start: 0}, map[string]string{}
	q := &pq{{0, start}}
	for q.Len() > 0 {
		it := heap.Pop(q).(item)
		if it.dist > dist[it.v] {
			continue // stale entry
		}
		for _, w := range neighbors(it.v) {
			nd := it.dist + W[it.v][w]
			if old, ok := dist[w]; !ok || nd < old {
				dist[w], prev[w] = nd, it.v
				heap.Push(q, item{nd, w})
			}
		}
	}
	return dist, prev
}

func main() {
	fmt.Println("BFS from A:", bfs("A"))
	var order []string
	dfs("A", map[string]bool{}, &order)
	fmt.Println("DFS from A:", order)

	dist, prev := dijkstra("A")
	fmt.Println("distances:", dist)
	path := []string{"F"}
	for v := "F"; v != "A"; v = prev[v] {
		path = append([]string{prev[v]}, path...)
	}
	fmt.Println("cheapest A->F:", path, "cost", dist["F"])
}
