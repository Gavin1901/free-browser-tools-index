# 2026-07-16 Post Reinforcement Deep Recheck

## Scope
After weak-site on-page reinforcement, performed a second pass over source, build output, production pages, deployment evidence, IndexNow evidence and all 8 live sites.

## Issues found during recheck
| Issue | Status | Evidence |
|---|---|---|
| The earlier `bad_mojibake_markers` field in production verify JSON was not reliable because terminal encoding displayed configured markers as question marks. | Corrected by Unicode-codepoint verification. | logs/2026-07-16-weak-sites-production-deep-recheck.json |
| PupVax source still had mojibake in JSX comments. It was not visible in production HTML, but source hygiene was not clean. | Fixed. Source now has no listed bad codepoints and `npm run build` passes. | logs/2026-07-16-weak-sites-source-out-verify.json plus fresh build output in terminal session |
| During comment cleanup, FAQ `q` fields in PupVax were accidentally overwritten, causing one local build failure. | Fixed immediately. FAQ questions restored, build passes. | Current `D:\Tools\pupvax\src\app\page.tsx`; build pass after repair |

## Rechecked production weak sites
Evidence: logs/2026-07-16-weak-sites-production-deep-recheck.json

| Site | HTTP | New block/link found | Bad mojibake codepoints |
|---|---:|---|---|
| freetdee.com | 200 | yes | none |
| pupvax.com | 200 | yes | none |
| invoicepad.net | 200 | yes | none |
| zoneplan.net | 200 | yes | none |

## Rechecked all 8 live sites
Evidence: logs/2026-07-16-8site-post-reinforcement-live-audit.json

Result: all 8 sites returned homepage 200, robots 200, sitemap 200, canonical present, no noindex found, no sitemap cross-domain issue found, and no listed mojibake codepoints found on homepages.

| Site | Home | Robots | Sitemap | Sitemap URLs |
|---|---:|---:|---:|---:|
| iworkviewer.com | 200 | 200 | 200 | 51 |
| livephotokit.com | 200 | 200 | 200 | 27 |
| plantingcalendar.net | 200 | 200 | 200 | 365 |
| freetdee.com | 200 | 200 | 200 | 43 |
| babypercent.com | 200 | 200 | 200 | 35 |
| invoicepad.net | 200 | 200 | 200 | 29 |
| zoneplan.net | 200 | 200 | 200 | 95 |
| pupvax.com | 200 | 200 | 200 | 36 |

## Current remaining caveats
1. GSC ranking and index-count effects are delayed. The on-page and IndexNow work is done, but GSC cannot show the effect immediately.
2. The four site project folders are not git repositories. Source changes are present locally and deployed; public evidence is committed in this evidence repository.
3. Some untracked files in this evidence repo are older or intermediate artifacts from blocked/failed attempts. They were intentionally not committed as final proof.

## Final conclusion
No current live-site blocker found after the second pass. One local PupVax source regression was found during the recheck and fixed before closeout.
