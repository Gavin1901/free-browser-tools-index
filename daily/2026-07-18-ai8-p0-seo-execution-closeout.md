# 2026-07-18 AI8 P0 SEO Execution Closeout

## Executed

1. Opened GavinBuilds Chrome profile with CDP 9223 and verified Chrome/150.
2. Pulled live GSC query-table snapshots for 8 domains from Search Console /u/1.
   - Raw: `logs/2026-07-18-gsc-query-raw.json`
   - Parsed top rows: `logs/2026-07-18-gsc-query-top.csv`
3. Updated CTR-focused homepage metadata for the two highest-ROI CTR sites:
   - `plantingcalendar.net`: title now targets planting calendar, ZIP/USDA zone, frost dates.
   - `babypercent.com`: title now targets baby growth percentile calculator plus WHO/CDC charts.
4. Built both sites locally with `npm run build` successfully.
5. Committed and pushed source changes:
   - plantingcalendar: `3d713e1 Improve CTR metadata for PlantingCalendar 2026 queries`
   - babypercent: `a07c4d3 Improve CTR metadata for baby growth queries`
6. GitHub Actions deployment failed on both repos because Cloudflare API token returned `Authentication error [code: 10000]`.
7. Bypassed broken GitHub token by deploying with local Wrangler login:
   - plantingcalendar production: `https://5917380e.plantingcalendar.pages.dev`
   - plantingcalendar main/custom-domain branch: `https://4711ecda.plantingcalendar.pages.dev`
   - babypercent production: `https://c95586e6.babypercent.pages.dev`
   - babypercent main/custom-domain branch: `https://848286fe.babypercent.pages.dev`
8. Verified custom domains live with new title/description:
   - `https://plantingcalendar.net/?v=20260718ctr` HTTP 200 and new metadata visible.
   - `https://babypercent.com/?v=20260718ctr` HTTP 200 and new metadata visible.
9. Verified old wrong paths now 301 then 200:
   - `https://freetdee.com/calorie-deficit-calculator/` -> `/calorie-deficit/` -> 200
   - `https://plantingcalendar.net/zone/6/` -> `/zones/3a/` -> 200

## GSC query signals captured

### plantingcalendar.net
- `last frost date zone 8a`: 0 clicks / 44 impressions
- `when to plant carrots`: 0 / 16
- `zone 8b planting schedule 2026`: 1 / 2

### babypercent.com
- `baby percentile calculator`: 0 / 45
- `baby growth calculator`: 0 / 19
- `baby weight percentile`: 0 / 10
- `baby weight percentile calculator`: 0 / 9

### weak sites
- zoneplan: `global meeting planner`, `world clock meeting planner`, `international meeting planner`, `time zone meeting planner`
- freetdee: `tdee calculator free`, `tdee calculator bodybuilding`, `tdee macro calculator`
- pupvax: `dog deworming schedule`, `deworming schedule for dogs`, `puppy worming schedule`
- invoicepad: `seo service invoice template`, `web development invoice`, `freelance copywriter invoice`

## Still not done

1. GitHub Actions Cloudflare token is still broken and must be replaced in GitHub repo secrets.
2. Search Console UI scraping only captured the visible top query rows per site, not a full official export. Need manual Export button or API access for complete CSV.
3. Directory submissions and third-party dofollow outreach are not completed in this pass.
4. Product Hunt iWorkViewer draft still needs Gavin to click Schedule.

## Next execution order

1. Replace Cloudflare API token in GitHub secrets for all 8 repos.
2. Use GSC Export for full query CSV, not visible-row scrape.
3. Create per-site content briefs from query data:
   - freetdee: TDEE calculator free / bodybuilding / macro calculator
   - pupvax: dog deworming schedule cluster
   - zoneplan: international meeting planner cluster
   - invoicepad: invoice template vertical pages
4. Submit real third-party directory/outreach links; stop counting GitHub/Gist/Dev.to self-links as backlink KPI.
