# 2026-07-16 AI outbound live publishing and site repair report

Run time: 2026-07-16 08:15 +08:00

## Published today

- Dev.to: https://dev.to/gavinbuildsai/eight-ai-built-browser-tools-i-maintained-today-3jfh
- GitHub Issue: https://github.com/Gavin1901/free-browser-tools-index/issues/8
- GitHub evidence page: https://github.com/Gavin1901/free-browser-tools-index/blob/master/daily/2026-07-16-backlink-reinforcement.md
- Weak-site Gists:
  - https://gist.github.com/Gavin1901/171ef604d099837c040ab6864f48f89e
  - https://gist.github.com/Gavin1901/1f00a2b3251e298018e2c21cb54d1147
  - https://gist.github.com/Gavin1901/25f479ad8fa072751c0f683939edf04e
  - https://gist.github.com/Gavin1901/63463e28aea28f36e30da7b84a3155f7

## Medium status

Medium was initially blocked by Cloudflare security verification, then passed in the GavinBuilds Chrome profile and was published.

Medium URL: https://medium.com/@lg695101011/eight-ai-built-browser-tools-i-maintained-today-00546f316f46

Evidence: logs/2026-07-16-medium-public-proof.json

## Eight-site live checks

Daily maintenance and IndexNow succeeded for all eight sites. Each site returned home 200, robots 200, sitemap 200, and 20 URLs were submitted to IndexNow.

Evidence: logs/2026-07-16-result.json

Chrome visual check was attempted through GavinBuilds Chrome CDP 9223. iWorkViewer, InvoicePad and PupVax opened in Chrome and screenshots were saved. Several other sites returned net::ERR_CONNECTION_CLOSED in Chrome, while the maintenance script still returned 200. This is recorded as a browser/network-layer issue, not a confirmed site-down issue.

Evidence: logs/2026-07-16-chrome-8sites-visual-proof.json

## Problems found and repaired locally

1. LivePhotoKit homepage metadata had mojibake in title/openGraph text. Local fix applied and npm run build passed.
2. FreeTDEE homepage title was shortened. Local fix applied and npm run build passed.
3. PupVax homepage title was shortened. Local fix applied and npm run build passed.

Backup suffix: bak_20260716_080736

## Deployment status

Cloudflare Pages deploy was completed after clearing the broken proxy environment variables. Production title checks passed for FreeTDEE, PupVax, and LivePhotoKit.

Evidence:

- logs/2026-07-16-production-title-recheck-final.json
- logs/2026-07-16-livephotokit-title-final-clean2.json

## Verification logs

- logs/2026-07-16-devto-browser-proof.json
- logs/2026-07-16-devto-github-issue-verification.json
- logs/2026-07-16-gist-backlinks-verified-final.json
- logs/2026-07-16-backlink-reinforcement-public-check.json
- logs/2026-07-16-course-level-8site-audit.json

## Final deployment fix

The wrangler deploy problem was caused by proxy environment variables pointing to 127.0.0.1:7897. Clearing HTTP_PROXY / HTTPS_PROXY / ALL_PROXY and lower-case variants allowed Cloudflare Pages deployments to complete.

LivePhotoKit required an additional page-level metadata fix in src/app/page.tsx because the homepage metadata overrode layout metadata. Final production title: LivePhotoKit - Free HEIC & Live Photo Converter.
