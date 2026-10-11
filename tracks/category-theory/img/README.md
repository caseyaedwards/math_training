# Category Theory Diagrams

Hand-authored SVG diagrams for the [Category Theory Track](../README.md), listed in the order they appear:

* [concept-map.svg](concept-map.svg): Category Theory Concept Map.
* [commuting-square.svg](commuting-square.svg): A commuting square, two paths with one answer.
* [cities-and-go-types.svg](cities-and-go-types.svg): Objects and arrows as towns and roads, and as Go types and funcs.
* [composition-pipe.svg](composition-pipe.svg): Composition as g after f, and a Unix pipe as one composed arrow.
* [identity-and-associativity.svg](identity-and-associativity.svg): Identity loops and the associativity law.
* [sets-and-functions.svg](sets-and-functions.svg): Functions between three finite sets and their composite.
* [isomorphism-round-trip.svg](isomorphism-round-trip.svg): A bijection with its inverse, beside a function that has no inverse.
* [functor-slices.svg](functor-slices.svg): The slice functor sending types to slice types and funcs to Map.
* [naturality-first.svg](naturality-first.svg): Naturality square for First with sample values.
* [product-pair.svg](product-pair.svg): Product with projections and the unique pairing arrow.
* [coproduct-either.svg](coproduct-either.svg): Coproduct with injections and the unique case arrow.
* [terminal-and-initial.svg](terminal-and-initial.svg): Terminal and initial objects in sets.
* [currying.svg](currying.svg): A two-input function as a table and as a function that returns rows.
* [monad-railway.svg](monad-railway.svg): Chaining steps that can fail, with an error track.

The generator script that computed the coordinates is kept outside this repository. Every embed in the track README carries a `<!-- diagram: ... -->` spec comment for regeneration.
