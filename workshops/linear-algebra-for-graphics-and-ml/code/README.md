# Code

Go standard library only. Tested with Go 1.27.2. Each program is one `main.go` in its own folder, needs no arguments, and finishes in well under a second. Run them from the workshop folder (the one holding `go.mod`).

| Program | Run | Prints |
|---|---|---|
| [transforms](transforms/main.go) | `go run ./code/transforms` | basis vectors under scale, rotate, shear, reflect; rotate-then-scale versus scale-then-rotate; the house rotated by 30 degrees; a 3x3 homogeneous rotate-then-translate |
| [similarity](similarity/main.go) | `go run ./code/similarity` | dot product, lengths, and angle for (3, 1) and (1, 2); cosine for same, right-angle, and opposite vectors; a hand-made 4-dimensional word embedding, its similarity matrix, and nearest neighbors by cosine |
| [regression](regression/main.go) | `go run ./code/regression` | the sums, the normal equations as a 2x2 system, m and b by the determinant rule, residuals with text bars, and the rate that reaches 80% CPU |

From inside a program folder, `go run .` works too.

## Optional Flag

`transforms -svg PATH` also writes the original and rotated house outlines as an SVG file at PATH, for example:

```txt
go run ./code/transforms -svg /tmp/house.svg
```

Write the file outside the repository. The committed figures in `../img/` come from a separate generator.

## Helpers

Each program carries its own small helpers on plain slices: `matmul`, `matvec`, `transpose`, `det2`, `dot`, `length`, `cosine`. No libraries, to keep every multiply in plain sight.
