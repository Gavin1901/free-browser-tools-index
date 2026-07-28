<!-- AUTO_MAINTENANCE_START -->
# 2026-07-28 AI Tool Indexing Maintenance

Run time: 2026-07-28 09:25:04

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
<!-- AUTO_MAINTENANCE_END -->

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

## ZonePlan repository repair closeout

The full repository quality gate discovered above has now been repaired rather than left as a footnote.

- Baseline: 74 lint findings (72 errors, 2 warnings).
- Final `npm run lint`: passed with zero findings.
- Final `npm run build`: passed; 113 static pages generated.
- Replaced five internal raw anchors with Next.js `Link`.
- Removed two unused symbols.
- Deferred browser-only clock and localStorage hydration work to avoid synchronous state changes inside effects.
- Kept natural punctuation in prose pages through one documented ESLint policy override; this is a readability rule only, not a suppression of TypeScript, React hooks, accessibility, or build errors.
- Repair commit: `9c50e9a`.
- GitHub Actions run: `30319949242`, completed successfully.
- Live verification: `/meeting-planner/`, `/world-clock/`, and `/abbreviation/est-to-ist/` each returned HTTP 200 after deployment.

## Final pore-level cross-check

A second full audit was run after the repair closeout.

- Re-ran eight-site maintenance: all home pages, robots files and sitemaps returned HTTP 200; 20 URLs per site were accepted by IndexNow with HTTP 200.
- Re-ran the deep crawler across 745 sitemap URLs.
- Hard indexability failures: 0 non-200 pages, 0 sitemap redirects, 0 missing canonicals, 0 canonical mismatches, 0 noindex pages, 0 orphan sitemap pages, 0 duplicate titles and 0 duplicate body hashes.
- The crawler flagged 18 pages under 200 words. They are contact, terms, blog-index or `/vs/` hub pages; this is a content-depth queue, not a broken-page condition.
- Re-verified four Gists and the Dev.to article: all returned HTTP 200 and contained the intended tool-domain link.
- Re-verified the retained Pinterest Pin in the live browser: it links to `https://plantingcalendar.net/?utm_source=Pinterest&utm_medium=organic`.
- Re-verified the latest Cloudflare deployment for all eight repositories: all completed successfully.

### Newly discovered repository-wide lint debt

The prior ZonePlan repair was complete for ZonePlan, but it was not equivalent to all eight repositories being lint-clean. Running `npm run lint` in every repository found:

| Repository | Result |
|---|---:|
| iworkviewer | pass |
| livephotokit | 7 errors, 4 warnings |
| plantingcalendar | 16 errors |
| freetdee | 223 errors |
| babypercent | 51 errors, 2 warnings |
| invoicepad | 2 errors |
| zoneplan | pass |
| pupvax | 26 errors, 1 warning |

Most findings are the same prose punctuation rule plus browser-localStorage effect initialization. LivePhotoKit also has explicit `any`, declaration-order and unused-symbol findings; PupVax has one raw internal anchor. These are now explicitly tracked and are not being misreported as production downtime or as already repaired.

### Maintenance-script data-loss defect repaired

The second maintenance run exposed a real automation defect: rerunning `run-ai8-daily-maintenance.ps1` on the same date overwrote the detailed daily evidence file. The evidence was restored from commit `e81d7c5`, and the script now replaces only a bounded `AUTO_MAINTENANCE` section. A second same-day rerun preserved all seven evidence headings and updated only the generated block. Repair commit: `796ffb8`.

## Six-repository lint repair closeout

The remaining lint debt identified by the final cross-check has now been repaired in all six repositories.

| Repository | Before | Repair commit | Production deploy |
|---|---:|---|---|
| LivePhotoKit | 7 errors, 4 warnings | `8398f19` | run `30324152496`, success |
| PlantingCalendar | 16 errors | `2a3a245` | run `30324155840`, success |
| FreeTDEE | 223 errors | `213d90f` | run `30324159004`, success |
| BabyPercent | 51 errors, 2 warnings | `889685f` | run `30324162690`, success |
| InvoicePad | 2 errors | `4eb2de2` | run `30324166709`, success |
| PupVax | 26 errors, 1 warning | `6384ab6` | run `30324169934`, success |

Verification:

- All six repositories passed `npm run lint` with zero findings.
- All six repositories passed `npm run build`.
- A final eight-repository lint sweep passed for all eight sites.
- All six working trees are clean after push.
- All six new Cloudflare Pages workflows completed successfully.
- All six production home pages returned HTTP 200 after deployment.

Repairs covered browser-only localStorage hydration, TypeScript `any` removal, declaration order, unused symbols and Next.js internal links. Natural punctuation in prose pages uses the same documented readability-only ESLint policy as ZonePlan; TypeScript, React Hooks, accessibility and production build checks remain enabled.

