---
tags: [resources, dashboard]
---
# Reading Log

Write one note per resource from the Resource template. Old-school university pages are welcome.

```dataview
TABLE kind, status, rating, finished
FROM "50 Resources"
WHERE kind
SORT status ASC, rating DESC
```
