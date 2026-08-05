# How We Fixed a Meeting Planner's SEO by Merging 6 Pages Into 1

ZonePlan is a free worldwide meeting planner that helps distributed teams find fair meeting times across time zones.

After weeks of watching our GSC data, we noticed a pattern: we had 6 different planner pages — global meeting planner, international meeting planner, meeting planner, remote team time zone planner, UTC converter, world clock planner — each getting impressions but nearly zero clicks.

The problem was clear: **Google didn't know which page was the real answer.**

## What we did

1. Chose `global-meeting-planner` as the single canonical page
2. Expanded it from 45 lines to 230 lines with real substance: usage steps, 4 scenario cards, time zone fairness logic, remote team best practices, 6 FAQ items with schema markup, and 5 internal tool links
3. Set canonical tags from the other planner pages to point to global-meeting-planner
4. Added 301 redirects for 3 thin pages (international, utc, world-clock) via Cloudflare `_redirects`
5. Redesigned the homepage to have a single CTA button pointing straight to the main planner

## The numbers that drove this decision

- **265 impressions** on "meeting planner worldwide" — zero clicks
- **132 impressions** on "global meeting planner" — zero clicks
- **120 impressions** on "international meeting planner" — zero clicks
- **4,670 total impressions** across all queries — only 5 clicks total (0.1% CTR)

When Google sees 6 near-identical pages competing for the same intent, it splits ranking signals across all of them. None ranks well enough to earn the click.

## The key insight

**Near-duplicate pages dilute authority.** It is not a content volume problem. It is a signal concentration problem.

Before consolidation, each planner page had thin content (~45 lines), weak internal links, and no clear differentiation. After merging into one comprehensive page with rich structure, internal links, and schema markup, Google has exactly one page to evaluate for "meeting planner" intent queries.

## What we are watching now

The consolidation went live August 4, 2026. We are in a 7-day observation window with no additional changes. Key metrics to track:

- Click-through rate on the main global-meeting-planner page
- Average position movement for "meeting planner worldwide"
- Index coverage changes (currently 30 indexed, 84 not indexed)

The tool itself is free, no sign-up, works instantly: **[zoneplan.net](https://zoneplan.net/)**

---

*This is part of an ongoing SEO growth experiment across 8 free browser tools. Each station gets one variable change per observation window so we can isolate what actually moves the needle.*
