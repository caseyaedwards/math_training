# Math Training vault

This folder is an [Obsidian](https://obsidian.md) vault for **tracking my own progress**.
The learning material itself (course, tracks, workshops, SVG diagrams, history, resources)
lives in the rest of this repo; notes here link out to it.

## Open it

1. Obsidian → *Open folder as vault* → pick `math_training/obsidian/`.
2. Settings → Community plugins → turn on, then install **Dataview** (optional but the
   dashboards use it). Everything still works as plain Markdown without it.
3. Open [[Home]].

## Layout

| Folder | What goes in it |
|---|---|
| `00 Inbox/` | Quick captures; sort them weekly |
| `01 Daily/` | One note per study day (template: Daily) |
| `02 Weekly/` | Weekly review (template: Weekly Review) |
| `10 Course/` | One progress note per course level (101, 201, ...) |
| `20 Tracks/` | One progress note per topic track (Number Theory, ...) |
| `30 Workshops/` | Real-world application workshops |
| `40 History/` | Notes while reading the History of Math |
| `50 Resources/` | Reading log for books, lecture notes, old-school university pages |
| `60 Concepts/` | One card per concept *in my own words*, with a confidence score |
| `70 Problems/` | Problem log and mistakes journal |
| `80 Questions/` | Open questions I want answered |
| `90 Templates/` | Note templates (core Templates plugin is pointed here) |
| `99 Meta/` | Goals, status board, conventions |

## Status conventions

Every progress note has YAML properties:

```yaml
status: not-started | in-progress | review | done | parked
confidence: 0-5        # 0 = never seen, 3 = can do it, 5 = can teach it
started:               # YYYY-MM-DD
finished:              # YYYY-MM-DD
next_review:           # YYYY-MM-DD, for spaced repetition
```

Git: `.obsidian/workspace*.json` and caches are ignored, shared settings are committed.
