// Coding theory starter kit: repetition codes, parity, checksums, Hamming
// distance, the Hamming (7,4) code with matrices, CRC long division, finite
// fields, Reed-Solomon erasure recovery, RAID parity, storage durability and
// a random fountain code. Standard library only.
package main

import (
	"fmt"
	"hash/crc32"
	"math"
	"math/bits"
	"math/rand/v2"
	"strings"
)

// binom returns n choose k as a float.
func binom(n, k int) float64 {
	r := 1.0
	for i := 1; i <= k; i++ {
		r = r * float64(n-k+i) / float64(i)
	}
	return r
}

// tailProb returns the probability that more than m of n independent
// pieces fail, when each fails with probability p.
func tailProb(n, m int, p float64) float64 {
	s := 0.0
	for k := m + 1; k <= n; k++ {
		s += binom(n, k) * math.Pow(p, float64(k)) * math.Pow(1-p, float64(n-k))
	}
	return s
}

// bitsOf prints a slice of 0/1 values as a compact string.
func bitsOf(v []int) string {
	var b strings.Builder
	for _, x := range v {
		fmt.Fprint(&b, x)
	}
	return b.String()
}

// parse turns a string such as "1011" into a slice of 0/1 values.
func parse(s string) []int {
	v := make([]int, len(s))
	for i, c := range s {
		v[i] = int(c - '0')
	}
	return v
}

// hamDist counts positions where two equal-length words differ.
func hamDist(a, b []int) int {
	d := 0
	for i := range a {
		if a[i] != b[i] {
			d++
		}
	}
	return d
}

// --- Hamming (7,4) ---
// Positions 1..7 hold p1 p2 d1 p3 d2 d3 d4. Parity bits sit at the powers of 2.

var dataPos = []int{3, 5, 6, 7}

// encode74 places 4 data bits and fills the 3 parity bits.
func encode74(d []int) []int {
	c := make([]int, 8) // index 0 unused
	for i, p := range dataPos {
		c[p] = d[i]
	}
	for _, pp := range []int{1, 2, 4} {
		s := 0
		for pos := 1; pos <= 7; pos++ {
			if pos != pp && pos&pp != 0 {
				s ^= c[pos]
			}
		}
		c[pp] = s
	}
	return c[1:]
}

// syndrome74 XORs together the position numbers of all 1 bits.
// It equals the column of H that matches the error, and 0 for a codeword.
func syndrome74(c []int) int {
	s := 0
	for i, b := range c {
		if b == 1 {
			s ^= i + 1
		}
	}
	return s
}

// --- CRC by hand ---

// crcSteps divides msg (with r zero bits appended) by gen over GF(2)
// and prints each XOR step. It returns the remainder bits.
func crcSteps(msg, gen string) string {
	r := len(gen) - 1
	work := parse(msg + strings.Repeat("0", r))
	g := parse(gen)
	fmt.Printf("dividend %s (message + %d zeros), divisor %s\n", bitsOf(work), r, gen)
	for i := 0; i+len(g) <= len(work); i++ {
		if work[i] == 0 {
			continue
		}
		for j := range g {
			work[i+j] ^= g[j]
		}
		fmt.Printf("  XOR at column %d -> %s\n", i, bitsOf(work))
	}
	return bitsOf(work[len(work)-r:])
}

// --- GF(256) multiply, with the AES polynomial x^8+x^4+x^3+x+1 ---
func gfMul(a, b byte) byte {
	var p byte
	for b > 0 {
		if b&1 == 1 {
			p ^= a
		}
		hi := a & 0x80
		a <<= 1
		if hi != 0 {
			a ^= 0x1B
		}
		b >>= 1
	}
	return p
}

// --- arithmetic mod a small prime ---
func mod(a, p int) int { return ((a % p) + p) % p }

func inv(a, p int) int {
	for x := 1; x < p; x++ {
		if mod(a*x, p) == 1 {
			return x
		}
	}
	return 0
}

// lagrange returns the coefficients (low degree first) of the unique
// polynomial of degree < len(xs) through the points, mod p.
func lagrange(xs, ys []int, p int) []int {
	k := len(xs)
	coef := make([]int, k)
	for i := 0; i < k; i++ {
		// basis polynomial l_i(x) = prod (x - x_j)/(x_i - x_j)
		basis := []int{1}
		denom := 1
		for j := 0; j < k; j++ {
			if j == i {
				continue
			}
			next := make([]int, len(basis)+1)
			for t, b := range basis {
				next[t] = mod(next[t]-xs[j]*b, p)
				next[t+1] = mod(next[t+1]+b, p)
			}
			basis = next
			denom = mod(denom*(xs[i]-xs[j]), p)
		}
		scale := mod(ys[i]*inv(denom, p), p)
		for t := range coef {
			coef[t] = mod(coef[t]+scale*basis[t], p)
		}
	}
	return coef
}

func evalPoly(c []int, x, p int) int {
	y := 0
	for i := len(c) - 1; i >= 0; i-- {
		y = mod(y*x+c[i], p)
	}
	return y
}

