# 2026-07-21 AI编程出海8站弱站优化证据

## GSC 2026-07-21 基准

| Site | Clicks | Impressions | CTR | Avg Pos | Indexed | Not Indexed |
|---|---:|---:|---:|---:|---:|---:|
| plantingcalendar.net | 19 | 5450 | 0.3% | 29.8 | 380 | 186 |
| freetdee.com | 1 | 194 | 0.5% | 44.6 | 10 | 47 |
| babypercent.com | 17 | 4490 | 0.4% | 19 | 46 | 25 |
| invoicepad.net | 1 | 701 | 0.1% | 51.8 | 28 | 17 |
| zoneplan.net | 2 | 1640 | 0.1% | 45 | 4 | 89 |
| pupvax.com | 0 | 212 | 0% | 34.3 | 8 | 32 |

Note: iworkviewer.com and livephotokit.com GSC data not captured due to ERR_CONNECTION_CLOSED during scrape. Health check via maintenance script confirms both are 200.

## 今日单变量：PupVax 全站 em dash 乱码修复

### 发现
- PupVax 8 个页面标题中使用 em dash (—, U+2014) 在生产环境全部显示为乱码字符 (��)
- 同时存在双重品牌后缀问题：页面 title 自带 `| PupVax`，layout.tsx template 追加 `| 2026 Dog Vaccine Tracker`
- PupVax 当前 0 点击、212 曝光、0% CTR，标题乱码和双重后缀直接损害点击率

### 修复
8 个页面 title 修复：

| Page | Before | After |
|---|---|---|
| /dog-vaccines | 2026 Dog Vaccines Explained — Core... \| PupVax | 2026 Dog Vaccines Explained: Core, Non-Core and the Full Schedule |
| /about | About PupVax (2026) — dog vaccine tracker | About PupVax (2026) |
| /blog | Blog — Guides & Tutorials \| PupVax | Blog: Guides and Tutorials |
| /breeds | 2026 Dog Vaccine Schedules by Breed — 20 Popular Breeds \| PupVax | 2026 Dog Vaccine Schedules by Breed: 20 Popular Breeds |
| /contact | Contact PupVax (2026) — Get in Touch | Contact PupVax (2026) |
| /privacy-policy | Privacy Policy (2026) — PupVax | Privacy Policy (2026) |
| /terms | Terms of Use (2026) — PupVax | Terms of Use (2026) |
| /vs | Free vs Paid Alternatives — PupVax | Free vs Paid Alternatives |

所有 title 统一：去除 em dash → 换用 ASCII 冒号，去除 `| PupVax` 双重后缀（layout template 自动添加 `| 2026 Dog Vaccine Tracker`）

### 部署
- Git commit: `ebdaa31` Fix em dash mojibake in 8 page titles, remove double branding
- GitHub Actions: in progress
- Build: npm run build passed
- 本地 backup: `.bak_20260721` 文件已保存

## 8站健康巡检

8站 home/robots/sitemap 全部 200，每站 20 URL IndexNow 全部 200。

证据文件: `D:\Tools\ai-tool-index\logs\2026-07-21-result.json`

## 深度SEO审计

| Site | Title Len | Canonical | Noindex | GA4 | AdSense | H1 |
|---|---|---|---|---|---|---|
| iworkviewer.com | 43 | YES | NO | YES | YES | YES |
| livephotokit.com | 51 | YES | NO | YES | YES | YES |
| freetdee.com | 54 | YES | NO | YES | YES | YES |
| babypercent.com | 56 | YES | NO | YES | YES | YES |
| invoicepad.net | 55 | YES | NO | YES | YES | YES |

plantingcalendar.net, zoneplan.net, pupvax.com 偶发 SSL EOF（Python requests 路径问题），维护脚本 PowerShell curl 均 200。

## 下一步

1. 等 PupVax GitHub Actions 部署完成，生产域名验证新 title。
2. 24-72 小时后复查 GSC，重点看 PupVax CTR 是否从 0% 上升。
3. Product Hunt iWorkViewer Launch 北京时间 15:01 监控。
4. ZonePlan 7 日实验 2026-07-26 复盘。
