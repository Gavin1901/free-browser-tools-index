<!-- AUTO_MAINTENANCE_START -->
# 2026-07-29 AI Tool Indexing Maintenance

Run time: 2026-07-29 17:22:59

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

## Live GSC decision

The authorized Search Console account `lg695101011@gmail.com` was read in the browser.

### FreeTDEE

- Clicks: 1
- Impressions: 214
- CTR: 0.5%
- Average position: 45.9
- Leading zero-click queries: `tdee calculator free` (16 impressions), `tdee calculator bodybuilding` (11), `tdee calculator 2026` (8).

The homepage title, description and H1 already match the leading query. No second FreeTDEE page variable was changed.

### PupVax

- Clicks: 1
- Impressions: 364
- CTR: 0.3%
- Average position: 48
- Leading queries: `puppy vaccinations` (24 impressions, 0 clicks), `dog deworming schedule` (20, 0), `dog deworming schedule chart` (10, 0).

The existing deworming page was live and useful, but its title only said “Puppy” while the strongest specific query said “Dog” and “schedule chart.”

## Single-variable page experiment

- Page: https://pupvax.com/puppy-deworming-schedule/
- Changed variable: metadata title only.
- Previous title: `Puppy Deworming Schedule: 2 Weeks to 6 Months`
- New title: `Dog Deworming Schedule Chart: Puppy to Adult (2026)`
- H1, description, body, canonical and URL: unchanged.
- Commit: `e3a3b85`.
- Local lint: passed.
- Local production build: passed; 53 static pages generated.
- Cloudflare Pages run: `30439745244`, success.
- Live page: HTTP 200; new title confirmed after deployment.

## New deep backlinks

Each page returned HTTP 200 and contained the clickable PupVax target link.

1. https://gist.github.com/Gavin1901/4cd3096ace902ed74706f2c95c80e8a1
2. https://gist.github.com/Gavin1901/e63a2f7bdb6cd5778f92fe65251fa19a
3. https://gist.github.com/Gavin1901/73ae9348c33868a881a541b252ac70b3
4. https://github.com/Gavin1901/pupvax/issues/5

The three Gists cover different intents: a puppy-to-adult schedule chart, common puppy worming mistakes, and deworming versus vaccination. The repository issue is the public experiment log.

## Platform sweep

- GitHub/Gist: published and verified.
- Dev.to: published and independently verified:
  https://dev.to/gavinbuilds/dog-deworming-schedule-chart-puppy-to-adult-2026-4f0e
  The public page returned HTTP 200 and contained the clickable PupVax target link.
- Hacker News submit: HTTP 200 page requires login.
- Product Hunt new-product route: HTTP 403 Cloudflare interstitial.
- SaaSHub submit: HTTP 200 but requires login/registration for continued product submissions.
- AlternativeTo: HTTP 403 Cloudflare interstitial; prior product-type restrictions remain.
- Indie Hackers: request timed out; no publish state was proven.
- Medium and Quora: last verified selected identity is `Gold Risk Notes`, so no AI-tool content was sent through that identity.
- Reddit remains isolated to the PGM account line.

IndexNow HTTP 200 means Bing accepted the requests; it does not prove Google indexing.

## Home SEO and deployment verification

- All eight home pages returned HTTP 200.
- Every home page had a non-empty title, description and H1.
- Every canonical matched the HTTPS root domain.
- No home page contained `noindex`.
- GA and AdSense front-end tags were present on all eight home pages.
- All JSON-LD blocks parsed successfully: seven sites had 2/2 valid blocks; PupVax had 3/3.
- The latest Cloudflare Pages workflow for every repository completed successfully.

Machine-readable evidence: `logs/2026-07-29-home-seo-audit.json`.

## Final backlink closeout

- Qualified public backlinks published today: 5.
- GitHub ecosystem: 3 Gists and 1 public issue.
- Independent domain: 1 Dev.to article.
- Medium and Quora were rechecked in the live browser. The selected Medium identity was still `Gold Risk Notes`; no AI-tool content was transmitted through the wrong identity.
- Hacker News was rechecked in the live browser and explicitly required a username/password login.
- Remaining directory/community platforms stayed at their documented login, Cloudflare, timeout, or product-fit terminal states. These states are not counted as publications.

## Second porous cross-audit

The earlier “Medium is the Gold Risk Notes identity” conclusion came from the wrong Chrome profile. Historical logs were re-read before retrying:

