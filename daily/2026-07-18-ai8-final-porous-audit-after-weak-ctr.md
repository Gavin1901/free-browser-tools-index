# 2026-07-18 AI8 Final Porous Audit After Weak CTR Execution

## Final result

Second cross-audit found no live-domain metadata mismatch.

## Live custom domain verification

All four weak-site custom domains returned HTTP 200 and the expected new metadata.

| Site | Expected title | Live OK |
|---|---|---:|
| zoneplan.net | Time Zone Meeting Planner 2026 · World Clock Scheduler | yes |
| freetdee.com | TDEE Calculator Free 2026 · BMR, Calories & Macros | yes |
| pupvax.com | Dog Deworming & Puppy Vaccine Schedule 2026 · PupVax | yes |
| invoicepad.net | Invoice Templates for Freelancers 2026 · Free Generator | yes |

All four pages also checked:

- canonical matches custom domain
- no `noindex`
- GA script present
- AdSense publisher marker present
- FAQPage schema present
- WebSite schema present

## Robots and sitemap

For zoneplan, freetdee, pupvax, invoicepad:

- homepage: 200
- robots.txt: 200
- sitemap.xml: 200
- sitemap/robots text contains same-domain URLs

## Repo cleanliness

Clean worktrees:

- `D:\Tools\zoneplan`
- `D:\Tools\freetdee`
- `D:\Tools\pupvax`
- `D:\Tools\invoicepad`
- `D:\Tools\plantingcalendar`
- `D:\Tools\babypercent`

Local archives:

- `D:\Tools\freetdee\_local_archive\2026-07-18-seo-cleanup\freetdee-out-20260718.zip`
- `D:\Tools\ai-tool-index\_local_archive\2026-07-18-p0-raw-evidence\` contains 16 raw evidence artifacts.

## Public evidence

The three public closeout pages all returned HTTP 200:

- `daily/2026-07-18-ai8-p0-seo-execution-closeout.md`
- `daily/2026-07-18-ai8-p0-cross-audit-and-self-correction.md`
- `daily/2026-07-18-ai8-weak-sites-ctr-metadata-execution.md`

## New finding during final audit

All four weak-site GitHub Actions deployment runs failed after push:

- zoneplan: failure on commit `95e0511`
- freetdee: failure on commit `9eb332f`
- pupvax: failure on commit `ff244f0`
- invoicepad: failure on commit `fbaff15`

This does NOT mean the sites are offline. The custom domains are live with new metadata because local Wrangler deployment succeeded.

Root cause remains the same: Cloudflare API token in GitHub Actions is broken. The system must not treat a future `git push` as deployed until the token is replaced or local Wrangler deployment is verified.

## Final audit evidence

- `logs/2026-07-18-final-porous-audit.json`

## Not done

- Cloudflare GitHub Actions token still needs replacement.
- Full official GSC Export still not done.
- Product Hunt schedule still needs Gavin confirmation.
- Third-party dofollow directory/outreach still not started.
