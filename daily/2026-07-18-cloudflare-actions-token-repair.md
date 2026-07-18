# 2026-07-18 Cloudflare Actions Token Repair

## Result

Cloudflare GitHub Actions deployment chain is repaired for the 8 AI outbound tool sites.

## Root cause

The old GitHub secret `CLOUDFLARE_API_TOKEN` existed in each repo, but it returned Cloudflare API authentication error `code: 10000` during Pages deployment.

Local Wrangler OAuth could deploy, but that OAuth token expires and is not a good GitHub Actions secret.

A historical long-lived Cloudflare token was found locally and verified against Cloudflare Pages API without printing the token.

## Secrets refreshed

`CLOUDFLARE_API_TOKEN` was refreshed in these repos:

- `Gavin1901/zoneplan`
- `Gavin1901/freetdee`
- `Gavin1901/pupvax`
- `Gavin1901/invoicepad`
- `Gavin1901/plantingcalendar`
- `Gavin1901/babypercent`
- `Gavin1901/livephotokit`
- `Gavin1901/iworkviewer`

Note: first attempt used wrong repo name `Gavin1901/iworkopener`, which returned 404. Correct repo is `Gavin1901/iworkviewer`.

## Actions verification

After refreshing secrets, workflow_dispatch was triggered and the latest deploy run succeeded for all 8 repos.

| Repo | Run | Conclusion | SHA |
|---|---:|---|---|
| zoneplan | 29631673866 | success | 95e0511 |
| freetdee | 29631675231 | success | 9eb332f |
| pupvax | 29631709564 | success | ff244f0 |
| invoicepad | 29631684932 | success | fbaff15 |
| plantingcalendar | 29631686150 | success | 3d713e1 |
| babypercent | 29631687469 | success | a07c4d3 |
| livephotokit | 29631688823 | success | 86a52cb |
| iworkviewer | 29631710659 | success | 470a49c |

## Live site verification

All 8 custom domains returned HTTP 200 after the Actions repair:

- https://iworkviewer.com/
- https://livephotokit.com/
- https://plantingcalendar.net/
- https://freetdee.com/
- https://babypercent.com/
- https://invoicepad.net/
- https://zoneplan.net/
- https://pupvax.com/

## Evidence files

- `logs/2026-07-18-cloudflare-actions-repair-final.json`
- `logs/2026-07-18-cloudflare-actions-repair-site-check.json`

## Remaining caveat

This repair uses a historical token found in local evidence. It is currently valid and Actions passed. For long-term hygiene, Gavin should later create a named Cloudflare token specifically for `AI8 GitHub Actions Pages Deploy`, with only Account Pages Edit/read scope, and rotate this secret intentionally.
