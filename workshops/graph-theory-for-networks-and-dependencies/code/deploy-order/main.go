// deploy-order computes a safe startup order for a small service
// dependency graph with the Kahn algorithm, then adds one bad edge and shows
// how Kahn stalls and how a three-color depth-first search names the cycle.
//
// Run from the workshop folder: go run ./code/deploy-order
package main

import (
	"fmt"
	"sort"
	"strings"
)

// Edge A -> B means "A needs B": B must be up before A starts.
type Graph struct {
	nodes []string
	needs map[string][]string // out-edges: what a service depends on
}

func NewGraph(nodes []string) *Graph {
	g := &Graph{nodes: append([]string(nil), nodes...), needs: map[string][]string{}}
	sort.Strings(g.nodes)
	for _, n := range g.nodes {
		g.needs[n] = nil
	}
	return g
}

func (g *Graph) AddEdge(from, to string) {
	g.needs[from] = append(g.needs[from], to)
	sort.Strings(g.needs[from])
}

// dependents builds the reverse adjacency list: who needs B?
func (g *Graph) dependents() map[string][]string {
	rev := map[string][]string{}
	for _, n := range g.nodes {
		for _, d := range g.needs[n] {
			rev[d] = append(rev[d], n)
		}
	}
	for k := range rev {
		sort.Strings(rev[k])
	}
	return rev
}

func (g *Graph) printAdjacency() {
	fmt.Println("Adjacency list (service -> what it needs):")
	for _, n := range g.nodes {
		fmt.Printf("  %-7s -> [%s]\n", n, strings.Join(g.needs[n], ", "))
	}
	fmt.Println()
	fmt.Println("Adjacency matrix (row needs column, 1 = edge):")
	fmt.Print("         ")
	for _, c := range g.nodes {
		fmt.Printf("%-3.3s ", c)
	}
	fmt.Println()
	for _, r := range g.nodes {
		fmt.Printf("  %-7s", r)
		set := map[string]bool{}
		for _, d := range g.needs[r] {
			set[d] = true
		}
		for _, c := range g.nodes {
			if set[c] {
				fmt.Print("  1 ")
			} else {
				fmt.Print("  . ")
			}
		}
		fmt.Println()
	}
	fmt.Println()
}

// Kahn returns the start order and the nodes it cannot place.
func (g *Graph) Kahn(verbose bool) ([]string, []string) {
	remaining := map[string]int{} // unmet dependencies per service
	for _, n := range g.nodes {
		remaining[n] = len(g.needs[n])
	}
	rev := g.dependents()
	var queue []string
	for _, n := range g.nodes {
		if remaining[n] == 0 {
			queue = append(queue, n)
		}
	}
	if verbose {
		fmt.Println("Kahn algorithm (queue = services with zero unmet dependencies):")
		fmt.Printf("  %-4s %-8s %-34s %s\n", "step", "start", "newly ready", "queue after")
		fmt.Printf("  %-4s %-8s %-34s [%s]\n", "0", "-", "-", strings.Join(queue, " "))
	}
	var order []string
	step := 0
	for len(queue) > 0 {
		n := queue[0]
		queue = queue[1:]
		order = append(order, n)
		step++
		var ready []string
		for _, m := range rev[n] {
			remaining[m]--
			if remaining[m] == 0 {
				ready = append(ready, m)
			}
		}
		queue = append(queue, ready...)
		if verbose {
			r := "-"
			if len(ready) > 0 {
				r = strings.Join(ready, " ")
			}
			fmt.Printf("  %-4d %-8s %-34s [%s]\n", step, n, r, strings.Join(queue, " "))
		}
	}
	var stuck []string
	for _, n := range g.nodes {
		if remaining[n] > 0 {
			stuck = append(stuck, fmt.Sprintf("%s(%d unmet)", n, remaining[n]))
		}
	}
	return order, stuck
}

// FindCycle runs a three-color DFS. WHITE = unseen, GRAY = on the current
// path, BLACK = finished. Reaching a GRAY node means a back edge: a cycle.
func (g *Graph) FindCycle() []string {
	const (
		white = 0
		gray  = 1
		black = 2
	)
	color := map[string]int{}
	parent := map[string]string{}
	var cycle []string
	var visit func(u string) bool
	visit = func(u string) bool {
		color[u] = gray
		for _, v := range g.needs[u] {
			if color[v] == gray {
				// Walk back from u to v along parent links.
				cycle = []string{v}
				for x := u; x != v; x = parent[x] {
					cycle = append(cycle, x)
				}
				cycle = append(cycle, v)
				// Reverse to read in edge direction.
				for i, j := 0, len(cycle)-1; i < j; i, j = i+1, j-1 {
					cycle[i], cycle[j] = cycle[j], cycle[i]
				}
				fmt.Printf("  back edge %s -> %s (%s is GRAY)\n", u, v, v)
				return true
			}
			if color[v] == white {
				parent[v] = u
				if visit(v) {
					return true
				}
			}
		}
		color[u] = black
		return false
	}
	for _, n := range g.nodes {
		if color[n] == white && visit(n) {
			return cycle
		}
	}
	return nil
}

func build() *Graph {
	g := NewGraph([]string{"lb", "web", "api", "auth", "worker", "db", "cache", "queue", "config"})
	edges := [][2]string{
		{"lb", "web"}, {"web", "api"},
		{"api", "auth"}, {"api", "cache"}, {"api", "queue"}, {"api", "db"},
		{"auth", "db"}, {"auth", "config"},
		{"worker", "queue"}, {"worker", "db"},
	}
	for _, e := range edges {
		g.AddEdge(e[0], e[1])
	}
	return g
}

func main() {
	fmt.Println("=== Part 1: healthy dependency graph (9 services, 10 edges) ===")
	g := build()
	g.printAdjacency()
	order, stuck := g.Kahn(true)
	fmt.Println()
	fmt.Println("Start order:", strings.Join(order, " -> "))
	fmt.Println("Stop order: ", strings.Join(reverse(order), " -> "))
	fmt.Println("Unprocessed:", len(stuck))
	fmt.Println()

	fmt.Println("=== Part 2: add bad edge db -> web (db init calls a web health check) ===")
	g.AddEdge("db", "web")
	order, stuck = g.Kahn(true)
	fmt.Println()
	fmt.Printf("Kahn placed %d of %d services: %s\n", len(order), len(g.nodes), strings.Join(order, " "))
	fmt.Println("Stuck:", strings.Join(stuck, " "))
	fmt.Println()
	fmt.Println("Three-color DFS:")
	c := g.FindCycle()
	fmt.Println("  cycle:", strings.Join(c, " -> "))
}

func reverse(s []string) []string {
	out := make([]string, len(s))
	for i, v := range s {
		out[len(s)-1-i] = v
	}
	return out
}
