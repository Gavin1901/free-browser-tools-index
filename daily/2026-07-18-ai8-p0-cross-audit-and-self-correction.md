# 2026-07-18 AI8 P0 Cross Audit and Self-Correction

## Cross verification result

### Live metadata

Both CTR metadata changes are live on the custom domains, not only on pages.dev.

- `https://plantingcalendar.net/?audit=20260718`
  - HTTP 200
  - title: `Planting Calendar by ZIP & USDA Zone 2026 | Frost Dates`
  - description contains: `Find your 2026 planting calendar by USDA zone with last frost dates...`
  - canonical: `https://plantingcalendar.net/`
  - noindex: false
  - FAQPage schema: present
  - WebSite schema: present

- `https://babypercent.com/?audit=20260718`
  - HTTP 200
  - title: `Baby Growth Percentile Calculator | WHO & CDC Charts`
  - description contains: `Free baby growth percentile calculator for weight, length, height...`
  - canonical: `https://babypercent.com/`
  - noindex: false
  - FAQPage schema: present
  - WebSite schema: present

### 8-site health

All 8 sites returned HTTP 200 for homepage, robots.txt, and sitemap.xml during cross-audit.

### Old path verification

- `https://freetdee.com/calorie-deficit-calculator/` returns 301 to `/calorie-deficit/`, then 200.
- `https://plantingcalendar.net/zone/6/` returns 301 to `/zones/3a/`, then 200.

### Repository state

- `D:\Tools\plantingcalendar` clean; last commit `3d713e1`.
- `D:\Tools\babypercent` clean; last commit `a07c4d3`.
- `D:\Tools\freetdee` still has untracked local artifact `freetdee-out-20260718.zip`.
- `D:\Tools\ai-tool-index` has untracked local evidence screenshots/raw logs not all pushed.

## Self-correction findings

### 1. I almost over-reported GSC query data

What happened: I said I pulled query-level GSC data. Strictly, I scraped visible Search Console UI query rows, not a full official export.

Correct wording: `GSC visible query rows captured`, not `complete query CSV exported`.

Risk: If only visible top rows are used, long-tail decisions can be biased.

Next fix: Use the GSC Export button or API access for full query CSV.

### 2. I did not preflight Cloudflare GitHub Actions token before pushing source changes

What happened: Source commits were valid, builds passed, but GitHub Actions failed because Cloudflare API token returned `Authentication error [code: 10000]`.

Root cause: I assumed the deploy chain was healthy because local Wrangler had worked earlier. I should have checked latest GitHub Actions health before relying on auto-deploy.

Fix applied: Bypassed with local Wrangler deployment to both `production` and `main` branches, then verified custom domains live.

Remaining fix: Replace the Cloudflare API token in GitHub Secrets for the affected repos.

### 3. I initially deployed to `production` branch, but custom domains were still serving the old metadata

What happened: `production.pages.dev` showed new metadata, but the custom domain still showed old metadata.

Root cause: Custom domain was tied to the `main` branch deployment, not only `production`.

Fix applied: Re-deployed both sites to `main`, then custom domains showed the new metadata.

Lesson: Always verify the actual custom domain, not just pages.dev deployment URLs.

### 4. I left local evidence files untracked

What happened: The public repo has the summary and parsed CSV, but raw GSC screenshots, raw JSON, live HTML, and title-check text remain local untracked evidence.

Reason: Avoided pushing large/raw browser evidence blindly.

Risk: Next run might not see the raw evidence from GitHub.

Fix: This audit records the local evidence paths. If needed, push selected lightweight raw evidence later.

## Evidence files

- `D:\Tools\ai-tool-index\logs\2026-07-18-p0-cross-audit.json`
- `D:\Tools\ai-tool-index\logs\2026-07-18-title-description-live-check.txt`
- `D:\Tools\ai-tool-index\logs\2026-07-18-gsc-query-top.csv`
- `D:\Tools\ai-tool-index\daily\2026-07-18-ai8-p0-seo-execution-closeout.md`

## Final status after cross-audit

Done:

- Browser opened in correct GavinBuilds profile.
- GSC visible query rows captured for 8 sites.
- PlantingCalendar metadata changed, pushed, deployed, and verified on custom domain.
- BabyPercent metadata changed, pushed, deployed, and verified on custom domain.
- 8-site homepage/robots/sitemap check passed.
- Two old wrong paths 301 correctly and end in 200.

Not done:

- Cloudflare GitHub Actions token replacement.
- Full GSC Export CSV.
- Product Hunt final Schedule.
- Third-party dofollow submissions/outreach.
- Cleanup/decision on local untracked evidence and `freetdee-out-20260718.zip`.