// rankGF2 returns the rank of a set of k-bit row vectors over GF(2).
func rankGF2(rows []uint64) int {
	basis := map[int]uint64{}
	for _, r := range rows {
		for r != 0 {
			top := 63 - bits.LeadingZeros64(r)
			b, ok := basis[top]
			if !ok {
				basis[top] = r
				break
			}
			r ^= b
		}
	}
	return len(basis)
}

func main() {
	fmt.Println("== Repetition codes on a link that flips 1 bit in 10 ==")
	for _, n := range []int{1, 3, 5, 7} {
		fmt.Printf("repeat %d times: rate 1/%d, wrong after majority vote %.5f\n", n, n, tailProb(n, n/2, 0.1))
	}

	fmt.Println("\n== Parity bit ==")
	word := parse("1011001")
	par := 0
	for _, b := range word {
		par ^= b
	}
	sent := append(append([]int{}, word...), par)
	check := func(v []int) int {
		s := 0
		for _, b := range v {
			s ^= b
		}
		return s
	}
	one := append([]int{}, sent...)
	one[2] ^= 1
	two := append([]int{}, one...)
	two[5] ^= 1
	fmt.Printf("data %s parity %d -> sent %s\n", bitsOf(word), par, bitsOf(sent))
	fmt.Printf("1 flip  %s check %d (odd: error caught)\n", bitsOf(one), check(one))
	fmt.Printf("2 flips %s check %d (even: error missed)\n", bitsOf(two), check(two))

	fmt.Println("\n== Checksums ==")
	isbn := func(s string) (plain, weighted int) {
		d := parse(s)
		for i, x := range d {
			plain += x
			weighted += (10 - i) * x
		}
		return plain % 10, weighted % 11
	}
	for _, s := range []string{"0306406152", "0306460152"} {
		p, w := isbn(s)
		fmt.Printf("ISBN %s: plain sum mod 10 = %d, weighted sum mod 11 = %d\n", s, p, w)
	}
	fmt.Printf("CRC-32 of \"123456789\" = %08X\n", crc32.ChecksumIEEE([]byte("123456789")))
	fmt.Printf("CRC-32 of \"123456798\" = %08X\n", crc32.ChecksumIEEE([]byte("123456798")))

	fmt.Println("\n== Hamming distance ==")
	a, b := parse("10110"), parse("11100")
	fmt.Printf("d(%s, %s) = %d\n", bitsOf(a), bitsOf(b), hamDist(a, b))
	for _, d := range []int{2, 3, 5, 7} {
		fmt.Printf("min distance %d: detects up to %d, corrects up to %d\n", d, d-1, (d-1)/2)
	}

	fmt.Println("\n== Hamming (7,4) ==")
	fmt.Println("generator rows (encodings of 1000, 0100, 0010, 0001):")
	for i := 0; i < 4; i++ {
		d := make([]int, 4)
		d[i] = 1
		fmt.Printf("  %s\n", bitsOf(encode74(d)))
	}
	fmt.Println("parity-check H (column j is j in binary, low bit on top):")
	for _, bit := range []int{1, 2, 4} {
		row := make([]int, 7)
		for j := 1; j <= 7; j++ {
			if j&bit != 0 {
				row[j-1] = 1
			}
		}
		fmt.Printf("  %s\n", bitsOf(row))
	}
	minW, all := 7, [][]int{}
	for m := 0; m < 16; m++ {
		d := []int{m >> 3 & 1, m >> 2 & 1, m >> 1 & 1, m & 1}
		c := encode74(d)
		all = append(all, c)
		w := 0
		for _, x := range c {
			w += x
		}
		if m > 0 && w < minW {
			minW = w
		}
	}
	fmt.Printf("16 codewords, smallest nonzero weight = %d = minimum distance\n", minW)
	fixed := 0
	for _, c := range all {
		for pos := 1; pos <= 7; pos++ {
			r := append([]int{}, c...)
			r[pos-1] ^= 1
			if s := syndrome74(r); s == pos {
				r[s-1] ^= 1
				if hamDist(r, c) == 0 {
					fixed++
				}
			}
		}
	}
	fmt.Printf("single-error tests repaired: %d of %d\n", fixed, 16*7)
	fmt.Printf("sphere packing: 16 codewords x (1 + 7) words each = %d = 2^7\n", 16*8)
	c := encode74(parse("1101"))
	r := append([]int{}, c...)
	r[5] ^= 1
	s := syndrome74(r)
	fmt.Printf("data 1101 -> codeword %s\n", bitsOf(c))
	fmt.Printf("received  %s syndrome %03b = %d\n", bitsOf(r), s, s)
	r[s-1] ^= 1
	fmt.Printf("repaired  %s\n", bitsOf(r))

	fmt.Println("\n== CRC by long division over GF(2) ==")
	rem := crcSteps("110101", "1011")
	fmt.Printf("remainder %s -> transmit 110101%s\n", rem, rem)
	fmt.Printf("check: remainder of 110101%s is %s\n", rem, crcCheck("110101"+rem, "1011"))

	fmt.Println("\n== Finite fields ==")
	fmt.Print("inverses mod 7:")
	for x := 1; x < 7; x++ {
		fmt.Printf(" %d->%d", x, inv(x, 7))
	}
	fmt.Println()
	fmt.Printf("GF(256): 0x53 * 0xCA = 0x%02X\n", gfMul(0x53, 0xCA))
	fmt.Printf("GF(256): 0x57 * 0x83 = 0x%02X\n", gfMul(0x57, 0x83))

	fmt.Println("\n== Reed-Solomon over GF(7): k = 2, n = 6 ==")
	data := []int{3, 2} // f(x) = 3 + 2x
	var shares []int
	for x := 0; x < 6; x++ {
		shares = append(shares, evalPoly(data, x, 7))
	}
	fmt.Printf("f(x) = 3 + 2x, shares at x = 0..5: %v\n", shares)
	got := lagrange([]int{2, 5}, []int{shares[2], shares[5]}, 7)
	fmt.Printf("keep only x=2 (%d) and x=5 (%d) -> recovered f(x) = %d + %dx\n", shares[2], shares[5], got[0], got[1])
	data3 := []int{2, 5, 1} // f(x) = 2 + 5x + x^2
	var sh3 []int
	for x := 0; x < 6; x++ {
		sh3 = append(sh3, evalPoly(data3, x, 7))
	}
	got3 := lagrange([]int{1, 3, 4}, []int{sh3[1], sh3[3], sh3[4]}, 7)
	fmt.Printf("k = 3: f(x) = 2 + 5x + x^2, shares %v, from x=1,3,4 -> %v\n", sh3, got3)

	fmt.Println("\n== RAID 5 parity ==")
	d1, d2, d3 := uint8(0b1011), uint8(0b0110), uint8(0b1100)
	p := d1 ^ d2 ^ d3
	fmt.Printf("D1 %04b  D2 %04b  D3 %04b  P = D1^D2^D3 = %04b\n", d1, d2, d3, p)
	fmt.Printf("disk 2 dies: D1^D3^P = %04b (was %04b)\n", d1^d3^p, d2)

	fmt.Println("\n== Storage schemes, each piece lost with probability 0.01 ==")
	type scheme struct {
		name   string
		n, k   int
		failOK int
	}
	for _, sc := range []scheme{
		{"3x replication", 3, 1, 2},
		{"RAID 5 (4+1)", 5, 4, 1},
		{"RAID 6 (4+2)", 6, 4, 2},
		{"RS 6+3", 9, 6, 3},
		{"RS 10+4", 14, 10, 4},
		{"RS 17+3", 20, 17, 3},
	} {
		fmt.Printf("%-15s overhead %.2fx  tolerates %d lost  P(data loss) %.2e\n",
			sc.name, float64(sc.n)/float64(sc.k), sc.failOK, tailProb(sc.n, sc.failOK, 0.01))
	}

	fmt.Println("\n== Peeling decoder (erasure LDPC / LT style) ==")
	src := []uint8{0b1010, 0b0111, 0b1100, 0b0001}
	type sym struct {
		nb  []int
		val uint8
	}
	recv := []sym{{[]int{0}, 0}, {[]int{0, 1}, 0}, {[]int{1, 2, 3}, 0}, {[]int{2, 3}, 0}, {[]int{1, 3}, 0}}
	for i := range recv {
		for _, j := range recv[i].nb {
			recv[i].val ^= src[j]
		}
	}
	known := map[int]uint8{}
	for progress := true; progress; {
		progress = false
		for _, rs := range recv {
			var unknown []int
			v := rs.val
			for _, j := range rs.nb {
				if kv, ok := known[j]; ok {
					v ^= kv
				} else {
					unknown = append(unknown, j)
				}
			}
			if len(unknown) == 1 {
				known[unknown[0]] = v
				fmt.Printf("symbol over %v has one unknown -> s%d = %04b\n", rs.nb, unknown[0]+1, v)
				progress = true
			}
		}
	}
	fmt.Printf("recovered %d of %d sources\n", len(known), len(src))

	fmt.Println("\n== Random linear fountain, k = 32 source blocks ==")
	rng := rand.New(rand.NewPCG(7, 11))
	const k, trials = 32, 2000
	total, hist := 0, map[int]int{}
	for t := 0; t < trials; t++ {
		var rows []uint64
		for rankGF2(rows) < k {
			rows = append(rows, rng.Uint64()&(1<<k-1))
		}
		extra := len(rows) - k
		total += extra
		hist[min(extra, 5)]++
	}
	fmt.Printf("average extra symbols needed: %.2f\n", float64(total)/trials)
	for e := 0; e <= 5; e++ {
		lab := fmt.Sprint(e)
		if e == 5 {
			lab = "5+"
		}
		fmt.Printf("  needed k+%-2s %5.1f%%\n", lab, 100*float64(hist[e])/trials)
	}
}

// crcCheck returns the remainder of a full codeword divided by gen.
func crcCheck(code, gen string) string {
	w := parse(code)
	g := parse(gen)
	for i := 0; i+len(g) <= len(w); i++ {
		if w[i] == 1 {
			for j := range g {
				w[i+j] ^= g[j]
			}
		}
	}
	return bitsOf(w[len(w)-len(g)+1:])
}
