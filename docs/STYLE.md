# Writing Style

All material in this repository follows the [Axibase technical writing guide](https://axibase.com/use-cases/workshop/technical-writing.html), adapted for math.

## Voice

* Use active voice and present tense. Avoid `will`, `should`, `could`, `would`, `may`.
* Address the reader directly or use the imperative: `Multiply both sides by 3.`
* Replace contractions with the full form: `do not`, `is not`.
* Replace `e.g.` and `i.e.` with `for example` and `that is`.
* Do not join independent clauses with a comma. Use two sentences.
* Avoid filler: `in order to` becomes `to`, `make sure` becomes `ensure`. Do not use `please`, `lets`, `a lot`, `robust`, `so` as a connector.
* Avoid possessives and quotation marks where practical. Use bold for terms on first definition.

## Numbers and Units

* Write numbers one through ten in words in prose, unless they carry a unit or are part of math.
* Inside math, always use digits: `3 + 4 = 7`.
* Add thousands separators: `1,024`. Put a space before multi-letter units: `8 GB`, `9.8 m/s²`. No space for one-letter units: `10%`.

## Headings and Formatting

* Use title case in headings. No trailing periods, no backticks in headings.
* Begin lists with a colon. Separate a list label from its content with a colon.
* Fence code with a dialect: `python`, `go`, `txt` for ASCII diagrams and machine output.
* Use relative links between Markdown files in this repository.
* Link text describes the target. Never `click here`.

## Math Notation

* GitHub renders LaTeX between `$...$` and `$$...$$`. Use it for anything beyond simple arithmetic.
* Show every step of a worked example on its own line, with the reason on the right:

```txt
  3x + 5 = 20
  3x     = 15      subtract 5 from both sides
   x     = 5       divide both sides by 3
```

## Diagrams

The reader is a visual learner. Every new idea gets a picture.

* Put SVG files next to the lesson in an `img/` folder and embed them: `![Number line from -5 to 5](img/number-line.svg)`.
* Hand-drawn SVG is fine until the generator in `svg/` (built in a separate thread) can render it.
  Above each embed, add a generator spec comment so the figure can be regenerated later:
  `<!-- diagram: type=number-line range=-5..5 marks=-3,2 caption="..." -->`
* Small sketches can be ASCII art in a `txt` block.
* Keep SVGs simple: white background, black or dark-gray strokes, one accent color (`#d9480f`), 14 px sans-serif labels, `viewBox` set, no external fonts or scripts.
