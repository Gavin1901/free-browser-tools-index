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
- Dev.to: the correct logged-in editor opened, but the browser-control session repeatedly timed out before a safe publish action; no post was fabricated.
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
