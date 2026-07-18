# 2026-07-18 AI8 Weak Sites CTR Metadata Execution

## Executed after cross-audit

Based on visible GSC query rows captured on 2026-07-18, the four weak sites received CTR-focused homepage metadata updates.

## Query basis

- zoneplan.net: `global meeting planner`, `world clock meeting planner`, `international meeting planner`, `meeting planner`, `time zone meeting planner`
- freetdee.com: `tdee calculator free`, `tdee calculator bodybuilding`, `tdee macro calculator`, `free tdee calculator`
- pupvax.com: `dog deworming schedule`, `deworming schedule for dogs`, `dog deworming schedule chart`, `puppy worming schedule`
- invoicepad.net: `seo service invoice template`, `web development invoice`, `freelance copywriter invoice`, `handyman invoice template`

## Code commits

- zoneplan: `95e0511 Improve CTR metadata for time zone meeting queries`
- freetdee: `9eb332f Improve CTR metadata for TDEE calculator queries`
- pupvax: `ff244f0 Improve CTR metadata for dog deworming queries`
- invoicepad: `fbaff15 Improve CTR metadata for invoice template queries`

## Build validation

All four sites passed `npm run build` locally before deployment.

## Deployment

GitHub Actions token is still not trusted, so deployment used local Wrangler login to the `main` branch.

- zoneplan: first Wrangler attempt failed with `fetch failed`, second attempt succeeded: `https://73bb4a06.zoneplan.pages.dev`
- freetdee: succeeded: `https://942bc6b9.freetdee.pages.dev`
- pupvax: succeeded: `https://ccd9c564.pupvax.pages.dev`
- invoicepad: succeeded: `https://6b0dc3b3.invoicepad.pages.dev`

## Custom domain verification

All custom domains returned HTTP 200 and the expected new title/description.

- `https://zoneplan.net/?audit=weakctr20260718`
  - title: `Time Zone Meeting Planner 2026 | World Clock Scheduler`
- `https://freetdee.com/?audit=weakctr20260718`
  - title: `TDEE Calculator Free 2026 | BMR, Calories & Macros`
- `https://pupvax.com/?audit=weakctr20260718`
  - title: `Dog Deworming & Puppy Vaccine Schedule 2026 | PupVax`
- `https://invoicepad.net/?audit=weakctr20260718`
  - title: `Invoice Templates for Freelancers 2026 | Free Generator`

## Self-correction during execution

I made a syntax replacement error on PupVax and InvoicePad: missing commas in the OpenGraph metadata object. Local build caught it before deployment. I fixed the commas and rebuilt successfully. No broken code was deployed.

## Remaining

- Replace Cloudflare API token in GitHub Actions secrets.
- Pull full official GSC export, not only visible rows.
- Build content clusters around these query groups.
- Start real third-party directory/outreach links.
