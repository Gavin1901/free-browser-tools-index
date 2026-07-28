# 2026-07-28 AI Tool Indexing Maintenance

Run time: 2026-07-28 07:38:20

## Live checks and IndexNow

| Site | Home | Robots | Sitemap | URLs submitted | IndexNow |
|---|---:|---:|---:|---:|---:|
| [iworkviewer.com](https://iworkviewer.com/) | 200 | 200 | 200 | 20 | 200 |
| [livephotokit.com](https://livephotokit.com/) | 200 | 200 | 200 | 20 | 200 |
| [plantingcalendar.net](https://plantingcalendar.net/) | 200 | 200 | 200 | 20 | 200 |
| [freetdee.com](https://freetdee.com/) | 200 | 200 | 200 | 20 | 200 |
| [babypercent.com](https://babypercent.com/) | 200 | 200 | 200 | 20 | 200 |
| [invoicepad.net](https://invoicepad.net/) | 200 | 200 | 200 | 20 | 200 |
| [zoneplan.net](https://zoneplan.net/) | 200 | 200 | 200 | 20 | 200 |
| [pupvax.com](https://pupvax.com/) | 200 | 200 | 200 | 20 | 200 |

## Public links

- [iworkviewer.com](https://iworkviewer.com/)
- [livephotokit.com](https://livephotokit.com/)
- [plantingcalendar.net](https://plantingcalendar.net/)
- [freetdee.com](https://freetdee.com/)
- [babypercent.com](https://babypercent.com/)
- [invoicepad.net](https://invoicepad.net/)
- [zoneplan.net](https://zoneplan.net/)
- [pupvax.com](https://pupvax.com/)

This daily note creates a public crawl path and records the indexing maintenance work for the eight tool sites.

## Cross-validation audit

### Homepage SEO checks

All eight live homepages were re-read on 2026-07-28.

- HTTP status: 8/8 returned 200.
- Title: 8/8 present.
- Meta description: 8/8 present.
- H1: 8/8 present.
- Canonical: 8/8 present and matched the production homepage.
- Noindex: 0/8.
- HTML language: 8/8 set to `en`.
- GA tag: 8/8 detected.
- AdSense tag: 8/8 detected.
- JSON-LD: all detected blocks parsed successfully.

Machine evidence: `logs/2026-07-28-home-seo-audit.json`.

### Deployment checks

The latest `Deploy to Cloudflare Pages` workflow run for each of the eight site repositories was checked through GitHub. All eight latest runs were completed with `success`.

This confirms the latest recorded deployments passed. It does not claim that a new deployment occurred on 2026-07-28 because no site source code was changed today.

### GSC boundary

The GSC collection script was run again, but GavinBuilds Chrome CDP port 9223 was not ready after 12 attempts and timed out. Therefore no fresh 2026-07-28 GSC clicks, impressions, CTR, ranking, query, or page data is reported.

### Manual platform scan

The current action-camp manual was re-extracted and 157 unique HTTP(S) entries were checked:

| Result | Count |
|---|---:|
| HTTP 200 | 83 |
| HTTP 403 | 42 |
| HTTP 404 | 9 |
| Request error | 14 |
| HTTP 429 | 1 |
| Other HTTP errors | 8 |
| Total | 157 |

An accessible URL is not publication proof. Many entries are login pages, paid services, ordinary reference pages, closed services, or platforms that do not accept this product type.

Machine evidence: `logs/2026-07-28-manual-platform-live-scan.json`.

## Browser publishing recovery

The Chrome extension control path was repaired and the currently selected Chrome profile was verified platform by platform before any write action.

### Published and verified

- Dev.to:
  https://dev.to/gavinbuilds/tdee-vs-bmr-vs-macros-a-practical-starting-point-4m7h
- Author route: `gavinbuilds`.
- Public page and title were visible.
- The article contains a clickable `https://freetdee.com/` link.

### Duplicate cleanup

The duplicate PlantingCalendar Pinterest Pin `1097893215437125297` was deleted from the Gavin Builds account. Pinterest redirected to the `Free Online Tools` board after confirmation. The retained Pin is:

https://www.pinterest.com/pin/1097893215437125765/

### Fresh GSC evidence

ZonePlan Search Console was read live. The selected account had property access.

- Last update: 6 hours ago.
- Total clicks: 2.
- Total impressions: 2,670.
- CTR: 0.1%.
- Average position: 45.8.
- Indexed pages: 30.
- Not indexed pages: 84.

Top visible queries:

| Query | Clicks | Impressions |
|---|---:|---:|
| zoneplan | 2 | 16 |
| international meeting planner | 0 | 91 |
| global meeting planner | 0 | 87 |
| world meeting planning | 0 | 73 |
| international meeting schedule | 0 | 64 |
| meeting planner time and date | 0 | 62 |
| meeting planner worldwide | 0 | 57 |
| meeting planner | 0 | 56 |
| meeting time planner | 0 | 48 |
| world clock meeting planner | 0 | 46 |

The existing `global-meeting-planner` and `international-meeting-planner` pages already use exact-match titles and H1s. No second page variable was changed during the active experiment window.

### Platform boundaries verified in the browser

- Medium was logged in as `Gold Risk Notes`, not the approved Gavin Builds publishing identity. No AI-tool article was posted there.
- Quora was logged in as `Gold Risk Notes`, while the duplicate posts belong to `Gan Liu`. The account menu offered no switch to Gan Liu, so the posts could not be safely deleted.
- SaaSHub was logged out and returned: `Please register to submit more than one product.`
- Paid platforms, dead services, non-product reference pages, and incompatible directories were not falsely counted as publishable platforms.

## Data-driven page refinement

The highest visible non-brand ZonePlan query was `international meeting planner` with 91 impressions and 0 clicks. One search-snippet variable was changed on the exact target page:

- Page: https://zoneplan.net/international-meeting-planner/
- Variable: meta description only.
- Previous: `Free international meeting planner for cross-border calls. Compare countries, cities, daylight saving time, and working-hour overlap.`
- New: `Find the best time for international meetings. Compare working-hour overlap, local dates and DST in one free planner—no sign-up required.`
- Commit: `43205af`.
- Local production build: passed.
- Changed-file ESLint: passed.
- Full repository ESLint: failed on 72 pre-existing errors outside the changed file; this was not hidden.
- GitHub Actions `Deploy to Cloudflare Pages`: completed with success.
- Live page: HTTP 200 and the new description is visible.
- Canonical: `https://zoneplan.net/international-meeting-planner/`.
- IndexNow resubmission: HTTP 200.

Only the description changed. Title, H1, body, tool interaction and canonical were held constant so the next GSC review can attribute any CTR movement to one primary variable.

## Additional action-manual platform verification

- Hacker News submit page: login required.
- Product Hunt new-product route: redirected to login.
- SaaSHub remaining products: registration/login required for more than one submission.
- Medium selected identity: `Gold Risk Notes`, not the approved AI-outbound identity.
- Quora selected identity: `Gold Risk Notes`; the duplicate Gan Liu posts are not editable by the selected identity.

No password, OAuth, payment or identity action was fabricated. These states are platform terminal states, not publication successes.
