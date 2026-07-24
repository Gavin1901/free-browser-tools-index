# 2026-07-24 Root-Cause Repair and Pinterest Backlinks

## Why this second pass was necessary

The first pass proved that all eight sites were alive and that ZonePlan had a serious indexation gap. The second pass repaired the operating system behind the work instead of only publishing more links.

## Repaired system faults

1. The Obsidian single-source file was full historical mojibake. It was backed up and rebuilt as a clean operating entry.
2. `gsc_8sites_scrape.py` now waits and retries when GavinBuilds Chrome CDP 9223 is not ready, instead of failing on the first HTTP 502.
3. The GSC script now extracts the visible top-query rows and writes them to a separate JSON evidence file.
4. `devto_publish.py` now matches CDP responses by request ID so asynchronous browser events cannot be mistaken for a publication response.

## Query-level evidence

ZonePlan's visible top queries show that the site has search demand but almost no non-brand clicks:

| Query | Clicks | Impressions |
|---|---:|---:|
| global meeting planner | 0 | 70 |
| international meeting planner | 0 | 69 |
| world meeting planning | 0 | 54 |
| meeting planner time and date | 0 | 50 |
| international meeting schedule | 0 | 48 |
| meeting planner | 0 | 47 |
| meeting planner worldwide | 0 | 46 |
| world clock meeting planner | 0 | 45 |
| meeting time planner | 0 | 37 |

Machine evidence:

`logs/2026-07-24-gsc-visible-top-queries.json`

## New external-domain backlinks

### 1. Meeting-across-time-zones guide

Public Pin:

https://www.pinterest.com/pin/1097893215436896360/

Destination:

https://zoneplan.net/blog/schedule-meeting-across-time-zones/?utm_source=Pinterest&utm_medium=organic

Verification:

1. Public Pin returns HTTP 200.
2. The Pin page contains a clickable destination link.
3. The destination points to the deep guide, not only the homepage.

### 2. Global meeting planner query page

Public Pin:

https://www.pinterest.com/pin/1097893215436896448/

Destination:

https://zoneplan.net/global-meeting-planner/?utm_source=Pinterest&utm_medium=organic

Verification:

1. Public Pin returns HTTP 200.
2. The Pin page contains a clickable destination link.
3. The destination directly matches the highest-impression non-brand query visible in GSC.

## Medium root cause and repair

Medium was not blocked by the account or by a platform publication limit.

The actual cause was the automation method. Injecting a complete article by directly replacing editor DOM state or sending one oversized synthetic input event caused Medium's draft backend to reject the story with:

`Something is wrong and we cannot save your story.`

A clean draft was created and filled through native keyboard events, one paragraph at a time. Every paragraph retained the visible `DraftSaved` state and no failed Medium network response was observed.

Published article:

https://medium.com/@lg695101011/zoneplan-indexing-experiment-what-1-950-impressions-revealed-17775f5374d5

Verification:

1. Medium displayed the published public story.
2. The page title and article body were visible.
3. The canonical URL matched the public `@lg695101011` article.
4. The article contained clickable links to:
   1. https://zoneplan.net/global-meeting-planner/
   2. https://zoneplan.net/blog/schedule-meeting-across-time-zones/
   3. https://zoneplan.net/

## Strict conclusion

Three new backlinks were published across Pinterest and Medium. The query-led links target `global meeting planner`, the strongest visible non-brand ZonePlan query. All three public pages were verified in the logged-in GavinBuilds browser, and each contained a clickable ZonePlan destination.
