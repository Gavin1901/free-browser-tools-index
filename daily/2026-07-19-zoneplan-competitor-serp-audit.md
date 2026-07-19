# 2026-07-19 ZonePlan competitor and SERP audit

Target page: https://zoneplan.net/utc-meeting-planner/
Target intent: free UTC meeting planner for distributed teams.
GSC 28-day baseline: 2 clicks, 1,390 impressions, 0.1% CTR, average position 44.7. Index coverage: 4 indexed, 89 not indexed.

## Search-result competitors reviewed

| Competitor | Search-result value proposition | Useful pattern | ZonePlan gap |
|---|---|---|---|
| https://timesheet.io/en/tools/time-zone-meeting-planner | Multi-city local-time table plus date rollover | Immediate interactive table | UTC guide needs a direct interactive planner above the fold |
| https://www.mytimezoneplanner.com/ | Best-window chips expressed in UTC | Ranked overlap suggestions | ZonePlan does not rank suggested slots on the UTC page |
| https://koalendar.com/tools | Tool hub, converter and scheduling utilities | Strong hub-and-spoke internal linking | ZonePlan has tools but the UTC page was previously weakly linked |
| https://freetoolly.com/en/tools/meeting-planner | 24-hour comparison grid | Full-day visual scan | ZonePlan guide is mostly text and lacks a 24-hour grid on this route |
| https://capitalcova.com/date-time/time-zone-meeting-planner | Exact-match tool title and direct utility | Tight query-intent match | ZonePlan title is relevant but page utility is indirect |
| https://zonecross.com/ | Unlimited zones, scored slots, DST handling | Clear differentiators and no-account promise | ZonePlan needs stronger benefit bullets and share/export behavior |
| https://www.8apps.co/free-tools/timezone-meeting-planner/ | Multi-zone meeting utility | Simple task-oriented route | ZonePlan can improve task completion speed |
| https://theutilitykit.com/tools/timezone-planner | Timeline visualization and DST positioning | Visual overlap metaphor | ZonePlan UTC page needs a visual layer, not only examples |

## Single-variable decision

Do not redesign the tool today. The one variable changed on 2026-07-19 is internal discoverability: the main `/meeting-planner/` hub now links directly to `/utc-meeting-planner/` with descriptive anchor text.

Why this variable: GSC shows only 4 indexed and 89 not indexed URLs for zoneplan.net. Before adding more content, strengthen crawl paths from an established hub.

Commit: https://github.com/Gavin1901/zoneplan/commit/26f0d5f

## Seven-day acceptance

Review on 2026-07-26:

1. Whether `/utc-meeting-planner/` appears in GSC page data.
2. Whether indexed count rises above 4.
3. Whether the target page gains impressions.
4. Whether zoneplan.net CTR rises above the 0.1% baseline.
5. Keep this internal-link variable isolated until the review.
