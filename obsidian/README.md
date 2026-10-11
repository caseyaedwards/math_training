# Math Training Vault

This folder is an [Obsidian](https://obsidian.md) vault for tracking my own progress.
The learning material lives in the rest of this repository: course, tracks, workshops, SVG diagrams, history and resources.
Notes here link to that material on GitHub.

## Open the Vault

1. In Obsidian, click **Open folder as vault** and select `math_training/obsidian/`.
2. Open **Settings > Community plugins**, turn them on, and install **Dataview**.
   The dashboards use Dataview. Without it, every note still works as plain Markdown.
3. Open [[Home]].

## Layout

| Folder | What goes in it |
|---|---|
| `00 Inbox/` | Quick captures. Sort them weekly |
| `01 Daily/` | One note per study day, from the Daily template |
| `02 Weekly/` | Weekly review, from the Weekly Review template |
| `10 Course/` | One progress note per course level: 101, 201, etc |
| `20 Tracks/` | One progress note per topic track: Number Theory, etc |
| `30 Workshops/` | Real-world application workshops |
| `40 History/` | Notes while reading the History of Math |
| `50 Resources/` | Reading log for books, lecture notes and old-school university pages |
| `60 Concepts/` | One card per concept in my own words, with a confidence score |
| `70 Problems/` | Problem log and mistakes journal |
| `80 Questions/` | Open questions I want answered |
| `90 Templates/` | Note templates. The core Templates plugin reads from here |
| `99 Meta/` | Goals, status board, conventions |

## Status Conventions

Every progress note has YAML properties:

```yaml
status: not-started | in-progress | review | done | parked
confidence: 0-5        # 0 = never seen, 3 = can do it, 5 = can teach it
started:               # YYYY-MM-DD
finished:              # YYYY-MM-DD
next_review:           # YYYY-MM-DD, for spaced repetition
```

Git ignores `.obsidian/workspace*.json` and caches. Shared settings are committed.
