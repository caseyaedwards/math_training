// Command hashbuckets shows hash(key) % N bucketing, the reshuffle
// problem, and consistent hashing.
//
// It hashes with SHA-256 (crypto/sha256) and keeps the first 8 bytes
// as a big-endian uint64, so the result is the same on every machine
// and every run. (Go map iteration order and hash/maphash seeds are
// randomized; never use them to pick a shard.)
//
// Prints:
//
//  1. How 10,000 keys spread over 4 buckets (ASCII bar chart)
//  2. How many keys move when N grows from 4 to 5 with hash % N
//  3. The same change with a consistent-hash ring (100 virtual nodes)
//  4. A summary table for several N -> N+1 changes
//
// Run from the workshop folder: go run ./code/hashbuckets
package main

import (
	"crypto/sha256"
	"encoding/binary"
	"fmt"
	"sort"
	"strings"
)

const (
	numKeys = 10_000
	vnodes  = 100
)

// h is a stable 64-bit hash of a string.
func h(text string) uint64 {
	sum := sha256.Sum256([]byte(text))
	return binary.BigEndian.Uint64(sum[:8])
}

var (
	keys   []string
	hashes []uint64
)

func init() {
	for i := 0; i < numKeys; i++ {
		k := fmt.Sprintf("user:%d", i)
		keys = append(keys, k)
		hashes = append(hashes, h(k))
	}
}

func modAssign(n int) []int {
	out := make([]int, numKeys)
	for i, hv := range hashes {
		out[i] = int(hv % uint64(n))
	}
	return out
}

type point struct {
	pos   uint64
	owner int
}

// Ring is a consistent-hash ring: sorted points, each owned by a node.
type Ring struct{ points []point }

func newRing(nodes int) Ring {
	var pts []point
	for node := 0; node < nodes; node++ {
		for v := 0; v < vnodes; v++ {
			pts = append(pts, point{h(fmt.Sprintf("node-%d#%d", node, v)), node})
		}
	}
	sort.Slice(pts, func(i, j int) bool { return pts[i].pos < pts[j].pos })
	return Ring{pts}
}

// lookup walks clockwise to the first node point after the key.
func (r Ring) lookup(keyHash uint64) int {
	i := sort.Search(len(r.points), func(i int) bool { return r.points[i].pos > keyHash })
	if i == len(r.points) {
		i = 0 // wrap around the ring
	}
	return r.points[i].owner
}

func ringAssign(n int) []int {
	ring := newRing(n)
	out := make([]int, numKeys)
	for i, hv := range hashes {
		out[i] = ring.lookup(hv)
	}
	return out
}

func moved(before, after []int) int {
	c := 0
	for i := range before {
		if before[i] != after[i] {
			c++
		}
	}
	return c
}

// comma formats an int with thousands separators.
func comma(n int) string {
	s := fmt.Sprint(n)
	var b strings.Builder
	for i, ch := range s {
		if i > 0 && (len(s)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(ch)
	}
	return b.String()
}

func pct(x float64) string { return fmt.Sprintf("%.1f%%", 100*x) }

func barChart(assign []int, n int, label string) {
	counts := make([]int, n)
	for _, b := range assign {
		counts[b]++
	}
	for i, c := range counts {
		fmt.Printf("  %s %d: %6s  %s\n", label, i, comma(c), strings.Repeat("#", c/100))
	}
}

func banner(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 60))
}

func main() {
	banner(fmt.Sprintf("1. hash(key) %% 4 spreads %s keys evenly", comma(numKeys)))
	for i := 0; i < 3; i++ {
		fmt.Printf("  %-8s hash = %20d  %% 4 = %d\n", keys[i], hashes[i], hashes[i]%4)
	}
	fmt.Println("  ...")
	barChart(modAssign(4), 4, "bucket")

	banner("2. Grow from 4 to 5 buckets with hash % N")
	mv := moved(modAssign(4), modAssign(5))
	fmt.Printf("  keys that change bucket: %s of %s (%s)\n", comma(mv), comma(numKeys), pct(float64(mv)/numKeys))
	fmt.Printf("  ideal (only the fair share of the new bucket moves): %s (%s)\n", comma(numKeys/5), pct(1.0/5))

	banner(fmt.Sprintf("3. Same change with a consistent-hash ring (%d vnodes/node)", vnodes))
	r4, r5 := ringAssign(4), ringAssign(5)
	rv := moved(r4, r5)
	fmt.Printf("  keys that change node: %s of %s (%s)\n", comma(rv), comma(numKeys), pct(float64(rv)/numKeys))
	wrong := 0
	for i := range r4 {
		if r4[i] != r5[i] && r5[i] != 4 {
			wrong++
		}
	}
	fmt.Printf("  keys that moved somewhere other than the new node 4: %d\n", wrong)
	fmt.Println("  load after the change:")
	barChart(r5, 5, "node")

	banner("4. Summary: fraction of keys that move when N -> N+1")
	fmt.Printf("  %-8s %10s %8s %14s\n", "N->N+1", "hash % N", "ring", "ideal 1/(N+1)")
	for _, n := range []int{2, 4, 8, 16} {
		a := float64(moved(modAssign(n), modAssign(n+1))) / numKeys
		b := float64(moved(ringAssign(n), ringAssign(n+1))) / numKeys
		fmt.Printf("  %-8s %10s %8s %14s\n", fmt.Sprintf("%d->%d", n, n+1), pct(a), pct(b), pct(1/float64(n+1)))
	}
}
