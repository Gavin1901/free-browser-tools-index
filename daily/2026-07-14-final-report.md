# 2026-07-14 AI编程出海每日运营最终报告

## 先读唯一总文件

已读：淦总领域/🤖AI系统/05_AI编程出海/AI编程出海唯一总文件.md
业务线确认：AI编程出海第二资产线，不进入PGM早会，不混黄金账号。

## 浏览器仓与账号核实

- Chrome仓：D:\ChromeProfiles\GavinBuilds
- CDP端口：9223
- CDP状态：可连接
- GSC：能进入 /u/1，当前落到 pupvax.com 概览页
- GA：analytics.google.com 返回 ERR_CONNECTION_CLOSED，今日不报GA数据

## 8站健康与IndexNow

证据：daily/2026-07-14-ai-tool-indexing-maintenance.md 和 logs/2026-07-14-result.json

| Site | Home | Robots | Sitemap | URLs submitted | IndexNow |
|---|---:|---:|---:|---:|---:|
| iworkviewer.com | 初始ERR，复核200 | 200 | 200 | 20 | 200 |
| livephotokit.com | 200 | 200 | 200 | 20 | 200 |
| plantingcalendar.net | 200 | 200 | 200 | 20 | 200 |
| freetdee.com | 200 | 200 | 200 | 20 | 200 |
| babypercent.com | 200 | 200 | 200 | 20 | 200 |
| invoicepad.net | 200 | 200 | 200 | 20 | 200 |
| zoneplan.net | 200 | 200 | 200 | 20 | 200 |
| pupvax.com | 200 | 200 | 200 | 20 | 200 |

## 深度SEO审计

证据：daily/2026-07-14-deep-seo-audit.md 和 logs/2026-07-14-deep-seo-audit.json

结果：7站 PASS，babypercent.com REVIEW。

babypercent.com REVIEW原因：homepage title 71字符，略超70字符阈值。

## Chrome目检

证据：logs/2026-07-14-chrome-visual-check.json

8站均可打开，bodyLen均大于100，不是空白页。

## GSC数据

今日状态：部分完成。

已核实：GSC /u/1 能进入，当前 pupvax.com 概览页可读，页面显示共有0次网页搜索点击，3个网页已编入索引，35个网页未编入索引。

未完成：8站逐个切换资产时 CDP/websocket 层报 `nothing to repeat at position 0`，未拿到8站今日完整点击、曝光、CTR、排名，所以不报8站新数据。

## GA状态

未完成但已核实：analytics.google.com 在 GavinBuilds Chrome 中返回 ERR_CONNECTION_CLOSED。

## 今日外链

已发布并复核HTTP 200和正文目标链接：

1. https://github.com/Gavin1901/free-browser-tools-index/blob/master/daily/2026-07-14-backlinks.md
2. https://github.com/Gavin1901/free-browser-tools-index/blob/master/daily/2026-07-14-weak-sites-backlinks.md
3. https://github.com/Gavin1901/free-browser-tools-index/blob/master/daily/2026-07-14-deep-seo-audit.md
4. https://gist.github.com/Gavin1901/b4af854559519caf5c204ea2cf15da1e
5. https://github.com/Gavin1901/free-browser-tools-index/issues/4
6. https://github.com/Gavin1901/free-browser-tools-index/issues/5
7. https://github.com/Gavin1901/free-browser-tools-index/issues/6
8. https://github.com/Gavin1901/free-browser-tools-index/issues/7

覆盖弱站：freetdee.com、pupvax.com、zoneplan.net、invoicepad.net。

## 修复项

本地源码已修：D:\Tools\babypercent\src\app\layout.tsx

动作：将 BabyPercent 首页默认title缩短为 `BabyPercent - Free Baby Growth Percentile Calculator`。

验证：npm run build 通过。

部署状态：未部署。该目录无git仓、无明确部署入口，本轮不冒充线上已修。

## Git证据

- 32b0e53 Daily indexing maintenance 2026-07-14
- d8e1226 Add 2026-07-14 deep SEO audit and backlink pages
- 667ab78 Record 2026-07-14 public backlink URLs

## 已完成

1. 读AI编程出海唯一总文件。
2. 启动并连接 GavinBuilds Chrome 9223。
3. 跑8站健康巡检。
4. 每站IndexNow提交20个URL。
5. 跑深度SEO审计。
6. Chrome目检8站首屏非空白。
7. 建立8条公开外链/证据路径。
8. 公开仓已push。
9. 外链URL已复核HTTP 200和正文目标链接。
10. babypercent title过长问题已本地修复并构建通过。

## 未完成但已核实

1. GA：ERR_CONNECTION_CLOSED，未拿到数据。
2. GSC：只核到pupvax概览，8站完整新数据未取到。
3. babypercent线上部署：未完成，缺明确部署入口。
4. Dev.to/Medium今日未新增发布，本轮走GitHub公开路径完成外链。

## 下一步

1. 找到 babypercent 的真实部署入口，把title修复上线，再复查线上title长度。
2. 修 GSC 8站切换脚本，不用当前有问题的 websocket 创建方式。
3. GA继续排查 ERR_CONNECTION_CLOSED。
4. 下一轮优先继续给 freetdee、pupvax、zoneplan、invoicepad 补 Dev.to 或 Medium 外链。

## 回到PGM主线

AI编程出海今日维护已做到可验证外链闭环，后续资源不继续占用PGM主线。
