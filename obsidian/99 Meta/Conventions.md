---
tags: [meta]
---
# Conventions

- **Status:** `not-started`, `in-progress`, `review`, `done`, `parked`.
- **Confidence, from 0 to 5:**
  - 0: never seen it.
  - 1: recognize it.
  - 2: can follow a worked example.
  - 3: can solve standard problems.
  - 4: can solve unfamiliar problems.
  - 5: can teach it.
- **Spaced review:** this follows the [study plan](https://caseyaedwards.github.io/math_training/docs/STUDY_PLAN/).
  After learning a concept, set `next_review` to one day out.
  After a good review, extend it to one week, then one month.
  After a failed review, reset it to one day.
- **Links to material:** point at the [course website](https://caseyaedwards.github.io/math_training/), for example
  `[Place Value](https://caseyaedwards.github.io/math_training/course/101/01-place-value-and-the-number-line/)`.
  Obsidian cannot open relative links outside the vault, so links use full URLs.
  The `material` property on each progress note holds the page address.
- **Diagrams:** browse every diagram with its steps in the [diagram showcase](https://caseyaedwards.github.io/math_training/diagrams/).
  To keep one in a note, copy the SVG file into `50 Resources/attachments/` and embed it with `![[file.svg]]`.
- **Math:** Obsidian renders LaTeX. Use `$a^2+b^2=c^2$` inline and `$$\int_0^1 x\,dx$$` for a block.
- **Tags:** `#stuck`, `#aha`, `#revisit`, `#proof`, `#visual`.
