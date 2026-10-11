// Command makewav builds A440 and the perfect fifth as audio samples and
// optionally saves them as a WAV file.
//
// By default it only prints the plan: each segment, its frequencies, the
// sample count, a few 16-bit samples, and the file size. Nothing is written.
//
//	go run ./code/makewav                      print only
//	go run ./code/makewav -wav                 also write a440_fifth.wav
//	go run ./code/makewav -wav -out x.wav      write to x.wav instead
//
// Segments (one second each, 44,100 samples per second, 16-bit mono):
//  1. A4 alone, 440 Hz
//  2. E5 alone, equal-tempered, 659.26 Hz
//  3. A4 + E5 just fifth (440 + 660 Hz)
//  4. A4 + E5 equal-tempered fifth (440 + 659.26 Hz)
//
// Standard library only. The WAV header is written by hand with
// encoding/binary: a 44-byte RIFF header followed by little-endian samples.
package main

import (
	"bytes"
	"encoding/binary"
	"flag"
	"fmt"
	"math"
	"os"
	"strings"
)

const (
	rate    = 44100
	seconds = 1.0
	volume  = 0.4  // fraction of full scale, leaves headroom
	fade    = 0.01 // 10 ms fade in and out, avoids clicks
)

var e5ET = 440 * math.Pow(2, 7.0/12)

type segment struct {
	name  string
	freqs []float64
}

var segments = []segment{
	{"A4 alone", []float64{440}},
	{"E5 alone (equal-tempered)", []float64{e5ET}},
	{"A4 + E5 just fifth 3:2", []float64{440, 660}},
	{"A4 + E5 equal-tempered fifth", []float64{440, e5ET}},
}

// segmentSamples returns 16-bit samples for an average of sine waves.
func segmentSamples(freqs []float64) []int16 {
	n := int(rate * seconds)
	fadeN := float64(rate) * fade
	out := make([]int16, n)
	for i := range out {
		t := float64(i) / rate
		v := 0.0
		for _, f := range freqs {
			v += math.Sin(2 * math.Pi * f * t)
		}
		v /= float64(len(freqs))
		env := math.Min(1, math.Min(float64(i)/fadeN, float64(n-1-i)/fadeN))
		out[i] = int16(math.Round(v * env * volume * 32767))
	}
	return out
}

// wavBytes wraps 16-bit mono samples in a 44-byte RIFF/WAVE header.
func wavBytes(samples []int16) []byte {
	var b bytes.Buffer
	dataLen := uint32(len(samples) * 2)
	b.WriteString("RIFF")
	binary.Write(&b, binary.LittleEndian, 36+dataLen)
	b.WriteString("WAVEfmt ")
	binary.Write(&b, binary.LittleEndian, uint32(16))     // fmt chunk size
	binary.Write(&b, binary.LittleEndian, uint16(1))      // PCM
	binary.Write(&b, binary.LittleEndian, uint16(1))      // mono
	binary.Write(&b, binary.LittleEndian, uint32(rate))   // sample rate
	binary.Write(&b, binary.LittleEndian, uint32(rate*2)) // bytes per second
	binary.Write(&b, binary.LittleEndian, uint16(2))      // bytes per frame
	binary.Write(&b, binary.LittleEndian, uint16(16))     // bits per sample
	b.WriteString("data")
	binary.Write(&b, binary.LittleEndian, dataLen)
	binary.Write(&b, binary.LittleEndian, samples)
	return b.Bytes()
}

// commaStr adds thousands separators to a formatted number such as "1318.51".
func commaStr(s string) string {
	whole, frac := s, ""
	if i := strings.IndexByte(s, '.'); i >= 0 {
		whole, frac = s[:i], s[i:]
	}
	var b strings.Builder
	for i, c := range whole {
		if i > 0 && (len(whole)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(c)
	}
	return b.String() + frac
}

func comma(n int) string { return commaStr(fmt.Sprint(n)) }

func main() {
	write := flag.Bool("wav", false, "write the WAV file")
	out := flag.String("out", "a440_fifth.wav", "output path")
	flag.Parse()

	fmt.Printf("sample rate %s Hz, Nyquist limit %s Hz, 16-bit mono\n", comma(rate), comma(rate/2))
	fmt.Printf("sample spacing 1 / %s s = %.2f microseconds\n", comma(rate), 1e6/rate)
	fmt.Printf("one A4 cycle (2.273 ms) spans %.2f samples\n", rate/440.0)
	fmt.Println()
	var all []int16
	for _, s := range segments {
		smp := segmentSamples(s.freqs)
		all = append(all, smp...)
		fs := []string{}
		for _, f := range s.freqs {
			fs = append(fs, fmt.Sprintf("%.2f", f))
		}
		fmt.Printf("%-30s %16s Hz  %s samples\n", s.name, strings.Join(fs, " + "), comma(len(smp)))
		fmt.Printf("  samples 441..446: %v\n", smp[441:447])
	}
	fmt.Println()
	fmt.Printf("equal-tempered E5 is %.2f Hz flat of 660 Hz (%.3f cents)\n", 660-e5ET, 1200*math.Log2(660/e5ET))
	fmt.Printf("on a real instrument, harmonic 3 of A4 (1,320 Hz) and harmonic 2 of E5 (%s Hz)\n", commaStr(fmt.Sprintf("%.2f", 2*e5ET)))
	fmt.Printf("  beat %.2f times per second; this file uses pure sines, which have no harmonics and hide most of that beat\n",
		math.Abs(1320-2*e5ET))
	data := wavBytes(all)
	fmt.Println()
	fmt.Printf("total %s samples, %.0f s, file size %s bytes\n", comma(len(all)),
		float64(len(segments))*seconds, comma(len(data)))
	if *write {
		if err := os.WriteFile(*out, data, 0o644); err != nil {
			fmt.Fprintln(os.Stderr, "write failed:", err)
			os.Exit(1)
		}
		fmt.Println("wrote " + *out)
	} else {
		fmt.Println("no file written (pass -wav to write a440_fifth.wav)")
	}
}
