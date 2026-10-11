---
tags: [meta, dashboard]
---
# Status Board

Overview of every progress note. The Dataview tables below build the board.
To use a card layout, install the **Kanban** community plugin and convert this note.

## Course Levels
```dataview
TABLE status, confidence, started, finished
FROM "10 Course"
WHERE level
SORT level ASC
```

## Tracks
```dataview
TABLE status, confidence, started
FROM "20 Tracks"
WHERE track
SORT status DESC, file.name ASC
```

## Workshops
```dataview
TABLE status, started, finished
FROM "30 Workshops"
WHERE workshop
SORT file.name ASC
```

## Counts
```dataview
TABLE length(rows) AS notes
FROM "10 Course" OR "20 Tracks" OR "30 Workshops" OR "60 Concepts"
WHERE status
GROUP BY status
```
