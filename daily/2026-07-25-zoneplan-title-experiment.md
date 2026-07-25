# Global Meeting Planner: a one-variable SEO experiment

On 2026-07-25, ZonePlan reached 2,120 Search Console impressions but still had only 2 clicks. The strongest non-brand queries were:

| Query | Clicks | Impressions |
|---|---:|---:|
| global meeting planner | 0 | 74 |
| international meeting planner | 0 | 74 |
| world meeting planning | 0 | 59 |
| meeting planner time and date | 0 | 54 |
| international meeting schedule | 0 | 52 |

## What changed

Only one SEO variable changed: the title of the [Global Meeting Planner](https://zoneplan.net/global-meeting-planner/) page.

Old title: `Global Meeting Planner 2026 - Find the Best Time Across Time Zones`

New title: `Global Meeting Planner - Find the Best Time Worldwide`

The page content, H1, description, schema, and tool interaction were deliberately left unchanged. This keeps the experiment interpretable.

## Why this variable

The page is already receiving impressions for the exact phrase `global meeting planner`, but no clicks. The new title keeps that phrase at the front, removes an unnecessary year, and adds a clearer worldwide-use benefit.

## Live verification

- Production page: https://zoneplan.net/global-meeting-planner/
- HTTP status after deployment: 200
- Git commit: https://github.com/Gavin1901/zoneplan/commit/53acc5960f2fe2b81e5649c58bffd98d3b6f1517
- Cloudflare deployment workflow: https://github.com/Gavin1901/zoneplan/actions/runs/30154910196

## Competitor pattern notes

Live checks showed that established tools emphasize either instant comparison or finding a meeting time:

- World Time Buddy: comparison at a glance and best-time scheduling.
- Timeanddate Meeting Planner: meeting planning is the core task, though the automated request returned HTTP 403.
- Every Time Zone: visual global time comparison.
- SavvyCal: developer-facing time-zone infrastructure rather than a direct meeting-planner SERP substitute.

The test will be reviewed after enough Search Console data accumulates. IndexNow submission is only a discovery signal, not proof of Google indexing or ranking.
