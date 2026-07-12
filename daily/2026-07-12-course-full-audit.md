# 2026-07-12 Course Full Audit for 8 AI Tool Sites

## Course checklist used

1. Public access: homepage must return 200.
2. Crawl access: robots.txt and sitemap.xml must return 200.
3. Sitemap quality: sitemap loc URLs must stay on the correct domain.
4. Technical SEO: title, description, H1, canonical and noindex check.
5. Indexing push: submit sitemap URLs through IndexNow.
6. External signals: maintain public GitHub pages, weekly issue links and Medium links.
7. Data layer: GA4 and AdSense code presence check.
8. GSC and GA backend: check only when account property access is available.
9. Review loop: weak indexed sites get more external links and description/title fixes.

## Final 8 site status

| Site | Home | Robots | Sitemap | Sitemap URLs | Title | Description | Canonical | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|---|
| iworkviewer.com | 200 | 200 | 200 | 51 | 73 | 129 | https://iworkviewer.com/ | PASS |
| livephotokit.com | 200 | 200 | 200 | 27 | 56 | 157 | https://livephotokit.com/ | PASS |
| plantingcalendar.net | 200 | 200 | 200 | 365 | 64 | 130 | https://plantingcalendar.net/ | PASS |
| freetdee.com | 200 | 200 | 200 | 43 | 58 | 152 | https://freetdee.com/ | PASS |
| babypercent.com | 200 | 200 | 200 | 35 | 71 | 133 | https://babypercent.com/ | PASS |
| invoicepad.net | 200 | 200 | 200 | 29 | 69 | 145 | https://invoicepad.net/ | PASS |
| zoneplan.net | 200 | 200 | 200 | 92 | 56 | 143 | https://zoneplan.net/ | PASS |
| pupvax.com | 200 | 200 | 200 | 36 | 65 | 158 | https://pupvax.com/ | PASS |

## Optimization done

ZonePlan had a description length of 174 characters. It was slightly over the preferred range. I shortened it to 143 characters, rebuilt the site, and deployed it to Cloudflare Pages production.

Deployment URL: https://ca60152a.zoneplan.pages.dev
Production verified: https://zoneplan.net/

## IndexNow

8 sites submitted 20 URLs each. All IndexNow responses returned 200.

Evidence: https://github.com/Gavin1901/free-browser-tools-index/blob/master/daily/2026-07-12-ai-tool-indexing-maintenance.md

## External links already pushed today

Weak site page:
https://github.com/Gavin1901/free-browser-tools-index/blob/master/daily/2026-07-12-weak-sites-backlinks.md

Medium records:
https://github.com/Gavin1901/free-browser-tools-index/blob/master/daily/2026-07-12-medium-backlinks.md

Daily backlinks:
https://github.com/Gavin1901/free-browser-tools-index/blob/master/daily/2026-07-12-backlinks.md

## Data layer

All 8 sites have GA4 code and AdSense publisher code on page.

## GSC and GA backend

GSC opened to welcome/property verification page, not the property report dashboard. Current Chrome profile does not expose usable Search Console property reports.

GA backend page did not expose a readable property report in this run.

No GSC or GA numbers were reported because they were not verifiable in the current session.

## Dev.to

Dev.to is not logged in. It is on magic link one-time email code page. No Dev.to post was counted in this run.

## Daily operating rule going forward

Every day:

1. Run 8-site HTTP, robots and sitemap check.
2. Run IndexNow for 20 sitemap URLs per site.
3. Check technical SEO drift: title length, description length, canonical, sitemap domain, noindex.
4. Add 3 to 5 real external links, prioritizing weak indexed sites.
5. Record all public URLs in GitHub daily notes.
6. If GSC is available, check indexed, not indexed, clicks, impressions and query terms.
7. If GSC is not available, write not checked. Do not invent.
8. Fix one clear technical SEO issue immediately when found.
