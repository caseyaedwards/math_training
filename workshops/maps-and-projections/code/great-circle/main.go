// Command great-circle computes great-circle distance, bearing, and a
// nearest-datacenter pick.
//
// It prints:
//  1. JFK to LHR step by step: 3D unit vectors, haversine, law of cosines
//  2. the initial bearing out of JFK
//  3. waypoints along the route, showing it bulges north of both ends
//  4. a distance table among several airports
//  5. for each user city, the nearest datacenter region and a
//     speed-of-light-in-fiber round-trip floor
//
// Coordinates are airport reference points rounded to 2 decimals
// (north and east positive). Datacenter coordinates are the metro areas
// of typical cloud regions, rounded to 2 decimals.
//
// Run from the workshop folder: go run ./code/great-circle
package main

import (
	"fmt"
	"math"
	"sort"
	"strings"
)

const (
	rEarthKm     = 6371.0 // mean Earth radius
	fiberKmPerMs = 200.0  // light in fiber: about 200,000 km/s
)

type place struct {
	code, name string
	lat, lon   float64
}

var airports = []place{
	{"JFK", "New York", 40.64, -73.78},
	{"LHR", "London", 51.47, -0.46},
	{"SFO", "San Francisco", 37.62, -122.38},
	{"NRT", "Tokyo Narita", 35.77, 140.39},
	{"SIN", "Singapore", 1.36, 103.99},
	{"SYD", "Sydney", -33.95, 151.18},
	{"GRU", "Sao Paulo", -23.44, -46.47},
}

var datacenters = []place{
	{"", "us-east (N. Virginia)", 39.04, -77.49},
	{"", "us-west (Oregon)", 45.84, -119.70},
	{"", "eu-west (Dublin)", 53.35, -6.26},
	{"", "ap-northeast (Tokyo)", 35.68, 139.69},
	{"", "ap-southeast (Singapore)", 1.35, 103.82},
}

func rad(d float64) float64 { return d * math.Pi / 180 }
func deg(r float64) float64 { return r * 180 / math.Pi }

// toXYZ puts a point on the unit sphere. x toward (0N, 0E), z toward the North Pole.
func toXYZ(lat, lon float64) [3]float64 {
	phi, lam := rad(lat), rad(lon)
	return [3]float64{math.Cos(phi) * math.Cos(lam), math.Cos(phi) * math.Sin(lam), math.Sin(phi)}
}

func dot3(a, b [3]float64) float64 { return a[0]*b[0] + a[1]*b[1] + a[2]*b[2] }

func haversineKm(lat1, lon1, lat2, lon2 float64) float64 {
	p1, p2 := rad(lat1), rad(lat2)
	dphi, dlam := p2-p1, rad(lon2-lon1)
	a := math.Pow(math.Sin(dphi/2), 2) + math.Cos(p1)*math.Cos(p2)*math.Pow(math.Sin(dlam/2), 2)
	return 2 * rEarthKm * math.Asin(math.Sqrt(a))
}

func cosinesKm(lat1, lon1, lat2, lon2 float64) float64 {
	p1, p2 := rad(lat1), rad(lat2)
	dlam := rad(lon2 - lon1)
	c := math.Sin(p1)*math.Sin(p2) + math.Cos(p1)*math.Cos(p2)*math.Cos(dlam)
	return rEarthKm * math.Acos(math.Max(-1, math.Min(1, c)))
}

func initialBearingDeg(lat1, lon1, lat2, lon2 float64) float64 {
	p1, p2 := rad(lat1), rad(lat2)
	dlam := rad(lon2 - lon1)
	y := math.Sin(dlam) * math.Cos(p2)
	x := math.Cos(p1)*math.Sin(p2) - math.Sin(p1)*math.Cos(p2)*math.Cos(dlam)
	return math.Mod(deg(math.Atan2(y, x))+360, 360)
}

// slerpPoint returns the point a fraction t of the way along the great circle from a to b.
func slerpPoint(a, b [3]float64, t float64) (lat, lon float64) {
	omega := math.Acos(dot3(a, b))
	s := math.Sin(omega)
	wa, wb := math.Sin((1-t)*omega)/s, math.Sin(t*omega)/s
	var p [3]float64
	for i := range p {
		p[i] = wa*a[i] + wb*b[i]
	}
	return deg(math.Asin(p[2])), deg(math.Atan2(p[1], p[0]))
}

// commas formats a number with thousands separators and the given decimals.
func commas(x float64, decimals int) string {
	s := fmt.Sprintf("%.*f", decimals, x)
	intPart, frac := s, ""
	if i := strings.IndexByte(s, '.'); i >= 0 {
		intPart, frac = s[:i], s[i:]
	}
	var b strings.Builder
	for i, c := range intPart {
		if i > 0 && (len(intPart)-i)%3 == 0 {
			b.WriteByte(',')
		}
		b.WriteRune(c)
	}
	return b.String() + frac
}

