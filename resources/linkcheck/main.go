// Command linkcheck checks every external URL in resources/*.md and prints its status.
//
// Usage, from the repository root:
//
//	go run ./resources/linkcheck            # every link with its status
//	go run ./resources/linkcheck -failed    # only links that need attention
//
// Standard library only. Exit code 0 when every link is OK, 1 otherwise.
//
// Status words:
//
//	OK       the server answered 2xx (after redirects)
//	OK-CERT  the page loads, but the TLS certificate does not verify (common on old university servers)
//	BLOCKED  the server answered 401, 403, or 429 to a script; open it in a browser
//	MOVED    the page redirected to a different host; check that it is still on topic
//	DEAD     404, 410, DNS failure, timeout, or any other error (network errors get two retries)
package main

import (
	"bufio"
	"crypto/tls"
	"errors"
	"flag"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"sync"
	"time"
)

const userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " +
	"(KHTML, like Gecko) Chrome/124.0 Safari/537.36 linkcheck"

var urlRE = regexp.MustCompile("https?://[^\\s<>()\\[\\]\"'`]+")

type result struct {
	word, code, note string
}

// resourcesDir finds the resources folder from the repository root, the resources folder, or linkcheck itself.
func resourcesDir(flagDir string) string {
	if flagDir != "" {
		return flagDir
	}
	for _, d := range []string{"resources", ".", ".."} {
		if m, _ := filepath.Glob(filepath.Join(d, "free-textbooks.md")); len(m) > 0 {
			return d
		}
	}
	return "resources"
}

func findURLs(dir string) (map[string]string, error) {
	files, err := filepath.Glob(filepath.Join(dir, "*.md"))
	if err != nil || len(files) == 0 {
		return nil, fmt.Errorf("no Markdown files found in %q", dir)
	}
	sort.Strings(files)
	urls := map[string]string{}
	for _, f := range files {
		fh, err := os.Open(f)
		if err != nil {
			return nil, err
		}
		sc := bufio.NewScanner(fh)
		sc.Buffer(make([]byte, 1024*1024), 1024*1024)
		for n := 1; sc.Scan(); n++ {
			for _, u := range urlRE.FindAllString(sc.Text(), -1) {
				u = strings.TrimRight(u, ".,;:")
				if _, seen := urls[u]; !seen {
					urls[u] = fmt.Sprintf("%s:%d", filepath.Base(f), n)
				}
			}
		}
		fh.Close()
	}
	return urls, nil
}

func newClient(verify bool) *http.Client {
	tr := http.DefaultTransport.(*http.Transport).Clone()
	tr.TLSClientConfig = &tls.Config{InsecureSkipVerify: !verify}
	tr.TLSHandshakeTimeout = 25 * time.Second // some old servers are slow to shake hands
	return &http.Client{Timeout: 45 * time.Second, Transport: tr}
}

var (
	strict = newClient(true)
	loose  = newClient(false)
)

func fetch(c *http.Client, raw string) (int, string, error) {
	req, err := http.NewRequest("GET", raw, nil)
	if err != nil {
		return 0, "", err
	}
	req.Header.Set("User-Agent", userAgent)
	req.Header.Set("Accept", "*/*")
	resp, err := c.Do(req)
	if err != nil {
		return 0, "", err
	}
	defer resp.Body.Close()
	io.CopyN(io.Discard, resp.Body, 2048)
	return resp.StatusCode, resp.Request.URL.String(), nil
}

func isCertError(err error) bool {
	var hostErr *tls.CertificateVerificationError
	return errors.As(err, &hostErr) || strings.Contains(err.Error(), "certificate")
}

func check(raw string) result {
	for attempt := 0; ; attempt++ {
		word := "OK"
		code, final, err := fetch(strict, raw)
		if err != nil && isCertError(err) {
			word = "OK-CERT"
			code, final, err = fetch(loose, raw)
		}
		if err != nil && attempt < 2 {
			time.Sleep(3 * time.Second) // retry timeouts and TLS handshake hiccups
			continue
		}
		if err != nil {
			msg := err.Error()
			if len(msg) > 80 {
				msg = msg[:80]
			}
			return result{"DEAD", "ERR", msg}
		}
		if (code == 429 || code == 503) && attempt < 2 {
			time.Sleep(10 * time.Second)
			continue
		}
		switch {
		case code == 401 || code == 403 || code == 429:
			return result{"BLOCKED", fmt.Sprint(code), ""}
		case code >= 400:
			return result{"DEAD", fmt.Sprint(code), ""}
		}
		a, _ := url.Parse(raw)
		b, _ := url.Parse(final)
		if a != nil && b != nil && a.Hostname() != b.Hostname() {
			return result{"MOVED", fmt.Sprint(code), "-> " + final}
		}
		return result{word, fmt.Sprint(code), ""}
	}
}

func main() {
	onlyFailed := flag.Bool("failed", false, "print only links that need attention")
	dirFlag := flag.String("dir", "", "folder with the Markdown files (default: auto-detect resources/)")
	flag.Parse()

	urls, err := findURLs(resourcesDir(*dirFlag))
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}

	results := map[string]result{}
	var mu sync.Mutex
	var wg sync.WaitGroup
	sem := make(chan struct{}, 16)
	for u := range urls {
		wg.Add(1)
		go func(u string) {
			defer wg.Done()
			sem <- struct{}{}
			r := check(u)
			<-sem
			mu.Lock()
			results[u] = r
			mu.Unlock()
		}(u)
	}
	wg.Wait()

	keys := make([]string, 0, len(results))
	for u := range results {
		keys = append(keys, u)
	}
	sort.Slice(keys, func(i, j int) bool {
		oi, oj := results[keys[i]].word != "OK", results[keys[j]].word != "OK"
		if oi != oj {
			return !oi
		}
		return keys[i] < keys[j]
	})

	counts := map[string]int{}
	for _, u := range keys {
		r := results[u]
		counts[r.word]++
		if *onlyFailed && (r.word == "OK" || r.word == "OK-CERT") {
			continue
		}
		fmt.Println(strings.TrimRight(fmt.Sprintf("%-8s %-4s %s  [%s] %s", r.word, r.code, u, urls[u], r.note), " "))
	}

	words := make([]string, 0, len(counts))
	for w := range counts {
		words = append(words, w)
	}
	sort.Strings(words)
	parts := make([]string, 0, len(words))
	bad := false
	for _, w := range words {
		parts = append(parts, fmt.Sprintf("%s %d", w, counts[w]))
		if w != "OK" && w != "OK-CERT" {
			bad = true
		}
	}
	fmt.Printf("\nChecked %d unique URLs: %s\n", len(results), strings.Join(parts, ", "))
	if bad {
		os.Exit(1)
	}
}
