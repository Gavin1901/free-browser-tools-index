# 2026-07-16 Four Weak Sites Git Baseline and Final Full Audit

## What was still unresolved
The four weak-site project folders were local projects without git history. This made future rollback and change attribution risky.

## Actions completed
1. Initialized local git repositories for the four weak-site projects.
2. Set local-only git identity in each repo: `Gavin Builds <lg695101011@gmail.com>`.
3. Committed the post-reinforcement baseline in each project.
4. Moved local backup files out of `src/` into `_local_archive/2026-07-16-backups/` and ignored local archives / `*.bak*`.
5. Re-ran `npm run build` on all four projects after cleanup. All four passed.
6. Ran a final 8-site live audit.

## Four local project git status
| Project | Path | Current HEAD | Status | Notes |
|---|---|---|---|---|
| FreeTDEE | `D:\Tools\freetdee` | `a8d5752` | clean | local git initialized, backups removed from source tree |
| PupVax | `D:\Tools\pupvax` | `9b847c7` | clean | local git initialized, backups removed from source tree |
| InvoicePad | `D:\Tools\invoicepad` | `8c85440` | clean | local git initialized, backups removed from source tree |
| ZonePlan | `D:\Tools\zoneplan` | `cce7f0f` | clean | local git initialized, backups removed from source tree |

## Build status
All four passed `npm run build` after local git initialization and backup cleanup.

## Final 8-site live audit
Evidence: `logs/2026-07-16-four-site-git-and-8site-final-audit.json`

| Site | Home | Robots | Sitemap | Canonical | Noindex | Sitemap URLs | Cross-domain sitemap URLs | Bad mojibake codepoints |
|---|---:|---:|---:|---|---|---:|---:|---:|
| iworkviewer.com | 200 | 200 | 200 | yes | no | 51 | 0 | 0 |
| livephotokit.com | 200 | 200 | 200 | yes | no | 27 | 0 | 0 |
| plantingcalendar.net | 200 | 200 | 200 | yes | no | 365 | 0 | 0 |
| freetdee.com | 200 | 200 | 200 | yes | no | 43 | 0 | 0 |
| babypercent.com | 200 | 200 | 200 | yes | no | 35 | 0 | 0 |
| invoicepad.net | 200 | 200 | 200 | yes | no | 29 | 0 | 0 |
| zoneplan.net | 200 | 200 | 200 | yes | no | 95 | 0 | 0 |
| pupvax.com | 200 | 200 | 200 | yes | no | 36 | 0 | 0 |

## Remaining risk after treatment
1. These four git repositories are local only. They now support local rollback, but are not yet pushed to remote GitHub repos.
2. Production was not redeployed after moving backup files because no runtime source content changed. Build output remains valid.
3. GSC ranking/index effects remain delayed and cannot be claimed same-day.

## Final conclusion
The unresolved four-site source-control risk has been handled locally. Four projects are now versioned, clean, buildable, and the eight live sites pass the final health audit.
