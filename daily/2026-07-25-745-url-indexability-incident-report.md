# 8-site indexability incident report: 705 sitemap URLs audited

Date: 2026-07-25

A full URL-level crawl was run across eight free browser-tool sites. The audit covered every URL currently present in each sitemap, not a sample.

## Scope

| Site | Sitemap URLs audited |
|---|---:|
| [iWorkViewer](https://iworkviewer.com/) | 53 |
| [LivePhotoKit](https://livephotokit.com/) | 30 |
| [PlantingCalendar](https://plantingcalendar.net/) | 375 |
| [FreeTDEE](https://freetdee.com/) | 53 |
| [BabyPercent](https://babypercent.com/) | 45 |
| [InvoicePad](https://invoicepad.net/) | 35 |
| [ZonePlan](https://zoneplan.net/) | 107 |
| [PupVax](https://pupvax.com/) | 47 |

Total: 745 sitemap URLs audited.

## Root causes found

1. Fifteen comparison pages across five domains used the placeholder canonical host `https://__domain__/` in production.
2. Twenty-two sitemap pages had zero internal links from another sitemap page.
3. Several utility pages were thin, but these were mainly contact, terms, blog index or comparison hub pages rather than the primary search landing pages.
4. The largest weak sites have many more sitemap URLs than indexed URLs, so crawl priority and perceived page value are the main bottleneck after technical eligibility.
5. Most backlinks were concentrated in GitHub-owned surfaces, limiting referring-domain diversity.

## Fixes shipped

1. Replaced all fifteen invalid canonical URLs with the correct production domains.
2. Repaired breadcrumb schema URLs on the same comparison pages.
3. Added visible internal crawl paths from the homepages to every previously orphaned sitemap page.
4. Built and deployed all eight sites through their Cloudflare Pages workflows.
5. Re-ran the full 745-URL audit after deployment.
6. Re-submitted all eight sitemaps in Google Search Console.
7. Submitted twenty URLs per site to IndexNow after deployment.

## Post-deployment verification

The final crawl found:

- 0 non-200 sitemap URLs
- 0 redirected sitemap URLs
- 0 missing canonical tags
- 0 canonical mismatches
- 0 noindex pages in sitemaps
- 0 missing titles
- 0 missing descriptions
- 0 missing H1s
- 0 orphan sitemap pages
- 0 duplicate titles
- 0 duplicate body hashes

IndexNow acceptance and sitemap submission are discovery signals. They are not proof that Google has indexed a URL. The next measurement is Google Search Console coverage and query movement after recrawl.

## Public code evidence

- iWorkViewer internal links: https://github.com/Gavin1901/iworkviewer/commit/6246f1b
- LivePhotoKit internal links: https://github.com/Gavin1901/livephotokit/commit/7d45b60
- PlantingCalendar canonical fix: https://github.com/Gavin1901/plantingcalendar/commit/1850e94
- FreeTDEE canonical fix: https://github.com/Gavin1901/freetdee/commit/2ff753c
- BabyPercent canonical fix: https://github.com/Gavin1901/babypercent/commit/ee5df55
- InvoicePad internal links: https://github.com/Gavin1901/invoicepad/commit/e8d88b3
- ZonePlan canonical fix: https://github.com/Gavin1901/zoneplan/commit/a94c7f4
- PupVax canonical fix: https://github.com/Gavin1901/pupvax/commit/479ca71