- Approved profile: `D:\ChromeProfiles\GavinBuilds`
- CDP port: `9223`
- Approved Medium route: `@lg695101011`

The correct profile was started and verified by navigating `/me`, which resolved to `https://medium.com/@lg695101011`.

### Full 8-site GSC closeout

The repaired historical scraper was run through the correct profile. All eight properties returned live 28-day metrics, top visible queries, and index counts.

| Site | Clicks | Impressions | CTR | Avg. position | Indexed | Not indexed |
|---|---:|---:|---:|---:|---:|---:|
| iworkviewer.com | 48 | 3,710 | 1.3% | 30.6 | 54 | 72 |
| livephotokit.com | 44 | 1,720 | 2.6% | 19.6 | 27 | 12 |
| plantingcalendar.net | 23 | 6,520 | 0.4% | 29.1 | 432 | 201 |
| freetdee.com | 1 | 213 | 0.5% | 45.8 | 41 | 33 |
| babypercent.com | 18 | 4,600 | 0.4% | 19.6 | 45 | 36 |
| invoicepad.net | 1 | 1,020 | 0.1% | 52.5 | 39 | 21 |
| zoneplan.net | 2 | 2,840 | 0.1% | 45.4 | 30 | 84 |
| pupvax.com | 1 | 360 | 0.3% | 48.2 | 10 | 43 |

Machine evidence:

- `logs/2026-07-29-gsc-8sites-metrics.json`
- `daily/2026-07-29-gsc-8sites-metrics.md`

All eight sitemaps were then resubmitted in GSC with visible success. Evidence:

- `logs/2026-07-29-gsc-sitemap-resubmission.json`

### Search-result comparison

The current search-result sample for the PupVax query family was audited against ten result types, including veterinarian-reviewed publishers, AKC, clinic resources, a professional guideline, chart pages, and an interactive calculator.

Evidence:

- `daily/2026-07-29-pupvax-serp-top10-audit.md`

The title remains the only PupVax page variable changed today. No second on-page edit was stacked.

### Content-cluster cross-check

The four weak sites already have their first content-cluster pages, so adding a duplicate page would violate both the existing asset truth and the one-variable experiment:

- FreeTDEE: TDEE for weight loss, macro tracking, calorie deficit, BMR, macro and protein calculator routes.
- PupVax: deworming schedule, vaccine schedule by age, first-vet/shot and breed schedule routes.
- ZonePlan: global, international, UTC, remote-team and world-clock meeting-planner routes.
- InvoicePad: web developer, SEO service, freelancer, consultant, writer, handyman and estimate routes.

The action-manual “first content-cluster page” item was therefore verified as historically complete rather than duplicated.

### Additional backlinks for the other three weak sites

FreeTDEE received four relevant public pages today:

1. https://medium.com/@lg695101011/tdee-calculator-vs-macro-calculator-which-number-should-you-use-first-c3c083a808fc
2. https://gist.github.com/Gavin1901/3b22ee59da4f6c483195c7a42b311f61
3. https://gist.github.com/Gavin1901/aa084e61c36f148aa9ca0a98c1f4e55f
4. https://github.com/Gavin1901/freetdee/issues/5

InvoicePad received four relevant public pages today:

1. https://medium.com/@lg695101011/web-development-invoice-checklist-7-details-that-prevent-payment-delays-0412a27aa756
2. https://gist.github.com/Gavin1901/4d90f082e90298005958e06d74ae738a
3. https://gist.github.com/Gavin1901/57d8244b9b4053e5975cdc87484f489f
4. https://github.com/Gavin1901/invoicepad/issues/5

ZonePlan received three relevant public pages today:

1. https://gist.github.com/Gavin1901/06a5a805964646eb1a73b41ae13a39e3
2. https://gist.github.com/Gavin1901/8eb42f1f992833c0a10c6b071afcb44b
3. https://github.com/Gavin1901/zoneplan/issues/6

The six new Gists and three issues returned HTTP 200 and contained their target links. Medium blocks anonymous scripted HTTP with 403, but both articles were published through the correct live profile and the post-publish DOM/canonical output contained the intended target link.

Machine evidence:

- `logs/2026-07-29-three-weak-sites-gists.json`
- `logs/2026-07-29-three-weak-sites-issues.json`
- `logs/2026-07-29-weak-site-backlink-verification.json`

### Historical platform-state corrections