func section(title string) {
	fmt.Println()
	fmt.Println(strings.Repeat("=", 66))
	fmt.Println(title)
	fmt.Println(strings.Repeat("=", 66))
}

func find(code string) place {
	for _, p := range airports {
		if p.code == code {
			return p
		}
	}
	panic("unknown airport " + code)
}

func partJfkLhr() {
	section("1. JFK to LHR, three ways")
	j, l := find("JFK"), find("LHR")
	fmt.Printf("JFK  lat %6.2f  lon %7.2f\n", j.lat, j.lon)
	fmt.Printf("LHR  lat %6.2f  lon %7.2f\n", l.lat, l.lon)
	a, b := toXYZ(j.lat, j.lon), toXYZ(l.lat, l.lon)
	fmt.Printf("JFK on unit sphere: (%.4f, %.4f, %.4f)\n", a[0], a[1], a[2])
	fmt.Printf("LHR on unit sphere: (%.4f, %.4f, %.4f)\n", b[0], b[1], b[2])
	d := dot3(a, b)
	ang := math.Acos(d)
	fmt.Printf("dot product = cos(central angle) = %.6f\n", d)
	fmt.Printf("central angle = %.6f rad = %.4f deg\n", ang, deg(ang))
	fmt.Printf("3D dot product   : %9s km\n", commas(rEarthKm*ang, 1))
	fmt.Printf("haversine        : %9s km\n", commas(haversineKm(j.lat, j.lon, l.lat, l.lon), 1))
	fmt.Printf("law of cosines   : %9s km\n", commas(cosinesKm(j.lat, j.lon, l.lat, l.lon), 1))
	chord := rEarthKm * math.Sqrt(math.Pow(a[0]-b[0], 2)+math.Pow(a[1]-b[1], 2)+math.Pow(a[2]-b[2], 2))
	fmt.Printf("straight tunnel  : %9s km  (chord through the Earth)\n", commas(chord, 1))
}

func partBearing() {
	section("2. Initial bearing (degrees clockwise from north)")
	for _, pair := range [][2]string{{"JFK", "LHR"}, {"LHR", "JFK"}, {"SFO", "NRT"}} {
		a, b := find(pair[0]), find(pair[1])
		fmt.Printf("%s -> %s: %6.1f deg\n", a.code, b.code, initialBearingDeg(a.lat, a.lon, b.lat, b.lon))
	}
	fmt.Println("a straight east line from JFK has bearing 90; the great circle starts")
	fmt.Println("well north of east, then swings round to come into London from the west")
}

func partWaypoints() {
	section("3. Waypoints JFK -> LHR along the great circle")
	j, l := find("JFK"), find("LHR")
	a, b := toXYZ(j.lat, j.lon), toXYZ(l.lat, l.lon)
	fmt.Println("  frac    lat     lon    latitude bar (each # = 1 deg above 40N)")
	for i := 0; i <= 10; i++ {
		t := float64(i) / 10
		lat, lon := slerpPoint(a, b, t)
		fmt.Printf("  %4.1f  %6.2f  %7.2f  %s\n", t, lat, lon, strings.Repeat("#", int(math.Round(lat-40))))
	}
	fmt.Println("the route climbs above 51.47 N (London) before it arrives:")
	fmt.Println("on a flat map that looks like a curve; on the globe it is straight")
}

func partTable() {
	section("4. Great-circle distance table (km, haversine, R = 6,371 km)")
	fmt.Print("      ")
	for _, p := range airports {
		fmt.Printf("%8s", p.code)
	}
	fmt.Println()
	for _, p := range airports {
		fmt.Printf("  %4s", p.code)
		for _, q := range airports {
			fmt.Printf("%8s", commas(haversineKm(p.lat, p.lon, q.lat, q.lon), 0))
		}
		fmt.Println()
	}
}

func partDatacenter() {
	section("5. Nearest datacenter for users at each airport")
	fmt.Println("  RTT floor = 2 x distance / (200 km per ms), light in fiber, no hops")
	type cand struct {
		km   float64
		name string
	}
	for _, p := range airports {
		var ranked []cand
		for _, d := range datacenters {
			ranked = append(ranked, cand{haversineKm(p.lat, p.lon, d.lat, d.lon), d.name})
		}
		sort.Slice(ranked, func(i, j int) bool { return ranked[i].km < ranked[j].km })
		best := ranked[0]
		rtt := 2 * best.km / fiberKmPerMs
		n := int(math.Round(rtt / 5))
		if n < 1 {
			n = 1
		}
		fmt.Printf("  %s %-14s -> %-24s %7s km  RTT >= %5.1f ms  %s\n",
			p.code, p.name, best.name, commas(best.km, 0), rtt, strings.Repeat("#", n))
	}
	fmt.Println("  (each # = 5 ms; real RTT is higher: routes are not great circles)")
}

func main() {
	partJfkLhr()
	partBearing()
	partWaypoints()
	partTable()
	partDatacenter()
}
