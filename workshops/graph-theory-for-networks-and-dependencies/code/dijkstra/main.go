// dijkstra finds the lowest-latency route between cloud regions with
// the Dijkstra algorithm and prints the frontier at every step. It then runs
// breadth-first search for the fewest-hops route and compares the two.
//
// Run from the workshop folder: go run ./code/dijkstra
package main

import (
	"fmt"
	"sort"
	"strings"
)

type link struct {
	to string
	ms int
}

var regions = []string{"us-east", "us-west", "sa-east", "eu-west", "eu-central", "ap-south", "ap-northeast"}

// Undirected links with round-trip latency in milliseconds (illustrative).
var links = []struct {
	a, b string
	ms   int
}{
	{"us-east", "us-west", 62},
	{"us-east", "eu-west", 75},
	{"us-east", "eu-central", 90},
	{"us-east", "sa-east", 115},
	{"us-east", "ap-south", 230},
	{"us-west", "ap-northeast", 105},
	{"us-west", "sa-east", 170},
	{"eu-west", "eu-central", 20},
	{"eu-west", "ap-south", 120},
	{"eu-central", "ap-south", 110},
	{"ap-south", "ap-northeast", 125},
}

func buildGraph() map[string][]link {
	g := map[string][]link{}
	for _, l := range links {
		g[l.a] = append(g[l.a], link{l.b, l.ms})
		g[l.b] = append(g[l.b], link{l.a, l.ms})
	}
	for k := range g {
		sort.Slice(g[k], func(i, j int) bool { return g[k][i].to < g[k][j].to })
	}
	return g
}

const inf = 1 << 30

// dijkstra uses a plain linear scan for the minimum: easy to read, and fine
// for a handful of nodes. Production code uses container/heap.
func dijkstra(g map[string][]link, src string) (map[string]int, map[string]string) {
	dist := map[string]int{}
	prev := map[string]string{}
	done := map[string]bool{}
	for _, r := range regions {
		dist[r] = inf
	}
	dist[src] = 0
	fmt.Println("Frontier = tentative distances of regions not yet finalized (inf = unknown)")
	fmt.Printf("%-4s %-17s", "step", "finalize")
	for _, r := range regions {
		fmt.Printf(" %13s", r)
	}
	fmt.Println()
	for step := 1; step <= len(regions); step++ {
		// Pick the unfinished region with the smallest distance.
		u, best := "", inf
		for _, r := range regions {
			if !done[r] && dist[r] < best {
				u, best = r, dist[r]
			}
		}
		if u == "" {
			break
		}
		done[u] = true
		for _, e := range g[u] {
			if !done[e.to] && dist[u]+e.ms < dist[e.to] {
				dist[e.to] = dist[u] + e.ms
				prev[e.to] = u
			}
		}
		fmt.Printf("%-4d %-17s", step, fmt.Sprintf("%s=%d", u, dist[u]))
		for _, r := range regions {
			switch {
			case done[r]:
				fmt.Printf(" %13s", "done")
			case dist[r] == inf:
				fmt.Printf(" %13s", "inf")
			default:
				fmt.Printf(" %13d", dist[r])
			}
		}
		fmt.Println()
	}
	return dist, prev
}

func bfs(g map[string][]link, src string) (map[string]int, map[string]string) {
	hops := map[string]int{src: 0}
	prev := map[string]string{}
	queue := []string{src}
	for len(queue) > 0 {
		u := queue[0]
		queue = queue[1:]
		for _, e := range g[u] {
			if _, seen := hops[e.to]; !seen {
				hops[e.to] = hops[u] + 1
				prev[e.to] = u
				queue = append(queue, e.to)
			}
		}
	}
	return hops, prev
}

func path(prev map[string]string, src, dst string) []string {
	p := []string{dst}
	for p[0] != src {
		p = append([]string{prev[p[0]]}, p...)
	}
	return p
}

func cost(g map[string][]link, p []string) int {
	total := 0
	for i := 0; i+1 < len(p); i++ {
		for _, e := range g[p[i]] {
			if e.to == p[i+1] {
				total += e.ms
			}
		}
	}
	return total
}

func main() {
	g := buildGraph()
	src, dst := "us-east", "ap-south"
	fmt.Printf("=== Dijkstra from %s ===\n", src)
	dist, prev := dijkstra(g, src)
	fmt.Println()
	fmt.Println("Final latency from us-east:")
	for _, r := range regions {
		bar := strings.Repeat("#", dist[r]/10)
		fmt.Printf("  %-13s %4d ms  %-24s via %s\n", r, dist[r], bar, strings.Join(path(prev, src, r), " > "))
	}
	fmt.Println()
	fmt.Printf("=== BFS (hop count) from %s ===\n", src)
	hops, bprev := bfs(g, src)
	for _, r := range regions {
		fmt.Printf("  %-13s hops = %d\n", r, hops[r])
	}
	fmt.Println()
	fp := path(prev, src, dst)
	hp := path(bprev, src, dst)
	fmt.Printf("Route %s -> %s\n", src, dst)
	fmt.Printf("  fewest hops : %-36s hops = %d, %d ms\n", strings.Join(hp, " > "), len(hp)-1, cost(g, hp))
	fmt.Printf("  lowest ms   : %-36s hops = %d, %d ms\n", strings.Join(fp, " > "), len(fp)-1, cost(g, fp))
}
