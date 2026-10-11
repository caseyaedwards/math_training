// Command mercator shows where Mercator puts latitude lines, the scale
// factors, and why Greenland looks so big.
//
// It prints:
//  1. Mercator y and equirectangular y for latitudes 0 to 85 degrees
//  2. an ASCII side-by-side grid: equal spacing versus stretched spacing
//  3. the scale factor sec(lat) and area factor sec^2(lat), as bars
//  4. Greenland versus Africa: true areas and how big Mercator draws them
//  5. a check that Mercator y is the integral of sec, by a midpoint sum
//
// All y values are in units of the Earth radius R (so R = 1).
//
// Run from the workshop folder: go run ./code/mercator
package main

import (
	"fmt"
	"math"
	"strings"
)

func rad(d float64) float64 { return d * math.Pi / 180 }

func mercY(lat float64) float64 {
	y := math.Log(math.Tan(math.Pi/4 + rad(lat)/2))
	if math.Abs(y) < 1e-12 { // tan(45 deg) is 0.99999... in floats
		return 0
	}
	return y
}

func equiY(lat float64) float64 { return rad(lat) }

func sec(lat float64) float64 { return 1 / math.Cos(rad(lat)) }

func section(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 64))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 64))
}

func partTable() {
	section("1. Where each latitude line lands (y in units of R)")
	fmt.Println("   lat   equirect y = phi   mercator y = ln tan(45 + lat/2)   gap above")
	lats := []float64{0, 15, 30, 45, 60, 75, 80, 85}
	for i, lat := range lats {
		gap := ""
		if i+1 < len(lats) && lats[i+1]-lat == 15 {
			gap = fmt.Sprintf("%.4f", mercY(lats[i+1])-mercY(lat))
		}
		line := fmt.Sprintf("   %3.0f   %10.4f         %10.4f                    %s", lat, equiY(lat), mercY(lat), gap)
		fmt.Println(strings.TrimRight(line, " "))
	}
	fmt.Println("   mercator y at 90 = ln(tan 90) = infinity: the poles never fit")
}

func partGrid() {
	section("2. Latitude lines every 10 degrees, same vertical scale")
	const step, top = 0.0625, 2.5
	rows := int(top/step) + 1
	fmt.Println("   y/R   equirectangular        mercator")
	for r := 0; r < rows; r++ {
		y := top - float64(r)*step
		var cells []string
		for _, proj := range []func(float64) float64{equiY, mercY} {
			cell := strings.Repeat(" ", 17)
			for lat := 0.0; lat <= 80; lat += 10 {
				if v := proj(lat); y-step/2 <= v && v < y+step/2 {
					cell = fmt.Sprintf("%s %2.0f", strings.Repeat("-", 14), lat)
					break
				}
			}
			cells = append(cells, cell)
		}
		fmt.Println(strings.TrimRight(fmt.Sprintf("  %5.2f  %s    %s", y, cells[0], cells[1]), " "))
	}
	fmt.Println("  equirectangular spaces lines evenly; mercator spreads them apart")
}

func partScale() {
	section("3. Scale factor k = sec(lat) and area factor k^2")
	fmt.Println("   lat     k = sec     k^2     area bar (each # = 1x)")
	for _, lat := range []float64{0, 10, 20, 30, 40, 50, 60, 70, 72, 80} {
		k := sec(lat)
		fmt.Printf("   %3.0f   %8.4f  %8.4f    %s\n", lat, k, k*k, strings.Repeat("#", int(math.Round(k*k))))
	}
}

func partGreenland() {
	section("4. Greenland versus Africa")
	const greenlandTrue = 2.166 // million km^2
	const africaTrue = 30.37    // million km^2
	const gLat, aLat = 72.0, 0.0
	gK, aK := math.Pow(sec(gLat), 2), math.Pow(sec(aLat), 2)
	fmt.Printf("   true area   Greenland %6.3f M km^2   Africa %6.2f M km^2\n", greenlandTrue, africaTrue)
	fmt.Printf("   Africa is %.1f times bigger on the globe\n", africaTrue/greenlandTrue)
	fmt.Printf("   Mercator area factor at %.0f N: sec^2 = %.2f\n", gLat, gK)
	fmt.Printf("   Mercator area factor at  %.0f N: sec^2 = %.2f\n", aLat, aK)
	gDrawn := greenlandTrue * gK
	fmt.Printf("   Greenland as drawn: %.3f x %.2f = %.1f M km^2 of map\n", greenlandTrue, gK, gDrawn)
	fmt.Printf("   Africa as drawn (equator value): %.2f M km^2 of map\n", africaTrue)
	fmt.Printf("   drawn ratio Africa : Greenland = %.2f : 1\n", africaTrue/gDrawn)
	fmt.Println("   (Africa reaches 35 S to 37 N and is drawn a bit larger than this;")
	fmt.Println("    the eye sees two shapes of similar size, not a 14 : 1 difference)")
}

func partIntegral() {
	section("5. Mercator y is the integral of sec from 0 to lat")
	for _, lat := range []float64{30, 60, 80} {
		const n = 10000
		h := rad(lat) / n
		total := 0.0
		for i := 0; i < n; i++ {
			total += 1 / math.Cos((float64(i)+0.5)*h)
		}
		total *= h
		fmt.Printf("   lat %.0f: midpoint sum = %.6f   ln tan(45 + lat/2) = %.6f\n", lat, total, mercY(lat))
	}
}

func main() {
	partTable()
	partGrid()
	partScale()
	partGreenland()
	partIntegral()
}
