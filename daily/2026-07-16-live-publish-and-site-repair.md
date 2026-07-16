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

Medium was opened in the GavinBuilds Chrome profile, but it stayed on Cloudflare security verification. No Medium post is claimed as published today.

Evidence: logs/2026-07-16-medium-cloudflare-block.json

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

Cloudflare Pages deploy was attempted through wrangler, but failed with fetch/network error in the current environment. Therefore these three title fixes are built locally but not verified as production deployed.

## Verification logs

- logs/2026-07-16-devto-browser-proof.json
- logs/2026-07-16-devto-github-issue-verification.json
- logs/2026-07-16-gist-backlinks-verified-final.json
- logs/2026-07-16-backlink-reinforcement-public-check.json
- logs/2026-07-16-course-level-8site-audit.json
