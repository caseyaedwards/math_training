# Link Checker

A small Go program that checks every external URL in `resources/*.md` and prints its status. It uses the standard library only.

## Run It

From the repository root:

```txt
go run ./resources/linkcheck/main.go            # every link with its status
go run ./resources/linkcheck/main.go -failed    # only links that need attention
```

The shorter form `go run ./resources/linkcheck` needs a `go.mod` file at the repository root. Without one, use the file path form above.

Flags:

* `-failed`: print only links that are not `OK` or `OK-CERT`.
* `-dir`: the folder with the Markdown files. By default the program finds `resources/` from the repository root, from `resources/`, or from this folder.

## Read the Output

* `OK`: the server answered 2xx after redirects.
* `OK-CERT`: the page loads, but the TLS certificate does not verify. Old university servers do this often.
* `BLOCKED`: the server answered 401, 403, or 429 to a script. Open the link in a browser.
* `MOVED`: the page redirected to a different host. Check that it still covers the same topic, then update the link.
* `DEAD`: 404, 410, DNS failure, or timeout after two retries.

The program exits with code 0 when every link is `OK` or `OK-CERT`, and 1 otherwise.
