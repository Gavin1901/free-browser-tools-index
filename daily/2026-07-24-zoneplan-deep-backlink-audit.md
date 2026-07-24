# 2026-07-24 ZonePlan Deep Backlink Audit

Target: https://zoneplan.net/blog/schedule-meeting-across-time-zones/

| Channel | Public URL | HTTP | Target visible | Clickable |
|---|---|---:|---:|---:|
| GitHub daily | https://github.com/Gavin1901/free-browser-tools-index/blob/master/daily/2026-07-24-zoneplan-deep-backlinks.md | 200 | yes | yes |
| Public Gist | https://gist.github.com/Gavin1901/ff5e2cc4dfee2627c0bfb3819f374c50 | 200 | yes | yes |
| Index issue | https://github.com/Gavin1901/free-browser-tools-index/issues/16 | 200 | yes | yes |
| ZonePlan issue | https://github.com/Gavin1901/zoneplan/issues/3 | 200 | yes | yes |
| Dev.to | https://dev.to/gavinbuildsai/why-1950-google-impressions-produced-only-2-clicks-149e | 200 | yes | yes |

## Strict result

5 public pages return HTTP 200 and contain a clickable deep link to the target guide.

The GitHub daily page is the public evidence note and also a crawl path. The Gist, two issues, and Dev.to article are separate public URLs.

## Self-audit findings

1. ZonePlan has 1,950 impressions but only 2 clicks, CTR 0.1%, average position 44.7.
2. GSC reports only 4 indexed pages and 89 not indexed. IndexNow 200 is discovery evidence, not Google indexation proof.
3. The current GSC scraper captures site totals but not query-level and page-level exports. That limits exact keyword selection.
4. The first GSC run failed because CDP 9223 was not ready and returned HTTP 502. The script lacks a readiness retry and later exceeded the shell timeout even though it eventually finished.
5. The first Dev.to verification script published successfully but printed unknown values because it did not match CDP responses by request id. Publication had to be reverified from the live public URL.
6. Four of five backlinks are in the GitHub ecosystem. The daily quantity gate is met, but domain diversity is still weak.
7. The vault unique-total file is mojibake and must not be treated as a healthy truth source until repaired from a clean backup.

## Root cause judgment

The biggest problem is not that the sites are down. The infrastructure is healthy. The real bottlenecks are weak Google index coverage, average positions outside page one, low CTR, insufficient query/page-level diagnosis, and repetitive backlink domains.
