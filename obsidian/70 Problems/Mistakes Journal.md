---
tags: [problems, dashboard]
---
# ❌ Mistakes Journal

Every wrong answer is data. Log it with the Problem template, tag the mistake type.

Mistake types: `#arithmetic-slip`, `#misread`, `#concept-gap`, `#wrong-method`, `#notation`.

```dataview
TABLE source, mistake, resolved
FROM "70 Problems"
WHERE mistake
SORT file.ctime DESC
```
