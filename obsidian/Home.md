---
tags: [dashboard]
---
# 🏠 Home

> Material lives in the repo; this vault tracks **me**.

## Today
- Open today's note: `Ctrl/Cmd+P` → *Daily notes: Open today's daily note*
- [[Status Board]] · [[Goals]] · [[Conventions]]

## Where I am
- **Course:** [[Course Overview]]
- **Tracks:** [[Tracks Overview]]
- **Workshops:** [[Workshops Overview]]
- **History:** [[History Overview]]
- **Reading:** [[Reading Log]]

## In progress
```dataview
TABLE status, confidence, next_review
FROM "10 Course" OR "20 Tracks" OR "30 Workshops"
WHERE status = "in-progress" OR status = "review"
SORT file.mtime DESC
```

## Due for review
```dataview
TABLE confidence, next_review
FROM "60 Concepts" OR "10 Course" OR "20 Tracks"
WHERE next_review AND next_review <= date(today)
SORT next_review ASC
```

## Low-confidence concepts
```dataview
LIST "confidence " + confidence
FROM "60 Concepts"
WHERE confidence < 3
SORT confidence ASC
LIMIT 15
```

## Recent study days
```dataview
TABLE minutes, focus
FROM "01 Daily"
SORT file.name DESC
LIMIT 7
```

## Open questions
```dataview
LIST
FROM "80 Questions"
WHERE status != "answered"
```