- Product Hunt forum thread is public, not pending:
  https://www.producthunt.com/p/general/i-got-1-950-search-impressions-and-only-2-clicks-here-is-what-i-changed
- Product Hunt iWorkViewer is not merely scheduled. It is public and displays `Launched 8d ago`:
  https://www.producthunt.com/products/iworkviewer
- SaaSHub iWorkViewer is now public with the official domain:
  https://www.saashub.com/iworkviewer
- SaaSHub ZonePlan and LivePhotoKit remain public with official domains.
- SaaSHub InvoicePad is public but the static page still lacks the official-domain link.
- FreeTDEE and PupVax SaaSHub routes remain 404.
- AlternativeTo and Indie Hackers remain historical password/OAuth blockers; no credential was invented.

### Full manual-entry re-scan

All 157 normalized HTTP(S) entries from the current action-camp corpus were rechecked:

| Result | Count |
|---|---:|
| HTTP 200 | 80 |
| HTTP 403 | 42 |
| HTTP 404 | 9 |
| HTTP 429 | 1 |
| Other HTTP statuses | 7 |
| Request errors | 18 |
| Total | 157 |

This scan is reachability evidence, not publication evidence. Paid listings, closed services, reference pages, account-gated submissions and incompatible product categories were not misreported as publishable backlinks.

Machine evidence:

- `logs/2026-07-29-manual-platform-live-scan.json`

### Final 745-URL reverse audit

The full sitemap corpus was audited again after the publishing and GSC work:

- Total URLs: 745.
- Non-200: 0.
- Redirects in sitemap: 0.
- Missing canonical: 0.
- Canonical mismatch: 0.
- Noindex: 0.
- Orphan sitemap pages: 0.
- Duplicate titles: 0.
- Duplicate page bodies: 0.
- Thin pages under 200 words: 18, limited to the already classified contact/terms/blog-index/comparison-index style queue.

The first pass recorded four SSL EOF transport errors. Each affected URL then returned HTTP 200 in three consecutive checks, and the full audit was rerun to a clean non-200 result. Transport noise was not misreported as a site defect.

Evidence:

- `daily/2026-07-29-deep-indexability-audit.md`
- `logs/2026-07-29-deep-indexability-audit.json`

## Fourth cross-audit: stale-route and account corrections

The final reverse audit found three additional stale conclusions:

1. FreeTDEE is public on SaaSHub under its submitted product name, not the guessed `/freetdee` slug:
   https://www.saashub.com/bmr-calories-macros
   The page returned HTTP 200 and contained `freetdee.com`.
2. The correct GavinBuilds profile is logged into Hacker News. A single relevant InvoicePad Show HN submission was attempted and the platform returned the explicit `/showlim` restriction. No public item was created.
3. The correct profile was rechecked for the remaining account-gated platforms:
   - AlternativeTo: visible sign-in form with password, Google, GitHub and Apple routes.
   - Indie Hackers: visible email/password sign-in form.
   - Quora: current navigation failed with `ERR_CONNECTION_CLOSED`; no current publish state was fabricated.

The two new Medium articles were re-opened through the correct profile. Both canonical URLs loaded and both DOMs contained their intended target links. Evidence:

- `logs/2026-07-29-medium-live-verification.json`
- `logs/2026-07-29-auth-blocker-recheck.json`

Historical pending submissions were also checked:

- Launching Next receipt remains HTTP 200 with title `Submission Received`.
- Startup88 and Startup Dope submission entries remain accessible, but no public LivePhotoKit listing was found.
- AppRater still has no independently verifiable public LivePhotoKit listing.

### Current SaaSHub truth

| Product | Current state |
|---|---|
| iWorkViewer | Public, HTTP 200, official domain present |
| LivePhotoKit | Public, HTTP 200, official domain present |
| ZonePlan | Public, HTTP 200, official domain present |
| FreeTDEE / BMR Calories Macros | Public, HTTP 200, official domain present |
| InvoicePad | Public, HTTP 200, official-domain link missing |
| PlantingCalendar | No public listing found |
| BabyPercent | No public listing found |
| PupVax | No public listing found |

### Final daily backlink count

- PupVax: 5 qualified public pages.
- FreeTDEE: 4 qualified public pages.
- InvoicePad: 4 qualified public pages.
- ZonePlan: 3 qualified public pages.
- Total new qualified public pages today: 16.

This count is separate from older Product Hunt, Hacker News, SaaSHub, Pinterest and directory assets.
