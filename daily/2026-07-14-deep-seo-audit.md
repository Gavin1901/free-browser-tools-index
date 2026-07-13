# 2026-07-14 AI 8 Sites Deep SEO Audit Corrected

This corrected page fixes the earlier markdown encoding noise and separates live-site status from local source fixes.

| Site | Home | Robots | Sitemap | URLs | Title length | Description length | Canonical | Noindex | GA4 | AdSense | Verdict | Issue |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---|
| iworkviewer.com | 200 | 200 | 200 | 51 | 69 | 124 | https://iworkviewer.com/ | NO | YES | YES | PASS |  |
| livephotokit.com | 200 | 200 | 200 | 27 | 52 | 153 | https://livephotokit.com/ | NO | YES | YES | PASS |  |
| plantingcalendar.net | 200 | 200 | 200 | 365 | 64 | 130 | https://plantingcalendar.net/ | NO | YES | YES | PASS |  |
| freetdee.com | 200 | 200 | 200 | 43 | 54 | 148 | https://freetdee.com/ | NO | YES | YES | PASS |  |
| babypercent.com | 200 | 200 | 200 | 35 | 71 | 133 | https://babypercent.com/ | NO | YES | YES | REVIEW | live_title_len_review |
| invoicepad.net | 200 | 200 | 200 | 29 | 69 | 145 | https://invoicepad.net/ | NO | YES | YES | PASS |  |
| zoneplan.net | 200 | 200 | 200 | 92 | 56 | 143 | https://zoneplan.net/ | NO | YES | YES | PASS |  |
| pupvax.com | 200 | 200 | 200 | 36 | 61 | 145 | https://pupvax.com/ | NO | YES | YES | PASS |  |

## Second pass findings

1. The eight homepages are live and not blank in Chrome CDP visual checks.
2. IndexNow submitted 20 URLs per site today.
3. The only live SEO review item is BabyPercent homepage title length. The live title is still 71 characters.
4. BabyPercent local source was shortened and `npm run build` passed, but no deploy entry was found, so the live site is not claimed as fixed.
5. GSC `/u/1` can open all eight domain properties, but overview metrics did not appear reliably in the captured text, so new 8-site clicks and impressions are not reported.
6. GA still returns `ERR_CONNECTION_CLOSED` and remains not reportable.

## Optimization completed in this second pass

1. Corrected the public deep SEO audit markdown encoding noise.
2. Added a second-pass review page with clear done and not-done boundaries.
3. Fixed the GSC automation approach enough to prove all eight GSC properties open under `/u/1`.
4. Kept the BabyPercent title fix as local-built-only until deployment is found.
