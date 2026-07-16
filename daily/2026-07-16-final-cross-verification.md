# 2026-07-16 final cross verification

Final status: PASS with one expected raw-curl limitation.

## First-pass red flags

- LivePhotoKit robots/sitemap returned 000 on direct no-proxy curl. Rechecked with normal route: 200.
- PlantingCalendar sitemap returned 000 on direct no-proxy curl. Rechecked with normal route: 200.
- BabyPercent home returned 000 on direct no-proxy curl. Rechecked with normal route: 200.
- Dev.to returned 000 on direct no-proxy curl. Rechecked header: 200. Browser proof exists.
- Medium returned 403 on raw curl because of Cloudflare challenge. Browser proof confirms the article is public and readable.

## Production site title checks

- iWorkViewer: iWorkViewer - Open Apple iWork Files Online
- LivePhotoKit: LivePhotoKit - Free HEIC & Live Photo Converter
- FreeTDEE: Free TDEE Calculator - BMR, Calorie & Macro Tools
- InvoicePad: InvoicePad - Free Invoice Generator for Freelancers
- PupVax: PupVax - Dog Vaccine Schedule Tracker

## Published links

- Dev.to: https://dev.to/gavinbuildsai/eight-ai-built-browser-tools-i-maintained-today-3jfh
- Medium: https://medium.com/@lg695101011/eight-ai-built-browser-tools-i-maintained-today-00546f316f46
- GitHub Issue: https://github.com/Gavin1901/free-browser-tools-index/issues/8
- Evidence page: https://github.com/Gavin1901/free-browser-tools-index/blob/master/daily/2026-07-16-live-publish-and-site-repair.md

## Evidence logs

- logs/2026-07-16-cross-verification-final.json
- logs/2026-07-16-cross-verification-resolution.json
- logs/2026-07-16-medium-public-proof.json
- logs/2026-07-16-livephotokit-title-final-clean2.json
- logs/2026-07-16-production-title-recheck-final.json
