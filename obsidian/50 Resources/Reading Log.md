---
tags: [resources, dashboard]
---
# Reading Log

Write one note per resource from the Resource template. Old-school university pages are welcome.
The repository keeps a curated list on the [Resources page](https://caseyaedwards.github.io/math_training/resources/) and a [free textbooks list](https://caseyaedwards.github.io/math_training/resources/free-textbooks/).

```dataview
TABLE kind, status, rating, finished
FROM "50 Resources"
WHERE kind
SORT status ASC, rating DESC
```
