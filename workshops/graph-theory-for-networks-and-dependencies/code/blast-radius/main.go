// blast-radius answers "if this service fails, who breaks?" with reverse
// reachability, prints in-degree and out-degree as a fan-in risk signal, and
// finds single points of failure (articulation points) with the Tarjan lowlink method.
//
// Run from the workshop folder: go run ./code/blast-radius
package main

import (
	"fmt"
	"sort"
	"strings"
)

var nodes = []string{"api", "auth", "cache", "config", "db", "lb", "queue", "web", "worker"}

// Edge A -> B means "A needs B".
var edges = [][2]string{
	{"lb", "web"}, {"web", "api"},
	{"api", "auth"}, {"api", "cache"}, {"api", "queue"}, {"api", "db"},
	{"auth", "db"}, {"auth", "config"},
	{"worker", "queue"}, {"worker", "db"},
}

func main() {
	needs := map[string][]string{}
	neededBy := map[string][]string{}
	for _, e := range edges {
		needs[e[0]] = append(needs[e[0]], e[1])
		neededBy[e[1]] = append(neededBy[e[1]], e[0])
	}

	fmt.Println("=== Degree table (in = dependents, out = dependencies) ===")
	fmt.Printf("  %-7s %3s %4s  %s\n", "service", "in", "out", "fan-in bar")
	type row struct {
		n       string
		in, out int
	}
	var rows []row
	for _, n := range nodes {
		rows = append(rows, row{n, len(neededBy[n]), len(needs[n])})
	}
	sort.SliceStable(rows, func(i, j int) bool { return rows[i].in > rows[j].in })
	for _, r := range rows {
		fmt.Printf("  %-7s %3d %4d  %s\n", r.n, r.in, r.out, strings.Repeat("#", r.in*4))
	}
	fmt.Println()

	fmt.Println("=== Blast radius (reverse reachability by BFS on needed-by edges) ===")
	for _, n := range nodes {
		hit := blast(neededBy, n, false)
		fmt.Printf("  %-7s %d  %-28s [%s]\n", n, len(hit), strings.Repeat("#", len(hit)*4), strings.Join(hit, " "))
	}
	fmt.Println()
	fmt.Println("Trace for db:")
	blast(neededBy, "db", true)
	fmt.Println()

	fmt.Println("=== Single points of failure (articulation points, edges treated as undirected) ===")
	und := map[string][]string{}
	for _, e := range edges {
		und[e[0]] = append(und[e[0]], e[1])
		und[e[1]] = append(und[e[1]], e[0])
	}
	for k := range und {
		sort.Strings(und[k])
	}
	aps := articulation(und)
	fmt.Println("  articulation points:", strings.Join(aps, " "))
	for _, a := range aps {
		fmt.Printf("  remove %-5s -> pieces: %s\n", a, strings.Join(components(und, a), " | "))
	}
}

// blast returns every service that transitively needs start.
func blast(neededBy map[string][]string, start string, trace bool) []string {
	seen := map[string]bool{start: true}
	queue := []string{start}
	var out []string
	for len(queue) > 0 {
		u := queue[0]
		queue = queue[1:]
		var added []string
		for _, v := range sortedCopy(neededBy[u]) {
			if !seen[v] {
				seen[v] = true
				queue = append(queue, v)
				out = append(out, v)
				added = append(added, v)
			}
		}
		if trace {
			fmt.Printf("  pop %-7s adds [%s]  queue [%s]\n", u, strings.Join(added, " "), strings.Join(queue, " "))
		}
	}
	sort.Strings(out)
	return out
}

func sortedCopy(s []string) []string {
	c := append([]string(nil), s...)
	sort.Strings(c)
	return c
}

// articulation uses Tarjan: a non-root u is a cut vertex when some child v has
// low[v] >= disc[u]; the root is one when it has two or more DFS children.
func articulation(g map[string][]string) []string {
	disc := map[string]int{}
	low := map[string]int{}
	isAP := map[string]bool{}
	timer := 0
	var dfs func(u, parent string)
	dfs = func(u, parent string) {
		timer++
		disc[u], low[u] = timer, timer
		children := 0
		for _, v := range g[u] {
			if v == parent {
				continue
			}
			if disc[v] == 0 {
				children++
				dfs(v, u)
				low[u] = min(low[u], low[v])
				if parent != "" && low[v] >= disc[u] {
					isAP[u] = true
				}
			} else {
				low[u] = min(low[u], disc[v])
			}
		}
		if parent == "" && children > 1 {
			isAP[u] = true
		}
	}
	for _, n := range nodes {
		if disc[n] == 0 {
			dfs(n, "")
		}
	}
	var out []string
	for _, n := range nodes {
		if isAP[n] {
			out = append(out, n)
		}
	}
	return out
}

// components lists connected pieces of g after removing node cut.
func components(g map[string][]string, cut string) []string {
	seen := map[string]bool{cut: true}
	var parts []string
	for _, n := range nodes {
		if seen[n] {
			continue
		}
		var part []string
		stack := []string{n}
		seen[n] = true
		for len(stack) > 0 {
			u := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			part = append(part, u)
			for _, v := range g[u] {
				if !seen[v] {
					seen[v] = true
					stack = append(stack, v)
				}
			}
		}
		sort.Strings(part)
		parts = append(parts, strings.Join(part, ","))
	}
	return parts
}
