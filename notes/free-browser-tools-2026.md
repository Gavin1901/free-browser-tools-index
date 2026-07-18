# Free Browser Tools 2026 — SEO & Link Building Playbook

Owner: Gavin1901 · Scope: the 8 privacy-first browser tool sites
Last updated: 2026-07-18 · Status: REPLACES the old nofollow self-link habit

---

## 0. TL;DR — what we are changing and why

From 2026-07-10 to 2026-07-18 the daily `*-backlinks*.md` logs pushed links to:
GitHub Issues, public Gists, Dev.to articles, Medium stories, and the README in this repo.

**All of those are `nofollow` / `ugc` / self-referential.** Google reads them as "one person
linking to himself" and they pass ~0 PageRank. That is the #1 reason domain authority is stuck
and weak sites stay "discovered but not indexed."

GSC reality check (2026-07-18 snapshot, from `daily/2026-07-18-ai8-final-execution-closeout.md`):

| Site | Clicks | Indexed | Not indexed |
|---|---:|---:|---:|
| iworkviewer.com | 45 | 69 | 53 |
| livephotokit.com | 40 | 8 | 26 |
| plantingcalendar.net | 19 | 380 | 186 |
| freetdee.com | 0 | 10 | 47 |
| babypercent.com | 17 | 46 | 25 |
| invoicepad.net | 1 | 28 | 17 |
| zoneplan.net | 1 | 4 | 89 |
| pupvax.com | 0 | 8 | 32 |

Two problems are visible:
1. **Weak sites are "discovered, not indexed"** (zoneplan 89, freetdee 47, pupvax 32). More
   IndexNow pings will NOT fix this. They need third-party authority + content thickness.
2. **High-impression sites waste clicks.** plantingcalendar (380 indexed) and babypercent
   already rank but CTR is ~0.4–0.5%. Fixing titles/descriptions is the fastest traffic win
   and needs no new rankings.

---

## 1. STOP doing this (no authority transfer)

- GitHub Issue / Gist links → `ugc`, nofollow.
- Dev.to / Medium self-authored articles → `nofollow` on outbound.
- README-in-this-repo links → self-referential, nofollow from GitHub.
- Daily "backlink" logs that only record the above → stop counting these as backlinks.

Keep doing: IndexNow pings, GSC URL inspection, sitemap health. Those are discovery, not authority.

---

## 2. START doing this (white-hat, dofollow, defensible)

### 2.1 Niche communities Google indexes heavily (per 破局行动营 manual)
- **Reddit**: "美国版贴吧", Google 收录权重极高, 帖子常出现在搜索结果首页.
  - Must 养号 first: 3+ days pure browsing, 50+ karma before posting, never open with a link.
  - Add value in `r/learnpython`, `r/webdev`, `r/SideProject`, `r/personalfinance`,
    `r/fitness`, `r/puppy101`, `r/gardening` etc. Drop a tool link only when it genuinely
    answers the question. Profile link is fair game.
- **Relevant forums / Q&A**: Stack Overflow answers, niche Facebook groups (no link spam).

### 2.2 Tool directories that give dofollow or high-trust links
- alternative.to (add each tool, category-relevant)
- Product Hunt / BetaList (launch the stronger tools)
- Tiny Helpers, Free for Devs, Awesome lists on GitHub (PR a link into a curated list —
  this IS a real editorial link, not self-posting)
- Privacy/security resource pages that list "free privacy-first tools"

### 2.3 Resource-page outreach (highest ROI per link)
- Find "best free X tools" / "X alternatives" pages via `intitle:"best * tools" <topic>`.
- Pitch inclusion with a 1-line why-it-fits. Target DR 30+ pages.

### 2.4 Digital PR / expert commentary
- HARO / Connectively: respond as "builder of privacy-first browser tools" on data/privacy topics.
- Original tiny data study (e.g., "we analyzed 1,000 HEIC photos users convert") → journalist bait.

### 2.5 Internal linking (free, compounding)
- Build one hub page per category (time-zone, fitness, photo, pet, baby, invoice, planting)
  that links to every sub-page. Each sub-page links back to the hub and to 2–3 siblings.
- This moves link equity from strong pages (iworkviewer, livephotokit) to weak ones.

---

## 3. Content depth (fixes "discovered, not indexed")
For zoneplan, freetdee, pupvax, invoicepad — each needs an info cluster, not a single calculator:
- 1 pillar page + 3–5 long-tail how-to posts + an FAQ with `FAQPage` schema.
- Target ≥800 words per post, real answers to People Also Ask.
- This is what earns indexing AND featured snippets.

---

## 4. P0 quick wins — titles & descriptions (do this week)
These two already rank; better SERP copy = more clicks with zero new rankings.

**plantingcalendar.net** (avg position ~29, CTR 0.4%)
- Title: `Planting Calendar by Zone & Crop | Free Seed-Date Planner`
- Desc: `Find exactly when to plant vegetables, herbs, and flowers by USDA zone and crop. Free, private, no sign-up.`

**babypercent.com** (avg position ~19, CTR 0.5%)
- Title: `Baby Growth Percentile Calculator by Age & Weight | Free`
- Desc: `Check your baby's weight, height, and head-circumference percentile by age. Instant, private, no account needed.`

Apply in site source, rebuild, redeploy. (Built `out/` HTML is overwritten on rebuild — edit source, not dist.)

---

## 5. Monthly targets
| Source | Target links/mo | Avg DR | Notes |
|---|---:|---:|---|
| Communities (Reddit etc.) | 5–8 | n/a | value-first, no link-dumps |
| Directories | 4–6 | 40+ | alternative.to, PH, lists |
| Resource-page outreach | 3–5 | 30+ | personalized |
| Digital PR / HARO | 2–4 | 60+ | expert quotes |
| **Total dofollow** | **14–23** | | replace the old 0-value loop |

---

## 6. How to log honestly going forward
Replace `*-backlinks*.md` self-link logs with `*-linkbuilding*.md` that records ONLY:
- Source URL, target site, whether `dofollow`, DR of source, date acquired.
- Drop any entry that is nofollow/self-authored from the "backlinks" count.

Data judgment is yours (manual, Phase 4). The script can fetch; you decide what counts.
