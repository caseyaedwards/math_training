---
tags: [dashboard]
---
# Home

The material lives in the repository. This vault tracks my progress.

## Today
- Open the note for today: press `Cmd+P` and run **Daily notes: Open today's daily note**.
- [[Status Board]] · [[Goals]] · [[Conventions]]

## Where I Am
- **Website:** [Math Training](https://caseyaedwards.github.io/math_training/) · [study plan](https://caseyaedwards.github.io/math_training/docs/STUDY_PLAN/) · [diagram showcase](https://caseyaedwards.github.io/math_training/diagrams/)
- **Course:** [[Course Overview]]
- **Tracks:** [[Tracks Overview]]
- **Workshops:** [[Workshops Overview]]
- **History:** [[History Overview]]
- **Reading:** [[Reading Log]]

## In Progress
```dataview
TABLE status, confidence, next_review
FROM "10 Course" OR "20 Tracks" OR "30 Workshops"
WHERE status = "in-progress" OR status = "review"
SORT file.mtime DESC
```

## Due for Review
```dataview
TABLE confidence, next_review
FROM "60 Concepts" OR "10 Course" OR "20 Tracks"
WHERE next_review AND next_review <= date(today)
SORT next_review ASC
```

## Low-Confidence Concepts
```dataview
LIST "confidence " + confidence
FROM "60 Concepts"
WHERE confidence < 3
SORT confidence ASC
LIMIT 15
```

## Recent Study Days
```dataview
TABLE minutes, focus
FROM "01 Daily"
SORT file.name DESC
LIMIT 7
```

## Open Questions
```dataview
LIST
FROM "80 Questions"
WHERE status != "answered"
```
