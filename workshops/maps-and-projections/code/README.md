# Code

Go standard library only. Tested with Go 1.27.2. Each program is one `main.go` in its own folder, needs no arguments, and finishes in well under a second. Run them from the workshop folder (the one holding `go.mod`).

| Program | Run | Prints |
|---|---|---|
| [great-circle](great-circle/main.go) | `go run ./code/great-circle` | JFK to LHR by 3D dot product, haversine, and the spherical law of cosines (5,540 km); initial bearings; waypoints along the great circle with a latitude bar chart; a distance table among seven airports; the nearest datacenter region per airport with a fiber round-trip-time floor |
| [mercator](mercator/main.go) | `go run ./code/mercator` | Mercator and equirectangular y for latitudes 0 to 85; an ASCII side-by-side grid of latitude lines; scale factor sec φ and area factor sec² φ as bars; Greenland versus Africa; a midpoint-sum check that Mercator y is the integral of sec |

From inside a program folder, `go run .` works too.

## Data Notes

* Airport coordinates are airport reference points rounded to two decimals, north and east positive.
* Datacenter coordinates are the metro areas of typical cloud regions (Northern Virginia, Oregon, Dublin, Tokyo, Singapore), rounded to two decimals. They are approximate on purpose: the exact building locations are not public.
* Distances use a spherical Earth with mean radius 6,371 km. Survey-grade work uses the WGS 84 ellipsoid instead.
