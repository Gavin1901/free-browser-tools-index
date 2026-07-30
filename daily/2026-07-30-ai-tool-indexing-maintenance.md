<!-- AUTO_MAINTENANCE_START -->
# 2026-07-30 AI Tool Indexing Maintenance

Run time: 2026-07-30 08:44:50

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

## GSC and sitemap evidence

All eight Search Console properties were read through the GavinBuilds browser and all eight sitemaps were resubmitted successfully.

| Site | Clicks | Impressions | CTR | Avg position | Indexed | Not indexed |
|---|---:|---:|---:|---:|---:|---:|
| iworkviewer.com | 48 | 3,710 | 1.3% | 30.8 | 54 | 72 |
| livephotokit.com | 48 | 1,780 | 2.7% | 19.8 | 27 | 12 |
| plantingcalendar.net | 23 | 6,500 | 0.4% | 29.0 | 432 | 201 |
| freetdee.com | 1 | 214 | 0.5% | 46.2 | 41 | 33 |
| babypercent.com | 18 | 4,460 | 0.4% | 19.5 | 45 | 36 |
| invoicepad.net | 0 | 1,050 | 0.0% | 52.5 | 39 | 21 |
| zoneplan.net | 2 | 3,110 | 0.1% | 44.9 | 30 | 84 |
| pupvax.com | 1 | 419 | 0.2% | 52.5 | 10 | 43 |

Evidence:

- `logs/2026-07-30-gsc-8sites-metrics.json`
- `logs/2026-07-30-gsc-visible-top-queries.json`
- `logs/2026-07-30-gsc-sitemap-resubmission.json`

## Single-variable experiment

InvoicePad had 1,050 impressions and zero clicks. Its leading visible query was `web development invoice` with 61 impressions and zero clicks.

Only the title of the existing page was changed:

- Page: <https://invoicepad.net/web-developer-invoice-template/>
- Old: `Web Developer Invoice Template - Free PDF Generator`
- New: `Web Development Invoice Template - Free PDF Generator`
- Commit: `3915f68`
- Cloudflare deploy run: `30504038907` — success
- Live verification: HTTP 200 and the new title is present.

The H1, description, body, canonical and URL were not changed.

## Public backlink evidence

1. Gist: <https://gist.github.com/Gavin1901/1f7a438ee09172101c5ef55a0302f83a>
2. GitHub issue: <https://github.com/Gavin1901/invoicepad/issues/6>
3. Dev.to: <https://dev.to/gavinbuildsai/web-development-invoice-template-what-clients-expect-in-2026-3h6>
4. Medium: <https://medium.com/@lg695101011/1aa6f4f0aa86>

The Gist, GitHub issue and Dev.to page each returned HTTP 200 and contained the target InvoicePad deep link. Medium was verified in the correct GavinBuilds browser: the public page, canonical and target link were present.

## Directory execution

- Planting Calendar submitted to SaaSHub: <https://www.saashub.com/planting-calendar/added>
- BabyPercent submitted to SaaSHub: <https://www.saashub.com/babypercent/added>
- PupVax submission was blocked by SaaSHub's explicit queue limit: one recent submission must be approved first.
- LivePhotoKit was submitted to AlternativeTo and CloudConvert was added as an alternative.
- AlternativeTo receipt: the app is pending admin approval and only the owner can see it until approval.

## Final cross-check

The full 745-URL audit was rerun after deployment.

- Redirects: 0
- Missing canonical: 0
- Canonical mismatch: 0
- Noindex: 0
- Orphan sitemap pages: 0
- Duplicate titles: 0
- Duplicate bodies: 0

Seven URLs returned transient request failures during the full crawl. Each was independently requested three times and returned `200,200,200`, so they are recorded as network noise rather than live site failures.
