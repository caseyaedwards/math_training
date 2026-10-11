# Code

Three small Go programs, one folder each, standard library only. Tested with Go 1.27.2. The `go.mod` file in the workshop folder lets `go run ./code/<name>` work from there.

Run each program from the workshop folder:

```txt
go run ./code/tuning
go run ./code/fourier
go run ./code/makewav
go run ./code/makewav -wav
```

Or step into a folder and run `go run .` (or `go run main.go`).

| Program | What it prints |
|---|---|
| `tuning/main.go` | One octave of equal temperament with periods; equal-tempered versus just intervals in cents (fifth 1.955 cents, major third 13.686 cents); peak alignment for 3:2 as an ASCII strip; piano key frequencies on a log2 scale; the harmonic series of 110 Hz; decibel ratios. |
| `fourier/main.go` | Square-wave partial sums as a table and ASCII plots, the Gibbs overshoot, a naive DFT that finds 440, 660, and 1,320 Hz in noise, daily and weekly seasonality in a synthetic hourly metric, and a scrape-interval aliasing table. Seeded with `rand.NewPCG(42, 42)`, which gives the same output on every run. |
| `makewav/main.go` | The audio plan: sample rate, Nyquist limit, sample counts, a few samples of each segment, and the file size. Writes nothing by default. |
| `makewav/main.go -wav` | Also writes `a440_fifth.wav` (four seconds, 44,100 Hz, 16-bit mono, 352,844 bytes) in the current folder: A4, E5, the just fifth, and the equal-tempered fifth. Add `-out path.wav` to choose another file name. |

All programs finish in under a second. Open the WAV file with any audio player, for example `afplay a440_fifth.wav` on macOS.
