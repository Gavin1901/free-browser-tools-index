# 2026-07-16 Weak Site On-page Reinforcement

## Trigger
GSC 28-day data showed weak conversion/indexing on FreeTDEE, PupVax, InvoicePad and ZonePlan.

## GSC basis
- FreeTDEE: 0 clicks, 128 impressions, average position 38.6, indexed 10 / not indexed 47.
- PupVax: 0 clicks, 150 impressions, average position 35.5, indexed 8 / not indexed 32.
- InvoicePad: 1 click, 526 impressions, average position 50.5, indexed 28 / not indexed 17.
- ZonePlan: 1 click, 896 impressions, average position 45.9, indexed 4 / not indexed 89.

## Changes shipped
| Site | Action |
|---|---|
| freetdee.com | Added GSC-driven homepage internal-link block to calorie calculator, calorie deficit, macro, protein, women over 40 and men over 50 pages. Cleaned visible homepage mojibake. |
| pupvax.com | Added GSC-driven homepage internal-link block to dog deworming, puppy schedule, rabies, senior dog vaccines and two breed pages. Cleaned visible homepage mojibake markers. |
| invoicepad.net | Added GSC-driven homepage internal-link block to invoice templates, estimate maker, web developer, writer, handyman and receipt pages. Cleaned visible homepage mojibake. |
| zoneplan.net | Expanded existing high-intent homepage block with time zone meeting planner, New York to London and San Francisco to Bangalore links. |

## Build and deployment
All four projects passed `npm run build` after source edits.

Deployment proof logs:
- logs/2026-07-16-freetdee-reinforce-final-deploy-retry.txt
- logs/2026-07-16-pupvax-reinforce-final-deploy.txt
- logs/2026-07-16-invoicepad-reinforce-final-deploy.txt
- logs/2026-07-16-zoneplan-reinforce-final-deploy.txt

Latest deployment URLs:
- https://d78bb59d.freetdee.pages.dev
- https://c8863203.pupvax.pages.dev
- https://dbe36f8f.invoicepad.pages.dev
- https://d7c8998f.zoneplan.pages.dev

## Production verification
Evidence file: logs/2026-07-16-weak-sites-production-verify-final.json

Verified on production domains with cache-bust query:
- freetdee.com: 200, new internal-link block found.
- pupvax.com: 200, new internal-link block found.
- invoicepad.net: 200, new internal-link block found.
- zoneplan.net: 200, reinforced links found.

## IndexNow
Submitted 7 priority URLs per weak site after deployment.
Evidence: logs/2026-07-16-weak-reinforce-indexnow-results.json

All four IndexNow submissions returned 200.

## Notes
- Earlier FreeTDEE deploy attempt uploaded files but failed at Cloudflare fetch/deploy stage. It was retried and succeeded.
- First insertion attempt did not hit the template anchors for three sites. This was caught by checking `out/index.html`, then fixed with component-anchor insertion and rebuilt.
