# AI8 porous cross-check final - 2026-07-18

## Scope

Cross-checked 8 sites across:

- Home page HTTP status
- robots.txt
- sitemap.xml
- sitemap URL count and same-domain check
- title length
- description length
- H1 count
- canonical
- noindex
- GA snippet presence
- AdSense snippet presence
- selected focus pages
- second-pass verification for timeout/ERR results

## Final site-level result

| Site | Home | Robots | Sitemap | Sitemap URLs | Canonical | TitleLen | DescLen | H1 | GA | AdSense | Final status |
|---|---:|---:|---:|---:|---|---:|---:|---:|---|---|---|
| iworkviewer.com | 200 | 200 | 200 | 53 | PASS | 43 | 129 | 1 | Present | Present | PASS |
| livephotokit.com | 200 | 200 | 200 | 33 | PASS | 51 | 157 | 1 | Present | Present | PASS after second-pass sitemap check |
| plantingcalendar.net | 200 | 200 | 200 | 375 | PASS | 64 | 130 | 1 | Present | Present | PASS, but old check path `/zone/6/` is invalid |
| freetdee.com | 200 | 200 | 200 | 53 | PASS | 53 | 152 | 1 | Present | Present | PASS, but old check path `/calorie-deficit-calculator/` is invalid |
| babypercent.com | 200 | 200 | 200 | 45 | PASS | 52 | 133 | 1 | Present | Present | PASS |
| invoicepad.net | 200 | 200 | 200 | 36 | PASS | 49 | 150+ | 1 | Present | Present | PASS after second-pass timeout check |
| zoneplan.net | 200 | 200 | 200 | 105 | PASS | 57 | 150+ | 1 | Present | Present | PASS after second-pass timeout check |
| pupvax.com | 200 | 200 | 200 | 45 | PASS | 37 | 158 | 1 | Present | Present | PASS |

## True issues found

### 1. PlantingCalendar old path mismatch

`https://plantingcalendar.net/zone/6/` returns 404.

Sitemap shows the valid structure is `/zones/`, `/zones/3a/`, etc. So future checks should not use `/zone/6/`.

### 2. FreeTDEE old path mismatch

`https://freetdee.com/calorie-deficit-calculator/` returns 404.

Sitemap shows the valid URL is:

- https://freetdee.com/calorie-deficit/

Future checks and backlinks should use the sitemap URL.

## Weak-link reinforcement completed after reading the handbook

Extra weak-site backlinks created after the initial 5-link pass:

1. FreeTDEE focused issue:
   - https://github.com/Gavin1901/freetdee/issues/1
   - Targets: `free TDEE calculator`, `macro calculator`, `protein calculator`

2. PupVax focused issue:
   - https://github.com/Gavin1901/pupvax/issues/1
   - Targets: `dog vaccine schedule`, `dog deworming schedule`

3. InvoicePad focused issue:
   - https://github.com/Gavin1901/invoicepad/issues/1
   - Targets: `free invoice generator`, `freelance writer invoice template`, `web developer invoice template`, `handyman invoice template`

Already created earlier today:

4. ZonePlan focused issue:
   - https://github.com/Gavin1901/zoneplan/issues/1
   - Target: `time zone meeting planner`

## Hacker News status

Hacker News submit page was opened from the GavinBuilds browser profile:

- https://news.ycombinator.com/submit

It returned: `You have to be logged in to submit.`

So Hacker News was not submitted and is not counted as completed.

## Final judgement

The 8-site infrastructure is healthy after second-pass verification. The real work is no longer basic availability. The next bottleneck is page-level indexing and weak-page external references.

Next priority:

1. ZonePlan: fix low indexed count by strengthening core pages.
2. FreeTDEE: use correct `/calorie-deficit/` URL, not the old invalid path.
3. PupVax: keep strengthening `dog vaccine schedule` and `dog deworming schedule`.
4. InvoicePad: keep pushing template pages and watch GSC after 24-72 hours.
