# I Crawled 743 URLs Across 8 AI-Built Tool Sites — Here Is What Broke

A homepage returning 200 does not mean a site is healthy. Today I ran a full crawl across eight free browser tools and checked every sitemap URL for HTTP status, redirects, canonical tags, noindex, missing titles, missing descriptions, missing H1s, duplicate text and orphan pages.

## Portfolio result

| Site | Sitemap URLs | Clicks | Impressions | CTR | Avg position |
|---|---:|---:|---:|---:|---:|
| [iWorkViewer](https://iworkviewer.com/open-pages-file-android/) | 54 | 45 | 3,580 | 1.3% | 31.1 |
| [LivePhotoKit](https://livephotokit.com/send-live-photo-as-gif-whatsapp/) | 31 | 51 | 2,140 | 2.4% | 26.4 |
| [PlantingCalendar](https://plantingcalendar.net/zones/8a/) | 375 | 12 | 4,100 | 0.3% | 29.9 |
| [FreeTDEE](https://freetdee.com/tdee-calculator-bodybuilding/) | 54 | 1 | 177 | 0.6% | 54.1 |
| [BabyPercent](https://babypercent.com/) | 45 | 11 | 2,940 | 0.4% | 20.7 |
| [InvoicePad](https://invoicepad.net/web-developer-invoice-template/) | 35 | 0 | 1,200 | 0% | 57.7 |
| [ZonePlan](https://zoneplan.net/global-meeting-planner/) | 102 | 4 | 5,860 | 0.1% | 44.0 |
| [PupVax](https://pupvax.com/puppy-vaccine-schedule-by-age/) | 47 | 1 | 831 | 0.1% | 68.1 |

## Two real defects survived the first pass

### 1. A new iWorkViewer growth page had no internal link

The Android Pages guide was in the sitemap but no crawled page linked to it. I added a contextual link from the homepage, rebuilt the site, deployed it and verified the live HTML.

### 2. ZonePlan listed noncanonical pages in its sitemap

Two older meeting-planner pages correctly pointed their canonical tags to the global meeting planner, but the sitemap still listed the old URLs. I removed both legacy URLs from the sitemap, rebuilt, deployed and verified that only the canonical target remains.

## False alarms that were not defects

The first crawl reported scattered non-200 pages on PlantingCalendar, BabyPercent, ZonePlan and PupVax. Every one returned HTTP 200 on retry. These were transient TLS/network failures, not broken pages.

The crawler also flagged several pages under 200 words. They were Contact, Terms, Blog index and comparison index pages. Adding filler text would make them worse, not better, so I left them alone.

## Final state

After deployment, I reran the full audit:

- 743 sitemap URLs checked
- zero persistent non-200 pages after retry
- zero redirected sitemap URLs
- zero missing or mismatched canonical tags
- zero noindex accidents
- zero missing title, description or H1
- zero duplicate titles, descriptions or page bodies
- zero orphan sitemap pages
- all eight repositories clean and synced
- all eight production homepages have canonical, schema, GA, AdSense and no noindex

The important lesson: fix defects that survive a second check. Do not manufacture content or stack SEO changes just to make an audit look greener.
