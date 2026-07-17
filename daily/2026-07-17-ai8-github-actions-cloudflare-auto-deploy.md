# 2026-07-17 AI8 GitHub Actions Cloudflare auto deploy

## Summary

Cloudflare native Git Provider remains `No` for these existing Direct Upload projects, but GitHub Actions automatic deployment has been added and tested for all 8 repositories.

Each repo now has:

- `.github/workflows/deploy-pages.yml`
- GitHub secret `CLOUDFLARE_API_TOKEN`
- Push-to-master trigger
- `npm ci`
- `npm run build`
- `wrangler pages deploy out --project-name <project> --branch main`

## Successful GitHub Actions runs

- invoicepad: success, run 29551990733
- zoneplan: success, run 29552057163
- freetdee: success, run 29552001891
- pupvax: success, run 29552007676
- babypercent: success, run 29552012420
- plantingcalendar: success, run 29552021114
- iworkviewer: success, run 29552024726
- livephotokit: success, run 29552030466

## Cloudflare production deployments from Actions

- invoicepad: https://0d77591a.invoicepad.pages.dev, source cf9776f
- zoneplan: https://076fa935.zoneplan.pages.dev, source f177c7c
- freetdee: https://835e748e.freetdee.pages.dev, source 6f31d95
- pupvax: https://57e07c4c.pupvax.pages.dev, source 1e4eecc
- babypercent: https://dfa9a64f.babypercent.pages.dev, source 54eff74
- plantingcalendar: https://1c8c33a6.plantingcalendar.pages.dev, source f04e0d1
- iworkviewer: https://1906c81f.iworkopener.pages.dev, source 470a49c
- livephotokit: https://0becb8c5.livephotokit.pages.dev, source 86a52cb

## Boundary

This is GitHub Actions based automatic deployment to existing Cloudflare Pages Direct Upload projects. It is not Cloudflare Dashboard native Git Provider binding. The official Cloudflare Git integration path is still dashboard-based: Workers & Pages > Create application > Pages > Connect to Git.
