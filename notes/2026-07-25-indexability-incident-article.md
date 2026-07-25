I audited every URL in the sitemaps of eight small Next.js tools because Google Search Console showed a strange pattern: all sites were live, their sitemaps returned 200, and impressions were growing, but indexed-page counts stayed low.

The audit covered 745 URLs across iWorkViewer, LivePhotoKit, PlantingCalendar, FreeTDEE, BabyPercent, InvoicePad, ZonePlan, and PupVax.

## The hidden canonical bug

Fifteen comparison pages on five domains had a production canonical URL that still contained a template placeholder:

`https://__domain__/vs/example/`

The visible URL returned 200, the title and H1 looked correct, and the page was in the sitemap. A normal health check would call it healthy. But the canonical told search engines that the preferred page lived on a nonexistent host.

I replaced every placeholder canonical with the correct production domain and repaired the same placeholder in the breadcrumb schema.

## The crawl-path problem

The audit also found twenty-two sitemap pages with no internal link from any other sitemap page. They were technically discoverable through the XML sitemap, but they had no normal crawl path and received no internal importance signal.

I added visible links from the relevant homepages to every orphan page. This included specialized calculators, long-form guides, scenario pages, comparison hubs, and underlinked articles.

## What the final crawl found

After building and deploying all eight projects, I crawled all 745 URLs again.

The final result was:

- zero non-200 sitemap URLs
- zero redirects in sitemaps
- zero missing canonical tags
- zero canonical mismatches
- zero noindex pages in sitemaps
- zero missing titles, descriptions, or H1s
- zero orphan sitemap pages
- zero duplicate titles
- zero duplicate body hashes

The full public incident report is here:

https://github.com/Gavin1901/free-browser-tools-index/blob/master/daily/2026-07-25-745-url-indexability-incident-report.md

## What this does not prove

A successful deployment does not prove indexing. A 200 response from IndexNow does not prove Google indexing. A successful sitemap submission only proves that Search Console accepted the sitemap action.

The next step is to wait for recrawl and compare indexed counts, impressions, clicks, and query-level movement. Technical eligibility is now clean. The remaining constraints are crawl demand, content value, site age, and referring-domain diversity.

The key lesson is simple: checking only the homepage, robots.txt, and sitemap status can miss the exact defect that blocks a page from being treated as canonical. URL-level audits matter.
