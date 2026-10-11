// Command backoff simulates a retry storm with and without jitter.
//
// Setup: 100 clients all hit a recovering server at t = 0 ms. The server
// completes at most 5 requests per 10 ms slot in total; the rest fail and retry.
//
// Strategies (attempt numbers start at 0 for the first retry):
//
//	no jitter    sleep = min(capMs, baseMs * 2^attempt)
//	full jitter  sleep = uniform(0, min(capMs, baseMs * 2^attempt))
//	equal jitter sleep = half + uniform(0, half), half = min(...) / 2
//
// Full jitter follows the AWS Architecture Blog post "Exponential Backoff
// And Jitter". For each strategy the program prints total calls, the
// most retries in one 10 ms slot, the finish time, and an ASCII
// histogram of retries per 100 ms.
//
// Standard library only. No arguments. Seeded: rand.NewPCG(42, 42).
// Run: go run ./code/backoff
package main

import (
	"container/heap"
	"fmt"
	"math"
	"math/rand/v2"
	"strings"
)

const (
	clients    = 100
	capacity   = 5 // requests the server completes per slot
	slotMs     = 10
	baseMs     = 100
	capMs      = 5000
	maxRetries = 15
)

func ceiling(attempt int) float64 {
	return math.Min(capMs, baseMs*math.Pow(2, float64(attempt)))
}

type strategy func(attempt int, rng *rand.Rand) float64

func noJitter(attempt int, _ *rand.Rand) float64 { return ceiling(attempt) }

func fullJitter(attempt int, rng *rand.Rand) float64 {
	return rng.Float64() * ceiling(attempt)
}

func equalJitter(attempt int, rng *rand.Rand) float64 {
	half := ceiling(attempt) / 2
	return half + rng.Float64()*half
}

// call is one pending request: when it fires, who sends it, and how many
// retries that client has used so far.
type call struct {
	t     float64
	id    int
	tries int
}

type callHeap []call

func (h callHeap) Len() int { return len(h) }
func (h callHeap) Less(i, j int) bool {
	if h[i].t != h[j].t {
		return h[i].t < h[j].t
	}
	return h[i].id < h[j].id
}
func (h callHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *callHeap) Push(x any)   { *h = append(*h, x.(call)) }
func (h *callHeap) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

type result struct {
	perSlot map[int]int // retries arriving in each 10 ms slot
	calls   int
	gaveUp  int
	finish  float64
}

func simulate(next strategy) result {
	rng := rand.New(rand.NewPCG(42, 42))
	h := &callHeap{}
	for c := 0; c < clients; c++ {
		*h = append(*h, call{0, c, 0})
	}
	heap.Init(h)
	res := result{perSlot: map[int]int{}}
	served := map[int]int{} // successes already handed out in each slot
	for h.Len() > 0 {
		slot := int((*h)[0].t / slotMs)
		var batch []call
		for h.Len() > 0 && int((*h)[0].t/slotMs) == slot {
			batch = append(batch, heap.Pop(h).(call))
		}
		rng.Shuffle(len(batch), func(i, j int) { batch[i], batch[j] = batch[j], batch[i] })
		res.calls += len(batch)
		for _, c := range batch {
			if c.tries > 0 {
				res.perSlot[slot]++ // count retries only, not the first try
			}
			switch {
			case served[slot] < capacity:
				served[slot]++
				res.finish = math.Max(res.finish, c.t)
			case c.tries >= maxRetries:
				res.gaveUp++
			default:
				heap.Push(h, call{c.t + next(c.tries, rng), c.id, c.tries + 1})
			}
		}
	}
	return res
}

func histogram(perSlot map[int]int) {
	const windowMs, untilMs, scale = 100, 1600, 2
	perWindow := map[int]int{}
	for slot, count := range perSlot {
		perWindow[slot*slotMs/windowMs] += count
	}
	for w := 0; w < untilMs/windowMs; w++ {
		count := perWindow[w]
		bar := strings.Repeat("#", (count+scale-1)/scale)
		fmt.Printf("  %5d-%-5d ms %4d %s\n", w*windowMs, (w+1)*windowMs, count, bar)
	}
}

func comma(n int) string {
	s := fmt.Sprint(n)
	var b strings.Builder
	for i, c := range s {
		if i > 0 && (len(s)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(c)
	}
	return b.String()
}

func main() {
	fmt.Println("Backoff ceiling per retry: min(cap, base * 2^attempt)")
	fmt.Println("  base = 100 ms, cap = 5,000 ms")
	parts := []string{}
	for a := 0; a < 10; a++ {
		parts = append(parts, fmt.Sprintf("%d:%.0f", a, ceiling(a)))
	}
	fmt.Println("  attempt: " + strings.Join(parts, "  "))
	fmt.Println()
	fmt.Printf("%d clients, server completes %d requests per %d ms slot\n", clients, capacity, slotMs)
	fmt.Println()

	type row struct {
		name string
		res  result
		max  int
	}
	var rows []row
	for _, s := range []struct {
		name string
		fn   strategy
	}{{"no jitter", noJitter}, {"full jitter", fullJitter}, {"equal jitter", equalJitter}} {
		res := simulate(s.fn)
		busiest := 0
		for _, c := range res.perSlot {
			busiest = max(busiest, c)
		}
		rows = append(rows, row{s.name, res, busiest})
		fmt.Printf("--- %s ---\n", s.name)
		fmt.Printf("  total calls %s, most retries in one 10 ms slot %d, last success at %s ms, gave up %d\n",
			comma(res.calls), busiest, comma(int(math.Round(res.finish))), res.gaveUp)
		fmt.Println("  retries per 100 ms window (# = 2 retries), first 1.6 s:")
		histogram(res.perSlot)
		fmt.Println()
	}
	fmt.Println("Summary")
	fmt.Printf("  %-14s%8s%14s%12s%9s\n", "strategy", "calls", "retries/slot", "done at ms", "gave up")
	for _, r := range rows {
		fmt.Printf("  %-14s%8s%14d%12s%9d\n", r.name, comma(r.res.calls), r.max,
			comma(int(math.Round(r.res.finish))), r.res.gaveUp)
	}
}
