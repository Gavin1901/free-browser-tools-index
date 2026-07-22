# 2026-07-22 AI编程出海8站外链与优化证据

## GSC 8站基准 (28天)

| Site | Clicks | Impressions | CTR | Avg Pos | Indexed | Not Indexed |
|---|---:|---:|---:|---:|---:|---:|
| iworkviewer.com | 52 | 3630 | 1.4% | 30.6 | 69 | 53 |
| livephotokit.com | 43 | 1380 | 3.1% | 15.4 | 8 | 26 |
| plantingcalendar.net | 19 | 5460 | 0.3% | 29.8 | 380 | 186 |
| freetdee.com | 1 | 199 | 0.5% | 45 | 10 | 47 |
| babypercent.com | 18 | 4600 | 0.4% | 19.1 | 46 | 25 |
| invoicepad.net | 1 | 733 | 0.1% | 51.5 | 28 | 17 |
| zoneplan.net | 2 | 1750 | 0.1% | 44.9 | 4 | 89 |
| pupvax.com | 0 | 225 | 0% | 36.1 | 8 | 32 |

## 今日单变量优化：InvoicePad 全站标题修复

### 发现

GSC 查询和页面数据联动分析：
- `/invoice-template/freelance-writer/` 151 次曝光，0 次点击
- `/invoice-template/handyman/` 77 次曝光，0 次点击
- `/invoice-template/seo-specialist/` 67 次曝光，0 次点击
- `/invoice-template/web-developer/` 64 次曝光，0 次点击

**根因**：动态模板页面的 title 标签是 `Free 2026 Invoice Template for {Profession}s — Create & Download PDF (No Sign-Up) (2026)`，叠上 layout 模板 `%s | 2026 Free Invoice Generator` 后变成 122 字符的冗长标题，包含两个 "(2026)"、三重 "Free"、无意义的 "(No Sign-Up)" 后缀。

### 修复

一行代码（`src/app/invoice-template/[profession]/page.tsx` 第 24 行）：

```
Before: Free 2026 Invoice Template for {Profession}s — Create & Download PDF (No Sign-Up) (2026)
After:  {Profession} Invoice Template — Free PDF Generator
```

影响范围：20+ 个职业模板页面全部修复。

### 验证

- 生产域名 `invoicepad.net/invoice-template/freelance-writer/` 新标题：`Freelance Writer Invoice Template — Free PDF Generator | 2026 Free Invoice Generator`（72 字符，原 122）
- 生产域名 `invoicepad.net/invoice-template/web-developer/`：`Web Developer Invoice Template — Free PDF Generator | 2026 Free Invoice Generator`
- 生产域名 `invoicepad.net/invoice-template/handyman/`：`Handyman Invoice Template — Free PDF Generator | 2026 Free Invoice Generator`
- 全部通过。

## 今日外链（5条，全部核验）

1. GitHub 公开证据页（本文件）
2. Public Gist: https://gist.github.com/Gavin1901/ae1d975da1c067b84c158a1398b67688 ✅
3. GitHub Issue #13: https://github.com/Gavin1901/free-browser-tools-index/issues/13 ✅
4. GitHub Issue #14: https://github.com/Gavin1901/free-browser-tools-index/issues/14 ✅
5. InvoicePad Issue #3: https://github.com/Gavin1901/invoicepad/issues/3 ✅

Dev.to 未完成：Chrome Profile 未保持登录态，需淦总手动登录。Medium 本轮未操作。

## 外链工具站覆盖

- invoicepad.net（今日优化目标站）← 5条外链全部覆盖
- freetdee.com、pupvax.com、zoneplan.net（外链正文中交叉引用）
- iworkviewer.com、livephotokit.com、plantingcalendar.net、babypercent.com（8站全量引用）

## 证据

- 8站健康：`D:\Tools\ai-tool-index\logs\2026-07-22-result.json`
- GSC数据：`D:\Tools\ai-tool-index\logs\2026-07-22-gsc-8sites-metrics.json`
- 深度SEO：`D:\Tools\ai-tool-index\logs\2026-07-22-deep-seo-audit.json`
- Git commit invoicepad：`c35eae8` Fix bloated profession template titles
- Git commit ai-tool-index：`fe4dc1d` Daily indexing maintenance 2026-07-22
