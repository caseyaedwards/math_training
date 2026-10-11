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
- **Spaced review:** after a session, set `next_review` to one day out.
  After each easy review, extend it to three, seven, 21 and then 60 days.
  After a hard review, reset it to one day.
- **Links to material:** point at the repository on GitHub, for example
  `[Lesson 101](https://github.com/caseyaedwards/math_training/tree/main/course/101)`.
  Obsidian cannot open relative links outside the vault, so links use GitHub URLs.
  The paths are placeholders until that content exists.
- **Diagrams:** copy SVG files from the generator into `50 Resources/attachments/` and embed
  them with `![[file.svg]]`, or link to the showcase on GitHub.
- **Math:** Obsidian renders LaTeX. Use `$a^2+b^2=c^2$` inline and `$$\int_0^1 x\,dx$$` for a block.
- **Tags:** `#stuck`, `#aha`, `#revisit`, `#proof`, `#visual`.
